from moviepy.editor import *
from PIL import Image, ImageDraw, ImageFont
import numpy as np
import os

# Prints the current directory for verification
current_dir = os.getcwd()
print(f"Current execution directory: {current_dir}")

# Lists files in the current directory
print("Files in the current directory:")
for file in os.listdir(current_dir):
    print(f" - {file}")

# Defines compatibility with both old and new Pillow versions
try:
    resample_filter = Image.Resampling.LANCZOS
except AttributeError:
    resample_filter = Image.ANTIALIAS

# Function to create a smooth zoom animation
def zoom_effect(clip, zoom_ratio=0.04):
    def effect(get_frame, t):
        img = get_frame(t)
        
        # Calculates the zoom factor based on time
        zoom_factor = 1 + zoom_ratio * t
        
        # Applies zoom using PIL
        pil_img = Image.fromarray(img)
        orig_size = pil_img.size
        
        # Calculates the new enlarged size
        new_size = (int(pil_img.size[0] * zoom_factor), 
                    int(pil_img.size[1] * zoom_factor))
        
        # Enlarges the image
        pil_img = pil_img.resize(new_size, resample=resample_filter)
        
        # Crops the image to maintain the original size
        crop_x1 = (new_size[0] - orig_size[0]) // 2
        crop_y1 = (new_size[1] - orig_size[1]) // 2
        crop_x2 = crop_x1 + orig_size[0]
        crop_y2 = crop_y1 + orig_size[1]
        pil_img = pil_img.crop((crop_x1, crop_y1, crop_x2, crop_y2))
        
        return np.array(pil_img)
    
    return clip.fl(effect)

# Function to create text with PIL (more reliable alternative)
def create_text_with_pil(text, size, fontsize=70):
    # Creates a transparent image
    txt_img = Image.new("RGBA", size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(txt_img)
    
    # Tries to use a standard font
    try:
        # Tries several fonts that may exist on the system
        try:
            font = ImageFont.truetype("Arial", fontsize)
        except:
            try:
                font = ImageFont.truetype("DejaVuSans", fontsize)
            except:
                font = ImageFont.load_default()
    except:
        font = ImageFont.load_default()
    
    # Removes emojis to avoid size calculation issues
    clean_text = ''.join(c for c in text if ord(c) < 10000)
    
    # Central position
    text_bbox = draw.textbbox((0, 0), clean_text, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]
    position = ((size[0] - text_width) // 2, (size[1] - text_height) // 2)
    
    # Draws the text with shadow for better visibility
    for offset in range(1, 4):
        draw.text((position[0]+offset, position[1]+offset), clean_text, fill=(0, 0, 0, 180), font=font)
    draw.text(position, clean_text, fill=(255, 255, 255, 255), font=font)
    
    # Converts to numpy array for MoviePy
    return np.array(txt_img)

# Main function to generate the video with animations
def create_animated_video(images, texts, output="output_animated.mp4", clip_duration=5):
    clips = []
    
    # Instagram format (vertical)
    video_width, video_height = 1080, 1350
    
    for i, (img_path, text) in enumerate(zip(images, texts)):
        print(f"\nProcessing image {i+1}: {img_path}")
        
        if os.path.isfile(img_path):
            print(f"✓ File found: {img_path}")
            try:
                # Loads the image
                img_clip = ImageClip(img_path).set_duration(clip_duration)
                print(f"✓ Image loaded successfully. Size: {img_clip.size}")
                
                # Resizes if necessary
                if img_clip.size != (video_width, video_height):
                    print(f"Resizing from {img_clip.size} to {video_width}x{video_height}")
                    img = img_clip.get_frame(0)
                    pil_img = Image.fromarray(img)
                    pil_img = pil_img.resize((video_width, video_height), resample=resample_filter)
                    img_clip = ImageClip(np.array(pil_img)).set_duration(clip_duration)
                
                # Applies zoom effect to the image
                img_clip = zoom_effect(img_clip)
                
                # Applies fade in/out effect to the image
                img_clip = img_clip.fadein(1).fadeout(1)
                
                # Creates text using the PIL method (more reliable)
                print(f"Creating text: '{text}' (no emojis)")
                txt_array = create_text_with_pil(text, (video_width, video_height), fontsize=70)
                txt_clip = ImageClip(txt_array).set_duration(clip_duration)
                
                # Defines text animation with position instead of transform
                def move_text(t):
                    # Smooth vertical movement
                    if t < 1.0:
                        # Entrance: slides from bottom to center
                        return ('center', video_height/2 + 200 * (1-t))
                    elif t > clip_duration - 1.0:
                        # Exit: slides from center to bottom
                        fade_out_progress = (clip_duration - t)
                        return ('center', video_height/2 + 200 * (1-fade_out_progress))
                    else:
                        # Middle: remains in center
                        return ('center', 'center')
                
                txt_clip = txt_clip.set_position(move_text)
                txt_clip = txt_clip.fadein(1).fadeout(1)
                
                # Combines image and text
                final_clip = CompositeVideoClip([img_clip, txt_clip])
                clips.append(final_clip)
                print(f"✓ Animated clip for '{text}' created successfully")
                
            except Exception as e:
                print(f"✗ Error: {str(e)}")
                import traceback
                traceback.print_exc()
        else:
            print(f"✗ File not found: {img_path}")
    
    if clips:
        # Combines everything with transitions
        print("\nGenerating animated video...")
        
        # Adds transitions between clips
        final_clips = []
        for i, clip in enumerate(clips):
            if i < len(clips) - 1:  # For all except the last one
                # Adds a crossfade transition
                final_clips.append(clip.crossfadeout(1.0))
            else:
                final_clips.append(clip)  # Last clip without crossfade at the end
            
        # Joins all clips with transitions
        video = concatenate_videoclips(final_clips, method="compose")
        
        # Generates the final video
        video.write_videofile(output, fps=30, codec='libx264')
        print(f"\n✓ Animated video generated successfully: {output}")
    else:
        print("\n✗ No video was generated because there are no valid clips.")

# List of images and texts
images = ["image1.jpeg", "image2.jpeg", "image3.jpeg"]
texts = [
    "Get noticed on Instagram!",
    "Turn images into videos",
    "Follow Decide Digital"  # Removed emoji for better compatibility
]

# Generates the video with animations
create_animated_video(images, texts)

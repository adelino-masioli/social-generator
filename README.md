# ✨ Social Generator 🎬

Blimey! 👋 Ever wanted to effortlessly turn your splendid images into eye-catching, animated videos perfect for grabbing attention on social media? Look no further! **Social Generator** is a nifty Python script designed to do just that. Create engaging vertical videos (ideal for Instagram Reels/Stories!) with smooth zooms, elegant text animations, and slick transitions. Let's make your posts pop! 💥

Find this project on GitHub: [adelino-masioli/social-generator](https://github.com/adelino-masioli/social-generator)

## What's All This Then? 🤔

This script takes a list of your images and corresponding text captions and magically stitches them together into a professional-looking animated video. It's brilliant for:

* Showcasing products or portfolio pieces 🖼️➡️🎞️
* Creating quick, engaging social media updates 📢
* Turning static content into dynamic video snippets ✨

## Core Features ✅

* **📸 Image to Video Magic:** Transforms a sequence of images into a single video file.
* **📱 Insta-Ready Format:** Creates videos in a vertical 1080x1350 resolution, spot on for Instagram.
* **🔎 Smooth Zoom Effect:** Adds a subtle, captivating zoom animation to each image.
* **✍️ Animated Text Overlays:** Superimposes your text with elegant slide-in/out and fade animations. Text includes a subtle shadow for better visibility.
* **✨ Slick Transitions:** Uses smooth crossfades for seamless transitions between different image/text clips.
* **🎨 PIL-Powered Text:** Robust text rendering using the Pillow library ensures compatibility and good looks.
* **⚙️ Customisable:** Easily change the input images, text captions, and clip duration.

## Getting Started 🚀

Right then, let's get you set up!

### Prerequisites

* Python 3 installed on your machine.
* `pip` (Python's package installer).

### Installation & Setup

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/adelino-masioli/social-generator.git](https://github.com/adelino-masioli/social-generator.git)
    cd social-generator
    ```

2.  **Install the necessary libraries:**
    It's highly recommended to use a virtual environment!
    ```bash
    # Create a virtual environment (optional but recommended)
    python -m venv venv
    # Activate it (Windows)
    .\venv\Scripts\activate
    # Activate it (macOS/Linux)
    source venv/bin/activate

    # Install dependencies
    pip install moviepy Pillow numpy
    ```
    *(You might want to create a `requirements.txt` file for easier dependency management!)*

3.  **Prepare Your Assets:**
    * Place the images you want to use (e.g., `image1.jpeg`, `image2.jpeg`) in the same directory as the Python script.
    * Make sure the image filenames match those listed in the script.

4.  **Configure the Script:**
    * Open the Python script (e.g., `social_generator.py` - *rename yours if different*).
    * Locate the `images` and `texts` lists near the bottom:
        ```python
        images = ["image1.jpeg", "image2.jpeg", "image3.jpeg"]
        texts = [
            "Get noticed on Instagram!",
            "Turn images into videos",
            "Follow Decide Digital"
        ]
        ```
    * Modify these lists to point to *your* image files and contain *your* desired text captions.

### Running the Generator

Simply execute the script from your terminal within the project directory (and with your virtual environment activated, if you're using one):

```bash
python your_script_name.py
 ```
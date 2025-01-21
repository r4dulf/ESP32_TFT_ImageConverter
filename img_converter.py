import os
from PIL import Image, ImageSequence
import numpy as np

def rgb_to_rgb565(r, g, b):
    r5 = (r >> 3) & 0x1F
    g6 = (g >> 2) & 0x3F
    b5 = (b >> 3) & 0x1F
    return (r5 << 11) | (g6 << 5) | b5

def calculate_mse(image1, image2):
    arr1 = np.array(image1)
    arr2 = np.array(image2)
    return np.mean((arr1 - arr2) ** 2)

def convert_gif_to_frames(gif_path, output_folder, similarity_threshold=10, target_size=None):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    frames = []
    unique_frames = []

    with Image.open(gif_path) as gif:
        for i, frame in enumerate(ImageSequence.Iterator(gif)):
            frame = frame.convert("RGB")
            if target_size:
                frame = frame.resize(target_size, Image.Resampling.LANCZOS)

            is_duplicate = False
            for existing_frame in unique_frames:
                mse = calculate_mse(frame, existing_frame)
                if mse < similarity_threshold:
                    is_duplicate = True
                    break

            if not is_duplicate:
                unique_frames.append(frame)

    for i, frame in enumerate(unique_frames):
        frame.save(os.path.join(output_folder, f"frame_{i:03d}.jpg"), "JPEG")

def generate_header(folder_path, output_file, variable_name="walk"):
    header_content = []
    header_content.append(f"#ifndef {variable_name.upper()}_H")
    header_content.append(f"#define {variable_name.upper()}_H")
    header_content.append("")

    all_images = [f for f in os.listdir(folder_path) if f.endswith('.jpg')]
    frames_count = len(all_images)

    if frames_count == 0:
        raise ValueError("No .jpg files found in the specified folder.")

    first_image = Image.open(os.path.join(folder_path, all_images[0]))
    width, height = first_image.size

    pixels_per_frame = width * height

    header_content.append(f"int frames = {frames_count};")
    header_content.append(f"int animation_width = {width};")
    header_content.append(f"int animation_height = {height};")
    header_content.append(f"const unsigned short PROGMEM {variable_name}[][ {pixels_per_frame} ] = {{")

    for img_index, img_name in enumerate(all_images):
        img_path = os.path.join(folder_path, img_name)
        image = Image.open(img_path).convert("RGB")
        pixel_data = []

        for y in range(height):
            for x in range(width):
                r, g, b = image.getpixel((x, y))
                rgb565 = rgb_to_rgb565(r, g, b)
                pixel_data.append(f"0x{rgb565:04X}")

        header_content.append("    {" + ", ".join(pixel_data) + "},")

    header_content.append("};")
    header_content.append("")
    header_content.append(f"#endif // {variable_name.upper()}_H")

    # Ensure the output directory exists
    output_dir = os.path.dirname(output_file)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)

    with open(output_file, "w") as header_file:
        header_file.write("\n".join(header_content))

# Example usage
# convert_gif_to_frames("path_to_gif_file.gif", "output_frames_folder", similarity_threshold=10, target_size=(128, 128))
# generate_header("output_frames_folder", "walk.h", variable_name="animation_data")

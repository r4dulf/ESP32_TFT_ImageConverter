# GIF to RGB565 Header Generator

This repository contains Python scripts for:
1. Extracting unique frames from a GIF file.
2. Converting those frames to the RGB565 format.
3. Generating a C/C++ header file that includes the frame data for use in embedded systems or other applications.

## Features
- **GIF Frame Extraction:** Converts animated GIFs into a sequence of unique frames.
- **RGB565 Conversion:** Converts RGB pixel data to the RGB565 format, which is widely used in embedded systems for displaying images on low-resource hardware.
- **Header File Generation:** Produces a `.h` file containing frame data as a constant array for integration into embedded projects.

## Prerequisites
Make sure you have the following installed on your system:
- Python 3.6 or later
- Required Python libraries:
  - `Pillow`
  - `numpy`

You can install the dependencies using pip:
```bash
pip install pillow numpy
```

## Usage

### 1. Extract Frames from GIF
Use the `convert_gif_to_frames` function to extract unique frames from a GIF file.

#### Example:
```python
convert_gif_to_frames(
    gif_path="path_to_gif_file.gif",
    output_folder="output_frames_folder",
    similarity_threshold=10,
    target_size=(128, 128)
)
```
**Parameters:**
- `gif_path`: Path to the input GIF file.
- `output_folder`: Directory where extracted frames will be saved as `.jpg` files.
- `similarity_threshold`: Mean Squared Error (MSE) threshold for detecting duplicate frames. Higher values detect more duplicates.
- `target_size`: Tuple `(width, height)` to resize frames. Optional.

### 2. Generate Header File
Use the `generate_header` function to create a header file from the extracted frames.

#### Example:
```python
generate_header(
    folder_path="output_frames_folder",
    output_file="walk.h",
    variable_name="animation_data"
)
```
**Parameters:**
- `folder_path`: Directory containing `.jpg` files of frames.
- `output_file`: Path to the output header file.
- `variable_name`: Name of the C/C++ variable storing the animation data.

### 3. Combine Both Steps
Extract frames and generate a header file in one workflow:
```python
convert_gif_to_frames("path_to_gif.gif", "output_frames", similarity_threshold=10, target_size=(128, 128))
generate_header("output_frames", "animation.h", variable_name="animation_data")
```

## Output
The generated `.h` file will contain:
- Frame count
- Frame dimensions
- RGB565 pixel data for each frame stored as a 2D array.

### Example Header File (`walk.h`):
```c
#ifndef ANIMATION_DATA_H
#define ANIMATION_DATA_H

int frames = 10;
int animation_width = 128;
int animation_height = 128;
const unsigned short PROGMEM animation_data[][16384] = {
    {0xF800, 0x07E0, 0x001F, ...},
    {0xF800, 0x07E0, 0x001F, ...},
    ...
};

#endif // ANIMATION_DATA_H
```

## Notes
- Ensure your GIF is compatible with the target dimensions and format requirements of your project.
- The RGB565 conversion uses 16 bits per pixel to reduce memory usage while maintaining color fidelity.
- Duplicate frames are filtered out based on the `similarity_threshold` parameter.


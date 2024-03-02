# QIBA Lung Collection Visualization & 3D Owl Model Rendering

## Project 1: QIBA Lung Collection Visualization

**Utilized Dataset:** QIBA_Lung_Collection - Philips (Spherical_10)  
**Download Link:** [QIBA Lung Collection Dataset](https://qidw.rsna.org/#item/5b845ae0b3467a6a92109a3a)  
**File Size:** 970 Mb (Utilized dataset folder size: 152 Mb)

### System Requirements:
- Python Version: 3.11.5
- VTK Version: 9.3.0
- Code Editor: Any of your preferences (Sublime Text 3, Visual Studio Code (VSCode), PyCharm, Jupyter Notebook)

### Running Process:
1. Ensure both the code and the dataset folder are placed in the same directory.
2. Run the code using your chosen code editor.
3. The code will display a window with the original view of the dataset.
4. Additionally, the terminal will display the following information:
    - Image dimensions
    - Voxel dimensions
    - Minimum pixel intensity
    - Maximum pixel intensity

## Project 2: 3D Owl Model Rendering

**Purpose:** This script renders and visualizes a 3D mechanical owl model using VTK and various shading techniques.

### Code Structure:
- Imports necessary libraries from VTK and pathlib.
- Reads the STL file (Owl_mechanical.stl) using VTK's vtkSTLReader.
- Creates different actors for:
    - Wireframe rendering
    - Flat shading
    - Gouraud shading
    - Phong shading
- Sets up renderers for each rendering technique.
- Defines viewport configurations to display each technique in different sections of the window.
- Adds actors to their respective renderers and assigns viewports accordingly.
- Defines a function to export the rendered window as an image file.
- Sets up the render window, render window interactor, and initializes rendering.
- Exports the rendered image as "GraphicMM1.jpg" in the same directory.
- Displays the number of vertices of the model in the terminal.

### Requirements:
- Python 3.11.5
- VTK 9.3.0

### Usage:
1. Ensure both the code and the model (Owl_mechanical.stl) are placed in the same directory.
2. Run the code using your preferred code editor.
3. Upon successful execution:
    - A JPG file named "GraphicMM1.jpg" will be generated in the same directory.
    - The terminal will display the number of vertices of the model.

## Authors:
- Morteza Mogharrab ([GitHub](https://github.com/Morteza-Mogharrab))

## License:
MIT License

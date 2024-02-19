# 3D Owl Model Rendering

This Python script is designed to render and visualize a 3D mechanical owl model (`Owl_mechanical.stl`) using the Visualization Toolkit (VTK). It employs various shading techniques, including wireframe, flat, Gouraud, and Phong, to display the model from different perspectives.

## Code Structure

- Imports necessary libraries from VTK and pathlib.
- Reads the STL file (`Owl_mechanical.stl`) using VTK's `vtkSTLReader`.
- Creates different actors for wireframe rendering and various shading techniques (flat, Gouraud, Phong).
- Sets up renderers for each rendering technique.
- Defines viewport configurations to display each rendering technique in different sections of the window.
- Adds actors to their respective renderers and assigns viewports accordingly.
- Defines a function `export_image` to export the rendered window to an image file.
- Sets up the render window, render window interactor, and initializes rendering.
- Exports the rendered image to a JPG file named "GraphicMM1.jpg" in the same directory.

## Requirements

- Python 3.11.5
- VTK 9.3.0

## Usage

1. Ensure that both the code and the model (`Owl_mechanical.stl`) are placed in the same directory.
2. Run the code using your preferred code editor, such as Sublime Text 3, Visual Studio Code, PyCharm, or Jupyter Notebook.
3. Upon successful execution, a JPG file named "GraphicMM1.jpg" will be generated in the same directory.
4. Additionally, the terminal will display the number of vertices of the model.

## Folder Structure

- `Owl_mechanical.stl`: 3D mechanical owl model file.
- `render_owl.py`: Python script for rendering the owl model.
- `GraphicMM1 & 2.jpg`: Rendered images of the owl model.

## Running Process

1. Ensure both the code and the model are placed in the same directory.
2. Run the code using the chosen code editor.
3. Upon successful execution, a JPG file named "GraphicMM1.jpg" will be generated in the same directory.
4. Additionally, the code editor's terminal will display the number of vertices.

## Authors

- [Morteza Mogharrab] - (https://github.com/morteza-mogharrab)

## License

This project is licensed under the [MIT License](LICENSE).

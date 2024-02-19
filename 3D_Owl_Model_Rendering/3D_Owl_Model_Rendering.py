# Import required libraries
from pathlib import Path
import vtk
from vtkmodules.vtkRenderingCore import vtkWindowToImageFilter
from vtkmodules.vtkCommonColor import vtkNamedColors
from vtkmodules.vtkIOImage import (
    vtkBMPWriter,
    vtkJPEGWriter,
    vtkPNGWriter,
    vtkPNMWriter,
    vtkPostScriptWriter,
    vtkTIFFWriter
)

# Initialize colors
vtk_colors = vtkNamedColors()

# Read the STL file
stl_reader = vtk.vtkSTLReader()
stl_reader.SetFileName("Owl_mechanical.stl")
stl_reader.Update()

# Create the mapper
polydata_mapper = vtk.vtkPolyDataMapper()
polydata_mapper.SetInputConnection(stl_reader.GetOutputPort())

# Access the polydata to get the number of vertices
polydata = polydata_mapper.GetInput()
num_vertices = polydata.GetNumberOfPoints()
print(f"Number of vertices: {num_vertices}")

# Create the wireframe actor
wireframe_actor = vtk.vtkActor()
wireframe_actor.SetMapper(polydata_mapper)
wireframe_actor.GetProperty().SetRepresentationToWireframe()

# Create the flat shading actor
flat_shading_actor = vtk.vtkActor()
flat_shading_actor.SetMapper(polydata_mapper)
flat_shading_actor.GetProperty().SetRepresentationToSurface()
flat_shading_actor.GetProperty().ShadingOn()
flat_shading_actor.GetProperty().SetInterpolationToFlat()
flat_shading_actor.GetProperty().SetColor(vtk_colors.GetColor3d('Gold'))

# Create the Gouraud shading actor
gouraud_shading_actor = vtk.vtkActor()
gouraud_shading_actor.SetMapper(polydata_mapper)
gouraud_shading_actor.GetProperty().SetRepresentationToSurface()
gouraud_shading_actor.GetProperty().ShadingOn()
gouraud_shading_actor.GetProperty().SetInterpolationToGouraud()
gouraud_shading_actor.GetProperty().SetColor(vtk_colors.GetColor3d('SaddleBrown'))

# Create the Phong shading actor
phong_shading_actor = vtk.vtkActor()
phong_shading_actor.SetMapper(polydata_mapper)
phong_shading_actor.GetProperty().SetRepresentationToSurface()
phong_shading_actor.GetProperty().ShadingOn()
phong_shading_actor.GetProperty().SetInterpolationToPhong()
phong_shading_actor.GetProperty().SetColor(vtk_colors.GetColor3d('Teal'))

# Create the renderers
wireframe_renderer = vtk.vtkRenderer()
flat_renderer = vtk.vtkRenderer()
gouraud_renderer = vtk.vtkRenderer()
phong_renderer = vtk.vtkRenderer()

# Add the wireframe actor to the wireframe renderer
wireframe_renderer.AddActor(wireframe_actor)

# Add actors to the other renderers
flat_renderer.AddActor(flat_shading_actor)
gouraud_renderer.AddActor(gouraud_shading_actor)
phong_renderer.AddActor(phong_shading_actor)

# Create the render window
render_window = vtk.vtkRenderWindow()
render_window.AddRenderer(wireframe_renderer)
render_window.AddRenderer(flat_renderer)
render_window.AddRenderer(gouraud_renderer)
render_window.AddRenderer(phong_renderer)

# Define viewport configurations
viewport_wireframe = [0, 0.5, 0.5, 1]  # Display wireframe in the top-left quarter
viewport_flat = [0.5, 0.5, 1, 1]       # Display flat shading in the top-right quarter
viewport_gouraud = [0, 0, 0.5, 0.5]    # Display Gouraud shading in the bottom-left quarter
viewport_phong = [0.5, 0, 1, 0.5]      # Display Phong shading in the bottom-right quarter

# Assign viewports to the renderers
renderer_wireframe = vtk.vtkRenderer()
renderer_flat = vtk.vtkRenderer()
renderer_gouraud = vtk.vtkRenderer()
renderer_phong = vtk.vtkRenderer()
render_window.AddRenderer(renderer_wireframe)
render_window.AddRenderer(renderer_flat)
render_window.AddRenderer(renderer_gouraud)
render_window.AddRenderer(renderer_phong)

renderer_wireframe.SetViewport(viewport_wireframe)
renderer_flat.SetViewport(viewport_flat)
renderer_gouraud.SetViewport(viewport_gouraud)
renderer_phong.SetViewport(viewport_phong)

# Add actors to respective renderers
renderer_wireframe.AddActor(wireframe_actor)
renderer_flat.AddActor(flat_shading_actor)
renderer_gouraud.AddActor(gouraud_shading_actor)
renderer_phong.AddActor(phong_shading_actor)

# Function to export rendered window to an image
def export_image(file_name, render_window, rgba=True):
    # Check if file name is provided
    if not file_name:
        raise RuntimeError('Need a filename.')

    # Dictionary mapping file extensions to corresponding writer classes
    valid_extensions_to_writer = {'.bmp': vtk.vtkBMPWriter,
                                  '.jpg': vtk.vtkJPEGWriter,
                                  '.png': vtk.vtkPNGWriter,
                                  '.pnm': vtk.vtkPNMWriter,
                                  '.ps': vtk.vtkPostScriptWriter,
                                  '.tiff': vtk.vtkTIFFWriter}

    # Extract file extension from the provided file name
    file_extension = Path(file_name).suffix.lower()

    # Get the appropriate writer class based on the file extension,
    # defaulting to PNG writer if extension is not recognized
    writer_class = valid_extensions_to_writer.get(file_extension, vtk.vtkPNGWriter)

    # Handle special case for PostScript format to set rgba flag
    if file_extension == '.ps' and rgba:
        rgba = False

    # Instantiate the selected writer class
    image_writer = writer_class()

    # Set up window to image filter
    window_to_image_filter = vtk.vtkWindowToImageFilter()
    window_to_image_filter.SetInput(render_window)
    window_to_image_filter.SetScale(1)  # Image quality

    # Set input buffer type based on whether rgba flag is True or False
    if rgba:
        window_to_image_filter.SetInputBufferTypeToRGBA()
    else:
        window_to_image_filter.SetInputBufferTypeToRGB()

    window_to_image_filter.ReadFrontBufferOff()
    window_to_image_filter.Update()

    # Set the output file name for the image writer
    image_writer.SetFileName(str(Path(file_name)))

    # Connect the window to image filter output to the image writer input
    image_writer.SetInputConnection(window_to_image_filter.GetOutputPort())

    # Write the image
    image_writer.Write()

# Start the render window
render_window.Render()
render_window.SetWindowName("GraphicMM1")

# Set up render window interactor
render_window_interactor = vtk.vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)
render_window.SetSize(700, 700)
render_window.Render()
# Export the image
export_image('GraphicMM1.jpg', render_window, rgba=False)
# Initialize and start the interactor
render_window_interactor.Initialize()
render_window_interactor.Start()

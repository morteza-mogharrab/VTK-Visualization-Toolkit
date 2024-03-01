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
from pathlib import Path

def read_stl_file(file_name):
    """Read STL file and return the reader object."""
    stl_reader = vtk.vtkSTLReader()
    stl_reader.SetFileName(file_name)
    stl_reader.Update()
    return stl_reader

def create_actor(mapper, representation='Surface', color=None):
    """Create an actor with specified properties."""
    actor = vtk.vtkActor()
    actor.SetMapper(mapper)
    if representation == 'Wireframe':
        actor.GetProperty().SetRepresentationToWireframe()
    elif representation == 'Surface':
        actor.GetProperty().SetRepresentationToSurface()
    if color:
        actor.GetProperty().SetColor(color)
    return actor


def create_renderer(viewport):
    """Create a renderer with the given viewport."""
    renderer = vtk.vtkRenderer()
    renderer.SetViewport(viewport)
    return renderer

def export_image(file_name, render_window, rgba=True):
    """Export the rendered window to an image file."""
    if not file_name:
        raise ValueError('File name must be provided.')

    valid_extensions_to_writer = {
        '.bmp': vtkBMPWriter,
        '.jpg': vtkJPEGWriter,
        '.png': vtkPNGWriter,
        '.pnm': vtkPNMWriter,
        '.ps': vtkPostScriptWriter,
        '.tiff': vtkTIFFWriter
    }

    file_extension = Path(file_name).suffix.lower()
    writer_class = valid_extensions_to_writer.get(file_extension, vtkPNGWriter)

    if file_extension == '.ps' and rgba:
        rgba = False

    image_writer = writer_class()
    window_to_image_filter = vtk.vtkWindowToImageFilter()
    window_to_image_filter.SetInput(render_window)
    window_to_image_filter.SetScale(1)

    if rgba:
        window_to_image_filter.SetInputBufferTypeToRGBA()
    else:
        window_to_image_filter.SetInputBufferTypeToRGB()

    window_to_image_filter.ReadFrontBufferOff()
    window_to_image_filter.Update()

    image_writer.SetFileName(str(Path(file_name)))
    image_writer.SetInputConnection(window_to_image_filter.GetOutputPort())
    image_writer.Write()

def main():
    vtk_colors = vtkNamedColors()
    stl_reader = read_stl_file("Owl_mechanical.stl")
    polydata_mapper = vtk.vtkPolyDataMapper()
    polydata_mapper.SetInputConnection(stl_reader.GetOutputPort())
    num_vertices = polydata_mapper.GetInput().GetNumberOfPoints()
    print(f"Number of vertices: {num_vertices}")

    wireframe_actor = create_actor(polydata_mapper, representation='Wireframe')
    flat_shading_actor = create_actor(polydata_mapper, representation='Surface', color=vtk_colors.GetColor3d('Gold'))
    gouraud_shading_actor = create_actor(polydata_mapper, representation='Surface', color=vtk_colors.GetColor3d('SaddleBrown'))
    phong_shading_actor = create_actor(polydata_mapper, representation='Surface', color=vtk_colors.GetColor3d('Teal'))

    wireframe_renderer = create_renderer([0, 0.5, 0.5, 1])
    flat_renderer = create_renderer([0.5, 0.5, 1, 1])
    gouraud_renderer = create_renderer([0, 0, 0.5, 0.5])
    phong_renderer = create_renderer([0.5, 0, 1, 0.5])

    wireframe_renderer.AddActor(wireframe_actor)
    flat_renderer.AddActor(flat_shading_actor)
    gouraud_renderer.AddActor(gouraud_shading_actor)
    phong_renderer.AddActor(phong_shading_actor)

    render_window = vtk.vtkRenderWindow()
    render_window.AddRenderer(wireframe_renderer)
    render_window.AddRenderer(flat_renderer)
    render_window.AddRenderer(gouraud_renderer)
    render_window.AddRenderer(phong_renderer)

    render_window.Render()
    render_window.SetWindowName("GraphicMM1")
    render_window.SetSize(700, 700)

    export_image('GraphicMM1.jpg', render_window, rgba=False)

    render_window_interactor = vtk.vtkRenderWindowInteractor()
    render_window_interactor.SetRenderWindow(render_window)
    render_window_interactor.Initialize()
    render_window_interactor.Start()

if __name__ == "__main__":
    main()

import vtk

def read_dicom_data(directory):
    """
    Read DICOM dataset from the specified directory using vtkDICOMImageReader.
    """
    dicom_reader = vtk.vtkDICOMImageReader()
    dicom_reader.SetDirectoryName(directory)
    dicom_reader.Update()
    return dicom_reader

def create_color_transfer_function():
    """
    Create and return a color transfer function for volume rendering.
    """
    color_tf = vtk.vtkColorTransferFunction()
    color_tf.AddRGBPoint(0, 0.0, 0.0, 0.0)
    color_tf.AddRGBPoint(255, 1.0, 0.5, 0.0)
    return color_tf

def create_opacity_transfer_function():
    """
    Create and return an opacity transfer function for volume rendering.
    """
    opacity_tf = vtk.vtkPiecewiseFunction()
    opacity_tf.AddPoint(0, 0.0)
    opacity_tf.AddPoint(255, 1.0)
    return opacity_tf

def create_volume_mapper(reader_output):
    """
    Create and return a volume mapper with the given input data.
    """
    volume_mapper = vtk.vtkSmartVolumeMapper()
    volume_mapper.SetInputConnection(reader_output.GetOutputPort())
    return volume_mapper

def create_volume_property(color_tf, opacity_tf):
    """
    Create and return a volume property with the specified transfer functions.
    """
    volume_property = vtk.vtkVolumeProperty()
    volume_property.SetColor(color_tf)
    volume_property.SetScalarOpacity(opacity_tf)
    volume_property.SetInterpolationTypeToLinear()
    return volume_property

def create_volume_actor(mapper, property):
    """
    Create and return a volume actor with the given mapper and property.
    """
    volume_actor = vtk.vtkVolume()
    volume_actor.SetMapper(mapper)
    volume_actor.SetProperty(property)
    return volume_actor

def create_isosurface_actor(reader_output, iso_value):
    """
    Create and return an isosurface actor with the given input data and iso value.
    """
    isosurface = vtk.vtkMarchingCubes()
    isosurface.SetInputConnection(reader_output.GetOutputPort())
    isosurface.ComputeNormalsOn()
    isosurface.SetValue(0, iso_value)
    iso_mapper = vtk.vtkPolyDataMapper()
    iso_mapper.SetInputConnection(isosurface.GetOutputPort())
    iso_actor = vtk.vtkActor()
    iso_actor.SetMapper(iso_mapper)
    iso_actor.GetProperty().SetColor(1, 0, 0)
    return iso_actor

def setup_renderers(volume_actor, iso_actor):
    """
    Create renderers and assign actors to viewports.
    """
    renderer1 = vtk.vtkRenderer()
    renderer1.AddVolume(volume_actor)

    renderer2 = vtk.vtkRenderer()
    renderer2.AddActor(iso_actor)

    renderer3 = vtk.vtkRenderer()
    renderer3.AddVolume(volume_actor)
    renderer3.AddActor(iso_actor)

    return renderer1, renderer2, renderer3

def setup_viewports(renderers):
    """
    Set viewport positions and sizes for the given renderers.
    """
    render_window = vtk.vtkRenderWindow()
    for index, renderer in enumerate(renderers):
        render_window.AddRenderer(renderer)
        viewport_size = 500
        renderer.SetViewport(index / len(renderers), 0, (index + 1) / len(renderers), 1)
        if index == 0:
            renderer.SetBackground(0.1, 0.2, 0.3)  # Dark blue background for viewport 1
        elif index == 1:
            renderer.SetBackground(0.5, 0.5, 0.5)  # Light gray background for viewport 2
        elif index == 2:
            renderer.SetBackground(0.9, 0.8, 0.7)  # Light peach background for viewport 3

    render_window.SetSize(viewport_size * len(renderers), viewport_size)
    return render_window

def setup_camera(renderer, position, focal_point):
    """
    Set camera position and focal point for the given renderer.
    """
    camera = vtk.vtkCamera()
    camera.SetPosition(position)
    camera.SetFocalPoint(focal_point)
    renderer.SetActiveCamera(camera)
    renderer.ResetCamera()

def print_dataset_information(reader_output):
    """
    Print information about the dataset.
    """
    dimensions = reader_output.GetOutput().GetDimensions()
    voxel_size = reader_output.GetOutput().GetSpacing()
    min_pixel_value, max_pixel_value = reader_output.GetOutput().GetScalarRange()
    print("Dimensions of the Image: ", dimensions)
    print("Voxel Dimensions: ", voxel_size)
    print("Minimum Pixel Intensity: ", min_pixel_value)
    print("Maximum Pixel Intensity: ", max_pixel_value)

def main():
    directory = "Repeat3"
    iso_value = 100

    dicom_reader = read_dicom_data(directory)
    color_tf = create_color_transfer_function()
    opacity_tf = create_opacity_transfer_function()
    volume_mapper = create_volume_mapper(dicom_reader)
    volume_property = create_volume_property(color_tf, opacity_tf)
    volume_actor = create_volume_actor(volume_mapper, volume_property)
    iso_actor = create_isosurface_actor(dicom_reader, iso_value)

    renderer1, renderer2, renderer3 = setup_renderers(volume_actor, iso_actor)
    render_window = setup_viewports([renderer1, renderer2, renderer3])

    camera_position = (350, 400, 850)
    focal_point = (0, 0, 0)
    for renderer in [renderer1, renderer2, renderer3]:
        setup_camera(renderer, camera_position, focal_point)

    interactor = vtk.vtkRenderWindowInteractor()
    interactor.SetRenderWindow(render_window)
    interactor.Initialize()

    render_window.Render()
    interactor.Start()

    print_dataset_information(dicom_reader)

if __name__ == "__main__":
    main()

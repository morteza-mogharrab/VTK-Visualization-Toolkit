import vtk
from vtkmodules.vtkCommonColor import vtkNamedColors

def create_plane(center, normal):
    # Create a vtkPlane object with the given center and normal
    plane = vtk.vtkPlane()
    plane.SetOrigin(center)
    plane.SetNormal(normal)
    return plane

def create_clipped_mapper(reader, clip_function):
    # Create a vtkClipPolyData object to clip the input data
    clipper = vtk.vtkClipPolyData()
    clipper.SetInputConnection(reader.GetOutputPort())
    clipper.SetClipFunction(clip_function)
    clipper.GenerateClipScalarsOn()
    clipper.SetValue(0)
    clipper.Update()

    # Create a mapper for the clipped data
    clipped_mapper = vtk.vtkPolyDataMapper()
    clipped_mapper.SetInputConnection(clipper.GetOutputPort())
    return clipped_mapper

def create_actor(mapper, wireframe=False):
    # Create a vtkActor object and set its mapper
    actor = vtk.vtkActor()
    actor.SetMapper(mapper)
    if wireframe:
        # Set the representation of the actor to wireframe if specified
        actor.GetProperty().SetRepresentationToWireframe()
    return actor

def create_intersection_actor(reader, plane):
    # Create a vtkCutter object to find the intersection between the data and a plane
    cutter = vtk.vtkCutter()
    cutter.SetInputConnection(reader.GetOutputPort())
    cutter.SetCutFunction(plane)
    cutter.GenerateCutScalarsOn()
    cutter.SetValue(0, 0)

    # Use vtkStripper to create triangle strips from the cut output
    stripper = vtk.vtkStripper()
    stripper.SetInputConnection(cutter.GetOutputPort())
    stripper.Update()

    # Use vtkTriangleFilter to ensure triangles are well-defined
    triangle_filter = vtk.vtkTriangleFilter()
    triangle_filter.SetInputConnection(stripper.GetOutputPort())
    triangle_filter.Update()

    # Create a mapper and actor for the intersection area
    intersection_mapper = vtk.vtkPolyDataMapper()
    intersection_mapper.SetInputConnection(triangle_filter.GetOutputPort())

    intersection_actor = vtk.vtkActor()
    intersection_actor.SetMapper(intersection_mapper)
    return intersection_actor

def create_plane_actor(plane):
    # Use vtkSampleFunction to sample the plane implicit function
    sample = vtk.vtkSampleFunction()
    sample.SetImplicitFunction(plane)
    sample.SetModelBounds(reader.GetOutput().GetBounds())
    sample.SetSampleDimensions(40, 40, 40)
    sample.ComputeNormalsOff()

    # Use vtkContourFilter to generate contours from the sampled function
    contour = vtk.vtkContourFilter()
    contour.SetInputConnection(sample.GetOutputPort())
    contour.GenerateValues(2, 0, 0)

    # Create a mapper and actor for the plane
    plane_mapper = vtk.vtkPolyDataMapper()
    plane_mapper.SetInputConnection(contour.GetOutputPort())

    plane_actor = vtk.vtkActor()
    plane_actor.SetMapper(plane_mapper)
    plane_actor.GetProperty().SetRepresentationToWireframe()
    return plane_actor

# Read the input file
reader = vtk.vtkSTLReader()
reader.SetFileName("Owl_mechanical.stl")
reader.Update()

# Step 2: Create the clipping planes
center = reader.GetOutput().GetCenter()
plane_normal = (0, 0, 1)
plane = create_plane(center, plane_normal)

auxiliary_plane_normal = (0, 0, -1)
auxiliary_plane = create_plane(center, auxiliary_plane_normal)

# Step 3: Clip the data and create mappers for clipped and remaining parts
clipped_mapper = create_clipped_mapper(reader, plane)
remaining_mapper = create_clipped_mapper(reader, auxiliary_plane)

# Create actors for clipped and remaining parts
chipped_model_actor = create_actor(clipped_mapper, wireframe=True)  # Set wireframe representation
remaining_actor = create_actor(remaining_mapper)

# Step 4: Create actor for intersection area between plane and polygonal data
intersection_actor = create_intersection_actor(reader, plane)

# Step 5: Create actor for displaying the plane
plane_actor = create_plane_actor(plane)

# Set color to black for chipped model
chipped_model_actor.GetProperty().SetColor(0, 0, 0)  # Black

# Set colors for other actors
colors = vtkNamedColors()
remaining_actor.GetProperty().SetColor(colors.GetColor3d("Orange"))
intersection_actor.GetProperty().SetColor(colors.GetColor3d("Red"))
plane_actor.GetProperty().SetColor(colors.GetColor3d("Yellow"))

# Create renderer and add actors
renderer = vtk.vtkRenderer()
renderer.SetBackground(0.95, 0.95, 0.95)  # Light gray background
renderer.AddActor(chipped_model_actor)
renderer.AddActor(remaining_actor)
renderer.AddActor(intersection_actor)
renderer.AddActor(plane_actor)

# Create window and add renderer to it
window = vtk.vtkRenderWindow()
window.AddRenderer(renderer)
window.SetSize(1000, 650)

# Create interactor and start the visualization
interactor = vtk.vtkRenderWindowInteractor()
interactor.SetRenderWindow(window)
interactor.Initialize()
window.Render()
interactor.Start()

# Print number of points for vertices
vertices = reader.GetOutput()
print(vertices.GetNumberOfPoints())
vertices = clipped_mapper.GetInput()
print(vertices.GetNumberOfPoints())
vertices = remaining_mapper.GetInput()
print(vertices.GetNumberOfPoints())

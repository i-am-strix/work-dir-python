import bpy
import mathutils


def nodegroup_node_group():
    """Initialize nodegroup node group"""
    nodegroup = bpy.data.node_groups.new(type='GeometryNodeTree', name="NodeGroup")

    nodegroup.color_tag = 'NONE'
    nodegroup.description = ""
    nodegroup.default_group_node_width = 140

    # nodegroup interface

    # Socket Instances
    instances_socket = nodegroup.interface.new_socket(name="Instances", in_out='OUTPUT', socket_type='NodeSocketGeometry')
    instances_socket.attribute_domain = 'POINT'
    instances_socket.default_input = 'VALUE'
    instances_socket.structure_type = 'AUTO'

    # Socket Curve
    curve_socket = nodegroup.interface.new_socket(name="Curve", in_out='INPUT', socket_type='NodeSocketGeometry')
    curve_socket.attribute_domain = 'POINT'
    curve_socket.default_input = 'VALUE'
    curve_socket.structure_type = 'AUTO'

    # Socket Count
    count_socket = nodegroup.interface.new_socket(name="Count", in_out='INPUT', socket_type='NodeSocketInt')
    count_socket.default_value = 10
    count_socket.min_value = 2
    count_socket.max_value = 100000
    count_socket.subtype = 'NONE'
    count_socket.attribute_domain = 'POINT'
    count_socket.default_input = 'VALUE'
    count_socket.structure_type = 'AUTO'

    # Initialize nodegroup nodes

    # Node Group Output
    group_output = nodegroup.nodes.new("NodeGroupOutput")
    group_output.name = "Group Output"
    group_output.is_active_output = True

    # Node Group Input
    group_input = nodegroup.nodes.new("NodeGroupInput")
    group_input.name = "Group Input"

    # Node Instance on Points
    instance_on_points = nodegroup.nodes.new("GeometryNodeInstanceOnPoints")
    instance_on_points.name = "Instance on Points"
    # Selection
    instance_on_points.inputs[1].default_value = True
    # Pick Instance
    instance_on_points.inputs[3].default_value = False
    # Instance Index
    instance_on_points.inputs[4].default_value = 0
    # Rotation
    instance_on_points.inputs[5].default_value = (0.0, 0.0, 0.0)
    # Scale
    instance_on_points.inputs[6].default_value = (1.0, 1.0, 1.0)

    # Node Curve to Points
    curve_to_points = nodegroup.nodes.new("GeometryNodeCurveToPoints")
    curve_to_points.name = "Curve to Points"
    curve_to_points.mode = 'COUNT'

    # Node Curve Circle
    curve_circle = nodegroup.nodes.new("GeometryNodeCurvePrimitiveCircle")
    curve_circle.name = "Curve Circle"
    curve_circle.mode = 'RADIUS'
    # Resolution
    curve_circle.inputs[0].default_value = 8
    # Radius
    curve_circle.inputs[4].default_value = 0.2200000286102295

    # Node Extrude Mesh
    extrude_mesh = nodegroup.nodes.new("GeometryNodeExtrudeMesh")
    extrude_mesh.name = "Extrude Mesh"
    extrude_mesh.mode = 'EDGES'
    # Selection
    extrude_mesh.inputs[1].default_value = True
    # Offset
    extrude_mesh.inputs[2].default_value = (0.0, 0.0, 0.0)
    # Offset Scale
    extrude_mesh.inputs[3].default_value = 0.0700000524520874

    # Node Curve to Mesh
    curve_to_mesh = nodegroup.nodes.new("GeometryNodeCurveToMesh")
    curve_to_mesh.name = "Curve to Mesh"
    # Scale
    curve_to_mesh.inputs[2].default_value = 1.0
    # Fill Caps
    curve_to_mesh.inputs[3].default_value = False

    # Node Transform Geometry
    transform_geometry = nodegroup.nodes.new("GeometryNodeTransform")
    transform_geometry.name = "Transform Geometry"
    transform_geometry.mode = 'COMPONENTS'
    # Translation
    transform_geometry.inputs[1].default_value = (0.0, 0.0, 0.0)
    # Rotation
    transform_geometry.inputs[2].default_value = (1.5707963705062866, 0.0, 0.0)
    # Scale
    transform_geometry.inputs[3].default_value = (1.0, 1.0, 1.0)

    # Set locations
    group_output.location = (647.2504272460938, 0.0)
    group_input.location = (-657.2504272460938, 0.0)
    instance_on_points.location = (457.2503967285156, 116.12984466552734)
    curve_to_points.location = (128.55609130859375, 221.82046508789062)
    curve_circle.location = (-457.25042724609375, -136.47933959960938)
    extrude_mesh.location = (-140.22467041015625, -104.02094268798828)
    curve_to_mesh.location = (-290.89825439453125, -188.23562622070312)
    transform_geometry.location = (64.65023803710938, -221.82046508789062)

    # Set dimensions
    group_output.width, group_output.height = 140.0, 100.0
    group_input.width, group_input.height = 140.0, 100.0
    instance_on_points.width, instance_on_points.height = 140.0, 100.0
    curve_to_points.width, curve_to_points.height = 140.0, 100.0
    curve_circle.width, curve_circle.height = 140.0, 100.0
    extrude_mesh.width, extrude_mesh.height = 140.0, 100.0
    curve_to_mesh.width, curve_to_mesh.height = 140.0, 100.0
    transform_geometry.width, transform_geometry.height = 140.0, 100.0

    # Initialize nodegroup links

    # curve_to_points.Points -> instance_on_points.Points
    nodegroup.links.new(curve_to_points.outputs[0], instance_on_points.inputs[0])
    # extrude_mesh.Mesh -> transform_geometry.Geometry
    nodegroup.links.new(extrude_mesh.outputs[0], transform_geometry.inputs[0])
    # curve_circle.Curve -> curve_to_mesh.Curve
    nodegroup.links.new(curve_circle.outputs[0], curve_to_mesh.inputs[0])
    # transform_geometry.Geometry -> instance_on_points.Instance
    nodegroup.links.new(transform_geometry.outputs[0], instance_on_points.inputs[2])
    # curve_to_mesh.Mesh -> extrude_mesh.Mesh
    nodegroup.links.new(curve_to_mesh.outputs[0], extrude_mesh.inputs[0])
    # group_input.Curve -> curve_to_points.Curve
    nodegroup.links.new(group_input.outputs[0], curve_to_points.inputs[0])
    # group_input.Count -> curve_to_points.Count
    nodegroup.links.new(group_input.outputs[1], curve_to_points.inputs[1])
    # instance_on_points.Instances -> group_output.Instances
    nodegroup.links.new(instance_on_points.outputs[0], group_output.inputs[0])

    return nodegroup


nodegroup = nodegroup_node_group()

def ring_spline_node_group():
    """Initialize ring_spline_001 node group"""
    ring_spline_001 = bpy.data.node_groups.new(type='GeometryNodeTree', name="Ring Spline")

    ring_spline_001.color_tag = 'NONE'
    ring_spline_001.description = ""
    ring_spline_001.default_group_node_width = 140
    ring_spline_001.is_modifier = True

    # ring_spline interface

    # Socket Geometry
    geometry_socket = ring_spline_001.interface.new_socket(name="Geometry", in_out='OUTPUT', socket_type='NodeSocketGeometry')
    geometry_socket.attribute_domain = 'POINT'
    geometry_socket.default_input = 'VALUE'
    geometry_socket.structure_type = 'AUTO'

    # Socket Geometry
    geometry_socket_1 = ring_spline_001.interface.new_socket(name="Geometry", in_out='INPUT', socket_type='NodeSocketGeometry')
    geometry_socket_1.attribute_domain = 'POINT'
    geometry_socket_1.default_input = 'VALUE'
    geometry_socket_1.structure_type = 'AUTO'

    # Socket Ring Count
    ring_count_socket = ring_spline_001.interface.new_socket(name="Ring Count", in_out='INPUT', socket_type='NodeSocketInt')
    ring_count_socket.default_value = 10
    ring_count_socket.min_value = -2147483648
    ring_count_socket.max_value = 2147483647
    ring_count_socket.subtype = 'NONE'
    ring_count_socket.attribute_domain = 'POINT'
    ring_count_socket.default_input = 'VALUE'
    ring_count_socket.structure_type = 'AUTO'

    # Initialize ring_spline_001 nodes

    # Node Group Input
    group_input_1 = ring_spline_001.nodes.new("NodeGroupInput")
    group_input_1.name = "Group Input"

    # Node Group Output
    group_output_1 = ring_spline_001.nodes.new("NodeGroupOutput")
    group_output_1.name = "Group Output"
    group_output_1.is_active_output = True

    # Node Self Object
    self_object = ring_spline_001.nodes.new("GeometryNodeSelfObject")
    self_object.name = "Self Object"

    # Node Group
    group = ring_spline_001.nodes.new("GeometryNodeGroup")
    group.name = "Group"
    group.node_tree = nodegroup

    # Node Join Geometry
    join_geometry = ring_spline_001.nodes.new("GeometryNodeJoinGeometry")
    join_geometry.name = "Join Geometry"

    # Set locations
    group_input_1.location = (-571.2015380859375, -18.959209442138672)
    group_output_1.location = (31.392349243164062, 98.54254913330078)
    self_object.location = (-617.7067260742188, 334.8184509277344)
    group.location = (-359.622802734375, -6.107391357421875)
    join_geometry.location = (-196.81558227539062, 89.55317687988281)

    # Set dimensions
    group_input_1.width, group_input_1.height = 140.0, 100.0
    group_output_1.width, group_output_1.height = 140.0, 100.0
    self_object.width, self_object.height = 140.0, 100.0
    group.width, group.height = 140.0, 100.0
    join_geometry.width, join_geometry.height = 140.0, 100.0

    # Initialize ring_spline_001 links

    # group_input_1.Geometry -> group.Curve
    ring_spline_001.links.new(group_input_1.outputs[0], group.inputs[0])
    # group_input_1.Ring Count -> group.Count
    ring_spline_001.links.new(group_input_1.outputs[1], group.inputs[1])
    # group.Instances -> join_geometry.Geometry
    ring_spline_001.links.new(group.outputs[0], join_geometry.inputs[0])
    # join_geometry.Geometry -> group_output_1.Geometry
    ring_spline_001.links.new(join_geometry.outputs[0], group_output_1.inputs[0])
    # group_input_1.Geometry -> join_geometry.Geometry
    ring_spline_001.links.new(group_input_1.outputs[0], join_geometry.inputs[0])

    return ring_spline_001


ring_spline_001 = ring_spline_node_group()


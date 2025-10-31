import bpy
from .. util.driver_upd_dep import update_dependencies

def add_ring_spline(self, context):
    obj = context.object
    if obj is None:
        self.report({'ERROR'}, "No active object.")
        return {'CANCELLED'}

    # --- Create or reuse node group ---
    group_name = "RingSplineModifier"
    node_group = bpy.data.node_groups.get(group_name)
    if not node_group:
        from . ring_spline import ring_spline_node_group
        node_group = ring_spline_node_group()

    obj.wk_ring_spline_ring_count = 10

    # --- Add Geometry Nodes modifier ---
    mod = obj.modifiers.new(name=group_name, type='NODES')
    mod.node_group = node_group

    # --- Add a custom property on the object ---
    if "wk_ring_spline_ring_count" not in obj.keys():
        obj["wk_ring_spline_ring_count"] = int(10)  # default value

    fcurve = mod.driver_add('["Socket_2"]')
    driver = fcurve.driver
    var = driver.variables.new()
    var.name = 'prop'
    var.targets[0].id = obj
    var.targets[0].data_path = '["wk_ring_spline_ring_count"]'
    driver.expression = 'prop'
    update_dependencies(obj)

    return {'FINISHED'}
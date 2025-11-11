import bpy

def object_add_handler(scene):
    global previous_objects
    current_objects = set(bpy.data.objects)
    new_objects = current_objects - previous_objects

    if new_objects:
        for obj in new_objects:

            if obj.type == 'MESH':
                obj["WorkDirObjSignature"] = "TERRAIN"
            elif obj.type == 'CURVE':
                obj["WorkDirObjSignature"] = "SPLINE"
                obj.wk_spline_type = 2

    previous_objects = current_objects

# Register handler if not already
if object_add_handler not in bpy.app.handlers.depsgraph_update_post:
    bpy.app.handlers.depsgraph_update_post.append(object_add_handler)
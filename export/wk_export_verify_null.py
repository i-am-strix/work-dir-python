import bpy

def verify_null(self, context):
    for obj in bpy.context.scene.objects:
        if obj.sig_type is not None and obj.sig_type == "TERRAIN":
            if not bpy.context.scene.objects.get(obj.wk_terrain_moving_path):
                bpy.data.objects.remove(obj.wk_terrain_moving_path)
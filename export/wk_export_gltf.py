import bpy

# Exports the gltf component of the stage (the geometry)
def export_gltf(self, context, target_path):
    bpy.ops.export_scene.gltf(
        filepath=target_path,
        export_extras=True,
    )

    self.report({'INFO'}, "did it work?")
    return {'FINISHED'}
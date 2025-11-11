import bpy

class MigrateToWK2(bpy.types.Operator):
    bl_idname = "workdir.migrate_to_v2"
    bl_label = "Migrate v1 WorkDir to v2"
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"
    bl_category = "WorkDir"

    def draw(self, context):
        self.layout.operator("workdir.migration_window", text = "message").message = 'Sample Text'
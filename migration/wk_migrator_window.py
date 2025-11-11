import bpy

from mathutils import Vector

# Object migration table
object_valid_signatures = {
    "Spring": 10,
    "DashRing": 11,
    "JumpPanel": 12,
    "Ring": 13,
    "ItemBox": 14,
    "DashPanel": 19,
    "Balloon": 20,
    "GrindBooster": 21,
    "TrickPanel": 22,
    "Pulley": 23,
    "CameraArea": 24,
    "WaterArea": 25,
    "SkydiveVolume": 26,
    "SwingPole": 27,
    "SakuraSwing": 100,
    "SakuraGlider": 101,
    "SakuraBounceTree": 102,
    "Checkpoint": 28,
    "Thorn": 29,
    "ThornSpike": 30,
    "Motobug": 31,
    "Buzzbomber": 32,
    "EggPawn": 33,
    "BoxWood": 34,
    "BoxBoom": 35
}

class WorkDirMigrationWindow(bpy.types.Operator):
    bl_idname = "workdir.migration_window"
    bl_label = ""

    NOTICE_MESSAGE = "Before migration, do note that some objects cannot be migrated properly due to change in behavior."

    def migrate_objects(self, context):
        for obj in bpy.data.objects:
            keep_searching_keys = True
            match obj.type:
                case 'MESH':
                    if 'Geometry' in obj.name or 'Wallrun' in obj.name:
                        obj["WorkDirObjSignature"] = "TERRAIN"
                        if 'Hidden' in obj.name:
                            obj.wk_cmn_is_hidden = True
                        if 'JumpThru' in obj.name:
                            obj.wk_terrain_is_jump_thru = True
                        if 'Wallrun' in obj.name:
                            obj.wk_terrain_is_wall_run = True
                        continue

                    for key in object_valid_signatures.keys():
                        if not keep_searching_keys:
                            break

                        if 'SakuraBounceTree' in obj.name:
                            obj["WorkDirObjSignature"] = "OBJECT"
                            obj.select_set(True)
                            bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
                            obj.select_set(False)
                            obj.wk_obj_uuid = object_valid_signatures['SakuraBounceTree']

                        if 'DashRing' in obj.name:
                            obj["WorkDirObjSignature"] = "OBJECT"
                            obj.wk_obj_uuid = object_valid_signatures['DashRing']
                            if obj.get("Allow Trick") is None:
                                obj["Allow Trick"] = False
                            keep_searching_keys = False
                            break

                        if 'ThornSpike' in obj.name:
                            obj["WorkDirObjSignature"] = "OBJECT"
                            obj.wk_obj_uuid = object_valid_signatures['ThornSpike']
                            keep_searching_keys = False
                            break

                        if 'ItemBox' in obj.name:
                            obj["WorkDirObjSignature"] = "OBJECT"
                            match obj["Type"]:
                                case 1:
                                    obj.wk_obj_uuid = 14
                                    obj.name = "10 Ring Item Box"
                                case 2:
                                    obj.wk_obj_uuid = 15
                                    obj.name = "25 Ring Item Box"
                                case 3:
                                    obj.wk_obj_uuid = 16
                                    obj.name = "50 Ring Item Box"
                                case 4:
                                    obj.wk_obj_uuid = 17
                                    obj.name = "Shield Item Box"
                                case 5:
                                    obj.wk_obj_uuid = 18
                                    obj.name = "Speed Shoes Item Box"
                            keep_searching_keys = False
                            break

                        if 'WaterArea' in obj.name or 'CameraArea' in obj.name or 'SkydiveVolume' in obj.name:
                            obj["WorkDirObjSignature"] = "OBJECT"
                            # this is gonna be dumb but we need to rescale the object, update its default scale and reapply it
                            starting_scale = Vector([obj.scale[0], obj.scale[1], obj.scale[2]])
                            obj.scale = (0.5, 0.5, 0.5)
                            bpy.ops.object.select_all(action='DESELECT')
                            obj.select_set(True)
                            bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
                            obj.select_set(False)
                            obj.scale = starting_scale * 2
                            if 'WaterArea' in obj.name:
                                obj.wk_obj_uuid = object_valid_signatures['WaterArea']
                            if 'CameraArea' in obj.name:
                                obj.wk_obj_uuid = object_valid_signatures['CameraArea']
                            if 'SkydiveVolume' in obj.name:
                                obj.wk_obj_uuid = object_valid_signatures['SkydiveVolume']

                            break

                        if key in obj.name:
                            obj["WorkDirObjSignature"] = "OBJECT"
                            obj.wk_obj_uuid = object_valid_signatures[key]
                            keep_searching_keys = False

                    if 'PlayerStart' in obj.name:
                        obj["WorkDirObjSignature"] = "SPAWN_POINT"

                case 'CURVE':
                    if 'Rail' in obj.name:
                        obj["WorkDirObjSignature"] = "SPLINE"
                        obj.wk_spline_type = '0'
                        obj.wk_spline_rail_start_terminal = True
                        obj.wk_spline_rail_end_terminal = True

                    if 'Zipline' in obj.name:
                        obj["WorkDirObjSignature"] = "SPLINE"
                        obj.wk_spline_type = '1'

    def execute(self, context):
        self.report({'INFO'}, "Beginning migration")
        self.migrate_objects(context)
        self.report({'INFO'}, "Migration successfully completed")
        return {'FINISHED'}

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self, width=600, confirm_text = "Proceed")

    def draw(self, context):
        self.layout.label(text=self.NOTICE_MESSAGE, icon="ERROR")
        self.layout.label(text = "One such case are ziplines, which need to be completely replaced with their newer prefab.")
        self.layout.label(text="Are you sure you want to proceed with the migration step?")


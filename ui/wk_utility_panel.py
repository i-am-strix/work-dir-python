from typing import List

import bpy
from bpy.props import IntProperty, BoolProperty, EnumProperty, PointerProperty, FloatProperty
from enum import Enum

from .. nodes.op_add_ring_spline import add_ring_spline
from .. migration.wk_migrator_bootstrapper import MigrateToWK2


def attempt_get(obj, key):
    return obj.get(key) if obj.get(key) is not None else ""

class ObjectSelectPanel(bpy.types.Panel):
    bl_label = "Object Utility"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Item'

    @classmethod
    def poll(cls, context):
        return (context.object is not None)

    def draw_header(self, context):
        layout = self.layout
        layout.label(text="WorkDir")



#region Signature Draws
    # Common stuff
    bpy.types.Object.wk_cmn_disable_collision = BoolProperty(default = False)
    bpy.types.Object.wk_cmn_is_hidden = BoolProperty(default = False)

    def get_signature(self):
        return self.get("WorkDirObjSignature", "")

    def set_signature(self, value):
        self["WorkDirObjSignature"] = value

    bpy.types.Object.WorkDirObjSignature = bpy.props.StringProperty(
        name="Object Type",
        options={'HIDDEN'},
        get=get_signature,
        set=set_signature
    )


    #region Object Sig
    bpy.types.Object.wk_obj_uuid = IntProperty(default = 0)

    def draw_obj_sig(self, context, box):
        if not context.object:
            return

        box.label(text="OBJECT SIGNATURE")
        box.prop(context.object, "wk_obj_uuid", text="Object UUID (DO NOT MODIFY)")
        box.operator("find.wk_get_last_id", text="Get Last Unique ID")

    #endregion

    #region Terrain Sig

    # Define signature specific shit here
    # TODO: split this into multiple files

    bpy.types.Object.wk_terrain_is_jump_thru = BoolProperty(default = False)
    bpy.types.Object.wk_terrain_is_wall_run = BoolProperty(default = False)

    bpy.types.Object.wk_terrain_is_moving_platform = BoolProperty(default = False)
    bpy.types.Object.wk_terrain_moving_path = PointerProperty(type = bpy.types.Object, name = "Moving Path")
    bpy.types.Object.wk_terrain_moving_speed = FloatProperty(default = 1.0, name = "Movement Speed")
    bpy.types.Object.wk_terrain_start_time = FloatProperty(default = 0, name = "Start Time along Path", min = 0.0, max = 1.0)
    bpy.types.Object.wk_terrain_moving_use_linear = BoolProperty(default = False)

    def draw_terrain_sig(self, context, box):
        if not context.object:
            return

        box.label(text="TERRAIN SIGNATURE")

        box.prop(context.object, "wk_terrain_is_jump_thru", text="Is Jump Thru")
        box.prop(context.object, "wk_terrain_is_wall_run", text="Wall Run Surface")

        box.prop(context.object, "wk_terrain_is_moving_platform", text="Is Moving Platform")

        if context.object.wk_terrain_is_moving_platform is True:
            box.prop(context.object, "wk_terrain_moving_path", text = "Moving Path")
            box.prop(context.object, "wk_terrain_moving_speed", text = "Movement Speed")
            box.prop(context.object, "wk_terrain_start_time", text = "Start Time along Path")
            box.prop(context.object, "wk_terrain_moving_use_linear", text = "Use Linear Movement?")

    #endregion

    #region Spline Sig

    def update_spline_type(self, context):
        # self = current scene in an EnumProperty callback!
        if self.wk_spline_type == '3':
            add_ring_spline(self, context)
        else:
            if self.modifiers["RingSplineModifier"]:
                bpy.data.node_groups.remove(self.modifiers["RingSplineModifier"].node_group)
                self.modifiers.remove(self.modifiers.get("RingSplineModifier"))


    bpy.types.Object.wk_spline_type = EnumProperty(items=[
        ('0', 'Rail', ''),
        ('1', 'Zipline', ''),
        ('2', '2D Spline', ''),
        ('3', 'Ring Spline', ''),], update=update_spline_type)

    bpy.types.Object.wk_spline_rail_start_terminal = BoolProperty(default = True)
    bpy.types.Object.wk_spline_rail_end_terminal = BoolProperty(default = True)
    bpy.types.Object.wk_ring_spline_ring_count = IntProperty(default = 10)

    def draw_spline_sig(self, context, box):
        if not context.object:
            return

        box.label(text="SPLINE SIGNATURE")

        box.prop(context.object, "wk_spline_type", text="Spline Type")
        if context.object.wk_spline_type == '0':
            box.prop(context.object, "wk_spline_rail_start_terminal", text="Has Start Homing Target")
            box.prop(context.object, "wk_spline_rail_end_terminal", text="Has End Homing Target")
        elif context.object.wk_spline_type == '3':
            box.prop(context.object, "wk_ring_spline_ring_count", text="Ring Count")


    #endregion

    # region Trigger Sig

    bpy.types.Object.wk_trigger_type = EnumProperty(items=[
        ('0', 'Camera Trigger', ''),
        ('1', 'Semi Path Trigger', 'Applies semi-pathing (similar to loops)'),
        ('2', 'Full Path Trigger', 'Applies rigid, full pathing (similar to 2D splines)'),
        ('3', 'Skydive Trigger', '')])

    bpy.types.Object.wk_twod_trigger_target_spline = PointerProperty(type = bpy.types.Object, name = "Target Spline")
    bpy.types.Object.wk_trigger_reset_on_exit = BoolProperty(default = True)
    bpy.types.Object.wk_twod_trigger_apply_cam = BoolProperty(default = False)
    bpy.types.Object.wk_semi_trigger_stick_intensity = FloatProperty(default = 1.0)
    bpy.types.Object.wk_trigger_activation_type = EnumProperty(items = [
        ('0', 'Enter', ''),
        ('1', 'Exit', '')
    ])

    def draw_trigger_sig(self, context, box):
        if not context.object:
            return

        box.label(text="TRIGGER SIGNATURE")

        box.prop(context.object, "wk_trigger_type", text="Trigger Type")
        if context.object.wk_trigger_type == '1':
            box.prop(context.object, "wk_twod_trigger_target_spline", text = "Target Spline")
            box.prop(context.object, "wk_semi_trigger_stick_intensity", text="Stick Intensity")
        if context.object.wk_trigger_type == '2':
            box.prop(context.object, "wk_twod_trigger_target_spline", text = "Target Spline")
            box.prop(context.object, "wk_twod_trigger_apply_cam", text = "Apply 2D Camera")

        box.prop(context.object, "wk_trigger_reset_on_exit", text = "Reset Trigger On Exit")
        if not attempt_get(context.object, "wk_trigger_reset_on_exit"):
            box.prop(context.object, "wk_trigger_activation_type", text = "When To Trigger")



    # endregion

#endregion

    def draw(self, context):
        layout = self.layout

        box = layout.box()
        box.label(text="Define how the game interprets this object")
        box.label(text="If the object doesn't have a signature, the game won't recognise it!", icon="ERROR")

        _obj_op = box.operator("workdir.verify_sig", text="Define as Object")
        _obj_op.sig_type = 0
        _obj_op.clear_sig = False

        _terr_op = box.operator("workdir.verify_sig", text="Define as Terrain")
        _terr_op.sig_type = 1
        _terr_op.clear_sig = False

        _spline_op = box.operator("workdir.verify_sig", text="Define as Spline")
        _spline_op.sig_type = 2
        _spline_op.clear_sig = False

        _trigger_op = box.operator("workdir.verify_sig", text="Define as Trigger")
        _trigger_op.sig_type = 3
        _trigger_op.clear_sig = False

        _spawn_op = box.operator("workdir.verify_sig", text="Define as Spawn Point")
        _spawn_op.sig_type = 4
        _spawn_op.clear_sig = False

        box.separator()

        _clear_op = box.operator("workdir.verify_sig", text="Remove Signatures")
        _clear_op.clear_sig = True

        box = layout.box()
        box.label(text = "Common Settings")
        box.prop(context.object, "wk_cmn_disable_collision", text="Disable Collision?")
        box.prop(context.object, "wk_cmn_is_hidden", text="Is Hidden")

        box = layout.box()

        if bpy.context.selected_objects.__len__() == 1:
            if bpy.context.selected_objects[0].get('WorkDirObjSignature') is None:
                bpy.context.selected_objects[0]["WorkDirObjSignature"] = "TERRAIN"

            if bpy.context.selected_objects[0]["WorkDirObjSignature"] == "TERRAIN":
                self.draw_terrain_sig(context, box)

            elif bpy.context.selected_objects[0]["WorkDirObjSignature"] == "SPLINE":
                self.draw_spline_sig(context, box)

            elif bpy.context.selected_objects[0]["WorkDirObjSignature"] == "OBJECT":
                self.draw_obj_sig(context, box)

            elif bpy.context.selected_objects[0]["WorkDirObjSignature"] == "TRIGGER":
                self.draw_trigger_sig(context, box)

        box.operator("workdir.migration_window", text = "Migrate Stage to WorkDir v2")

def possible_items(context):
    return ["object", "terrain", "path", "trigger"]


class AddObjectSignature(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "workdir.verify_sig"
    bl_label = "Add Object Signature"

    sig_type : IntProperty(name="SignatureType", default = 0)
    clear_sig : BoolProperty(name="ClearSignature", default = False)

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        selected_objects = [obj for obj in context.selected_objects]

        for obj in selected_objects:
            if self.clear_sig is True:
                obj.WorkDirObjSignature = ""
                break

            match self.sig_type:
                case 0:
                    obj.WorkDirObjSignature = "OBJECT"
                case 1:
                    obj.WorkDirObjSignature = "TERRAIN"
                case 2:
                    obj.WorkDirObjSignature = "SPLINE"
                case 3:
                    obj.WorkDirObjSignature = "TRIGGER"
                case 4:
                    obj.WorkDirObjSignature = "SPAWN_POINT"

        return {'FINISHED'}

bpy.utils.register_class(AddObjectSignature)

class GetLastUniqueID(bpy.types.Operator):
    bl_idname = "find.wk_get_last_id"
    bl_label = "Get Last Unique ID"

    @classmethod
    def poll(cls, context):
        return context.active_object is not None
    def execute(self, context):
        highest_id = 0

        for obj in context.scene.objects:
            if obj.wk_obj_uuid > highest_id:
                highest_id = obj.wk_obj_uuid

        bpy.context.selected_objects[0].wk_obj_uuid = highest_id

        return {'FINISHED'}

bpy.utils.register_class(GetLastUniqueID)



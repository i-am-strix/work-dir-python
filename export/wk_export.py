import os
import shutil

import bpy
import json
from pathlib import Path

from bpy_extras.io_utils import ExportHelper
from bpy.props import StringProperty
import tempfile

from .wk_export_gltf import export_gltf
from .wk_export_splines import export_spline
from .signatures.wk_signature import analyze_signatures
from .signatures.export_signature import export_signature
from .wk_export_verify_null import verify_null

class WorkDirExport(bpy.types.Operator, ExportHelper):
    bl_idname = "export.horizons_stage"
    bl_label = "Sonic Horizons Stage"
    filename_ext = ".stg"
    filter_glob: StringProperty(
        default="*.stg",
        options={'HIDDEN'},
    )
    filepath: bpy.props.StringProperty(subtype="FILE_PATH")
    def execute(self, context):
        parent_path = Path(self.filepath).parent.absolute()

        os.mkdir(parent_path.joinpath("export"))
        work_folder = parent_path.joinpath("export").absolute()

        export_gltf(self, context, str(work_folder) + "/geometry.glb")
        export_spline(self, context, str(work_folder) + "/splines.cvd")
        export_signature(self, context, str(work_folder) + "/signatures.sig")

        # archive the stage and write to target location

        archive = shutil.make_archive(Path(self.filepath).stem, "zip", str(work_folder))
        if os.path.isfile(self.filepath):
            os.remove(self.filepath)

        shutil.move(archive, self.filepath)

        shutil.rmtree(parent_path.joinpath("export"), ignore_errors=True)

        self.report({'INFO'}, "Exported stage successfully")
        return {'FINISHED'}

    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}


def menu_func_export(self, context):
    self.layout.operator(WorkDirExport.bl_idname, text="Sonic Horizons Stage (.stg)")


bl_info = {
    "name": "Horizons Workdir System",
    "blender": (2, 80, 0),
    "category": "Tools",
    "description": "WorkDir Level pipeline for Sonic Horizons",
    "author": "strix",
    "version": (2, 0, 0),
}

from . export.wk_export import WorkDirExport
from . export.wk_export import menu_func_export
from . ui.wk_utility_panel import ObjectSelectPanel
import bpy

if "bpy" in locals():
    import importlib

    if "export.wk_export.WorkDirExport" in locals():
        importlib.reload(WorkDirExport)

def register():
    print("Hello World")
    bpy.utils.register_class(WorkDirExport)
    bpy.types.TOPBAR_MT_file_export.append(menu_func_export)
    bpy.utils.register_class(ObjectSelectPanel)

def unregister():
    print("Goodbye World")
    bpy.utils.unregister_class(WorkDirExport)
    bpy.types.TOPBAR_MT_file_export.remove(menu_func_export)
    bpy.utils.unregister_class(ObjectSelectPanel)

if __name__ == "__main__":
    register()
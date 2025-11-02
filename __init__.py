"""
Hi there, this is the WorkDir Blender source code

If you're snooping around here, I want you to know that I am, in fact, a HORRIBLE
Python developer, and that a lot of this code probably doesn't adhere to Python standards
or is even good

but it works in practice so like idgaf
"""

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
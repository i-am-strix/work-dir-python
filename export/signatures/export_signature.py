import bpy
import json
from typing import Generic, TypeVar, List, Dict

from .signature import WorkDirSignatureManager, SignatureComplianceOutputEncoder, WorkDirSignatureCompliantObject

sig_data = WorkDirSignatureManager([])

T = TypeVar('T')

def attempt_get(obj, key):
    return obj.get(key) if obj.get(key) is not None else ""

def export_signature(self, context, target_path):
    sig_data.signatures = []

    for obj in bpy.data.objects:
        output_sig_data = WorkDirSignatureCompliantObject(
            name = obj.name,
            uuid = int(attempt_get(obj, "obj_uuid")) if attempt_get(obj, "obj_uuid") is not "" else 0,
            signature = attempt_get(obj, "WorkDirObjSignature"),
            active = obj.visible_get(),
            spline_type = 0,
            custom_properties = {}
        )

        for key in obj.keys():
            value = obj[key]

            value_kind = type(value).__name__ # I found this online idk if this is good syntax lol
            if key == "WorkDirObjSignature":
                continue

            print(key, value, value_kind)

            if not value_kind == "Object": # if its not a pointer do the default shit
                output_sig_data.custom_properties[key] = str(value)
            else:
                name = getattr(value, "name", None)
                output_sig_data.custom_properties[key] = str(name)

        sig_data.signatures.append(output_sig_data)

    sig_js = json.dumps(sig_data, indent=1, cls=SignatureComplianceOutputEncoder)

    with open(target_path, 'w') as f:
        f.write(sig_js)

    self.report({'INFO'}, "exported signature to " + target_path)

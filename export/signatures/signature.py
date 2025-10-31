import json
import dataclasses

from typing import List, Dict

from dataclasses import dataclass
from json import JSONEncoder

@dataclass
class WorkDirSignatureCompliantObject:
    name: str
    object_uuid: int
    signature: str
    active: bool

    # terrain signature properties

    # spline signature properties

    spline_type : int

    custom_properties : dict[str, str]

    def __init__(self, name, uuid, signature, active, spline_type, custom_properties : dict[str, str]):
        self.name = name
        self.object_uuid = uuid
        self.signature = signature
        self.active = active
        self.spline_type = spline_type
        self.custom_properties = custom_properties

@dataclass
class WorkDirSignatureManager:
    signatures : List[WorkDirSignatureCompliantObject]

    def __init__(self, signatures):
        self.signatures = signatures

class SignatureComplianceOutputEncoder(json.JSONEncoder):
    def default(self, o: WorkDirSignatureManager):
        if dataclasses.is_dataclass(o):
            return dataclasses.asdict(o)
        return super().default(o)

import json
from dataclasses import dataclass
from mathutils import Quaternion, Vector
from typing import List
from json import JSONEncoder

#region Simple Data Types
@dataclass
class WorkDirVector3:
    x: float
    y: float
    z: float

    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    @classmethod
    def from_bvector(cls, v: Vector):
        return cls(v.x, v.y, v.z)

@dataclass
class WorkDirQuaternion:
    x: float
    y: float
    z: float
    w: float

    def __init__(self, x, y, z, w):
        self.x = x
        self.y = y
        self.z = z
        self.w = w

    @classmethod
    def from_bquat(cls, v: Quaternion):
        return cls(v.x, v.y, v.z, v.w)

#endregion


@dataclass
class WorkDirSplinePointData:
    position: WorkDirVector3

    def __init__(self, position):
        self.position = position

@dataclass
class WorkDirSplineObject:
    name: str
    object_id: str
    position: WorkDirVector3
    rotation_type: int # 0 is quaternion rotation, 1 is euler rotation, anything else is negligible
    quat_rotation: WorkDirQuaternion
    euler_rotation: WorkDirVector3
    scale: WorkDirVector3
    path_type: str
    points: list[WorkDirSplinePointData]

    def __init(self, name, object_id, position, rotation_type, quat_rotation, euler_rotation, scale, path_type, points):
        self.name = name
        self.object_id = object_id
        self.position = position
        self.rotation_type = rotation_type
        self.quat_rotation = quat_rotation
        self.euler_rotation = euler_rotation
        self.scale = scale
        self.path_type = path_type
        self.points = points

@dataclass
class WorkDirSplineOutput:
    splines: list[WorkDirSplineObject]

    def __init(self, splines):
        self.splines = splines

import dataclasses

class WorkDirSplineOutputEncoder(json.JSONEncoder):
    def default(self, o : WorkDirSplineObject):
        if dataclasses.is_dataclass(o):
            return dataclasses.asdict(o)
        return super().default(o)



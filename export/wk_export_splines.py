import bpy
import json

from mathutils import Vector

from ..data_types import WorkDirSplineObject, WorkDirSplinePointData, WorkDirSplineOutput, WorkDirSplineOutputEncoder, WorkDirVector3, WorkDirQuaternion
from mathutils import Quaternion, Vector

nurb_data = WorkDirSplineOutput([])


def sample_curve(t: float, curve_points) -> Vector:
    t = max(0.0, min(1.0, t))
    total = len(curve_points)
    idx_f = t * (total - 1)
    i0 = int(idx_f)
    i1 = min(i0 + 1, total - 1)
    frac = idx_f - i0
    return curve_points[i0].lerp(curve_points[i1], frac)

def export_spline(self, context, filepath):
    nurb_data.splines = []

    for obj in bpy.data.objects:
        self.report({'INFO'}, "object type: {0}".format(obj.type))
        if not obj or obj.type != 'CURVE':
            continue

        depsgraph = bpy.context.evaluated_depsgraph_get()
        eval_obj = obj.evaluated_get(depsgraph)
        curve_eval = eval_obj.to_mesh()

        spline = obj.data.splines[0]
        resolution = spline.resolution_u * len(spline.bezier_points or spline.points)

        curve_points = [v.co for v in curve_eval.vertices]

        output_rotation_euler = obj.rotation_euler.to_quaternion()
        output_rotation_quat = obj.rotation_quaternion

        output_quat = output_rotation_quat if obj.rotation_mode is "QUATERNION" else output_rotation_euler

        output_data = WorkDirSplineObject(obj.name,
                                          "0",
                                          WorkDirVector3.from_bvector(obj.location),
                                          obj.rotation_mode,
                                          WorkDirQuaternion(output_quat.x, -output_quat.z, output_quat.y, output_quat.w),
                                          WorkDirVector3.from_bvector(obj.rotation_euler),
                                          WorkDirVector3.from_bvector(obj.scale),
                                          "BEZIER",
                                          []
                                          )

        for i in range(resolution  + 1):  # we can't just push nurbs path data to the file, because Unity has absolutely zero idea how to represent it. Instead, we're going to sample some points from this and push a low res version to the file, and load that up
            time = i * 1.0 / resolution

            point = sample_curve(time, curve_points)

            output_data.points.append(WorkDirSplinePointData(WorkDirVector3.from_bvector(point)))

        nurb_data.splines.append(output_data)

        # curve = obj.data
        # self.report({'INFO'}, "curve type: {0}".format(curve.splines[0].type))

        # if curve.splines[0].type == "BEZIER":
            # export_bezier(obj, curve.splines[0])
        # elif curve.splines[0].type == "NURBS":
            # self.report({'INFO'}, "DOES THE NURBS THING EVEN WORK CMON")
            # export_path(obj, curve.splines[0])


    # man python sucks
    nurb_js = json.dumps(nurb_data, indent=1, cls=WorkDirSplineOutputEncoder)
    self.report({'INFO'}, "json output data: {0}".format(nurb_js))

    with open(filepath, 'w') as f:
        f.write(nurb_js)

    self.report({'INFO'}, "curve data written")
    return {'FINISHED'}

def export(obj : bpy.types.Object, spline):
    pass



'''
def export_bezier(obj : bpy.types.Object, spline):
    output_data = WorkDirSplineObject(obj.name,
                                      "0",
                                      WorkDirVector3(0,0,0),
                                      obj.rotation_mode,
                                      WorkDirQuaternion.from_bquat(obj.rotation_quaternion),
                                      WorkDirVector3.from_bvector(obj.rotation_euler),
                                      WorkDirVector3.from_bvector(obj.scale),
                                      "BEZIER",
                                      []
                                      )


    for point in spline.bezier_points:
        w_matrix = obj.matrix_world

        global_point_position = w_matrix @ point.co
        global_handle_left = w_matrix @ point.handle_left
        global_handle_right = w_matrix @ point.handle_right

        output_data.points.append(
            WorkDirSplinePointData(WorkDirVector3.from_bvector(global_point_position),
                                   WorkDirVector3.from_bvector(global_handle_left),
                                   WorkDirVector3.from_bvector(global_handle_right),
                                   point.tilt))

    nurb_data.splines.append(output_data)

def export_path(obj: bpy.types.Object, spline):
    print("DOES THIS WORK OR NOT")
    output_data = WorkDirSplineObject(obj.name,
                                      "0",
                                      WorkDirVector3(0,0,0),
                                      obj.rotation_mode,
                                      WorkDirQuaternion.from_bquat(obj.rotation_quaternion),
                                      WorkDirVector3.from_bvector(obj.rotation_euler),
                                      WorkDirVector3.from_bvector(obj.scale),
                                      "NURBS",
                                      []
                                      )

    """obj = bpy.context.object
        curve = obj.data.splines[0]
        
        # Number of sample points (higher = smoother)
        samples = 32
        points = []
        
        # Sample along the evaluated curve
        for i in range(samples + 1):
            t = i / samples
            co = obj.matrix_world @ obj.data.splines[0].evaluate(t)
            points.append([co.x, co.y, co.z])"""

    nurbs_sampling_samples = 32
    w_matrix = obj.matrix_world

    for i in range(nurbs_sampling_samples + 1): # we can't just push nurbs path data to the file, because Unity has absolutely zero idea how to represent it. Instead, we're going to sample some points from this and push a low res version to the file, and load that up
        time = i * 1.0 / nurbs_sampling_samples

        point = w_matrix @ spline.curve_time(time)

        output_data.points.append(WorkDirSplinePointData(WorkDirVector3.from_bvector(point),
                                                 WorkDirVector3(0, 0, 0),
                                                 WorkDirVector3(0, 0, 0),
                                                 point.tilt))




    nurb_data.splines.append(output_data)

'''

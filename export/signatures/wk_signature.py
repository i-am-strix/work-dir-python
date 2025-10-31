import bpy

def analyze_signatures(self, context):
    for obj in bpy.data.objects:
        for KEY, VALUE in obj.items():
            self.report({"INFO"}, "key {0} with value {1}".format(KEY, VALUE))
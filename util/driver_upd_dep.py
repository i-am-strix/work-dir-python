import bpy

"""
bo : bpy_types.Object
"""

def update_dependencies(ob):
    def update_exp(d):
        # https://blender.stackexchange.com/questions/118350/how-to-update-the-dependencies-of-a-driver-via-python-script
        d.driver.expression += " "
        d.driver.expression = d.driver.expression[:-1]
    try:
        drivers = ob.animation_data.drivers
        for d in drivers:
            update_exp(d)
    except AttributeError:
        return

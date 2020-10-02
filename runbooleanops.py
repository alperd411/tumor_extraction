import bpy
import sys
bpy.ops.import_mesh.stl(filepath=f'{sys.argv[1]}')
bpy.ops.object.origin_set(type='GEOMETRY_ORIGIN', center='MEDIAN')
bpy.context.active_object.name = 'alper'
bpy.ops.import_mesh.stl(filepath=f'{sys.argv[2]}')#küpün dosya yolunu kesinleştir


target_obj = bpy.data.objects["Tamkup"]
obj = bpy.data.objects["alper"]

BOOL = 'BOOLEAN'
    # first add them.

bool_mod = target_obj.modifiers.new(name='diff_' + obj.name, type=BOOL)
bool_mod.operation = 'DIFFERENCE'
bool_mod.object = obj

for modifier in target_obj.modifiers:
        bpy.ops.object.modifier_apply(modifier=modifier.name)

bpy.ops.object.select_all(action='DESELECT')
bpy.data.objects['alper'].select_set(True)
bpy.ops.object.delete(use_global=False, confirm=False)
bpy.ops.object.select_all()
bpy.ops.export_mesh.stl(filepath=f'{sys.argv[3]}')
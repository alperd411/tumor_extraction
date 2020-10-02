import bpy 

bpy.ops.import_mesh.stl(filepath='C:/Users/demir/PycharmProjects/tumor_extract/poly_tumor.stl')
bpy.ops.object.origin_set(type='GEOMETRY_ORIGIN', center='MEDIAN')
bpy.ops.import_mesh.stl(filepath='C:/Users/demir/PycharmProjects/deneme_contour_extraction/tamkup.stl')

bpy.ops.object.modifier_add(type='BOOLEAN')
print(bpy.ops.object.modifiers[0])
bpy.ops.object.modifiers["Boolean"].operation = 'DIFFERENCE'

bpy.ops.object.modifiers["Boolean"].object = bpy.data.objects["Poly Tumor"]
bpy.ops.object.modifier_apply(apply_as='DATA', modifier="Boolean")
for obj in bpy.context.selected_objects:
    obj.select_set(False)
bpy.data.objects['Poly Tumor'].select_set(True)
bpy.ops.object.delete(use_global=False, confirm=False)

import bpy, os

# 1) Ensure the .blend file is saved
blend_fp = bpy.data.filepath
if not blend_fp:
    raise RuntimeError("Please save the .blend file first!")

# 2) Create Export folder next to the .blend file
blend_dir  = os.path.dirname(blend_fp)
output_dir = os.path.join(blend_dir, "Export")
os.makedirs(output_dir, exist_ok=True)

# 3) Set render engine to Cycles and prepare EMIT bake
scene = bpy.context.scene
scene.render.engine = 'CYCLES'
scene.cycles.bake_type = 'EMIT'
scene.render.bake_margin = 16

# 4) Iterate over all selected mesh objects
for obj in [o for o in bpy.context.selected_objects if o.type == 'MESH']:
    # a) Set object as active
    bpy.ops.object.select_all(action='DESELECT')
    obj.select_set(True)
    bpy.context.view_layer.objects.active = obj

    # b) Ensure UV map exists
    if not obj.data.uv_layers:
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.uv.smart_project(angle_limit=66, island_margin=0.02)
        bpy.ops.object.mode_set(mode='OBJECT')

    # c) Get original material and Base Color image
    mat = obj.active_material
    if not mat or not mat.use_nodes:
        raise RuntimeError(f"{obj.name} has no node-based material!")
    bsdf = next((n for n in mat.node_tree.nodes if n.type == 'BSDF_PRINCIPLED'), None)
    if not bsdf:
        raise RuntimeError(f"No Principled BSDF found in material {mat.name}!")
    input_link = bsdf.inputs['Base Color'].links
    if not input_link:
        raise RuntimeError(f"Base Color of {mat.name} is not linked!")
    orig_node = input_link[0].from_node
    if orig_node.type != 'TEX_IMAGE':
        raise RuntimeError("Base Color link is not from an image texture node!")
    orig_image = orig_node.image

    # d) Create new low-res bake image (e.g. 512x512)
    img_name = f"{obj.name}_Baked"
    bake_img = bpy.data.images.new(img_name, width=512, height=512)

    # e) Replace material nodes for EMIT bake
    tree = mat.node_tree
    tree.nodes.clear()
    bake_node = tree.nodes.new('ShaderNodeTexImage')
    bake_node.image = bake_img
    bake_node.select = True
    tree.nodes.active = bake_node
    color_node = tree.nodes.new('ShaderNodeTexImage')
    color_node.image = orig_image
    emit_node = tree.nodes.new('ShaderNodeEmission')
    out_node = tree.nodes.new('ShaderNodeOutputMaterial')
    links = tree.links
    links.new(color_node.outputs['Color'], emit_node.inputs['Color'])
    links.new(emit_node.outputs['Emission'], out_node.inputs['Surface'])

    # f) Perform EMIT bake (no lighting/shadows)
    bpy.ops.object.bake(type='EMIT', use_clear=True, margin=16)

    # g) Save baked image
    bake_path = os.path.join(output_dir, img_name + ".png")
    bake_img.filepath_raw = bake_path
    bake_img.file_format = 'PNG'
    bake_img.save()

    # h) Create new material with baked texture
    new_mat = bpy.data.materials.new(name=f"{obj.name}_Baked_Mat")
    new_mat.use_nodes = True
    nt = new_mat.node_tree
    nt.nodes.clear()
    bsdf2 = nt.nodes.new('ShaderNodeBsdfPrincipled')
    out2 = nt.nodes.new('ShaderNodeOutputMaterial')
    tex2 = nt.nodes.new('ShaderNodeTexImage')
    tex2.image = bake_img
    nt.links.new(tex2.outputs['Color'], bsdf2.inputs['Base Color'])
    nt.links.new(bsdf2.outputs['BSDF'], out2.inputs['Surface'])
    obj.data.materials.clear()
    obj.data.materials.append(new_mat)

    # i) Export as FBX with embedded texture
    fbx_path = os.path.join(output_dir, obj.name + ".fbx")
    bpy.ops.export_scene.fbx(
        filepath=fbx_path,
        use_selection=True,
        apply_unit_scale=True,
        apply_scale_options='FBX_SCALE_ALL',
        path_mode='COPY',
        embed_textures=True,
        add_leaf_bones=False,
        bake_space_transform=True
    )

print("✅ Done! Check the Export folder:", output_dir)

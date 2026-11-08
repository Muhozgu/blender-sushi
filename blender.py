
import bpy
import math
import bmesh
import random
from mathutils import Vector
import bpy

# =====================================================
# PREMIUM SUSHI STUDIO
# Professional procedural Blender scene
# Blender 4.x
# =====================================================

random.seed(12)

# ---------------- SCENE RESET ------------------------

bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)

for datablocks in (bpy.data.materials, bpy.data.curves):
    pass

scene = bpy.context.scene
scene.render.engine = 'BLENDER_EEVEE'
scene.render.resolution_x = 1600
scene.render.resolution_y = 1200
scene.render.resolution_percentage = 100

# ---------------- MATERIAL SYSTEM --------------------

def material(name, color, roughness=0.45,
             metallic=0.0, noise=False):

    mat = bpy.data.materials.new(name)
    mat.diffuse_color = (*color, 1)
    mat.use_nodes = True

    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    bsdf = nodes.get("Principled BSDF")

    bsdf.inputs["Base Color"].default_value = (*color, 1)
    bsdf.inputs["Roughness"].default_value = roughness
    bsdf.inputs["Metallic"].default_value = metallic

    if noise:
        tex = nodes.new("ShaderNodeTexNoise")
        tex.inputs["Scale"].default_value = 35
        tex.inputs["Detail"].default_value = 3
        tex.inputs["Roughness"].default_value = 0.7

        bump = nodes.new("ShaderNodeBump")
        bump.inputs["Strength"].default_value = 0.16
        bump.inputs["Distance"].default_value = 0.035

        links.new(tex.outputs["Fac"], bump.inputs["Height"])
        links.new(bump.outputs["Normal"], bsdf.inputs["Normal"])

    return mat


rice_mat = material("01 | Pearl White Rice",
                    (0.91, 0.86, 0.72), 0.72, noise=True)

nori_mat = material("02 | Roasted Nori",
                    (0.018, 0.045, 0.025), 0.5, noise=True)

salmon_mat = material("03 | Fresh Salmon",
                      (0.95, 0.22, 0.075), 0.3, noise=True)

fat_mat = material("04 | Salmon Fat",
                   (1.0, 0.72, 0.48), 0.32)

avocado_mat = material("05 | Avocado",
                       (0.27, 0.48, 0.12), 0.42)

cucumber_mat = material("06 | Cucumber",
                        (0.22, 0.55, 0.22), 0.4)

black_mat = material("07 | Sesame Black",
                     (0.015, 0.012, 0.009), 0.4)

white_mat = material("08 | Sesame White",
                     (0.98, 0.91, 0.75), 0.45)

plate_mat = material("09 | Midnight Ceramic",
                     (0.035, 0.055, 0.075), 0.24, 0.18)

table_mat = material("10 | Dark Walnut",
                     (0.095, 0.045, 0.025), 0.48, noise=True)

ginger_mat = material("11 | Pickled Ginger",
                      (0.95, 0.48, 0.42), 0.4)

wasabi_mat = material("12 | Wasabi",
                      (0.38, 0.58, 0.12), 0.5)

soy_mat = material("13 | Soy Sauce",
                   (0.055, 0.018, 0.008), 0.18)

# ---------------- OBJECT HELPERS ---------------------

def cube(name, loc, dimensions, mat, bevel=0.04):

    bpy.ops.mesh.primitive_cube_add(size=1, location=loc)
    obj = bpy.context.object
    obj.name = name
    obj.dimensions = dimensions

    bpy.ops.object.transform_apply(
        location=False, rotation=False, scale=True
    )

    obj.data.materials.append(mat)

    if bevel:
        mod = obj.modifiers.new("Precision Edge Bevel", 'BEVEL')
        mod.width = bevel
        mod.segments = 4

        obj.modifiers.new("Weighted Surface Normals", 'WEIGHTED_NORMAL')

    return obj


def array_sushi(obj):

    horizontal = obj.modifiers.new("01 | Three Sushi Pieces", 'ARRAY')
    horizontal.count = 3
    horizontal.use_relative_offset = False
    horizontal.use_constant_offset = True
    horizontal.constant_offset_displace = (1.55, 0, 0)

    vertical = obj.modifiers.new("02 | Second Sushi Row", 'ARRAY')
    vertical.count = 2
    vertical.use_relative_offset = False
    vertical.use_constant_offset = True
    vertical.constant_offset_displace = (0, 1.48, 0)

    return obj


def cylinder(name, loc, radius, depth, mat, vertices=64):

    bpy.ops.mesh.primitive_cylinder_add(
        vertices=vertices,
        radius=radius,
        depth=depth,
        location=loc
    )

    obj = bpy.context.object
    obj.name = name
    obj.data.materials.append(mat)

    bevel = obj.modifiers.new("Soft Edge", 'BEVEL')
    bevel.width = min(depth * 0.25, 0.06)
    bevel.segments = 3

    obj.modifiers.new("Weighted Normals", 'WEIGHTED_NORMAL')
    return obj


def linked_duplicate(obj, location, name):

    new_obj = obj.copy()
    new_obj.data = obj.data
    bpy.context.collection.objects.link(new_obj)
    new_obj.location = location
    new_obj.name = name

    return new_obj


# =====================================================
# 01 | SUSHI RICE BODY
# =====================================================

# One detailed rice block, repeated with Array modifiers.

rice = cube(
    "SUSHI | Rice Foundation",
    (-1.55, -0.74, 0.69),
    (1.32, 1.20, 0.86),
    rice_mat,
    0.10
)

# Subdivision Surface modifier
sub = rice.modifiers.new("Subdivision | Soft Rice Form", 'SUBSURF')
sub.levels = 1
sub.render_levels = 2

# Array modifiers
array_sushi(rice)

# =====================================================
# 02 | NATURE OF NORI
# Four seaweed strips around each rice block
# =====================================================

nori_specs = [
    ((-1.55, -0.74 - 0.60, 0.67), (1.30, 0.055, 0.78)),
    ((-1.55, -0.74 + 0.60, 0.67), (1.30, 0.055, 0.78)),
    ((-1.55 - 0.66, -0.74, 0.67), (0.055, 1.16, 0.78)),
    ((-1.55 + 0.66, -0.74, 0.67), (0.055, 1.16, 0.78))
]

for i, (loc, dims) in enumerate(nori_specs):

    seaweed = cube(
        "NORI | Seaweed Panel " + str(i + 1),
        loc, dims, nori_mat, 0.018
    )

    array_sushi(seaweed)

# =====================================================
# 03 | SALMON TOPPING
# =====================================================

salmon = cube(
    "SALMON | Fresh Fish Layer",
    (-1.55, -0.74, 1.16),
    (1.17, 0.99, 0.20),
    salmon_mat,
    0.095
)

array_sushi(salmon)

# =====================================================
# 04 | SALMON FAT LINES
# =====================================================

def create_stripe(name, x_offset):

    curve = bpy.data.curves.new(name, 'CURVE')
    curve.dimensions = '3D'
    curve.resolution_u = 16
    curve.bevel_depth = 0.014
    curve.bevel_resolution = 3

    spline = curve.splines.new('POLY')

    points = [
        (-0.42 + x_offset, -0.36, 0.0),
        (-0.30 + x_offset, -0.12, 0.015),
        (-0.36 + x_offset, 0.12, 0.015),
        (-0.22 + x_offset, 0.37, 0.0)
    ]

    spline.points.add(len(points) - 1)

    for p, co in zip(spline.points, points):
        p.co = (*co, 1)

    obj = bpy.data.objects.new(name, curve)
    bpy.context.collection.objects.link(obj)

    obj.location = (-1.55, -0.74, 1.275)
    obj.data.materials.append(fat_mat)

    array_sushi(obj)

    return obj


for i, offset in enumerate([-0.23, 0.0, 0.23]):
    create_stripe("SALMON | Marbling " + str(i + 1), offset)

# =====================================================
# 05 | AVOCADO AND CUCUMBER FILLING
# =====================================================

avocado = cube(
    "FILLING | Avocado",
    (-1.55, -0.74, 1.29),
    (0.37, 0.43, 0.045),
    avocado_mat,
    0.055
)
array_sushi(avocado)

cucumber = cube(
    "FILLING | Cucumber",
    (-1.55, -0.74, 1.32),
    (0.17, 0.28, 0.035),
    cucumber_mat,
    0.025
)
array_sushi(cucumber)

# =====================================================
# 06 | INDIVIDUAL RICE GRAINS
# Linked duplication for efficiency
# =====================================================

bpy.ops.mesh.primitive_uv_sphere_add(
    segments=12,
    ring_count=8,
    radius=1,
    location=(-2.0, -1.15, 1.12)
)

grain = bpy.context.object
grain.name = "RICE | Master Grain"
grain.scale = (0.035, 0.018, 0.023)
grain.data.materials.append(rice_mat)

# A restrained set of grains around the visible top edges
for row in range(2):
    for col in range(5):

        x = -2.02 + col * 0.19
        y = -1.18 + row * 0.16

        g = linked_duplicate(
            grain,
            (x, y, 1.115),
            "RICE | Linked Grain"
        )

        g.rotation_euler[2] = random.uniform(-0.5, 0.5)

# =====================================================
# 07 | SESAME SEEDS
# =====================================================

for i in range(32):

    x = random.uniform(-0.48, 0.48)
    y = random.uniform(-0.40, 0.40)

    # Restrict to the topping surface
    if abs(x) < 0.53 and abs(y) < 0.43:

        bpy.ops.mesh.primitive_uv_sphere_add(
            segments=8,
            ring_count=6,
            radius=1,
            location=(-1.55 + x, -0.74 + y, 1.275)
        )

        seed = bpy.context.object
        seed.name = "SESAME | Seed"
        seed.scale = (0.023, 0.012, 0.009)
        seed.data.materials.append(
            white_mat if i % 2 == 0 else black_mat
        )

        # Use linked duplicates for remaining sushi rows
        if i == 0:
            master_seed = seed

# =====================================================
# 08 | CERAMIC SERVING PLATE
# =====================================================

plate = cylinder(
    "PLATE | Midnight Ceramic",
    (0, 0, 0.04),
    1,
    0.22,
    plate_mat,
    128
)

plate.scale = (4.25, 2.75, 1)

# Refined rim
bpy.ops.mesh.primitive_torus_add(
    major_radius=1,
    minor_radius=0.025,
    major_segments=128,
    minor_segments=12,
    location=(0, 0, 0.17)
)

rim = bpy.context.object
rim.name = "PLATE | Decorative Rim"
rim.scale = (3.95, 2.45, 0.55)
rim.data.materials.append(fat_mat)

# =====================================================
# 09 | SOY SAUCE DISH
# =====================================================

dish = cylinder(
    "SIDE | Soy Sauce Dish",
    (3.0, -1.35, 0.23),
    0.63,
    0.16,
    plate_mat
)

dish.scale.x = 1.2
dish.scale.y = 0.85

sauce = cylinder(
    "SIDE | Soy Sauce",
    (3.0, -1.35, 0.33),
    0.51,
    0.035,
    soy_mat
)

sauce.scale.x = 1.2
sauce.scale.y = 0.85

# =====================================================
# 10 | WASABI
# =====================================================

bpy.ops.mesh.primitive_uv_sphere_add(
    segments=24,
    ring_count=16,
    radius=1,
    location=(2.85, 1.45, 0.32)
)

wasabi = bpy.context.object
wasabi.name = "SIDE | Wasabi"
wasabi.scale = (0.35, 0.26, 0.17)
wasabi.data.materials.append(wasabi_mat)

# =====================================================
# 11 | PICKLED GINGER
# =====================================================

for i in range(5):

    bpy.ops.mesh.primitive_uv_sphere_add(
        segments=20,
        ring_count=12,
        radius=1,
        location=(
            3.25 + i * 0.09,
            1.35 + math.sin(i * 0.8) * 0.12,
            0.30 + i * 0.015
        )
    )

    ginger = bpy.context.object
    ginger.name = "SIDE | Pickled Ginger"
    ginger.scale = (0.22, 0.12, 0.035)
    ginger.rotation_euler[2] = i * 0.25
    ginger.data.materials.append(ginger_mat)

# =====================================================
# 12 | CHOPSTICKS
# =====================================================

def make_stick(name, start, end, radius, mat):

    start = Vector(start)
    end = Vector(end)

    direction = end - start

    bpy.ops.mesh.primitive_cylinder_add(
        vertices=32,
        radius=radius,
        depth=direction.length,
        location=(start + end) / 2
    )

    obj = bpy.context.object
    obj.name = name
    obj.rotation_euler = direction.to_track_quat('Z', 'Y').to_euler()
    obj.data.materials.append(mat)

    bevel = obj.modifiers.new("Polished Stick Edges", 'BEVEL')
    bevel.width = 0.012
    bevel.segments = 3

    return obj


chopstick_mat = material(
    "14 | Lacquered Chopsticks",
    (0.11, 0.025, 0.015),
    0.23,
    0.2
)

make_stick(
    "CHOPSTICKS | One",
    (1.7, 2.2, 0.25),
    (3.8, 3.0, 0.25),
    0.045,
    chopstick_mat
)

make_stick(
    "CHOPSTICKS | Two",
    (1.8, 2.0, 0.25),
    (3.9, 2.8, 0.25),
    0.045,
    chopstick_mat
)

# =====================================================
# 13 | WOODEN STUDIO TABLE
# =====================================================

table = cube(
    "ENVIRONMENT | Walnut Studio Surface",
    (0, 0, -0.24),
    (200, 200, 0.25),
    table_mat,
    0
)

# =====================================================
# 14 | PROFESSIONAL LIGHTING
# =====================================================

def area_light(name, location, power, size, color):

    bpy.ops.object.light_add(
        type='AREA',
        location=location
    )

    light = bpy.context.object
    light.name = name
    light.data.energy = power
    light.data.shape = 'DISK'
    light.data.size = size
    light.data.color = color

    target = Vector((0, 0, 0.5))
    direction = target - light.location

    light.rotation_euler = direction.to_track_quat(
        '-Z', 'Y'
    ).to_euler()

    return light


area_light(
    "LIGHT | Main Softbox",
    (-3, -4, 8),
    1400,
    6,
    (1.0, 0.83, 0.68)
)

area_light(
    "LIGHT | Cool Fill",
    (5, 1, 6),
    1000,
    5,
    (0.72, 0.84, 1.0)
)

area_light(
    "LIGHT | Back Rim",
    (-2, 5, 5),
    1700,
    4,
    (1.0, 0.55, 0.35)
)

# =====================================================
# 15 | CAMERA COMPOSITION
# =====================================================

bpy.ops.object.camera_add(
    location=(7.5, -9.5, 8.5)
)

camera = bpy.context.object
camera.name = "CAMERA | Sushi Hero Shot"

target = Vector((0.1, 0.0, 0.4))
direction = target - camera.location

camera.rotation_euler = direction.to_track_quat(
    '-Z', 'Y'
).to_euler()

camera.data.type = 'ORTHO'
camera.data.ortho_scale = 10.8
camera.data.lens = 50

scene.camera = camera

# =====================================================
# 16 | WORLD AND RENDER
# =====================================================

world = bpy.data.worlds.new("Studio Environment")
scene.world = world
world.use_nodes = True

world.node_tree.nodes["Background"].inputs[0].default_value = (
    0.075, 0.085, 0.11, 1
)

world.node_tree.nodes["Background"].inputs[1].default_value = 0.35

scene.render.resolution_x = 1600
scene.render.resolution_y = 1200
scene.render.resolution_percentage = 100

scene.render.image_settings.file_format = 'PNG'

scene.render.engine = 'BLENDER_EEVEE'

scene.render.image_settings.color_mode = 'RGBA'

# Ambient lighting and shadows
scene.render.film_transparent = False

# Color management
scene.view_settings.view_transform = 'AgX'
scene.view_settings.look = 'AgX - Medium High Contrast'
scene.view_settings.exposure = 0
scene.view_settings.gamma = 1

# Camera depth of field disabled for clear presentation

# Select main sushi object
bpy.ops.object.select_all(action='DESELECT')
rice.select_set(True)


# Demonstrate Inset and Extrude Along Normals

bpy.context.view_layer.objects.active = rice
rice.select_set(True)

bpy.ops.object.mode_set(mode='EDIT')
bpy.ops.mesh.select_mode(type='FACE')
bpy.ops.mesh.select_all(action='DESELECT')

bm = bmesh.from_edit_mesh(rice.data)

top_face = max(bm.faces, key=lambda f: f.normal.z)
top_face.select_set(True)

bmesh.update_edit_mesh(rice.data)

# Inset selected face
bpy.ops.mesh.inset(thickness=0.025)

# Extrude along normals
bpy.ops.mesh.extrude_region_shrink_fatten(
    TRANSFORM_OT_shrink_fatten={"value": 0.008}
)

bpy.ops.object.mode_set(mode='OBJECT')

print("==========================================")
print("PREMIUM SUSHI SCENE SUCCESSFULLY CREATED")
print("6 sushi pieces with layered materials")
print("Nori, salmon, rice and decorative details")
print("Ceramic plate, sauce, ginger and wasabi")
print("Professional camera and studio lighting")
print("Press F12 to render")
print("==========================================")

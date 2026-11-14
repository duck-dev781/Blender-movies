# The Toilet That Wanted Revenge — Blender 2.79 scene builder
# Creates an editable 50-minute cartoon animatic project.
import bpy, math, os
from mathutils import Vector

def mat(name, color):
    m = bpy.data.materials.new(name)
    m.diffuse_color = (color[0], color[1], color[2])
    return m

def cube(name, loc, scale, material):
    bpy.ops.mesh.primitive_cube_add(location=loc)
    o=bpy.context.object; o.name=name; o.dimensions=scale
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    o.data.materials.append(material)
    bevel=o.modifiers.new("Cartoon soft edges","BEVEL"); bevel.width=.08; bevel.segments=2
    return o

def ball(name, loc, scale, material):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=20, ring_count=12, location=loc)
    o=bpy.context.object; o.name=name; o.scale=scale; o.data.materials.append(material)
    for p in o.data.polygons: p.use_smooth=True
    return o

def text(body, loc, size, material):
    c=bpy.data.curves.new(body,"FONT"); c.body=body; c.size=size; c.extrude=.004
    o=bpy.data.objects.new(body,c); bpy.context.scene.objects.link(o)
    o.location=loc; o.rotation_euler=(math.radians(90),0,0); o.data.materials.append(material)
    return o

def aim(cam, target):
    cam.rotation_euler=(Vector(target)-cam.location).to_track_quat("-Z","Y").to_euler()

# Clean default scene
bpy.ops.object.select_all(action="SELECT"); bpy.ops.object.delete(use_global=False)
s=bpy.context.scene
s.frame_start=1; s.frame_end=72000; s.render.fps=24
s.render.resolution_x=640; s.render.resolution_y=360; s.render.resolution_percentage=50
s.render.image_settings.file_format="PNG"; s.render.filepath="//frames/"
s.render.engine="BLENDER_RENDER"
s.world.horizon_color=(.12,.16,.22)

porcelain=mat("Glossy porcelain",(.92,.96,1.0))
blue=mat("Bathroom blue",(.08,.32,.72)); tile=mat("Tile",(.55,.75,.86))
dark=mat("Midnight",(.025,.035,.08)); skin=mat("Warm skin",(.82,.48,.3))
yellow=mat("Sunny shirt",(1,.62,.04)); purple=mat("Purple trousers",(.24,.08,.42))
red=mat("Hero red",(.85,.04,.06)); gold=mat("Gold", (1,.58,.04))
white=mat("White",(.96,.98,1)); black=mat("Black",(.01,.01,.02))
green=mat("Sewer green",(.08,.32,.2)); steel=mat("Steel",(.3,.38,.45))

# Four connected stage locations: bathroom, sewer, city, resistance HQ
stages=[(-0, "BATHROOM", tile, blue),(30,"SEWER",green,dark),(60,"CITY",dark,blue),(90,"RESISTANCE HQ",steel,dark)]
for x,label,floor_mat,wall_mat in stages:
    cube(label+" floor",(x,0,-.3),(20,14,.6),floor_mat)
    cube(label+" back wall",(x,6,3.5),(20,.4,7),wall_mat)
    text(label,(x-3,5.72,5.8),.55,gold)
# Bathroom tile accents and city buildings
for x in range(-8,9,2): cube("Wall tile stripe",(x,5.72,2.7),(.045,.04,5.4),white)
for x,h in [(52,4),(56,6),(60,5),(64,7),(68,4)]:
    cube("City block",(x,5.65,h/2),(2.4,.5,h),dark)
for x in range(24,38,3):
    bpy.ops.object.lamp_add(type="POINT", location=(x,3,3))
    bpy.context.object.data.energy=90

# Main toilet character: bowl, tank, seat, eyes, brows, arms and feet
toilet=ball("TOILET — animation root",(-1.5,.8,1.0),(.95,1,.55),porcelain)
parts=[
 cube("Toilet tank",(-1.5,2,1.75),(1.35,.62,1.55),porcelain),
 ball("Toilet pedestal",(-1.5,.85,.48),(.6,.75,.6),porcelain),
 ball("Toilet seat",(-1.5,.65,1.3),(.95,.95,.15),dark),
 cube("Raised lid",(-1.5,1.55,1.75),(1.5,.15,1.55),porcelain),
 ball("Eye L",(-1.82,1.52,2.05),(.18,.08,.22),white),
 ball("Eye R",(-1.18,1.52,2.05),(.18,.08,.22),white),
 ball("Pupil L",(-1.82,1.42,2.05),(.07,.04,.1),black),
 ball("Pupil R",(-1.18,1.42,2.05),(.07,.04,.1),black),
 cube("Angry brow L",(-1.83,1.42,2.31),(.42,.08,.1),dark),
 cube("Angry brow R",(-1.17,1.42,2.31),(.42,.08,.1),dark),
 ball("Mouth",(-1.5,1.42,1.72),(.22,.05,.09),black)]
for side in (-1,1):
    bpy.ops.mesh.primitive_cylinder_add(vertices=16,radius=.1,depth=.85,location=(-1.5+side*.9,.8,1))
    a=bpy.context.object; a.name="Toilet arm"; a.data.materials.append(porcelain); parts.append(a)
    parts.append(ball("Toilet hand",(-1.5+side*1.2,.8,.62),(.17,.17,.17),porcelain))
    bpy.ops.mesh.primitive_cylinder_add(vertices=16,radius=.12,depth=.6,location=(-1.5+side*.42,.5,.15))
    leg=bpy.context.object; leg.name="Toilet leg"; leg.data.materials.append(dark); parts.append(leg)
    parts.append(ball("Toilet shoe",(-1.5+side*.42,.2,-.05),(.24,.34,.14),dark))
for p in parts:
    p.parent=toilet; p.matrix_parent_inverse=toilet.matrix_world.inverted()

# Human and Captain Plunger
human=cube("HUMAN — root",(3,-.4,1.45),(.75,.48,.95),yellow)
hparts=[ball("Human head",(3,-.4,2.25),(.37,.35,.4),skin),
        ball("Human hair",(3,-.38,2.5),(.39,.36,.18),dark)]
for side in (-1,1):
    bpy.ops.mesh.primitive_cylinder_add(vertices=16,radius=.13,depth=.8,location=(3+side*.22,-.4,.55))
    o=bpy.context.object; o.name="Human leg"; o.data.materials.append(purple); hparts.append(o)
for p in hparts: p.parent=human; p.matrix_parent_inverse=human.matrix_world.inverted()
hero=cube("CAPTAIN PLUNGER — root",(90,-.4,1.5),(.75,.48,1),red)
hero_parts=[ball("Captain Plunger head",(90,-.4,2.3),(.38,.35,.4),skin),
            ball("Captain Plunger helmet",(90,-.4,2.58),(.45,.38,.18),gold)]
for p in hero_parts: p.parent=hero; p.matrix_parent_inverse=hero.matrix_world.inverted()

# Small toilet army
army=[]
for i in range(4):
    x=27+i*1.8
    r=ball("Mini toilet bot %d"%i,(x,.8,.75),(.48,.55,.35),porcelain)
    t=cube("Mini bot tank %d"%i,(x,1.5,1.25),(.72,.45,.85),porcelain)
    e1=ball("Bot eye",(x-.15,1.25,1.35),(.09,.05,.12),black)
    e2=ball("Bot eye",(x+.15,1.25,1.35),(.09,.05,.12),black)
    for p in (t,e1,e2): p.parent=r; p.matrix_parent_inverse=r.matrix_world.inverted()
    army.append(r)

# Camera and lighting
bpy.ops.object.camera_add(location=(0,-14,6))
cam=bpy.context.object; cam.name="Feature film camera"; cam.data.lens=42
s.camera=cam
def camkey(frame,loc,target):
    cam.location=loc; aim(cam,target)
    cam.keyframe_insert(data_path="location",frame=frame)
    cam.keyframe_insert(data_path="rotation_euler",frame=frame)
bpy.ops.object.lamp_add(type="AREA",location=(0,-5,9))
lamp=bpy.context.object; lamp.data.energy=1100; lamp.data.size=7
bpy.ops.object.lamp_add(type="AREA",location=(60,-5,9))
bpy.context.object.data.energy=1000; bpy.context.object.data.size=7

# Title and act cards
title=text("THE TOILET THAT WANTED REVENGE",(-5.2,3.8,4.7),.55,gold)
subtitle=text("A COLORFUL 3D CARTOON",( -2.6,3.78,4.1),.32,white)
end=text("THE END — PLEASE FLUSH RESPONSIBLY",(-4.5,3.8,4.5),.42,gold)
def visibility(o,start,endf):
    o.hide=True; o.hide_render=True
    o.keyframe_insert(data_path="hide",frame=1); o.keyframe_insert(data_path="hide_render",frame=1)
    o.hide=False; o.hide_render=False
    o.keyframe_insert(data_path="hide",frame=start); o.keyframe_insert(data_path="hide_render",frame=start)
    o.hide=True; o.hide_render=True
    o.keyframe_insert(data_path="hide",frame=endf); o.keyframe_insert(data_path="hide_render",frame=endf)
visibility(title,1,240); visibility(subtitle,1,240); visibility(end,71500,72000)

# Story beats in frames; each act has a camera setup and character blocking.
def F(m,sec=0): return int((m*60+sec)*24)+1
acts=[
 (0,5,0,(0,-14,6),(0,1,1.7),"ACT 1 — AN ORDINARY BATHROOM"),
 (5,12,0,(0,-12,5.5),(0,1,1.8),"ACT 2 — THE TOILET AWAKENS"),
 (12,20,60,(60,-15,6),(60,0,2),"ACT 3 — THE GREAT ESCAPE"),
 (20,28,30,(30,-14,5.5),(30,1,1.7),"ACT 4 — THE TOILET ARMY"),
 (28,36,90,(90,-14,5.5),(90,1,1.8),"ACT 5 — THE HUMAN RESISTANCE"),
 (36,46,60,(60,-16,6),(60,0,2),"ACT 6 — THE FINAL BATTLE"),
 (46,50,60,(60,-14,5.2),(60,0,1.8),"ACT 7 — THE END")]
for start,finish,x,cloc,target,label in acts:
    camkey(F(start),cloc,target)
    camkey(F(finish),cloc,target)
    card=text(label,(-4.5,3.75,4.7),.38,gold)
    visibility(card,F(start),F(start,8))
# Character motion beats
for frame,loc in [(F(0),(-1.5,.8,1)),(F(5),(-1.5,.8,1)),(F(12),(1,.8,1)),
                  (F(15),(58,.8,1)),(F(20),(28,.8,1)),(F(28),(32,.8,1)),
                  (F(36),(57,.8,1)),(F(42),(61,.8,1)),(F(46),(60,.8,1)),
                  (F(49),(60,.8,1.35)),(F(50),(60,.8,1))]:
    toilet.location=loc; toilet.keyframe_insert(data_path="location",frame=frame)
for frame,loc in [(F(0),(3,-.4,1.45)),(F(12),(4,-.4,1.45)),
                  (F(15),(58,-.4,1.45)),(F(20),(60,-.4,1.45)),
                  (F(36),(63,-.4,1.5)),(F(42),(59,-.4,1.5)),(F(50),(62,-.4,1.5))]:
    human.location=loc; human.keyframe_insert(data_path="location",frame=frame)
for i,r in enumerate(army):
    for frame,loc in [(F(20),(27+i*1.8,.8,.75)),(F(24),(28+i*1.8,.8,.9)),(F(28),(29+i*1.8,.8,.75))]:
        r.location=loc; r.keyframe_insert(data_path="location",frame=frame)
for frame,loc in [(F(28),(87,-.4,1.5)),(F(30),(90,-.4,1.5)),(F(36),(92,-.4,1.5)),(F(46),(62,-.4,1.5)),(F(50),(62,-.4,1.5))]:
    hero.location=loc; hero.keyframe_insert(data_path="location",frame=frame)

# A few visible dialogue cards (visual captions, not recorded voice acting).
lines=[
 ("HUMAN: Just another normal Tuesday.",0),
 ("TOILET: You never appreciate me!",5),
 ("HUMAN: WHY DOES THE TOILET HAVE LEGS?!",12),
 ("TOILET: BEHOLD... MY FLUSH FORCE!",20),
 ("CAPTAIN PLUNGER: The bathroom needs a hero.",28),
 ("TOILET: THIS ENDS NOW!",36),
 ("HUMAN: Can we please just use the sink?",46)]
for line,m in lines:
    o=text(line,(-4.7,3.72,.7),.24,white); visibility(o,F(m,12),F(m,57))
# Smooth animation curves
for ob in s.objects:
    if ob.animation_data and ob.animation_data.action:
        for fc in ob.animation_data.action.fcurves:
            for kp in fc.keyframe_points: kp.interpolation="BEZIER"

s.frame_set(1)
out=os.environ.get("BLEND_OUTPUT",os.path.join(os.getcwd(),"dist","The_Toilet_That_Wanted_Revenge.blend"))
os.makedirs(os.path.dirname(os.path.abspath(out)),exist_ok=True)
bpy.ops.wm.save_as_mainfile(filepath=os.path.abspath(out))
print("SAVED_BLENDER_PROJECT="+os.path.abspath(out))
print("Timeline: 50 minutes at 24 fps. This is an animated animatic foundation; it does not yet contain recorded voice acting, music, or a rendered feature film.")

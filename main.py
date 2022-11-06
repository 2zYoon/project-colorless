import os
import sys
from ursina import *

# Basedir
BASEDIR = os.path.abspath(os.path.dirname(__file__))

# Color
TRANSPARENT =   (0, 0, 0, 0)
WHITE =         (255, 255, 255, 255)
BLACK =         (0, 0, 0, 255)
DARKGRAY =      (32, 32, 32, 255)
GRAY =          (128, 128, 128, 255)
WHITEGRAY =     (192, 192, 192, 255)

ALPHA = lambda pct: int(255 * pct / 100)

def toggle_button_list(button_list):
    for button in button_list:
        button.enabled = not button.enabled

def toggle_button(button):
    button.enabled = not button.enabled

def bound(val, lower, upper):
    return max(min(val, upper), lower)

def is_bounded(val, lower, upper):
    return val <= upper and val >= lower

def is_in_entity(xy, entity):
    assert(len(xy) == 2)
    
    return is_bounded(xy[0], entity.x - entity.scale[0] / 2, entity.x + entity.scale[0] / 2) and \
        is_bounded(xy[1], entity.y - entity.scale[1] / 2, entity.y + entity.scale[1] / 2)



app = Ursina(editor_ui_enabled=False)

app.setBackgroundColor(255, 255, 255)


SPEED_DEFAULT = 2
SPEED_BOOST = 2

# Live map data
basemap = Entity(model='quad', color=color.gray, scale=(1, 1), x=5, y=5)
walls = []

def update_map(mapname="test"):
    global basemap
    global walls

    # Cleanup all of components
    destroy(basemap)
    for wall in walls:
        destroy(wall)
        walls.remove(wall)

    # New map path
    mappath = f"{BASEDIR}/map/{mapname}"

    # Load basic data
    with open(f"{mappath}/meta.dat") as f:
        metadat = f.read().strip().split(",")
        
        mapname = metadat[0]
        size_x = float(metadat[1])
        size_y = float(metadat[2])

    # TODO: map image
    basemap = Entity(model='quad', color=color.gray, scale=(size_x, size_y))

    with open(f"{mappath}/wall.dat") as f:
        walls_tmp = f.read().strip().split("\n") 
        for wall in walls_tmp:
            try:
                wall_x, wall_y, wall_w, wall_h = list(map(float, wall.split(",")))
            except:
                break

            # FIXME: make transparent
            walls.append(Entity(model="quad", color=color.black, scale=(wall_w, wall_h), x=wall_x, y=wall_y, z=-1, collider="box"))
        
    

player = Entity(model='sphere', color=color.azure, scale=(0.25, 0.25), x=0, y=0, z=-1)


button_menu = Button(
    text='Menu', 
    color=color.azure, 
    scale_x=0.2,
    scale_y=0.05, 
    text_origin=(0,0),
    position=(0.5*window.aspect_ratio - 0.1, 0.5 - 0.025),
    on_click=lambda: toggle_button_list(button_list_menu)
)

button_list_menu = [
    Button(text="Option", scale_x=0.2, scale_y=0.05, text_origin=(0,0), position=(0.5*window.aspect_ratio - 0.1, 0.5 - 0.075), on_click=lambda: application.quit()),
    Button(text="Save & Exit", scale_x=0.2, scale_y=0.05, text_origin=(0,0), position=(0.5*window.aspect_ratio - 0.1, 0.5 - 0.125), on_click=lambda: application.quit())
]


camera.add_script(SmoothFollow(target=player, offset=[0,-30], speed=2))
EditorCamera() # temporary 

update_map()


# Move
def move_player():
    move_direction = Vec2((held_keys['d']-held_keys['a']), (held_keys['w']-held_keys['s'])).normalized()
    speed = SPEED_DEFAULT + held_keys['space'] * SPEED_BOOST
    
    dest_x = player.position[0] + move_direction[0] * speed * time.dt
    dest_y = player.position[1] + move_direction[1] * speed * time.dt

    if not is_in_entity([dest_x, player.position[1]], basemap):
        move_direction[0] = 0

    if not is_in_entity([player.position[0], dest_y], basemap):
        move_direction[1] = 0

    for wall in walls:
        if is_in_entity([dest_x, player.position[1]], wall):
            move_direction[0] = 0
            break

    for wall in walls:
        if is_in_entity([player.position[0], dest_y], wall):
            move_direction[1] = 0
            break
        
    player.position += move_direction * speed * time.dt


# Eager status
box_eager_status = Entity(model='quad', origin=(0.5, -0.5), color=color.azure, position=(0, 0))
txt_coordinate = Text("", origin=(0.5, -0.5), position=(0.5*window.aspect_ratio, -0.5), color=color.black50)

def update_eager_status():
    global txt_coordinate

    txt_coordinate.text=f"[{player.x:.2f}, {player.y:.2f}]"
    

def update():
    move_player()
    update_eager_status()

          
def input(key):
    if key == 'c': # debug
        print(player.x, player.y)
        print("press C")
        
    if key == 'x': # debug
        print("press X")

    if key == "q":
        print("press Q")
        application.quit()

app.run()

import os
import sys

from ursina import *
from ursina.prefabs.health_bar import HealthBar
from ursina.prefabs.window_panel import WindowPanel, Space

from lib.common import *
from lib.player import *

# Basedir
BASEDIR = os.path.abspath(os.path.dirname(__file__))

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
        
    
player_data = Player()
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

IDX_BAR_HP = 0
IDX_BAR_MP = 1
IDX_BAR_EXP = 2
IDX_BAR_ENCOUNTER = 3

bars = [
    HealthBar(),    # HP
    HealthBar(),    # MP
    HealthBar(),    # EXP
    HealthBar()     # Encounter
]

IDX_END_BATTLE = 3
battle_panel = WindowPanel(
    title = "Battle",
    content=[
        Space(height=5),
        Text("..."),
        Space(height=5),
        Button(text='End Battle', color=color.azure),
    ],
    popup=True
)

def close_battle():
    global battle_panel
    
    battle_panel.close()
    player_data.movable_system = True

def open_battle():
    global battle_panel

    battle_panel.enabled = True
    player_data.movable_system = False

def init_battle_UI():
    global battle_panel
    
    # prevent dragging
    battle_panel.origin = (0, 0)
    battle_panel.lock = Vec3(1,1,1)
    battle_panel.y = 0.3

    battle_panel.panel.color = NORMALIZE_COLOR((25, 25, 255, 100))

    battle_panel.content[IDX_END_BATTLE].on_click = close_battle

    # popup, but disable manual closing
    battle_panel.bg.on_click = None

def update_bars():
    global bars

    bars[IDX_BAR_HP].max_value = player_data.HP
    bars[IDX_BAR_HP].value = player_data.HP_live

    bars[IDX_BAR_MP].max_value = player_data.MP
    bars[IDX_BAR_MP].value = player_data.MP_live

    bars[IDX_BAR_EXP].max_value = player_data.calculate_required_exp()
    bars[IDX_BAR_EXP].value = player_data.EXP

    bars[IDX_BAR_ENCOUNTER].value = player_data.encounter

def init_bars():
    global bars
    global player_data

    # set visual properties
    bars[IDX_BAR_HP].bar.color = RED
    bars[IDX_BAR_HP].position = (-0.45 * window.aspect_ratio, 0.45)

    bars[IDX_BAR_MP].bar.color = BLUE
    bars[IDX_BAR_MP].position = (-0.45 * window.aspect_ratio, 0.42)

    bars[IDX_BAR_EXP].bar.color = GREEN
    bars[IDX_BAR_EXP].position = (-0.45 * window.aspect_ratio, 0.39)

    bars[IDX_BAR_ENCOUNTER].bar.color = NORMALIZE_COLOR(DARK_ORANGE)
    bars[IDX_BAR_ENCOUNTER].position = (-0.5 * window.aspect_ratio, -0.50 + Text.size)
    bars[IDX_BAR_ENCOUNTER].scale = (1.0 * window.aspect_ratio, Text.size)
    bars[IDX_BAR_ENCOUNTER].animation_duration = 0
    bars[IDX_BAR_ENCOUNTER].show_text = False

    # set some (static) values
    bars[IDX_BAR_HP].min_value = 0
    bars[IDX_BAR_MP].min_value = 0
    bars[IDX_BAR_EXP].min_value = 0
    bars[IDX_BAR_ENCOUNTER].max_value = MAX_ENCOUNTER
    bars[IDX_BAR_ENCOUNTER].min_value = 0

    # texts
    texts = [
        Text(text="HP", position=(-0.48 * window.aspect_ratio, 0.45 - 0.003)),
        Text(text="MP", position=(-0.48 * window.aspect_ratio, 0.42 - 0.003)),
        Text(text="EXP", position=(-0.48 * window.aspect_ratio, 0.39 - 0.003))
    ]

    for txt in texts:
        txt.color = BLACK
        txt.resolution = 100 * Text.size
        txt.scale = 0.9
        
    # set initial value
    update_bars()

def init_player():
    global player
    global player_data

    player_data.position = player.position



camera.add_script(SmoothFollow(target=player, offset=[0,-30], speed=2))
# EditorCamera() # temporary 

update_map()

# periodic update
def update_periodic():
    pass


# Move
def move_player():
    global player_data

    if not player_data.movable():
        return

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
    player_data.position = player.position
    player_data.encounter += 1.0 * 200.0 * (abs(move_direction[0]) + abs(move_direction[1])) * time.dt

    if int(player_data.encounter) != int(player_data.last_encounter):
        if int(player_data.encounter / 100) != int(player_data.last_check_encounter / 100):
            # check if battle is needed
            initiate_battle = random_prob(player_data.encounter / MAX_ENCOUNTER * 100)
            player_data.last_check_encounter = int(player_data.encounter)

            if initiate_battle:
                # do battle
                open_battle()
                pass

        update_bars()
        player_data.last_encounter = int(player_data.encounter)



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
    global player_data

    if key == 'c': # debug
        print(player.x, player.y)
        player_data.HP_live += 150
        update_bars()
        print("press C")
        
    if key == 'x': # debug
        print("press X")
        player_data.HP_live -= 150
        update_bars()

    if key == 't': # debug
        print("press T, LOCK switch")
        player_data.movable_system = not player_data.movable_system

    if key == 'y': # debug
        print("press Y, popup close")
        battle_panel.close()

    if key == "q":
        
        print("press Q")
        application.quit()

init_player()
init_bars()
init_battle_UI()

app.run()

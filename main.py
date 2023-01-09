import os
import sys

import textwrap
import time

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
    HealthBar(),    # Encounter
]

IDX_BATTLE_MON_NAME = 0
IDX_BATTLE_MON_HP_BAR = 1
IDX_BATTLE_MON_SPRITE = 2
IDX_BATTLE_CHAR_SPRITE = 3
IDX_BATTLE_LOG = 4

BATTLE_UI_BG_SCALE_X = 0.5
BATTLE_UI_BG_SCALE_Y = 0.7

# its y-scale follows the main bg
BATTLE_UI_LOG_BG_SCALE_X = 0.35

# its y-scale follows the main bg
BATTLE_UI_ACTION_BG_SCALE_X = 0.35

BATTLE_UI_MON_SPRITE_SCALE_SMALL = 0.15
BATTLE_UI_MON_SPRITE_SCALE_LARGE = 0.30
BATTLE_UI_CHAR_SPRITE_SCLAE = 0.15

BATTLE_UI_MARGIN = 0.01

BATTLE_UI_LOG_FONTSIZE = 0.75
BATTLE_UI_LOG_MAX_CHAR_PER_LINE = 31
BATTLE_UI_LOG_MAX_LINE = 34

battle_ui_darkness =  Entity(model='quad', parent=camera.ui, scale=(window.aspect_ratio, 1), color=NORMALIZE_COLOR(UI_BASE_DARKGRAY))
battle_ui_bgs = [
    # main bg
    Entity(model='quad', parent=camera.ui, scale=(BATTLE_UI_BG_SCALE_X, BATTLE_UI_BG_SCALE_Y), color=NORMALIZE_COLOR(UI_BASE_DARKGRAY),
        position=(0,0)),
    # log bg
    Entity(model='quad', parent=camera.ui, scale=(BATTLE_UI_LOG_BG_SCALE_X, BATTLE_UI_BG_SCALE_Y), color=NORMALIZE_COLOR(UI_BASE_DARKGRAY),
        position=(0.5 * BATTLE_UI_BG_SCALE_X + 0.5 * BATTLE_UI_LOG_BG_SCALE_X + BATTLE_UI_MARGIN, 0, 0)),
    # action bg
    Entity(model='quad', parent=camera.ui, scale=(BATTLE_UI_ACTION_BG_SCALE_X, BATTLE_UI_BG_SCALE_Y), color=NORMALIZE_COLOR(UI_BASE_DARKGRAY),
        position=(-0.5 * BATTLE_UI_BG_SCALE_X - 0.5 * BATTLE_UI_ACTION_BG_SCALE_X - BATTLE_UI_MARGIN, 0, 0))
]
battle_ui = [
    # main bg
    Text("sample-monster", color=NORMALIZE_COLOR(WHITE), scale=1, 
        position=Vec3(-0.5 * BATTLE_UI_BG_SCALE_X + BATTLE_UI_MARGIN, 0.5 * BATTLE_UI_BG_SCALE_Y - 2 * Text.size, -0.1)),
    HealthBar(scale=(BATTLE_UI_BG_SCALE_X - 2 * BATTLE_UI_MARGIN, Text.size),
        position=Vec3(-0.5 * BATTLE_UI_BG_SCALE_X + BATTLE_UI_MARGIN, 0.5 * BATTLE_UI_BG_SCALE_Y - 3 * Text.size, -0.1)),
    Sprite(parent=camera.ui, scale=(BATTLE_UI_MON_SPRITE_SCALE_LARGE, BATTLE_UI_MON_SPRITE_SCALE_LARGE), origin=(0,0),
        position=Vec3(0, 0.5 * BATTLE_UI_BG_SCALE_Y - 5 * Text.size - 0.5 * BATTLE_UI_MON_SPRITE_SCALE_LARGE, -0.1)),
    Sprite(parent=camera.ui, scale=(BATTLE_UI_CHAR_SPRITE_SCLAE, BATTLE_UI_CHAR_SPRITE_SCLAE), origin=(0,0),
        position=Vec3(0, 0.5 * BATTLE_UI_BG_SCALE_Y - 5 * Text.size - BATTLE_UI_MON_SPRITE_SCALE_LARGE - BATTLE_UI_CHAR_SPRITE_SCLAE, -0.1)),
    
    # log bg
    Text(text="No log...\n", scale=BATTLE_UI_LOG_FONTSIZE, font="./asset/fonts/Consolas.ttf",
        position=Vec3(0.5*BATTLE_UI_BG_SCALE_X + 2*BATTLE_UI_MARGIN, 0.5*BATTLE_UI_BG_SCALE_Y - 2*Text.size, -0.1)),

]

# Rarely changes (except 'enabled')
battle_ui_misc = [
    Text("Battle", color=NORMALIZE_COLOR(WHITE), scale=1.5, 
        position=Vec3(-0.5 * BATTLE_UI_BG_SCALE_X, 0.5 * BATTLE_UI_BG_SCALE_Y, -0.1)),
    Text("Log", color=NORMALIZE_COLOR(WHITE), scale=1.5, 
        position=Vec3(0.5 * BATTLE_UI_BG_SCALE_X + BATTLE_UI_MARGIN, 0.5 * BATTLE_UI_BG_SCALE_Y, -0.1)),
    Text("Action", color=NORMALIZE_COLOR(WHITE), scale=1.5, 
        position=Vec3(-0.5 * BATTLE_UI_BG_SCALE_X - BATTLE_UI_ACTION_BG_SCALE_X - BATTLE_UI_MARGIN, 0.5 * BATTLE_UI_BG_SCALE_Y, -0.1)),
]

def close_battle():
    global player_data
    global battle_ui_bgs
    global battle_ui
    global battle_ui_misc
    global battle_ui_darkness

    for e in battle_ui:
        e.enabled = False
    for e in battle_ui_misc:
        e.enabled = False 
    for e in battle_ui_bgs:
        e.enabled = False

    battle_ui_darkness.enabled = False

    player_data.movable_system = True
    player_data.encounter = 0
    update_bars()   

def open_battle():
    global player_data
    global battle_ui_bgs
    global battle_ui
    global battle_ui_misc
    global battle_ui_darkness

    # simple animation

    battle_ui_darkness.enabled = True
    for i in range(100):
       #time.sleep(0.1)
       # how?
        battle_ui_darkness.color = NORMALIZE_COLOR((0, 0, 0, 2*i))


    for e in battle_ui:
        e.enabled = True
    for e in battle_ui_misc:
        e.enabled = True
    for e in battle_ui_bgs:
        e.enabled = True

    battle_ui[IDX_BATTLE_MON_SPRITE].texture = "./asset/monster/sample-dragon.png"
    battle_ui[IDX_BATTLE_CHAR_SPRITE].texture = "./asset/character/sample-char.png"

    player_data.movable_system = False


def append_battle_log(msg="..."):
    global battle_ui
    cur_line = len(battle_ui[IDX_BATTLE_LOG].text.split("\n")) 
    
    # If the number of line exceeds the limit, cut oldest one
    if cur_line >= BATTLE_UI_LOG_MAX_LINE:
        battle_ui[IDX_BATTLE_LOG].text = "\n".join(battle_ui[IDX_BATTLE_LOG].text.split("\n")[cur_line - BATTLE_UI_LOG_MAX_LINE + 1:])
  
    battle_ui[IDX_BATTLE_LOG].text += "\n".join(textwrap.wrap(msg, width=BATTLE_UI_LOG_MAX_CHAR_PER_LINE)) + "\n"



def init_battle_UI():
    global battle_ui
    global bars

    # initially closed
    close_battle()
    pass


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

    #
    # set some (static) values
    #
    bars[IDX_BAR_HP].min_value = 0
    bars[IDX_BAR_MP].min_value = 0
    bars[IDX_BAR_EXP].min_value = 0
    # In most case, the actual max value cannot be reached, so we use 20% of MAX_ENCOUNTER as a max value
    bars[IDX_BAR_ENCOUNTER].max_value = MAX_ENCOUNTER / 5
    bars[IDX_BAR_ENCOUNTER].min_value = 0

    # texts
    texts = [
        Text(text="HP", position=(-0.48 * window.aspect_ratio, 0.45 - 0.003)), 
        Text(text="MP", position=(-0.48 * window.aspect_ratio, 0.42 - 0.003)),
        Text(text="EXP", position=(-0.48 * window.aspect_ratio, 0.39 - 0.003)),
        Text(text="Encounter Gauge", position=(-0.5 * window.aspect_ratio, -0.50 + 2 * Text.size)),
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
        close_battle()

    if key == "p":
        print("update")
        append_battle_log()


    if key == "q":
        
        print("press Q")
        application.quit()

init_player()
init_battle_UI()
init_bars()

app.run()

from ursina import *

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


app = Ursina(editor_ui_enabled=False)
app.setBackgroundColor(255, 255, 255)

SPEED_DEFAULT = 2

def update_map(map=None):
    map = Entity(model='quad', color=color.gray, scale=(8, 8))

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
    Button(text="Option", scale_x=0.2, scale_y=0.05, text_origin=(0,0), position= (0.5*window.aspect_ratio - 0.1, 0.5 - 0.075), on_click=lambda: application.quit()),
    Button(text="Save & Exit", scale_x=0.2, scale_y=0.05, text_origin=(0,0), position= (0.5*window.aspect_ratio - 0.1, 0.5 - 0.125), on_click=lambda: application.quit())
]


camera.add_script(SmoothFollow(target=player, offset=[0,-30], speed=2))

update_map()

def update():
    move_direction = Vec2((held_keys['d']-held_keys['a']), (held_keys['w']-held_keys['s'])).normalized()
    player.position += move_direction * SPEED_DEFAULT * time.dt

    #move_direction = Vec2(-(held_keys['d']-held_keys['a']), -(held_keys['w']-held_keys['s'])).normalized()
    #map.position += move_direction * SPEED_DEFAULT * time.dt

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

from ursina import *
from ursina.prefabs.platformer_controller_2d import PlatformerController2d

from PIL import Image

TRANSPARENT =   (0, 0, 0, 0)
WHITE =         (255, 255, 255, 255)
BLACK =         (0, 0, 0, 255)
GRAY =          (128, 128, 128, 255)

ALPHA = lambda pct: int(255 * pct / 100)

# PRELOAD
#preload_block_1 = Entity(model="cube", texture="asset/block/1.png", scale=(1,1), origin=(-.5, .5))

def toggle_button_list(button_list):
    for button in button_list:
        button.enabled = not button.enabled

def toggle_button(button):
    button.enabled = not button.enabled

def render_map(mapname="test"):
    texture = load_texture(f"map/{mapname}/map.png")

    for y in range(texture.height):
        for x in range(texture.width):
            col = texture.get_pixel(x, y)
            
            if col == color.black:
                mod = (x + y) % 5
                Entity(model="cube", texture=f"asset/block/{mod}.png", origin=(-.5, .5), scale=(1, 1), x=x, y=y, collider="box")
                    

    # we cannot go further
    Entity(model="cube", color=(255, 0, 0, 255), origin=(-.5, .5), scale=(0.2, texture.height), x=0, y=(texture.height-1), collider="box")
    Entity(model="cube", color=(255, 0, 0, 255), origin=(-.5, .5), scale=(0.2, texture.height), x=texture.width, y=(texture.height-1), collider="box")



app = Ursina(editor_ui_enabled=False)
app.setBackgroundColor(255,255,255)

camera.orthographic = True
camera.fov = 30

button_list_menu = [
    Button(text="Option", scale_x=0.2, scale_y=0.05, text_origin=(0,0), position= (0.5*window.aspect_ratio - 0.1, 0.5 - 0.075), on_click=lambda: application.quit()),
    Button(text="Save & Exit", scale_x=0.2, scale_y=0.05, text_origin=(0,0), position= (0.5*window.aspect_ratio - 0.1, 0.5 - 0.125), on_click=lambda: application.quit())
]

button_menu = Button(
    text='Menu', 
    color=color.azure, 
    scale_x=0.2,
    scale_y=0.05, 
    text_origin=(0,0),
    position=(0.5*window.aspect_ratio - 0.1, 0.5 - 0.025),
    on_click=lambda: toggle_button_list(button_list_menu)
)

def input(key):
    if key == 'c': # debug
        pass
        player.rotate((1, 1, 1))

        
    if key == 'x': # debug
        button_menu.disable()
    
    if key == "q":
        camera.orthographic = True
        

render_map()

player = PlatformerController2d(
    scale_y=1.5,
    jump_height=4,
    x=3, 
    y=6,
    jump_duration = 0.5,
    use_jump_dust=False)

camera.add_script(SmoothFollow(target=player, offset=[0,5,-30], speed=2))
#EditorCamera()


app.run()

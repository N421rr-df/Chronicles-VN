###############################################################################
## TRANSFORMS
###############################################################################

transform mm_logo_entrance:

    alpha 0.0
    xoffset -35

    pause 0.2

    ease 1.0 alpha 1.0 xoffset 0

transform mm_character_breath:

    zoom 1.0
    yoffset 0

    ease 3.5 zoom 1.010 yoffset -5
    ease 3.5 zoom 1.0 yoffset 0

    repeat

transform mm_button_entrance(delay=0.0):

    alpha 0.0
    xoffset -25

    pause delay

    ease 0.45 alpha 1.0 xoffset 0

transform mm_card_animation(delay=0.0):

    on show:
        alpha 0.0
        xoffset 40
        zoom 1.0

        pause delay

        ease 0.55 alpha 1.0 xoffset 0

    on idle:
        ease 0.18 zoom 1.0

    on hover:
        ease 0.18 zoom 1.025

transform mm_light_pulse:

    alpha 0.45

    ease 4.0 alpha 0.62
    ease 4.5 alpha 0.42

    repeat


    alpha 0.25
    xoffset -80

    linear 18.0 xoffset 80
    linear 18.0 xoffset -80

    repeat

transform mm_fog_back:

    alpha 0.12
    zoom 1.06
    xoffset -60

    linear 28.0 xoffset 60
    linear 28.0 xoffset -60

    repeat

transform mm_fog_front:

    alpha 0.18
    zoom 1.10
    xoffset 90

    linear 20.0 xoffset -90
    linear 20.0 xoffset 90

    repeat

###############################################################################
## PARTÍCULAS
###############################################################################

image mm atmospheric_particles = SnowBlossom(
    "gui/main_menu/particle.png",
    count=50,
    border=40,
    xspeed=(20, 45),
    yspeed=(8, 18),
    start=6.0
)

###############################################################################
## MAIN MENU
###############################################################################

screen main_menu():

    tag menu

    add "gui/main_menu/background.webp"

    add "gui/main_menu/light_overlay.png":
        at mm_light_pulse
    
    add "gui/main_menu/fog.png":
        at mm_fog_back

    add "gui/main_menu/character.png":
        xpos 600
        ypos 100
        at mm_character_breath
    
    add "gui/main_menu/fog.png":
        at mm_fog_front
    
    add "mm atmospheric_particles"
    
    add "gui/main_menu/vignette.png"

    add "gui/main_menu/logo.png":
        xpos 90
        ypos 220
        at mm_logo_entrance
    
    vbox:
        style_prefix "main_menu_custom"

        xpos 120
        ypos 520
        spacing 12

        textbutton _("New Game"):
            action Start()
            at mm_button_entrance(0.35)
            hover_sound "audio/ui_hover.mp3"
            activate_sound "audio/ui_click.mp3"
        textbutton _("Continuer"):
            action Continue()
            at mm_button_entrance(0.43)
            hover_sound "audio/ui_hover.mp3"
            activate_sound "audio/ui_click.mp3"
        textbutton _("Load"):
            action ShowMenu("load")
            at mm_button_entrance(0.51)
            hover_sound "audio/ui_hover.mp3"
            activate_sound "audio/ui_click.mp3"
        textbutton _("Settings"):
            action ShowMenu("preferences")
            at mm_button_entrance(0.59)
            hover_sound "audio/ui_hover.mp3"
            activate_sound "audio/ui_click.mp3"
        textbutton _("Credits"):
            action [
                Play(
                    "music",
                    "audio/music/credits_theme.mp3",
                    fadeout=1.0,
                    fadein=2.0,
                    loop=True
                ),
                ShowMenu("credits_screen")
            ]
            at mm_button_entrance(0.67)
            hover_sound "audio/ui_hover.mp3"
            activate_sound "audio/ui_click.mp3"
        textbutton _("Quit"):
            action Quit(confirm=True)
            at mm_button_entrance(0.75)
            hover_sound "audio/ui_hover.mp3"
            activate_sound "audio/ui_click.mp3"
    
    vbox:
        xpos 1450
        ypos 570
        spacing 20

        imagebutton:
            idle "gui/main_menu/card_01_idle.webp"
            hover "gui/main_menu/card_01_hover.webp"
            action NullAction()
            hover_sound "audio/ui_hover.mp3"
            activate_sound "audio/ui_click.mp3"
            focus_mask True
            at mm_card_animation(0.65)

        imagebutton:
            idle "gui/main_menu/card_02_idle.webp"
            hover "gui/main_menu/card_02_hover.webp"
            action NullAction()
            hover_sound "audio/ui_hover.mp3"
            activate_sound "audio/ui_click.mp3"
            focus_mask True
            at mm_card_animation(0.78)

style main_menu_custom_button:
    background None
    padding (0, 0)

style main_menu_custom_button_text:
    font "gui/fonts/menu_font.ttf"
    size 55
    color "#d8d3cc"
    hover_color "#ffffff"
    insensitive_color "#666666"
    hover_xoffset 12
    outlines [(2, "#000000aa", 0, 2)]

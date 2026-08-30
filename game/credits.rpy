init python:

    def exit_credits_to_main_menu():
        """
        Substitui a música dos créditos pela música do menu
        e abre novamente o menu principal.
        """

        renpy.music.play(
            config.main_menu_music,
            channel="music",
            loop=True,
            fadeout=1.0,
            fadein=1.5
        )

        renpy.show_screen("main_menu")
        renpy.restart_interaction()

################################################################################
## CONFIGURAÇÕES
################################################################################

define credits_duration = 60.0
define credits_height = 2600

define credits_hold_duration = 2.0
define credits_hold_interval = 0.05


################################################################################
## TRANSFORM DE ROLAGEM
################################################################################

transform credits_scroll:

    xalign 0.5

    # Começa abaixo da tela.
    ypos config.screen_height

    # Sobe até desaparecer completamente.
    linear credits_duration ypos -credits_height


################################################################################
## COMPONENTE DE SEÇÃO
################################################################################

screen credits_section(title, names):

    vbox:

        xalign 0.5
        xsize 900
        spacing 8

        text title:

            xalign 0.5
            text_align 0.5

            font "gui/fonts/credits_regular.ttf"
            size 50
            color "#182126"

            bold True
            italic True

        for person in names:

            text person:

                xalign 0.5
                text_align 0.5

                font "gui/fonts/credits_regular.ttf"
                size 30
                color "#3a3a3a"


################################################################################
## TELA PRINCIPAL
################################################################################

screen credits_screen():

    tag menu

    default escape_held = False
    default escape_progress = 0.0

    modal True
    zorder 200

    add Solid("#000000")

    fixed:

        xfill True
        ysize credits_height

        at credits_scroll

        vbox:

            xalign 0.5
            xsize 900
            spacing 65

            null height 120

            use credits_section(
                "GAME CONCEPT",
                [
                    "Nome do responsável",
                    "Segundo integrante",
                ]
            )

            use credits_section(
                "PRODUCTION",
                [
                    "Nome do produtor",
                    "Assistente de produção",
                ]
            )

            use credits_section(
                "PROGRAMMING",
                [
                    "Seu Nome",
                    "Chronicles VN Team",
                ]
            )

            use credits_section(
                "GAME DESIGN",
                [
                    "Nome do game designer",
                ]
            )

            use credits_section(
                "STORY",
                [
                    "Nome do responsável pela história",
                ]
            )

            use credits_section(
                "WRITING",
                [
                    "Nome do roteirista",
                    "Nome do revisor",
                ]
            )

            use credits_section(
                "CONCEPT & CHARACTER ART",
                [
                    "Nome do artista",
                    "Nome do character designer",
                ]
            )

            use credits_section(
                "MUSIC & SOUND",
                [
                    "Nome do compositor",
                    "Nome do sound designer",
                ]
            )

            use credits_section(
                "SPECIAL THANKS",
                [
                    "Comunidade Ren'Py",
                    "Família e amigos",
                    "Todos que apoiaram o projeto",
                ]
            )

            null height 80

            text "MADE WITH REN'PY":

                xalign 0.5
                text_align 0.5

                font "gui/fonts/credits_regular.ttf"
                size 30
                color "#20282c"

                bold True
                italic True

            text "CHRONICLES VN":

                xalign 0.5
                text_align 0.5

                font "gui/fonts/credits_regular.ttf"
                size 36
                color "#444444"

                bold True

            text "Obrigado por jogar.":

                xalign 0.5
                text_align 0.5

                font "gui/fonts/credits_regular.ttf"
                size 28
                color "#333333"

            null height 500

    # Logo fixa no canto inferior esquerdo.
    add "gui/credits/chronicles_logo.png":

        xalign 0.035
        yalign 0.94

        xysize (420, 180)
        fit "contain"

        alpha 0.75

    frame:

        background None

        xalign 0.965
        yalign 0.94

        padding (0, 0)

        hbox:

            spacing 18
            yalign 0.5

            # Representação visual da tecla Esc.
            frame:

                background None

                xalign 0.965
                yalign 0.94

                padding (0, 0)

                hbox:

                    spacing 18
                    yalign 0.5

                    frame:

                        background Solid("#d8d8d8")

                        xsize 62
                        ysize 54

                        padding (0, 0)

                        text "Esc":

                            xalign 0.5
                            yalign 0.5

                            font "DejaVuSans.ttf"
                            size 23
                            color "#171717"

                    vbox:

                        yalign 0.5
                        spacing 8

                        text "Segure para pular":

                            font "DejaVuSans.ttf"
                            size 27
                            color "#bcbcbc"
                            bold True

                        fixed:

                            xsize 235
                            ysize 5

                            add Solid("#252525")

                            bar:

                                value StaticValue(
                                    escape_progress,
                                    credits_hold_duration
                                )

                                xsize 235
                                ysize 5

                                left_bar Solid("#bcbcbc")
                                right_bar Solid("#252525")

                                thumb None
                                thumb_shadow None

    # Detecta o início da retenção.
    key "keydown_K_ESCAPE" action SetScreenVariable(
        "escape_held",
        True
    )

    # Cancela ao soltar a tecla.
    key "keyup_K_ESCAPE" action [
        SetScreenVariable("escape_held", False),
        SetScreenVariable("escape_progress", 0.0)
    ]

    # Atualiza o progresso da retenção.
    timer credits_hold_interval repeat True action If(
        escape_held,
        [
            SetScreenVariable(
                "escape_progress",
                min(
                    escape_progress + credits_hold_interval,
                    credits_hold_duration
                )
            ),
            If(
                escape_progress + credits_hold_interval
                >= credits_hold_duration,
                Function(exit_credits_to_main_menu)
            )
        ],
        NullAction()
    )

    # Continua fechando automaticamente ao fim dos créditos.
    timer credits_duration action Function(
        exit_credits_to_main_menu
    )

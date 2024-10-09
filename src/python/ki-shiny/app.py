import shinyswatch
from shiny import App, ui

from core.di_container import DiContainer
from modules.agent import agent_server, agent_ui
from modules.my_module import my_module_server, my_module_ui

di_container = DiContainer()


def placeholder():
    """Placeholder ui module"""
    # Open README.md and save its content as string
    with open("README.md", "r") as file:
        readme = file.read()
    return ui.div(ui.markdown(readme))


def render_basics_navbar():
    return ui.page_navbar(
        # ui.nav_panel("Chat", my_module_ui("mymodule")),
        ui.nav_panel("Agents", agent_ui("agents")),
        #ui.nav_panel("MyModule Sub 3", placeholder()),
    )


def app_ui():
    return ui.page_sidebar(
        ui.sidebar(shinyswatch.theme_picker_ui(), open="closed"),
        ui.page_navbar(
            # ui.nav_panel("Intro", placeholder()),
            ui.nav_panel("Chat", render_basics_navbar()),
            ui.nav_spacer(),
            ui.nav_control(),
            title="KI Weißwurstfrühstück...",
        ),
        theme=shinyswatch.theme.sandstone,
    )


def app_server(input, output, session):
    # my_module_server("mymodule", di_container)
    agent_server("agents", di_container)
    shinyswatch.theme_picker_server()


app = App(app_ui(), app_server)

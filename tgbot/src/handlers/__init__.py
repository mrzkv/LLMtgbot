from . import add_models, menu, start, un_handled

routers = [
    start.router,
    menu.router,
    add_models.router,


    # Stay last
    un_handled.router,
]

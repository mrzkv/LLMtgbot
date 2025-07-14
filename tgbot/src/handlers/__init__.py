from . import menu, models, start, un_handled

routers = [
    start.router,
    menu.router,
    models.router,


    # Stay last
    un_handled.router,
]

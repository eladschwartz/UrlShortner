from . import home, api, auth

ROUTERS = [
    home.router,
    api.router,
    auth.router
]
#!/usr/bin/env python3
"""This is just a simple authentication example.

Please see the `OAuth2 example at FastAPI <https://fastapi.tiangolo.com/tutorial/security/simple-oauth2/>`_  or
use the great `Authlib package <https://docs.authlib.org/en/v0.13/client/starlette.html#using-fastapi>`_ to implement a classing real authentication system.
Here we just demonstrate the NiceGUI integration.
"""
import pymongo
from typing import Optional

from fastapi import Request
from fastapi.responses import RedirectResponse
from starlette.middleware.base import BaseHTTPMiddleware

from nicegui import app, ui

from login.config import Config

# in reality users passwords would obviously need to be hashed
passwords = {}

unrestricted_page_routes = {'/login'}


class AuthMiddleware(BaseHTTPMiddleware):
    """This middleware restricts access to all NiceGUI pages.

    It redirects the user to the login page if they are not authenticated.
    """

    async def dispatch(self, request: Request, call_next):
        if not app.storage.user.get('authenticated', False):
            if not request.url.path.startswith('/_nicegui') and request.url.path not in unrestricted_page_routes:
                app.storage.user['referrer_path'] = request.url.path  # remember where the user wanted to go
                return RedirectResponse('/login')
        return await call_next(request)


app.add_middleware(AuthMiddleware)


@ui.page('/')
def main_page() -> None:
    def logout() -> None:
        app.storage.user.clear()
        ui.navigate.to('/login')

    with ui.column().classes('absolute-center items-center'):
        ui.label(f'Hello {app.storage.user["username"]}!').classes('text-2xl')
        ui.button(on_click=logout, icon='logout').props('outline round')


@ui.page('/subpage')
def test_page() -> None:
    ui.label('This is a sub page.')


@ui.page('/login')
def login() -> Optional[RedirectResponse]:
    def try_login() -> None:  # local function to avoid passing username and password as arguments
        if passwords.get(username.value) == password.value:
            app.storage.user.update({'username': username.value, 'authenticated': True})
            ui.navigate.to(app.storage.user.get('referrer_path', '/'))  # go back to where the user wanted to go
        else:
            ui.notify('Wrong username or password', color='negative')

    if app.storage.user.get('authenticated', False):
        return RedirectResponse('/')
    with ui.card().classes('absolute-center'):
        username = ui.input('Username').on('keydown.enter', try_login)
        password = ui.input('Password', password=True, password_toggle_button=True).on('keydown.enter', try_login)
        ui.button('Log in', on_click=try_login)
    return None


def init_database(cfg: Config):
    # connection
    client = pymongo.MongoClient(
        cfg.mongo_host,
        cfg.mongo_port,
        username=cfg.mongo_user,
        password=cfg.mongo_pass
    )
    # drop collections
    client["login"].drop_collection("users")
    client["login"].drop_collection("outbox")
    # create collections
    col_users = client["login"]["users"]
    col_outbox = client["login"]["outbox"]
    # fillup sample data
    users = [
        {"name": "kem", "pass": "kem"},
        {"name": "gim", "pass": "gim"},
    ]
    col_users.insert_many(users)

def read_users(cfg: Config):
    # connection
    client = pymongo.MongoClient(
        cfg.mongo_host,
        cfg.mongo_port,
        username=cfg.mongo_user,
        password=cfg.mongo_pass
    )
    # collection
    col_users = client["login"]["users"]
    # query
    query = {}
    projection = {}
    for user in col_users.find(query, projection):
        passwords[user["name"]] = user["pass"]

if __name__ in {'__main__', '__mp_main__'}:
    cfg = Config()
    init_database(cfg)
    read_users(cfg)
    # start gui
    ui.run(storage_secret='THIS_NEEDS_TO_BE_CHANGED')


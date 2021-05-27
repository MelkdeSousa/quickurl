from uuid import uuid4

from starlette.applications import Starlette
from starlette.requests import Request
from starlette.responses import JSONResponse, RedirectResponse
from starlette.routing import Route
from starlette.middleware import Middleware
from starlette.middleware.gzip import GZipMiddleware
from starlette.config import Config

from pony.orm import Database, db_session, set_sql_debug, commit
from pony.orm.core import PrimaryKey, Required

from nanoid import generate


config = Config('.env')
db = Database()


def setup_database(db) -> None:
    db.bind(provider='sqlite', filename='database.sqlite', create_db=True)
    db.generate_mapping(create_tables=True)

    set_sql_debug(True, True)

    print('\U0001F3B2 \U0001F3E6 Successfully connection at database!')


def bootstrap() -> None:
    print('\U0001F525 Server running!')


class Link(db.Entity):
    _table_ = 'links'

    id = PrimaryKey(str, default=lambda: str(uuid4()))
    id_shortened_url = Required(str, unique=True)
    shortened_url = Required(str, unique=True)
    url_original = Required(str, unique=True)


@db_session
def create_link(shortened_url: str, id_shortened_url: str, url_original: str):
    link = {
        "id_shortened_url": id_shortened_url,
        "shortened_url": shortened_url,
        "url_original": url_original
    }

    return Link(**link)


@db_session
def get_link(id_shortened_url: int):
    return Link.get(id_shortened_url=id_shortened_url)


async def shorten(request: Request) -> JSONResponse:
    path = f'{request.url.scheme}://{request.url.netloc}'

    await request.json()

    url = request._json['url']

    id: str = generate('1234567890abcdef', 8)

    shortened_url = f'{path}/{id}'

    link = create_link(shortened_url, id, url)

    return JSONResponse(link.to_dict(), status_code=201)


async def redirect(request: Request):
    id = request.path_params['id']

    link = get_link(id)

    return RedirectResponse(link.url_original, status_code=301)

routes = [
    Route('/shorten', shorten, methods=['POST']),
    Route('/{id}', redirect, methods=['GET'])
]

middlewares = [
    Middleware(GZipMiddleware)
]

app = Starlette(
    debug=True,
    routes=routes,
    middleware=middlewares,
    on_startup=[lambda: setup_database(db)]
)

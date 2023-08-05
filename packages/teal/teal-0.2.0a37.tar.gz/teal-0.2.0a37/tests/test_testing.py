from distutils.version import StrictVersion
from typing import Tuple
from unittest.mock import MagicMock

from flask import Response, json

from teal.client import Client
from teal.config import Config
from teal.db import SchemaSQLAlchemy
from teal.teal import Teal


def test_json_encoder(app: Teal):
    """
    Ensures that Teal is using the custom JSON Encoder through Flask's
    json.
    """
    with app.app_context():
        # Try to dump a type flask's json encoder cannot handle
        json.dumps({'foo': StrictVersion('1.3')})


def test_cors(fconfig: Config, db: SchemaSQLAlchemy):
    DeviceDef, *_ = fconfig.RESOURCE_DEFINITIONS  # type: Tuple[ResourceDef]

    def foo(*args, **kw):
        return Response(status=200)

    DeviceDef.VIEW.get = MagicMock(side_effect=foo)
    client = Teal(config=fconfig, db=db).test_client()  # type: Client
    _, response = client.get('/devices/')
    headers = response.headers.to_list()
    assert ('Access-Control-Expose-Headers', 'Authorization') in headers
    assert ('Access-Control-Allow-Origin', '*') in headers

#
# NOT WORKING STILL PENDING TO FINISH/TEST
#

from app import create_app
from flask import json


def test_add():
    given = {
        "email": "robson@robson.com.br",
        "password": "123456",
    }
    response = app.test_client().post(
        '/auth/signin',
        data=json.dumps(given),
        content_type='application/json',
    )

    assert response.status_code == 200

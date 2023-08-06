
import datetime
import uuid

import pytest

from jupyterlab_sql.handlers.serializer import make_row_serializable


@pytest.mark.parametrize(
    "test_input",
    [
        ((1, 'hello'),),
        ((1, {'some': 'dict'}),),
        ((1, {'some': ['array', 'in', 'dict']}),)
    ])
def test_make_row_serializable_unchanged(test_input):
    assert make_row_serializable(test_input) == test_input


def test_serialize_uuid():
    uuid_str = '6e1d16e3-ca00-4e96-9735-95bf92a8c46c'
    row = (1, uuid.UUID(uuid_str))
    assert make_row_serializable(row) == (1, uuid_str)


def test_serialize_datetime():
    dt = datetime.datetime(2019, 2, 10, 11, 45, 22)
    expected_str = "2019-02-10 11:45:22"
    row = (1, dt)
    assert make_row_serializable(row) == (1, expected_str)


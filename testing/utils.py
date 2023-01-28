import json


def mongo_check_id(init_data, data, key, id):
    return init_data["_id"] != id or str(init_data[key]) == data[key]["$oid"]


def mongo_check_update(mongo_db, data):
    test_data = mongo_db.tests.find_one(data)
    assert test_data


def endpoint_test_handler(resp):
    assert resp.status == 200


async def get_endpoint_test_handler(cli, path, initial_data, initial_id, **kwargs):
    resp = await cli.get(path, **kwargs)
    text = await resp.text()
    data = json.loads(text)

    endpoint_test_handler(resp)
    assert len(initial_data) == len(data)
    assert all([[d[p] == data[i][p] if p != "_id" else mongo_check_id(d, data[i], p, initial_id) for p in d] for i, d in enumerate(initial_data)])


async def post_endpoint_test_handler(cli, path, **kwargs):
    resp = await cli.post(path, **kwargs)
    endpoint_test_handler(resp)

    json_response = await resp.json()
    assert json_response["status"] == "OK"

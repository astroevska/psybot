def mongo_check_update(mongo_db, data):
    test_data = mongo_db.tests.find_one(data)
    assert test_data


def endpoint_test_handler(resp):
    assert resp.status == 200


async def post_endpoint_test_handler(cli, path, **kwargs):
    resp = await cli.post(path, **kwargs)
    endpoint_test_handler(resp)

    json_response = await resp.json()
    assert json_response["status"] == "OK"

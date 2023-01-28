async def endpoint_test_handler(cli, path, **kwargs):
    resp = await cli.post(path, **kwargs)
    assert resp.status == 200

    json_response = await resp.json()
    assert json_response["status"] == "OK"

def mongo_update_handler(mongo_db, data):
    test_data = mongo_db.tests.find_one(data)
    assert test_data

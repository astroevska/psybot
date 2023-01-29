import json
from testing.utils import endpoint_check_status, mongo_check_id


async def get_endpoint_test_handler(cli, path, initial_data, initial_id, **kwargs):
    resp = await cli.get(path, **kwargs)
    text = await resp.text()
    data = json.loads(text)

    endpoint_check_status(resp)
    assert len(initial_data) == len(data)
    assert all([[d[p] == data[i][p] if p != "_id" else mongo_check_id(d, data[i], p, initial_id) for p in d] for i, d in enumerate(initial_data)])


async def post_endpoint_test_handler(cli, path, **kwargs):
    resp = await cli.post(path, **kwargs)
    endpoint_check_status(resp)

    json_response = await resp.json()
    assert json_response["status"] == "OK"

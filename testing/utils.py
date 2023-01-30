def mongo_check_id(init_data, data, key, id):
    return init_data["_id"] != id or str(init_data[key]) == data[key]["$oid"]


def mongo_check_update(mongo_db, data, tableName):
    test_data = mongo_db[tableName].find_one(data)
    assert test_data


def endpoint_check_status(resp):
    assert resp.status == 200

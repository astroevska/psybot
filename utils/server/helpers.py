import json
from aiohttp import web
from datetime import datetime
from dateutil import parser
from bson.objectid import ObjectId

from utils.helpers import json_serialize

def getHandlerFactory(getter, keys=[]):
    def get_handler(request):
        return web.Response(body=json_serialize(list(getter({k:request.rel_url.query[k] for k in keys if k in request.rel_url.query}))))

    return get_handler

def postHandlerFactory(post_method, required={}, isDateNeed=False, updateGetter=None):
    async def add_handler(request):
        try:
            data = await request.json()
        except:
            return web.json_response({"status": "error", "message": "Invalid JSON"})

        if (updateGetter and "_id" not in data) or not all([all([subkey in data[field] for subkey in required[idx]]) if type(required[idx]) == list else field in data for idx, field in enumerate(required)]):
            return web.json_response({"status": "error", "message": "Identifiers is undefined."})

        try:
            if updateGetter:
                if len(data) <= len(required):
                    return web.json_response({"status": "error", "message": "You had updated no one field."})

                currentData = json.loads(json_serialize(updateGetter({'_id': ObjectId(data['_id'])})))
                response = {**{k: currentData[k] for k in currentData if k != '_id'}, **{k: data[k] for k in data if k != '_id'}}

            else:
                response = {k:data[k] for k in data}

            if isDateNeed:
                response["date"] = parser.parse(str(datetime.now()))

            post_method({"$set": response}, {'_id': ObjectId(currentData['_id']['$oid'])}) if updateGetter else await post_method(response)
        except Exception as e:
            return web.json_response({"status": "error", "message": f"Request is failed. {e}"})

        return web.json_response({"data": data, "status": "OK"})

    return add_handler
import json
from aiohttp import web
from dateutil import parser
from datetime import datetime
from bson.objectid import ObjectId
from asyncio.coroutines import iscoroutinefunction

from ...utils.helpers import json_serialize

def getHandlerFactory(getter, keys=[]):
    async def get_handler(request):
        filters = {k:request.rel_url.query[k] for k in keys if k in request.rel_url.query}

        return web.Response(text=json_serialize(list(getter(filters))))

    return get_handler

def postHandlerFactory(post_method, required=[], isDateNeed=False, updateGetter=None):
    async def post_handler(request):
        try:
            data = await request.json()
        except Exception as e:
            return web.json_response({"status": "error", "message": "Invalid JSON", "details": e})

        isUpdate = bool(updateGetter)

        if (isUpdate and "_id" not in data) or not all([all([subkey in data[required[idx - 1]] for subkey in field]) if type(field) == list else field in data for idx, field in enumerate(required)]):
            return web.json_response({"status": "error", "message": "Identifiers is undefined."})

        try:
            if isUpdate:
                if len(data) < len(required):
                    return web.json_response({"status": "error", "message": "You had updated no one field."})

                currentData = json.loads(json_serialize(updateGetter({'_id': ObjectId(data['_id'])})))

                if not currentData:
                    return web.json_response({"status": "error", "message": "You had updated no one field."})

                response = {**{k: currentData[k] for k in currentData if k != '_id'}, **{k: data[k] for k in data if k != '_id'}}

            else:
                response = {k:data[k] for k in data}

            if isDateNeed:
                response["date"] = parser.parse(str(datetime.now()))

            if bool(isUpdate):
                post_method({'_id': ObjectId(currentData['_id']['$oid'])}, {"$set": response})
            elif iscoroutinefunction(post_method):
                await post_method(response)
            else:
                post_method(response)

            return web.json_response({"message": data, "status": "OK"})

        except Exception as e:
            return web.json_response({"status": "error", "message": f"Request is failed. {e}"})

    return post_handler

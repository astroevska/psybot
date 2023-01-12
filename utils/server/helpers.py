from aiohttp import web

from utils.helpers import json_serialize

def getHandlerFactory(getter, keys=[]):
    def get_handler(request):
        return web.Response(body=json_serialize(list(getter({k:request.rel_url.query[k] for k in keys if k in request.rel_url.query}))))

    return get_handler
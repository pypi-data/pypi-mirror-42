
import aiohttp
import asyncio
import async_timeout


class ArangoClient(object):
    
    def __init__(self, host='127.0.0.1', port=8529, dbname='', username='root', password=''):
        self.max_retry = 1
        self.timeout = 3
        self.host = host
        self.port = port
        self.dbname = dbname
        self.username = username
        self.password = password
        self.token = None
        self.base_url = f"http://{self.host}:{self.port}"

    async def get_token(self, session):
        params = {"username": self.username, "password": self.password}
        endpoint = f"{self.base_url}/_open/auth"
        with async_timeout.timeout(self.timeout):
            try:
                async with session.post(endpoint, json=params) as response:
                    res = await response.json()
                    self.token = res['jwt']
                    res = await response.json()
            except (aiohttp.ClientConnectionError, asyncio.CancelledError) as e:
                return None

    async def execute(self, query):
        async with aiohttp.ClientSession() as session:
            params = { "query" : query }
            endpoint = f"{self.base_url}/_db/{self.dbname}/_api/cursor"

            retry = 0
            while retry <= self.max_retry:
                headers = {"Authorization": f"bearer {self.token}"}
                with async_timeout.timeout(self.timeout):
                    try:
                        async with session.post(endpoint, json=params, headers=headers) as response:
                            res = await response.json()
                    except (aiohttp.ClientConnectionError, asyncio.CancelledError) as e:
                        return None
                
                if res['code'] == 401:
                    if retry == self.max_retry:
                        return None
                    else:
                        await self.get_token(session)
                elif res['code'] >= 400:
                    return None
                else:
                    result = res['result']
                    return result
                
                retry += 1
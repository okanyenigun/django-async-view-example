import aiohttp
import ssl
import certifi
import time
import requests
import asyncio
from django.shortcuts import render

def sync_view(request):
    "synchronous view"
    start = time.time()
    brewery_list = []
    url = "https://api.openbrewerydb.org/breweries/random"
    for _ in range(100):
        response = requests.get(url)
        brewery_list.append(response.json()[0]["id"])
    count = len(brewery_list)
    execution_time = time.time() - start
    return render(request, './templates/exp1.html', {"data":brewery_list, "count": count, "time": execution_time})

async def async_view(request):
    "asyncronous view"
    start = time.time()
    brewery_list = []
    url = "https://api.openbrewerydb.org/breweries/random"
    ssl_context = ssl.create_default_context(cafile=certifi.where())
    conn = aiohttp.TCPConnector(ssl=ssl_context)
    async with aiohttp.ClientSession(connector=conn) as session:
        for _ in range(100):
            async with session.get(url) as response:
                data = await response.json()
                brewery_list.append(data[0]["id"])
    count = len(brewery_list)
    execution_time = time.time() - start
    return render(request, './templates/exp1.html', {"data":brewery_list, "count": count, "time": execution_time})

async def get_brewery(session, url):
    "helper function to pull data from url"
    async with session.get(url) as response:
        data = await response.json()
    return data[0]["id"]

async def async_view_actions(request):
    "asynchronous + asyncio view"
    start = time.time()
    brewery_list = []
    actions = []
    url = "https://api.openbrewerydb.org/breweries/random"
    ssl_context = ssl.create_default_context(cafile=certifi.where())
    conn = aiohttp.TCPConnector(ssl=ssl_context)
    async with aiohttp.ClientSession(connector=conn) as session:
        for _ in range(100):
            #actions.append(asyncio.ensure_future(get_brewery(session, url)))
            actions.append(asyncio.create_task(get_brewery(session, url)))
        brew_response = await asyncio.gather(*actions)
        for data in brew_response:
            brewery_list.append(data)
    count = len(brewery_list)
    execution_time = time.time() - start
    return render(request, './templates/exp1.html', {"data":brewery_list, "count": count, "time": execution_time})

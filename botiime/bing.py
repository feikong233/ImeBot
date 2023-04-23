import asyncio
import os
import aiohttp
import datetime

from pathlib import Path

date = str(datetime.datetime.now().strftime('%Y-%m-%d'))


# 这个函数用来获取每天的必应每日一图并存储在对应的文件夹
async def bing_image_get():
    ero_url = "https://www.bing.com/HPImageArchive.aspx?format=js&n=1"
    async with aiohttp.ClientSession() as session:
        async with session.get(ero_url) as r:
            ret = await r.json()
        pic_url = "https://cn.bing.com" + ret["images"][0]["url"]
        async with session.get(pic_url) as r:
            pic = await r.read()

    # 按日期存储图片
    Path("./imgs/bing/" + date + "-bing.jpg").write_bytes(pic)


# 这个函数用来获取对应的图片信息
async def bing_info_get():
    ero_url = "https://www.bing.com/HPImageArchive.aspx?format=js&n=1"
    async with aiohttp.ClientSession() as session:
        async with session.get(ero_url) as r:
            ret = await r.json()
        pic_url = "https://cn.bing.com" + ret["images"][0]["url"]
        copyr = ret["images"][0]["copyright"]
        title = ret["images"][0]["title"]
        return_tuple = [title, copyr, pic_url]
        return return_tuple


# 这个函数用来检测今天的每日一图是否已经被生成，避免重复下载
def try_todays_bing():
    if os.path.exists("./imgs/bing/" + date + "-bing.jpg"):
        return True
    else:
        await bing_image_get()
        return True

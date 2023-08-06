# coding:utf-8

from webmother.service import ctrl_mine
from asyncio import get_event_loop


async def my_identities(uid, access_token):
    args = (uid, access_token)
    return await get_event_loop().run_in_executor(None, ctrl_mine.my_identities, *args)

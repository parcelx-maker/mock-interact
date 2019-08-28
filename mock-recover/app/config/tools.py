#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
-------------------------------------------------
@Author :   luzhao
@Email :    zhao.lu@parcelx.io 
@DateTime ： 8/28/2019 11:42 AM
@Description :
-------------------------------------------------
"""
from os.path import dirname, join, abspath

import json
import requests

from app.app import app

root_dir = dirname(dirname(abspath(__file__)))

def get_path_base_root(*path):
    """
    return the path that join the project root dir
    """
    result = root_dir
    for tempath in path:
        result = join(result, tempath)
    return abspath(result)

def do_post(agent, funcEnumName, funcParam):
    sync_chain_data = {
        "groupId": agent["groupId"],
        "funcEnumName": funcEnumName,
        "funcParam": funcParam,
    }
    app.logger.info("TO POST: %s", json.dumps(sync_chain_data, indent=4))
    if agent["post"]:
        r = requests.post(agent["sync-chain-url"], json=sync_chain_data, headers={"Content-Type": "application/json", })
        r.raise_for_status()
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
-------------------------------------------------
@Author :   luzhao
@Email :    zhao.lu@parcelx.io 
@DateTime ： 8/28/2019 11:10 AM
@Description :
-------------------------------------------------
"""
import configparser
import json
import os
import random

from .tools import get_path_base_root

def loadConfig(filepath):
    """
    :param filepath:
    :return:
    """
    config = configparser.ConfigParser()
    config.read(filepath)
    return {
        "mock-service": {
            "host": os.environ["BCOS_AGENT_HOST"] if "BCOS_AGENT_HOST" in os.environ else config.get("mock-service", "host"),
            "port": os.environ["APP_PORT"] if "APP_PORT" in os.environ else config.get("mock-service", "port"),
            "provider": config.get("mock-service", "provider"),
            "route": config.get("mock-service", "route")
        },

        "parcel-no": {
            "upload-parcel-path": config.get("parcel-no", "upload-parcel-path"),
            "startswith": config.get("parcel-no", "startswith"),
            "contains": config.get("parcel-no", "contains"),
            "min-block-number": config.getint("parcel-no", "min-block-number"),
        },
        "task": {
            "id": config.get("task", "id"),
            "seconds": config.getint("task", "seconds"),
            "ratio": config.getint("task", "ratio"),
        },
        "bcos-agent": {
            "sync-chain-url": os.environ["BCOS_AGENT_ADD_URL"] if "BCOS_AGENT_ADD_URL" in os.environ else config.get(
                "bcos-agent",
                "sync-chain-url"),
            "post": True if config.has_option("bcos-agent", "post") and config.get("bcos-agent",
                                                                                     "post") == "true" else False,
            "groupId": os.environ["BCOS_AGENT_GROUPID"] if "BCOS_AGENT_GROUPID" in os.environ else config.get("bcos-agent",
                                                                                                              "groupId"),
        }
    }


mockConfig = loadConfig(get_path_base_root("config", "config.ini"))

# check the config file
with open(get_path_base_root("config", mockConfig["mock-service"]["provider"]), mode="r", encoding="utf8") as fp:
    AccountNos = json.load(fp)
    if AccountNos and isinstance(AccountNos, list):
        for accountNo in AccountNos:
            if "id" not in accountNo or "name" not in accountNo:
                raise KeyError("服务商字段不符合要求!")
        accountNoSize = len(AccountNos)
        randomAccountInfo = lambda: AccountNos[random.randrange(0, accountNoSize)]
    else:
        raise ValueError("服务商配置文件不符合要求!")

if mockConfig["mock-service"]["route"]:
    with open(get_path_base_root("config", mockConfig["mock-service"]["route"]), mode="r", encoding="utf8") as fp:
        RouteIDs = json.load(fp)
        if isinstance(RouteIDs, list):
            for route_id in RouteIDs:
                if not isinstance(route_id, str):
                    raise ValueError("链路配置不符合要求!")
            RouteIDs = set(RouteIDs)
        else:
            raise ValueError("链路配置文件不符合要求!")

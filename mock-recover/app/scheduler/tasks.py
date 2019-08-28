#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
-------------------------------------------------
@Author :   luzhao
@Email :    zhao.lu@parcelx.io 
@DateTime ： 8/28/2019 12:13 PM
@Description :
-------------------------------------------------
"""
import random
import time

from flask_apscheduler import APScheduler

from app.config.config import mockConfig
from app.config.tools import do_post
from app.store.sqlitedb import db, app, ParcelTrack

scheduler = APScheduler()

parcelOperateNames = [
    "COLLECT", u"拣货",
    "SENDOUT", u"发货",
    "TAKEOFF", u"起运",
    "LANDING", u"着陆",
    "CLEARANCE_START", u"清关开始",
    "CLEARANCE_END", u"清关结束",
    # "CLEARANCE_ERROR", u"清关错误",
    "HANDOVER", u"提货",
    "DELIVERY", u"快递配送",
    "SIGNING", u"用户签收",
    # "STOP_DELIVERY", u"停止配送",
]
parcelOperateLimit = len(parcelOperateNames)

randomNumber = lambda n: ''.join([random.choice("1234567890") for _ in range(n)])
randomNumberChar = lambda n: ''.join([random.choice("1234567890abcdefghijklmnopqrstuvwxyz") for _ in range(n)])
currentTime = lambda: time.strftime("%Y%m%d%H%M%S", time.localtime())
currentTimeStamp = lambda: "%s" % int(time.time() * 1000)

Locations = [u"日本-东京", u"日本-大阪", u"日本-名古屋", u"日本-横滨",
             u"日本-京都", u"日本-神户", u"日本-北九州", u"日本-横须贺",
             u"日本-广岛", u"日本-北海道", u"日本-冲绳", u"日本-福冈", ]
LocationsSize = len(Locations)
randomLocation = lambda: Locations[random.randrange(0, LocationsSize)]

ToLocations = [u"中国-上海-松江", u"中国-上海-徐家汇", u"中国-上海-青浦", u"中国-上海-浦东",
               u"中国-江苏-无锡", u"中国-江苏-常州", u"中国-江苏-苏州", u"中国-江苏-南京"]
ToLocationsSize = len(ToLocations)
randomToLocation = lambda: ToLocations[random.randrange(0, ToLocationsSize)]


@scheduler.task('interval', id=mockConfig["task"].get("id", "task1"), seconds=mockConfig["task"].get("seconds", 30))
def task():
    app.logger.info('task %s start' % mockConfig["task"].get("id", "task1"))
    parcelObjs = ParcelTrack.query.filter_by(status=False)
    for parcel in parcelObjs:
        # first step
        if not parcel.track:
            app.logger.info("%s 准备轨迹操作: %s", parcel, parcelOperateNames[1])
            track = {
                "index": 0,
                "history": [[parcelOperateNames[0], currentTime()]]
            }
            # do post
            do_post(mockConfig["bcos-agent"], "FUNC_PARCEL_TRACK_UPDATE", parcel.data)
            # update parcel
            ParcelTrack.query.filter_by(id=parcel.id).update(dict(track=track))

        else:
            # 概率过滤步骤， 打散间隔固定时间执行顺序
            random_ratio = random.randrange(0, 100)
            if mockConfig["task"].get("ratio", 100) <= random_ratio:
                app.logger.info("%s: random_ratio=%d, continue!", parcel, random_ratio)
                continue

            track = parcel.track
            nextDo = track["index"] + 2
            app.logger.info("%s: random_ratio=%d, To do: %s", parcel, random_ratio, parcelOperateNames[nextDo + 1])

            data = parcel.data
            data["id"] = randomNumberChar(32)
            data["operationName"] = parcelOperateNames[nextDo]
            data["updateTime"] = currentTimeStamp()
            if data["operationName"] == "LANDING":
                data["location"] = u"中国-青岛-海关"
            elif data["operationName"] == "HANDOVER":
                data["location"] = randomToLocation()
            data["description"] = parcelOperateNames[nextDo + 1]

            # do post
            do_post(mockConfig["bcos-agent"], "FUNC_PARCEL_TRACK_UPDATE", data)

            track["index"] = nextDo
            track["history"].append([parcelOperateNames[nextDo], currentTime()])
            # update parcel
            parcel.data = data
            parcel.track = track

            if nextDo + 2 == parcelOperateLimit:
                ParcelTrack.query.filter_by(id=parcel.id).update(dict(data=data, track=track, status=True))
            else:
                ParcelTrack.query.filter_by(id=parcel.id).update(dict(data=data, track=track))

        db.session.commit()

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
-------------------------------------------------
@Author :   luzhao
@Email :    zhao.lu@parcelx.io 
@DateTime ： 8/28/2019 3:01 PM
@Description :
-------------------------------------------------
"""
import json
from datetime import datetime

from flask import request, jsonify

from app.app import app
from app.config.config import RouteIDs, mockConfig, randomAccountInfo
from app.scheduler.tasks import randomNumberChar, parcelOperateNames, currentTime, currentTimeStamp, randomLocation
from app.store.sqlitedb import ParcelTrack, db

def get_tx_info(header):
    return {
        "block-number": header.get("Block-Num"),
        "block-hash": header.get("Block-Data-Hash"),
        "channel-id": header.get("Channel-Id"),
        "transaction-hash": header.get("Transaction-Id"),
        "func-name": header.get("Func-Name"),
    }


def filter_parcel(parcel, tx_info):
    parcel_no = parcel.get("parcelNo", None)
    route_no = parcel.get("routeNo", None)

    if not parcel_no or not route_no:
        return False

    # 若route不进行配置, 则默认不筛选
    if RouteIDs and route_no not in RouteIDs:
        return False

    # 区块高度限制
    min_block_number = mockConfig["parcel-no"]["min-block-number"]
    if min_block_number > int(tx_info["block-number"]):
        return False

    # 编号规则限制
    startswith_str = mockConfig["parcel-no"]["startswith"]
    contains_str = mockConfig["parcel-no"]["contains"]
    if startswith_str and not parcel_no.startswith(startswith_str):
        return False
    if contains_str and not contains_str in parcel_no:
        return False

    return True


def create_parcel_track(parcel_no):
    """
    :param parcel_no:
    :return:
    """
    parcelObj = ParcelTrack.query.filter_by(id=parcel_no).first()
    if not parcelObj:
        parcel_track = random_parcel_track(parcel_no)
        db.session.add(ParcelTrack(
            id=parcel_no,
            data=parcel_track,
            status=False,
            created_time=datetime.now()
        ))
    else:
        app.logger.warning("%s exist!" % parcelObj)


def random_parcel_track(parcel_no):
    """
    Template:
    {
        "id":"ed45a40ac180465ba99cca272738cb12",
        "parcelNo":"1604c4d9b52d422aa43472fd92461919",
        "operationName":"COLLECT",
        "accountName":"服务商测试1号",
        "accountNo":"488355f438b64cd2a17a071c12cee74a",
        "internationalDeliveryNo":"11111111231231231",
        "updateTime":"1557460800000",
        "location":"日本东京",
        "description":"拣货"
    }
    :return:
    """
    account = randomAccountInfo()
    return {
        "id": randomNumberChar(32),
        "parcelNo": parcel_no,
        "operationName": parcelOperateNames[0],
        "accountNo": account["id"],
        "accountName": account["name"],
        "internationalDeliveryNo": currentTime(),
        "updateTime": currentTimeStamp(),
        "location": randomLocation(),
        "description": parcelOperateNames[1]
    }


@app.route('/api/v1/recoverdata/<path:subpath>', methods=['POST'])
def recover_api(subpath):
    if not request.is_json:
        app.logger.warning("http request data is not json! %s",
                           json.dumps({"path": request.path, "data": request.get_data()}, indent=4))
        return jsonify({'status': 'true'})

    tx_info = get_tx_info(request.headers)
    data = request.get_json()

    # 对包裹上传通知接口进行获取相应包裹ParcelNo, 并创建包裹轨迹.
    if "/%s" % subpath == mockConfig["parcel-no"]["upload-parcel-path"]:
        if isinstance(data, dict) and filter_parcel(data, tx_info):
            create_parcel_track(data.get("parcelNo", None))
        else:
            app.logger.warning("mismatch condition! not to create parcel!")

    app.logger.info(json.dumps({"path": request.path, "header": tx_info, "data": data}, indent=4))
    return jsonify({'status': 'true'})

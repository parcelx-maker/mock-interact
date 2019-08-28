#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@Time:   2019/5/27 14:49
@Author: quanbin_zhu
@Email:  quanbin@parcelx.io
"""

import os

from app.app import app
from app.config.config import mockConfig
from app.scheduler.tasks import scheduler
from app.store.sqlitedb import db

if __name__ == '__main__':
    db.create_all()
    scheduler.init_app(app)
    scheduler.start()
    host = mockConfig["mock-service"]["host"]
    port = os.environ["APP_PORT"] if "APP_PORT" in os.environ else mockConfig["mock-service"]["port"]
    app.run(host=host if host else "127.0.0.1",
            port=port if port else 5000)

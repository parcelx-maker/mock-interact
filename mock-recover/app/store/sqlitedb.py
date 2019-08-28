#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
-------------------------------------------------
@Author :   luzhao
@Email :    zhao.lu@parcelx.io 
@DateTime ： 8/28/2019 12:04 PM
@Description :
-------------------------------------------------
"""

from flask_sqlalchemy import SQLAlchemy

from app.config.tools import root_dir
from app.app import app

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///%s/mock.db' % root_dir
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SCHEDULER_API_ENABLED'] = True
db = SQLAlchemy(app)

class ParcelTrack(db.Model):
    id = db.Column(db.String(64), primary_key=True)
    track = db.Column(db.PickleType, nullable=True)
    data = db.Column(db.PickleType, nullable=False)
    status = db.Column(db.Boolean, default=False)
    created_time = db.Column(db.DateTime, nullable=False, )

    def __repr__(self):
        return '<ParcelTrack %r>' % self.id
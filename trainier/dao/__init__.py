#!/usr/bin/env python
# -*- coding: utf-8 -*-

from peewee import Model
from playhouse.pool import PooledSqliteDatabase

from trainier import AppConfig

db = PooledSqliteDatabase(str(AppConfig.DB_FILE), max_connections=8, thread_safe=True,
                          pragmas=dict(journal_mode='WAL', autocommit=False, cache_size=-1024 * 8))
db.connect(True)


class BaseModel(Model):
    class Meta:
        database = db

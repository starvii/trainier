#!/usr/bin/env python
# -*- coding: utf-8 -*-

from peewee import Model, SqliteDatabase
from playhouse.pool import PooledSqliteDatabase

from trainier.config import AppConfig

# db = PooledSqliteDatabase(str(AppConfig.DB_FILE), max_connections=8, thread_safe=False,
#                           pragmas=dict(journal_mode='WAL', autocommit=False, cache_size=-1024 * 8))
# 连接池在tornado下有问题，tornado会开启新线程查询，导致连接出错
db = SqliteDatabase(str(AppConfig.DB_FILE), pragmas=dict(journal_mode='WAL', autocommit=False, cache_size=-1024 * 8))

# db.connect(True)


class BaseModel(Model):
    class Meta:
        database = db

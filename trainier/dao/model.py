#!/usr/bin/env python
# -*- coding: utf-8 -*-

from peewee import IntegerField, CharField, Field, TextField, AutoField, BooleanField

from trainier.dao.orm import BaseModel, db


class Trunk(BaseModel):
    db_id: Field = AutoField(primary_key=True)
    entity_id: Field = CharField(max_length=20, unique=True, default='')
    code: Field = CharField(max_length=100, unique=True, default='')
    en_trunk: Field = TextField(default='')
    cn_trunk: Field = TextField(default='')
    en_trunk_text: Field = TextField(index=True, default='')
    cn_trunk_text: Field = TextField(index=True, default='')
    explanation: Field = TextField(index=True, default='')
    source: Field = TextField(index=True, default='')
    level: Field = IntegerField(default=0)
    comment: Field = TextField(default='')
    order_num: Field = IntegerField(index=True, default=0)
    parent_id: Field = CharField(max_length=20, index=True, default='')
    # 为 '' 时表示单项题目，'root'时表示根题目节点，其下的子题目该项为父题目的ID

    class Meta:
        table_name = 'trunk'


class Option(BaseModel):
    db_id: Field = AutoField(primary_key=True)
    entity_id: Field = CharField(max_length=20, unique=True, default='')
    trunk_id: Field = CharField(max_length=20, index=True, default='')
    code: Field = CharField(max_length=100, unique=True, default='')
    en_option: Field = TextField(index=True, default='')
    cn_option: Field = TextField(index=True, default='')
    is_true: Field = BooleanField(default=False)
    order_num: Field = IntegerField(index=True, default=0)
    comment: Field = TextField(default='')

    class Meta:
        table_name = 'option'


class Quiz(BaseModel):
    db_id: Field = AutoField(primary_key=True)
    entity_id: Field = CharField(max_length=20, unique=True, default='')
    code: Field = CharField(max_length=100, unique=True, default='')
    name: Field = TextField(index=True, default='')
    questions: Field = TextField(default='')
    random_trunk: Field = BooleanField(default=False)
    random_choice: Field = BooleanField(default=False)
    comment: Field = TextField(default='')

    class Meta:
        table_name = 'quiz'


class Result(BaseModel):
    db_id: Field = AutoField(primary_key=True)
    entity_id: Field = CharField(max_length=20, unique=True, default='')
    quiz_id: Field = CharField(max_length=20, index=True, default='')
    instance_id: Field = CharField(max_length=20, index=True, default='')
    user_id: Field = CharField(max_length=20, index=True, default='')
    trunk_id: Field = CharField(max_length=20, index=True, default='')
    answer: Field = TextField(default='')
    is_true: Field = BooleanField(default=True)

    class Meta:
        table_name = 'result'


class User(BaseModel):
    db_id: Field = AutoField(primary_key=True)
    entity_id: Field = CharField(max_length=20, unique=True, default='')
    username: Field = CharField(max_length=20, unique=True)
    password: Field = CharField(max_length=50)
    salt: Field = CharField(max_length=50)
    auth: Field = CharField(max_length=50)
    comment: Field = TextField(default='')

    class Meta:
        table_name = 'user'


def create():
    db.create_tables(BaseModel.__subclasses__())


if __name__ == '__main__':
    create()

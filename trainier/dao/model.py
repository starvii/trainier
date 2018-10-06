#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sqlalchemy import Column, Integer, String, BLOB, DATETIME, TEXT

from trainier.dao.orm import Base, metadata


class Trunk(Base):
    __tablename__ = 'trunk'
    __table_args__ = {'extend_existing': True}

    db_id = Column(Integer, primary_key=True, autoincrement=True)
    entity_id = Column(String(24), unique=True, index=True, default='')
    code = Column(String(100), unique=True, index=True, default='')
    en_trunk = Column(TEXT, default='')
    cn_trunk = Column(TEXT, default='')
    en_trunk_text = Column(TEXT, index=True, default='')
    cn_trunk_text = Column(TEXT, index=True, default='')
    analysis = Column(TEXT, index=True, default='')
    source = Column(TEXT, index=True, default='')
    level = Column(Integer, default=0)
    comment = Column(TEXT, default='')
    order_num = Column(Integer, default=0)
    parent = Column(String(24), default='')  # 为 '' 时表示单项题目， 'root'时表示根题目节点， 其下的子题目该项为父题目的 ID

    def __repr__(self) -> str:
        super().__repr__()
        return '''{{
db_id="{}",
entity_id="{}",
code="{}",
en_trunk="{}",
cn_trunk="{}",
analysis="{}",
source="{}",
level="{}",
comment="{}",
order_num="{}",
parent="{}",
}}'''.format(
            self.db_id,
            self.entity_id,
            self.code,
            self.en_trunk,
            self.cn_trunk,
            self.analysis,
            self.source,
            self.level,
            self.comment,
            self.order_num,
            self.parent,
        )


class Option(Base):
    __tablename__ = 'option'
    __table_args__ = {'extend_existing': True}

    db_id = Column(Integer, primary_key=True, autoincrement=True)
    entity_id = Column(String(24), unique=True, index=True, default='')
    trunk_id = Column(String(24), nullable=False, index=True, default='')
    code = Column(String(100), unique=True, index=True, default='')
    en_option = Column(TEXT, index=True, default='')
    cn_option = Column(TEXT, index=True, default='')
    is_true = Column(Integer, default=0)
    order_num = Column(Integer, default=0)
    comment = Column(TEXT, default='')

    def __repr__(self) -> str:
        super().__repr__()
        return '''{{
db_id="{}",
entity_id="{}",
code="{}",
trunk_id="{}",
en_option="{}",
cn_option="{}",
is_true="{}",
order_num="{}",
comment="{}",
}}'''.format(
            self.db_id,
            self.entity_id,
            self.code,
            self.trunk_id,
            self.en_option,
            self.cn_option,
            self.is_true,
            self.order_num,
            self.comment
        )


## 由于使用了 ckeditor ，使用外部的图片链接，暂时不需要 Pic
# class Pic(Base):
#     __tablename__ = 'pic'
#     __table_args__ = {'extend_existing': True}
#
#     db_id = Column(Integer, primary_key=True, autoincrement=True)
#     entity_id = Column(String(24), unique=True, index=True, default='')
#     trunk_id = Column(String(24), nullable=False, index=True, default='')
#     code = Column(String(100), index=True, default='')
#     name = Column(TEXT, index=True, default='')
#     data = Column(BLOB, default=b'')
#     source = Column(TEXT, index=True, default='')
#     order_num = Column(Integer, default=0)
#     comment = Column(TEXT, default='')
#
#     def __repr__(self) -> str:
#         super().__repr__()
#         return '''{{
# db_id="{}",
# entity_id="{}",
# trunk_id="{}",
# code="{}",
# name="{}",
# data="{}",
# source="{}",
# order_num="{}",
# comment="{}"
# }}'''.format(
#             self.db_id,
#             self.entity_id,
#             self.trunk_id,
#             self.code,
#             self.name,
#             self.data,
#             self.source,
#             self.order_num,
#             self.comment
#         )


class Quiz(Base):
    __tablename__ = 'quiz'
    __table_args__ = {'extend_existing': True}

    db_id = Column(Integer, primary_key=True, autoincrement=True)
    entity_id = Column(String(24), unique=True, index=True, default='')
    code = Column(String(100), index=True, default='')
    name = Column(TEXT, index=True, default='')
    questions = Column(TEXT, default='')  # 使用【,】进行分割
    random_trunk = Column(Integer, default=0)
    random_choice = Column(Integer, default=0)
    comment = Column(TEXT, default='')

    def __repr__(self) -> str:
        super().__repr__()
        return '''{{
db_id="{}",
entity_id="{}",
code="{}",
name="{}",
questions="{}",
random_trunk="{}",
random_choice="{}",
comment="{}"
}}'''.format(
            self.db_id,
            self.entity_id,
            self.code,
            self.name,
            self.questions,
            self.random_trunk,
            self.random_choice,
            self.comment
        )


class Result(Base):
    __tablename__ = 'result'
    __table_args__ = {'extend_existing': True}

    db_id = Column(Integer, primary_key=True, autoincrement=True)
    entity_id = Column(String(24), unique=True, index=True, default='')
    quiz_id = Column(String(24), index=True, default='')
    quiz_inst_id = Column(String(24), index=True, default='')
    trunk_id = Column(String(24), index=True, default='')
    answer = Column(TEXT, default='')


class User(Base):
    __tablename__ = 'user'
    __table_args__ = {'extend_existing': True}

    db_id = Column(Integer, primary_key=True, autoincrement=True)
    entity_id = Column(String(24), unique=True, index=True, default='')
    username = Column(String(20), unique=True, index=True, default='')
    password = Column(String(50), default='')
    salt = Column(String(50), default='')
    auth = Column(String(50), default='')
    comment = Column(TEXT, default='')


def create():
    print(metadata.tables)
    metadata.create_all()


if __name__ == '__main__':
    create()

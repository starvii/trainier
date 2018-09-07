#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sqlalchemy import Column, Integer, String, BLOB, DATETIME, TEXT
from dao.orm import Base, metadata


class Trunk(Base):
    __tablename__ = 'trunk'
    __table_args__ = {'extend_existing': True}

    db_id = Column(Integer, primary_key=True, autoincrement=True)
    entity_id = Column(String(24), unique=True, index=True, default='')
    code = Column(String(100), unique=True, index=True, default='')
    en_trunk = Column(TEXT, index=True, default='')
    cn_trunk = Column(TEXT, index=True, default='')
    analysis = Column(TEXT, index=True, default='')
    source = Column(TEXT, index=True, default='')
    level = Column(Integer, default=0)
    comment = Column(TEXT, default='')
    parent = Column(String(24), default='')

    def __repr__(self) -> str:
        super().__repr__()
        return '''{{
entity_id="{}",
code="{}",
en_trunk="{}",
cn_trunk="{}",
analysis="{}",
source="{}",
level="{}",
comment="{}",
}}
'''.format(
            self.entity_id,
            self.code,
            self.en_trunk,
            self.cn_trunk,
            self.analysis,
            self.source,
            self.level,
            self.comment
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
entityId="{}",
code="{}",
trunkId="{}",
enOption="{}",
cnOption="{}",
isTrue="{}",
orderNum="{}",
comment="{}",
}}
'''.format(
            self.entity_id,
            self.code,
            self.trunk_id,
            self.en_option,
            self.cn_option,
            self.is_true,
            self.order_num,
            self.comment
        )


class Pic(Base):
    __tablename__ = 'pic'
    __table_args__ = {'extend_existing': True}

    db_id = Column(Integer, primary_key=True, autoincrement=True)
    entity_id = Column(String(24), unique=True, index=True, default='')
    trunk_id = Column(String(24), nullable=False, index=True, default='')
    code = Column(String(100), index=True, default='')
    name = Column(TEXT, index=True, default='')
    data = Column(BLOB, default=b'')
    source = Column(TEXT, index=True, default='')
    order_num = Column(Integer, default=0)
    comment = Column(TEXT, default='')


class Quiz(Base):
    __tablename__ = 'quiz'
    __table_args__ = {'extend_existing': True}

    db_id = Column(Integer, primary_key=True, autoincrement=True)
    entity_id = Column(String(24), unique=True, index=True, default='')
    code = Column(String(100), index=True, default='')
    name = Column(TEXT, index=True, default='')
    questions = Column(TEXT, default='')
    comment = Column(TEXT, default='')


class Result(Base):
    __tablename__ = 'result'
    __table_args__ = {'extend_existing': True}

    db_id = Column(Integer, primary_key=True, autoincrement=True)
    entity_id = Column(String(24), unique=True, index=True, default='')
    quiz_id = Column(String(24), index=True, default='')
    trunk_id = Column(String(24), index=True, default='')
    answer = Column(TEXT, default='')
    time = Column(DATETIME, default='')


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

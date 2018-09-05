#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sqlalchemy import Column, Integer, String, BLOB
from trainier.orm import Base


class Trunk(Base):
    __tablename__ = 'trunk'
    __table_args__ = {'extend_existing': True}

    entityId = Column(String(24), primary_key=True, default='')
    code = Column(String, unique=True, default='')
    enTrunk = Column(String, default='')
    cnTrunk = Column(String, default='')
    analysis = Column(String, default='')
    source = Column(String, default='')
    level = Column(Integer, default=0)
    comment = Column(String, default='')

    def __repr__(self) -> str:
        super().__repr__()
        return '''{{
entityId="{}",
code="{}",
enTrunk="{}",
cnTrunk="{}",
analysis="{}",
source="{}",
level="{}",
comment="{}",
}}
'''.format(
            self.entityId,
            self.code,
            self.enTrunk,
            self.cnTrunk,
            self.analysis,
            self.source,
            self.level,
            self.comment
        )


class Option(Base):
    __tablename__ = 'option'
    __table_args__ = {'extend_existing': True}

    entityId = Column(String(24), primary_key=True, default='')
    trunkId = Column(String(24), nullable=False, default='')
    code = Column(String, unique=True, default='')
    enOption = Column(String, default='')
    cnOption = Column(String, default='')
    isTrue = Column(Integer, default=0)
    orderNum = Column(Integer, default=0)
    comment = Column(String, default='')

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
            self.entityId,
            self.code,
            self.trunkId,
            self.enOption,
            self.cnOption,
            self.isTrue,
            self.orderNum,
            self.comment
        )


class Pic(Base):
    __tablename__ = 'pic'
    __table_args__ = {'extend_existing': True}

    entityId = Column(String(24), primary_key=True, default='')
    trunkId = Column(String(24), nullable=False, default='')
    code = Column(String, default='')
    title = Column(String, default='')
    data = Column(BLOB, default=b'')
    source = Column(String, default='')
    orderNum = Column(Integer, default=0)
    comment = Column(String, default='')

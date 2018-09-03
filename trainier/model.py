#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sqlalchemy import Column, Integer, String, BLOB
from trainier.orm import Base


class Trunk(Base):
    __tablename__ = 'trunk'
    __table_args__ = {'extend_existing': True}

    entityId = Column(String(24), primary_key=True)
    code = Column(String, unique=True)
    enTrunk = Column(String)
    cnTrunk = Column(String)
    analysis = Column(String)
    source = Column(String)
    level = Column(Integer)
    comment = Column(String)

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

    entityId = Column(String(24), primary_key=True)
    trunkId = Column(String(24), nullable=False)
    code = Column(String, unique=True)
    enOption = Column(String)
    cnOption = Column(String)
    isTrue = Column(Integer)
    orderNum = Column(Integer)
    comment = Column(String)

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

    entityId = Column(String(24), primary_key=True)
    trunkId = Column(String(24), nullable=False)
    title = Column(String)
    data = Column(BLOB)
    orderNum = Column(Integer)
    comment = Column(String)

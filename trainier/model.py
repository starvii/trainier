#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sqlalchemy import Column, Integer, String, BLOB
from trainier.orm import Base


class Trunk(Base):
    __tablename__ = 'trunk'

    entityId = Column(String(32), primary_key=True)
    enTrunk = Column(String)
    cnTrunk = Column(String)
    analysis = Column(String)
    source = Column(String)
    level = Column(Integer)
    comment = Column(String)



class Option(Base):
    __tablename__ = 'option'

    entityId = Column(String(32), primary_key=True)
    trunkId = Column(String(32), nullable=False)
    enOption = Column(String)
    cnOption = Column(String)
    isTrue = Column(Integer)
    orderNum = Column(Integer)
    comment = Column(String)


class Pic(Base):
    __tablename__ = 'pic'

    entityId = Column(String(32), primary_key=True)
    trunkId = Column(String(32), nullable=False)
    title = Column(String)
    data = Column(BLOB)
    orderNum = Column(Integer)
    comment = Column(String)

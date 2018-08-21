#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm.session import sessionmaker
from sqlalchemy import create_engine
from trainier import Config

__uri: str = 'sqlite:///{}'.format(Config.default.SQLALCHEMY_DATABASE_URI)

engine = create_engine(__uri, echo=True)

Base = declarative_base(bind=engine)

Session = sessionmaker(bind=engine)

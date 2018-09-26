#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm.session import sessionmaker

from trainier import Config

__uri: str = 'sqlite:///{}'.format(Config.default.SQLALCHEMY_DATABASE_URI)

engine = create_engine(__uri, echo=True)
metadata = MetaData(engine)
Base = declarative_base(bind=engine, metadata=metadata)

Session = sessionmaker(bind=engine)

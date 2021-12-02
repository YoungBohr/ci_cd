# -*- coding: utf-8 -*-


from sqlalchemy import Column, ForeignKey, Integer, DateTime, String, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class Server(Base):
    __tablename__ = 'dtk_cicd_server'

    id = Column(Integer, primary_key=True)
    name = Column(String(20), nullable=False)
    ip = Column(String(30), nullable=False)
    domain_name = Column(String(30), nullable=True)

    app = relationship('App', back_populates='server')


class App(Base):
    __tablename__ = 'dtk_cicd_app'

    id = Column(Integer, primary_key=True)
    name = Column(String(20), nullable=False)
    type = Column(String(10), nullable=False)
    project = Column(String(30), nullable=False)
    server_id = Column(Integer, ForeignKey('server.id'))

    server = relationship('Server', back_populates='app')
    version = relationship('Version', back_populates='app')
    release = relationship('Release', back_populates='app')


class Version(Base):
    __tablename__ = 'dtk_cicd_version'

    id = Column(Integer, primary_key=True, autoincrement=True)
    app_id = Column(Integer, ForeignKey('app.id'))
    version = Column(String(15), nullable=False)
    date = Column(DateTime, nullable=False)
    commit_hash = Column(String(60), nullable=False)
    commit_log = Column(Text, nullable=True)

    app = relationship('App', back_populates='version')
    release = relationship('Release', back_populates='version')


class User(Base):
    __tablename__ = 'dtk_cicd_user'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(20), nullable=False)
    email_address = Column(String(30), nullable=False)

    build = relationship('Build', back_populates='user')
    release = relationship('Release', back_populates='publisher')


class Build(Base):
    __tablename__ = 'dtk_devops_build'

    id = Column(Integer, primary_key=True, autoincrement=True)
    date = Column(DateTime, nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'))
    repo = Column(String(30), nullable=False)
    branch = Column(String(15), nullable=False)
    version = Column(String(15), nullable=False)
    commit_hash = Column(String(60), nullable=False)
    commit_author = Column(String(20), nullable=False)
    committer_email = Column(String(30), nullable=False)
    commit_date = Column(DateTime, nullable=False)
    commit_message = Column(String(30), nullable=False)
    commit_count = Column(String(30), nullable=True)

    md5 = Column(String(32), nullable=False)
    sha1 = Column(String(40), nullable=False)
    sha512 = Column(String(128), nullable=False)

    user = relationship('User', back_populates='build')
    release = relationship('Release', uselist=False, back_populates='artifact')


class Release(Base):
    __tablename__ = 'dtk_cicd_release'

    id = Column(Integer, primary_key=True, autoincrement=True)
    date = Column(DateTime, nullable=False)

    app_id = Column(Integer, ForeignKey('app.id'))
    app = relationship('App', back_populates='publishment')

    version_id = Column(Integer, ForeignKey('version.id'))
    version = relationship('Version', back_populates='publishment')

    publisher_id = Column(Integer, ForeignKey('user.id'))
    publisher = relationship('User', back_populates='publishment')

    artifact_id = Column(Integer, ForeignKey('build.id'))
    artifact = relationship('Build', back_populates='publishment')
    statue = Column(String(10), nullable=True)




import sys
import os
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref
from sqlalchemy import create_engine
Base = declarative_base()


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    name = Column(String(200), nullable=False)
    email = Column(String(200), nullable=False)


class SocCompany(Base):
    __tablename__ = 'soccompany'
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User, backref="soccompany")

    @property
    def serialize(self):
        """Return objects data in easily serializeable formats"""
        return {
            'name': self.name,
            'id': self.id
        }


class SocName(Base):
    __tablename__ = 'socname'
    id = Column(Integer, primary_key=True)
    name = Column(String(350), nullable=False)
    build = Column(String(150))
    cores = Column(String(10))
    frequency = Column(String(250))
    date = Column(DateTime, nullable=False)
    soccompanyid = Column(Integer, ForeignKey('soccompany.id'))
    soccompany = relationship(
        SocCompany, backref=backref('socname', cascade='all, delete'))
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User, backref="socname")

    @property
    def serialize(self):
        """Return objects data in easily serializeable formats"""
        return {
            'name': self. name,
            'build': self. build,
            'cores': self. cores,
            'frequency': self. frequency,
            'date': self. date,
            'id': self. id
        }

engin = create_engine('sqlite:///chipset.db')
Base.metadata.create_all(engin)

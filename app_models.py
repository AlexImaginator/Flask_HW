from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, func, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base


DSN = 'postgresql://flask_admin:flaskadmin@127.0.0.1:5432/flask_test_db'

engine = create_engine(DSN)

Base = declarative_base()


class UserModel(Base):
    __tablename__ = 'user'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False, unique=True)
    rating = Column(Integer, nullable=False, default=0)
    advert = relationship('AdvModel', back_populates='owner', cascade='all, delete-orphan')


class AdvModel(Base):
    __tablename__ = 'adv'
    
    id = Column(Integer, primary_key=True)
    title = Column(String(50), nullable=False)
    description = Column(Text, nullable=False)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    owner_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    owner = relationship('UserModel', back_populates='advert')


Base.metadata.create_all(engine)

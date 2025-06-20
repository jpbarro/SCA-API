from sqlalchemy import Column, Integer, String, Boolean, Float, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base

class Cat(Base):
    __tablename__ = "cats"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    years_of_experience = Column(Integer)
    breed = Column(String)
    salary = Column(Float)
    
    mission = relationship("Mission", back_populates="cat", uselist=False)

class Mission(Base):
    __tablename__ = "missions"
    id = Column(Integer, primary_key=True, index=True)
    complete = Column(Boolean, default=False)
    cat_id = Column(Integer, ForeignKey("cats.id"), nullable=True, unique=True)

    cat = relationship("Cat", back_populates="mission")
    targets = relationship("Target", back_populates="mission", cascade="all, delete-orphan")

class Target(Base):
    __tablename__ = "targets"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    country = Column(String)
    notes = Column(String, nullable=True)
    complete = Column(Boolean, default=False)
    mission_id = Column(Integer, ForeignKey("missions.id"))

    mission = relationship("Mission", back_populates="targets")
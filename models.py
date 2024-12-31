from sqlalchemy import Column, Integer, String, Float, ForeignKey, Table, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from geoalchemy2 import Geometry

Base = declarative_base()

# Association table for many-to-many relationship between languages and model types
language_models = Table(
    'language_models',
    Base.metadata,
    Column('language_id', Integer, ForeignKey('languages.id'), primary_key=True),
    Column('model_type_id', Integer, ForeignKey('model_types.id'), primary_key=True)
)

class Language(Base):
    """
    Model representing a language and its geographical location.
    """
    __tablename__ = 'languages'

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    iso_code = Column(String(10), nullable=False, unique=True)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    geom = Column(Geometry('POINT'), nullable=True)

    # Relationship to model types through the association table
    model_types = relationship(
        'ModelType',
        secondary=language_models,
        back_populates='languages'
    )

    def __repr__(self):
        return f"<Language(name='{self.name}', iso_code='{self.iso_code}')>"


class ModelType(Base):
    """
    Model representing different types of language models (TTS, NMT, etc.).
    """
    __tablename__ = 'model_types'

    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False, unique=True)
    description = Column(String(255))

    # Relationship to languages through the association table
    languages = relationship(
        'Language',
        secondary=language_models,
        back_populates='model_types'
    )

    def __repr__(self):
        return f"<ModelType(name='{self.name}')>"
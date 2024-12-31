from sqlalchemy import Column, Integer, String, Float, ForeignKey, Table, MetaData, Boolean
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

class LanguageFamily(Base):
    """Model representing language families."""
    __tablename__ = 'language_families'

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False, unique=True)
    description = Column(String(1000))

    # Relationships
    subfamilies = relationship('LanguageSubfamily', back_populates='family')
    languages = relationship('Language', back_populates='family')

class LanguageSubfamily(Base):
    """Model representing language subfamilies."""
    __tablename__ = 'language_subfamilies'

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    description = Column(String(1000))
    family_id = Column(Integer, ForeignKey('language_families.id'))

    # Relationships
    family = relationship('LanguageFamily', back_populates='subfamilies')
    languages = relationship('Language', back_populates='subfamily')

class Language(Base):
    """Model representing a language and its geographical information."""
    __tablename__ = 'languages'

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    iso_code = Column(String(10), nullable=False, unique=True)
    glottocode = Column(String(20))
    speakers = Column(Integer)
    main_city = Column(String(255))
    continent = Column(String(100))
    latitude = Column(Float)
    longitude = Column(Float)
    geom = Column(Geometry('POINT'))
    resources_url = Column(String(500))
    description = Column(String(1000))

    # Model availability flags and metadata
    asr = Column(Boolean, default=False)
    asr_hours = Column(Float)
    asr_speakers = Column(Integer)
    asr_url = Column(String(500))

    nmt = Column(Boolean, default=False)
    nmt_pairs = Column(String(500))
    nmt_url = Column(String(500))

    tts = Column(Boolean, default=False)
    tts_hours = Column(Float)
    tts_url = Column(String(500))

    # Foreign keys for family relationships
    family_id = Column(Integer, ForeignKey('language_families.id'))
    subfamily_id = Column(Integer, ForeignKey('language_subfamilies.id'))

    # Relationships
    family = relationship('LanguageFamily', back_populates='languages')
    subfamily = relationship('LanguageSubfamily', back_populates='languages')
    model_types = relationship(
        'ModelType',
        secondary=language_models,
        back_populates='languages'
    )

    def __repr__(self):
        return f"<Language(name='{self.name}', iso_code='{self.iso_code}')>"

class ModelType(Base):
    """Model representing different types of language models."""
    __tablename__ = 'model_types'

    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False, unique=True)
    description = Column(String(255))

    languages = relationship(
        'Language',
        secondary=language_models,
        back_populates='model_types'
    )

    def __repr__(self):
        return f"<ModelType(name='{self.name}')>"
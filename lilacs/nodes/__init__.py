from sqlalchemy.ext.declarative import declarative_base

__author__ = "JarbasAI"


Base = declarative_base()


from sqlalchemy import Column, ForeignKey, Integer, String, Text, Table, UnicodeText, Unicode
from sqlalchemy.orm import relationship, backref


#concept_cons = Table('concept_connections', Base.metadata,
#     Column('concept_id', ForeignKey('concepts.id'), primary_key=True),
#     Column('connections_id', ForeignKey('connections.id'), primary_key=True), extend_existing=True
#)


class Concept(Base):
    __tablename__ = "concepts"
    id = Column(Integer, primary_key=True, nullable=False)
    description = Column(UnicodeText)
    name = Column(UnicodeText)
    type = Column(Unicode, default="label")
    last_seen = Column(Integer, default=0)
    out_connections = relationship("Connection", back_populates="source",
                                   foreign_keys="Connection.source_id", cascade="all, delete-orphan")
    in_connections = relationship("Connection", back_populates="target",
                                  foreign_keys="Connection.target_id", cascade="all, delete-orphan")

    def __repr__(self):
        return self.name + ":" + str(self.id)


class Connection(Base):
    __tablename__ = 'connections'
    id = Column(Integer, primary_key=True, nullable=False)
    last_seen = Column(Integer, default=0)
    strength = Column(Integer, default=50)
    type = Column(Unicode, default="related")
    source_id = Column(Integer, ForeignKey('concepts.id'))
    target_id = Column(Integer, ForeignKey('concepts.id'))
    source = relationship("Concept", back_populates="out_connections", foreign_keys=[source_id])
    target = relationship("Concept", back_populates="in_connections", foreign_keys=[target_id])

    def __repr__(self):
        #return str(self.id) + ": " + str(self.source_id) + "->" + str(self.target_id)
        return self.type + ": " + str(self.source.name) + "->" + str(self.target.name)


def model_to_dict(obj):
    serialized_data = {c.key: getattr(obj, c.key) for c in obj.__table__.columns}
    return serialized_data


def props(cls):
    return [i for i in list(cls.__dict__.keys()) if i[:1] != '_']



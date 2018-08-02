from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError

from lilacs.nodes import Base, Concept, Connection
from lilacs.settings import DATABASE_DIR

from os.path import join


class ConceptDatabase(object):
    path = 'concepts.db'
    path = "sqlite:///" + join(DATABASE_DIR, path)
    db = create_engine(path)
    Base.metadata.create_all(db)

    def __init__(self, debug=False):
        self.db.echo = debug
        Session = sessionmaker(bind=self.db)
        self.session = Session()

    def update_timestamp(self, concept_id, timestamp):
        concept = self.get_concept_by_id(concept_id)
        if concept:
            concept = concept[0]
        else:
            return False
        concept.last_seen = timestamp
        self.commit()
        return True

    def get_concepts(self):
        return self.session.query(Concept).all()

    def get_connections(self):
        return self.session.query(Connection).all()

    def get_connection_by_id(self, connection_id):
        return self.session.query(Connection).get(connection_id)

    def get_concept_by_id(self, concept_id):
        return self.session.query(Concept).get(concept_id)

    def search_connection_by_type(self, type="related"):
        return self.session.query(Connection).filter_by(type=type).all()

    def search_connection_by_concept(self, name):
        return self.session.query(Connection).filter(Concept.name==name).all()

    def search_connection_by_concept_pair(self, source, target):
        source = self.first_concept_by_name(source)
        target = self.first_concept_by_name(target)
        if source and target:
            return self.session.query(Connection).filter(Connection.source_id == source.id).filter(
                Connection.target_id == target.id).all()
        return []

    def search_connection_by_concept_pair_id(self, source, target):
        source = self.get_concept_by_id(source)
        target = self.get_concept_by_id(target)
        if source and target:
            return self.session.query(Connection).filter(Connection.source_id == source.id).filter(
                Connection.target_id == target.id).all()
        return []

    def search_concept_by_type(self, type):
        return self.session.query(Concept).filter_by(type=type).all()

    def first_concept_by_name(self, name):
        return self.session.query(Concept).filter_by(name=name).first()

    def search_concept_by_name(self, name):
        return self.session.query(Concept).filter_by(name=name).all()

    def add_concept(self, name=None, description="", type="idea"):
        c = self.first_concept_by_name(name)
        if not c:
            concept = Concept(name=name, description=description, type=type, id=self.total_concepts() + 1)
            self.session.add(concept)
            if self.commit():
                return concept
        return None

    def add_connection(self, source_name, target_name, type="related", strength=50):
        source = self.first_concept_by_name(source_name)
        if not source:
            source = self.add_concept(source_name)

        connection = Connection(type=type, id=self.total_connections() + 1, strength=strength)

        target = self.first_concept_by_name(target_name)
        if not target:
            target = self.add_concept(target_name)

        if not self.search_connection_by_concept_pair_id(source.id, target.id) and target and source:
            connection.target = target
            connection.source = source

            self.session.add(connection)
            if self.commit():
                return connection
        return None

    def add_connection_by_id(self, source_id, target_name, type="related", strength=50):
        source = self.get_concept_by_id(source_id)
        if not source:
            raise AssertionError("invalid concept id")

        connection = Connection(type=type, id=self.total_connections() + 1, strength=strength)

        target = self.first_concept_by_name(target_name)
        if not target:
            target = self.add_concept(target_name)

        if not self.search_connection_by_concept_pair_id(source.id, target.id):
            connection.target = target
            connection.source = source

            self.session.add(connection)
            if self.commit():
                return connection
        return None

    def total_connections(self):
        return self.session.query(Connection).count()

    def total_concepts(self):
        return self.session.query(Concept).count()

    def commit(self):
        try:
            self.session.commit()
            return True
        except IntegrityError:
            self.session.rollback()
            return False


if __name__ == "__main__":
    d = ConceptDatabase()
    # concept creation
    print(d.add_concept("self"))  # should return concept or None if exists
    # connection + auto concept creation test
    print(d.add_connection("dog", "mammal", "instance of")) # should return con or None if exists
    print(d.add_concept("dog")) # None , created previously
    # concept search test,
    print(d.search_concept_by_name("dog")) # should return list len 1
    print(d.first_concept_by_name("dog"))  # should return concept or None
    print(d.first_concept_by_name("invalid"))  # should return concept or None
    # connection search test
    c = d.search_connection_by_concept("dog")
    print(c) # should return list len 1
    c = d.search_connection_by_concept("invalid")
    print(c)  # should return list len 0

    # connection search test
    c = d.search_connection_by_concept_pair("dog", "invalid")
    print(c)  # should return list len 0

    c = d.search_connection_by_concept_pair("dog", "mammal")
    print(c) # should return list len 1

    # attribute test
    print(c[0].source)  # should return concept object -> dog
    print(c[0].target)  # should return concept object -> mammal
    print(c[0].type)  # should return "instance of"

    c = d.first_concept_by_name("dog") #  dog concept
    print(c.name) # dog
    print(c.out_connections) # list with dog->mammal connection
    print(c.in_connections) # empty list

from uuid import uuid4
from flask_sqlalchemy import BaseQuery
from sqlalchemy.dialects.postgresql import UUID
from . import TimestampedModelMixin, ModelsMixin
from ..db import db
from sqlalchemy import or_
from sqlalchemy.orm import relationship, foreign, aliased


class RegistryOfMarriagesQuery(BaseQuery):

     def get_one(self, _id):
         try:
             return self.filter(RegistryOfMarriages.id == _id).first()
         except Exception as e:
             db.session.rollback()
             return None

     @staticmethod
     def query_details():
        from . import Person, City, ListItem, Document, District, Archdiocese, Note, RegistryOfBaptisms, User
        person2 = aliased(Person)
        mother1 = aliased(Person)
        father1 = aliased(Person)
        mother2 = aliased(Person)
        father2 = aliased(Person)
        best_man = aliased(Person)
        best_man2 = aliased(Person)
        city1 = aliased(City)
        city2 = aliased(City)
        religion1 = aliased(ListItem)
        religion2 = aliased(ListItem)
        parents_canonically_married1 = aliased(ListItem)
        parents_canonically_married2 = aliased(ListItem)
        document_marriage = aliased(Document)
        document_baptism1 = aliased(Document)
        document_baptism2 = aliased(Document)
        registry_of_baptism1 = aliased(RegistryOfBaptisms)
        registry_of_baptism2 = aliased(RegistryOfBaptisms)
        baptism_district1 = aliased(District)
        baptism_district2 = aliased(District)
        return db.session.query(Person, RegistryOfMarriages, person2, mother1, father1,
                                mother2, father2, best_man, best_man2, city1, city2, religion1, religion2,
                                document_marriage, document_baptism1, document_baptism2, registry_of_baptism1,
                                registry_of_baptism2, parents_canonically_married1, parents_canonically_married2,
                                baptism_district1, baptism_district2,
                                District, Archdiocese, Note, User, ListItem) \
            .join(
            Person,
            RegistryOfMarriages.person_id == Person.id,
            isouter=False) \
            .join(person2, RegistryOfMarriages.person2_id == person2.id, isouter=True) \
            .join(best_man, RegistryOfMarriages.best_man == best_man.id, isouter=True) \
            .join(best_man2, RegistryOfMarriages.best_man == best_man2.id, isouter=True) \
            .join(mother1, Person.mother_id == mother1.id, isouter=True) \
            .join(father1, Person.father_id == father1.id, isouter=True) \
            .join(mother2, person2.mother_id == mother2.id, isouter=True) \
            .join(father2, person2.father_id == father2.id, isouter=True) \
            .join(city1, Person.birth_place == city1.id, isouter=False) \
            .join(city2, person2.birth_place == city2.id, isouter=False) \
            .join(religion1, Person.religion == religion1.id, isouter=False) \
            .join(religion2, person2.religion == religion2.id, isouter=False) \
            .join(document_marriage, RegistryOfMarriages.id == document_marriage.id, isouter=True) \
            .join(District, document_marriage.district == District.id, isouter=True) \
            .join(Archdiocese, District.archdiocese_id == Archdiocese.id, isouter=True) \
            .join(User, document_marriage.act_performed == User.id, isouter=True) \
            .join(registry_of_baptism1, Person.id == registry_of_baptism1.person_id, isouter=True) \
            .join(parents_canonically_married1, registry_of_baptism1.parents_canonically_married == parents_canonically_married1.id, isouter=True) \
            .join(document_baptism1, registry_of_baptism1.id == document_baptism1.id, isouter=True) \
            .join(baptism_district1, document_baptism1.id == baptism_district1.id, isouter=True) \
            .join(registry_of_baptism2, person2.id == registry_of_baptism2.person_id, isouter=True) \
            .join(parents_canonically_married2, registry_of_baptism2.parents_canonically_married == parents_canonically_married2.id, isouter=True) \
            .join(document_baptism2, registry_of_baptism2.id == document_baptism2.id, isouter=True) \
            .join(baptism_district2, document_baptism2.id == baptism_district2.id, isouter=True) \
            .join(Note, Note.id == RegistryOfMarriages.id, isouter=True)

     def get_one_details(self, _id):
         try:
             return self.query_details().filter(RegistryOfMarriages.id == _id).first()
         except Exception as e:
             db.session.rollback()
             return None


class RegistryOfMarriages(ModelsMixin, TimestampedModelMixin, db.Model):

    __tablename__ = 'registry_of_marriages'

    query_class = RegistryOfMarriagesQuery

    STATUSES = {
        'active': 1,
        'inactive': 0
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    id = db.Column(UUID(as_uuid=True), default=uuid4, primary_key=True)
    person_id = db.Column(UUID(as_uuid=True),
                                 db.ForeignKey('persons.id'),
                                 nullable=False)
    person2_id = db.Column(UUID(as_uuid=True),
                                 db.ForeignKey('persons.id'),
                                 nullable=False)
    best_man = db.Column(UUID(as_uuid=True),
                                 db.ForeignKey('persons.id'),
                                 nullable=False)
    best_man2 = db.Column(UUID(as_uuid=True),
                                 db.ForeignKey('persons.id'),
                                 nullable=False)
    status = db.Column(
        db.SmallInteger, nullable=False,
        default=STATUSES['active'], server_default=str(STATUSES['active']))




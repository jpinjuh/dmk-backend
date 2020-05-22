from flask import current_app, url_for
from flask_script import Command
from ..controllers.states_controller.controller import StateController
from ..controllers.cities_controller.controller import CityController
from ..controllers.roles_controller.controller import RoleController
from ..controllers.districts_controller.controller import DistrictController
from ..controllers.users_controller.controller import UserController
from ..controllers.permissions_controller.controller import PermissionController
from ..controllers.privileges_controller.controller import PrivilegeController
from ..controllers.archdioceses_controller.controller import ArchdioceseController
from ..controllers.lists_controller.controller import ListController
from ..controllers.listItems_controller.controller import ListItemController
from ..controllers.persons_controller.controller import PersonController
from ..models.states import State, StateQuery
from ..models.cities import City, CityQuery
from ..models.roles import Role
from ..models.districts import District
from ..models.users import User
from ..models.privileges import Privilege
from ..models.permissions import Permission
from ..models.archdioceses import Archdiocese
from ..models.lists import List
from ..models.listItems import ListItem
from ..models.persons import Person
from werkzeug.security import generate_password_hash, check_password_hash
import re


class Seed(Command):
    """Seeds database with fake but realistic data"""

    def run(self):
        current_app.logger.info('Seeding database with test data...')
        controller = StateController(
            state=State(
                name='BiH'
            ))
        controller.create()
        controller = ArchdioceseController(
            archdiocese=Archdiocese(
                name='Mostarsko-duvanjska biskupija'
            ))
        controller.create()
        state = State.query.filter_by(name='BiH').first()
        controller = CityController(
            city=City(
                name='Grude',
                state_id=state.id
            ))
        controller.create()
        city = City.query.filter_by(name='Grude').first()
        archdiocese = Archdiocese.query.filter_by(name='Mostarsko-duvanjska biskupija').first()
        controller = DistrictController(
            district=District(
                name='Gorica-Sovići',
                address='Podkrstina bb',
                city_id=city.id,
                archdiocese_id=archdiocese.id
            ))
        controller.create()
        controller = RoleController(
            role=Role(
                name='admin'
            ))
        controller.create()
        role = Role.query.filter_by(name='admin').first()
        district = District.query.filter_by(name='Gorica-Sovići').first()
        controller = UserController(
            user=User(
                first_name='Anđela',
                last_name='Bošnjak',
                username='andjelabosnjak',
                email='andjela.bosnjak30@gmail.com',
                password_hash=generate_password_hash('123456', method='sha256'),
                roles_id=role.id,
                districts_id=district.id
            ))
        controller.create()
        controller = UserController(
            user=User(
                first_name='Marija',
                last_name='Bošnjak',
                username='marijabosnjak',
                email='marijabosnjak998@gmail.com',
                password_hash=generate_password_hash('123456', method='sha256'),
                roles_id=role.id,
                districts_id=district.id
            ))
        controller.create()

        for rule in current_app.url_map.iter_rules():
            for method in rule.methods:
                if method == 'OPTIONS' or method == 'HEAD':
                    pass
                else:
                    controller = PermissionController(
                        permission=Permission(
                            name=re.sub(
                                '<[^>]+>', "", str(rule.rule[0].replace("/", "") + rule.rule[1:].replace("/", " "))),
                            route=str(rule.rule),
                            method=str(method)

                        ))
                    controller.create()

        permissions = Permission.query.all()
        for permission in permissions:
            if any(path in permission.route for path in ['/permission', '/privilege', '/role', '/user', '/city', '/district', '/state', '/archdiocese']):
                controller = PrivilegeController(
                    privilege=Privilege(
                        roles_id=role.id,
                        permissions_id=permission.id

                    ))
                controller.create()
        controller = ListController(
            list=List(
                name='child'
            ))
        controller.create()
        controller = ListController(
            list=List(
                name='religions'
            ))
        controller.create()
        controller = ListController(
            list=List(
                name='document_types'
            ))
        controller.create()
        controller = ListController(
            list=List(
                name='yes/no list'
            ))
        controller.create()
        list = List.query.filter_by(name='child').first()
        controller = ListItemController(
            list_item=ListItem(
                value='Sin',
                list_id=list.id
            ))
        controller.create()
        controller = ListItemController(
            list_item=ListItem(
                value='Kći',
                list_id=list.id
            ))
        controller.create()
        list = List.query.filter_by(name='religions').first()
        controller = ListItemController(
            list_item=ListItem(
                value='Kršćanstvo',
                list_id=list.id
            ))
        controller.create()
        religion = ListItem.query.filter_by(value='Kršćanstvo').first()
        controller = ListItemController(
            list_item=ListItem(
                value='Islam',
                list_id=list.id
            ))
        controller.create()
        list = List.query.filter_by(name='yes/no list').first()
        controller = ListItemController(
            list_item=ListItem(
                value='Da',
                list_id=list.id
            ))
        controller.create()
        controller = ListItemController(
            list_item=ListItem(
                value='Ne',
                list_id=list.id
            ))
        controller.create()
        list = List.query.filter_by(name='document_types').first()
        controller = ListItemController(
            list_item=ListItem(
                value='Matica krštenih',
                list_id=list.id
            ))
        controller.create()
        controller = ListItemController(
            list_item=ListItem(
                value='Matica vjenčanih',
                list_id=list.id
            ))
        controller.create()
        controller = ListItemController(
            list_item=ListItem(
                value='Matica umrlih',
                list_id=list.id
            ))
        controller.create()
        controller = PersonController(
            person=Person(
                first_name='Mirjana',
                last_name='Bošnjak',
                maiden_name='Marijanović',
                birth_date='17/01/1973',
                identity_number='1701973155631',
                district=district.id,
                religion=religion.id
            ))
        controller.create()
        mother = Person.query.filter_by(identity_number='1701973155631').first()
        controller = PersonController(
            person=Person(
                first_name='Marija',
                last_name='Bošnjak',
                birth_date='25/06/1998',
                identity_number='2506998155631',
                mother_id=mother.id,
                district=district.id,
                religion=religion.id
            ))
        controller.create()
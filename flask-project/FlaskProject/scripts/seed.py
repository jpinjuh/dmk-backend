from flask import current_app, url_for
from flask_script import Command
from ..controllers.states_controller.controller import StateController
from ..controllers.cities_controller.controller import CityController
from ..controllers.roles_controller.controller import RoleController
from ..controllers.districts_controller.controller import DistrictController
from ..controllers.users_controller.controller import UserController
from ..controllers.permissions_controller.controller import PermissionController
from ..controllers.privileges_controller.controller import PrivilegeController
from ..models.states import State, StateQuery
from ..models.cities import City, CityQuery
from ..models.roles import Role
from ..models.districts import District
from ..models.users import User
from ..models.privileges import Privilege
from ..models.permissions import Permission
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
        state = State.query.filter_by(name='BiH').first()
        controller = CityController(
            city=City(
                name='Grude',
                state_id=state.id
            ))
        controller.create()
        city = City.query.filter_by(name='Grude').first()
        controller = DistrictController(
            district=District(
                name='Gorica-Sovići',
                city_id=city.id
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
        """
        controller = PermissionController(
            permission=Permission(
                name='Pregled svih korisnika',
                route='/user',
                method='GET'
            ))
        controller.create()
        controller = PermissionController(
            permission=Permission(
                name='Dodaj novog korisnika',
                route='/user',
                method='POST'
            ))
        controller.create()
        controller = PermissionController(
            permission=Permission(
                name='Uredi korisnika',
                route='/user/<string:user_id>',
                method='PUT'
            ))
        controller.create()
        controller = PermissionController(
            permission=Permission(
                name='Izbriši korisnika',
                route='/user/<string:user_id>',
                method='DELETE'
            ))
        controller.create()
        controller = PermissionController(
            permission=Permission(
                name='Aktiviraj korisnika',
                route='/user/activate',
                method='POST'
            ))
        controller.create()
        controller = PermissionController(
            permission=Permission(
                name='Pregled detalja o korisniku',
                route='/user/<string:user_id>',
                method='GET'
            ))
        controller.create()
        controller = PermissionController(
            permission=Permission(
                name='Autocomplete korisnika',
                route='/user/autocomplete',
                method='POST'
            ))
        controller.create()
        controller = PermissionController(
            permission=Permission(
                name='Dodaj novu rolu',
                route='/role',
                method='POST'
            ))
        controller.create()
        controller = PermissionController(
            permission=Permission(
                name='Uredi rolu',
                route='/role/<string:role_id>',
                method='PUT'
            ))
        controller.create()
        controller = PermissionController(
            permission=Permission(
                name='Izbriši rolu',
                route='/role/<string:role_id>',
                method='DELETE'
            ))
        controller.create()
        controller = PermissionController(
            permission=Permission(
                name='Aktiviraj rolu',
                route='/role/activate',
                method='POST'
            ))
        controller.create()
        controller = PermissionController(
            permission=Permission(
                name='Pregled detalja o roli',
                route='/role/<string:role_id>',
                method='GET'
            ))
        controller.create()
        controller = PermissionController(
            permission=Permission(
                name='Autocomplete role',
                route='/role/autocomplete',
                method='POST'
            ))
        controller.create()
        controller = PermissionController(
            permission=Permission(
                name='Pregled svih rola',
                route='/role',
                method='GET'
            ))
        controller.create()
        permission = Permission.query.filter_by(name='Pregled svih korisnika').first()
        controller = PrivilegeController(
            privilege=Privilege(
                roles_id=role.id,
                permissions_id=permission.id

            ))
        controller.create()
        permission = Permission.query.filter_by(name='Dodaj novog korisnika').first()
        controller = PrivilegeController(
            privilege=Privilege(
                roles_id=role.id,
                permissions_id=permission.id

            ))
        controller.create()
        permission = Permission.query.filter_by(name='Uredi korisnika').first()
        controller = PrivilegeController(
            privilege=Privilege(
                roles_id=role.id,
                permissions_id=permission.id

            ))
        controller.create()
        permission = Permission.query.filter_by(name='Pregled svih rola').first()
        controller = PrivilegeController(
            privilege=Privilege(
                roles_id=role.id,
                permissions_id=permission.id

            ))
        controller.create()
        permission = Permission.query.filter_by(name='Izbriši rolu').first()
        controller = PrivilegeController(
            privilege=Privilege(
                roles_id=role.id,
                permissions_id=permission.id

            ))
        controller.create()
        permission = Permission.query.filter_by(name='Aktiviraj rolu').first()
        controller = PrivilegeController(
            privilege=Privilege(
                roles_id=role.id,
                permissions_id=permission.id

            ))
        controller.create()
"""
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
            if any(path in permission.route for path in ['/permission', '/privilege', '/role', '/user', '/city', '/district', '/state']):
                controller = PrivilegeController(
                    privilege=Privilege(
                        roles_id=role.id,
                        permissions_id=permission.id

                    ))
                controller.create()
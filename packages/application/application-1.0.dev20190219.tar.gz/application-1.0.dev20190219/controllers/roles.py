
from models.roles import Roles
from schemas.roles import RolesSchema, RolesGetSchema
from config import db
from flask_restful import reqparse, abort, Api, Resource


class Getcreateroles(Resource):
    def __init__(self):
        pass
        
     def post(self):
            da = request.get_json()
            print("=======",da)
            name = da['name']
            dit = {key:value for key,value in da.items()}
            existing_role = (Roles.query.filter(Roles.name == name).one_or_none())
            if existing_role is None:
                schema = RolesSchema()
                new_role = schema.load(dit, session=db.session).data
                db.session.add(new_role)
                db.session.commit()
                data = schema.dump(new_role).data
                return data, 201
            else:
                return("Role name exists already")

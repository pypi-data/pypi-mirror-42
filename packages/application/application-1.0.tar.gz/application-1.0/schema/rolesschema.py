from models.roles import Roles
from config import ma,db

class RolesSchema(ma.ModelSchema):
    class Meta:
        model =Roles
        fields = ('id','name')
        sqla_session = db.session

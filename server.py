from flask import Flask, jsonify, request
from flask.views import MethodView

from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app_models import engine, UserModel, AdvModel
from validators import HttpError, CreateUserSchema, PatchUserSchema, CreateAdvSchema, PatchAdvSchema, validate


app = Flask('app')


@app.errorhandler(HttpError)
def error_handler(error: HttpError):
    response = jsonify({"status": "error",
                        "message": error.message
                        })
    response.status_code = error.status_code
    return response


class UserView(MethodView):
    
    def post(self):
        json_data = request.json
        with Session(engine) as session:
            try:
                new_user = UserModel(**validate(json_data, CreateUserSchema))
                session.add(new_user)
                session.commit()
            except IntegrityError:
                raise HttpError(409, 'user already exists')
            return jsonify({'user_id': new_user.id,
                            'name': new_user.name,
                            'rating': new_user.rating,
                            'status': 'added'
                            })
    
    def get(self, user_id: int):
        with Session(engine) as session:
            user = session.query(UserModel).get(user_id)
            if user is None:
                raise HttpError(404, 'no such user')
            return jsonify({'user_id': user.id, 'user': user.name, 'rating': user.rating, 'status': 'exists'})
        
    def delete(self, user_id: int):
        with Session(engine) as session:
            user = session.query(UserModel).get(user_id)
            if user is None:
                raise HttpError(404, 'no such user')
            session.delete(user)
            session.commit()
            return jsonify({'user': user.name, 'status': 'deleted'})
        
    def patch(self, user_id: int):
        patch_data = validate(request.json, PatchUserSchema)
        with Session(engine) as session:
            user = session.query(UserModel).get(user_id)
            for field, value in patch_data.items():
                setattr(user, field, value)
            session.commit()
            return jsonify({'user_id': user.id, 'name': user.name, 'rating': user.rating, 'status': 'patched'})


class AdvView(MethodView):
    
    def post(self):
        json_data = request.json
        with Session(engine) as session:
            try:
                new_adv = AdvModel(**validate(json_data, CreateAdvSchema))
                session.add(new_adv)
                session.commit()
            except IntegrityError:
                raise HttpError(404, 'owner with such owner_id is not exists')
            return jsonify({'adv_id': new_adv.id,
                            'title': new_adv.title,
                            'status': 'added'
                            })
    
    def get(self, adv_id: int):
        with Session(engine) as session:
            adv = session.query(AdvModel).get(adv_id)
            if adv is None:
                raise HttpError(404, 'no such adv')
            return jsonify({'adv_id': adv.id,
                            'title': adv.title,
                            'description': adv.description,
                            'created_at': adv.created_at.isoformat(),
                            'owner': adv.owner.name,
                            'status': 'exists'})
    
    def delete(self, adv_id: int):
        with Session(engine) as session:
            adv = session.query(AdvModel).get(adv_id)
            if adv is None:
                raise HttpError(404, 'no such adv')
            session.delete(adv)
            session.commit()
            return jsonify({'adv': adv.title, 'status': 'deleted'})
    
    def patch(self, adv_id: int):
        patch_data = validate(request.json, PatchAdvSchema)
        with Session(engine) as session:
            adv = session.query(AdvModel).get(adv_id)
            for field, value in patch_data.items():
                setattr(adv, field, value)
            session.commit()
            return jsonify({'adv_id': adv.id, 'title': adv.title, 'status': 'patched'})


app.add_url_rule('/user', view_func=UserView.as_view('add_user'), methods=['POST'])
app.add_url_rule('/user/<int:user_id>', view_func=UserView.as_view('user_info'), methods=['GET', 'DELETE', 'PATCH'])
app.add_url_rule('/adv', view_func=AdvView.as_view('add_adv'), methods=['POST'])
app.add_url_rule('/adv/<int:adv_id>', view_func=AdvView.as_view('adv_info'), methods=['GET', 'DELETE', 'PATCH'])

app.run()

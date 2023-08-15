from flask import request
from flask_login import login_required

from sifa_rehberi import app,db
from model import Bitki, User


@app.route('/api/user', methods=['GET'])
def user_listesi():
    try:
        users = User.query.all()
        return {"code": "ok", "data": [user.simple_dict for user in users]}
    except Exception as ex:
        return {"code": "error", "msg": str(ex)}

@app.route('/api/bitki', methods=['POST'])
@login_required
def bitki_ekle():
    try:
        ad = request.form['ad']
        grup = request.form['grup']
        alt_grup = request.form['alt_grup']
        new_bitki = Bitki(ad=ad, grup=grup, alt_grup=alt_grup)
        db.session.add(new_bitki)
        db.session.commit()
        return {"code": "ok"}
    except Exception as ex:
        return {"code": "error", "msg": str(ex)}


@app.route('/api/bitki', methods=['GET'])
@login_required
def bitki_listesi():
    try:
        bitkiler = Bitki.query.all()
        return {"code": "ok", "data": bitkiler}
    except Exception as ex:
        return {"code": "error", "msg": str(ex)}


@app.route('/api/bitki/<bitki_id>', methods=['GET'])
@login_required
def get_bitki(bitki_id):
    try:
        bitki = Bitki.query.get(bitki_id)
        if not bitki:
            return {"code":"error","msg":"Incorrect Bitki Id"},
        return {"code": "ok", "data": bitki}
    except Exception as ex:
        return {"code": "error", "msg": str(ex)}

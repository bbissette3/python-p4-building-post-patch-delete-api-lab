#!/usr/bin/env python3

from flask import Flask, request, make_response, jsonify
from flask_migrate import Migrate

from models import db, Bakery, BakedGood

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def home():
    return '<h1>Bakery GET-POST-PATCH-DELETE API</h1>'

@app.route('/bakeries')
def bakeries():
    bakeries = [bakery.to_dict() for bakery in Bakery.query.all()]
    return make_response(bakeries, 200)

@app.route('/bakeries/<int:id>', methods=['GET', 'PATCH'])
def bakery_by_id(id):
    bakery = Bakery.query.filter_by(id=id).first()

    if request.method == 'GET':
        return make_response(bakery.to_dict(), 200)
    
    elif request.method == 'PATCH':
        for attr in request.form:
            setattr(bakery, attr, request.form.get(attr))

        db.session.add(bakery)
        db.session.commit()

        return make_response(bakery.to_dict(), 200)

@app.route('/baked_goods', methods=['GET', 'POST'])
def baked_goods():

    if request.method == 'GET':

        baked_goods = [bakery.to_dict() for bakery in BakedGood.query.all()]
        return make_response(baked_goods, 200)
    
    elif request.method == 'POST':

        new_baked_good = BakedGood(
            name = request.form.get("name"),
            price = request.form.get("price"),
            bakery_id = request.form.get("bakery_id")
        )
        
        db.session.add(new_baked_good)
        db.session.commit()

        return make_response(new_baked_good.to_dict(), 201)
    
@app.route('/baked_goods/<int:id>', methods=['GET', 'DELETE'])
def baked_good_by_id(id):
    baked_good = BakedGood.query.filter_by(id=id).first()

    if request.method == 'GET':
        return make_response(baked_good.to_dict(), 200)
    
    elif request.method == 'DELETE':
        db.session.delete(baked_good)
        db.session.commit()

        response_body = {
            "delete_sucessful": True,
            "message": "Review deleted."
        }

        return make_response(response_body, 200)


@app.route('/baked_goods/by_price')
def baked_goods_by_price():
    baked_goods_by_price = [bakery.to_dict() for bakery in BakedGood.query.order_by(BakedGood.price).all()]
    return make_response(baked_goods_by_price,200)


@app.route('/baked_goods/most_expensive')
def most_expensive_baked_good():
    most_expensive_baked_good = BakedGood.query.order_by(BakedGood.price.desc()).first().to_dict()
    return make_response(most_expensive_baked_good, 200)

if __name__ == '__main__':
    app.run(port=5555, debug=True)

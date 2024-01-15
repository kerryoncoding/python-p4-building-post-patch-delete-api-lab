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
    return make_response(  bakeries,   200  )

@app.route('/bakeries/<int:id>', methods = ['GET', 'PATCH'])
def bakery_by_id(id):
    bakery = Bakery.query.filter_by(id=id).first()
    if request.method == 'GET':
        # bakery = Bakery.query.filter_by(id=id).first()
        bakery_serialized = bakery.to_dict()
        return make_response ( bakery_serialized, 200 )

# Define a PATCH block inside of the /bakeries/<int:id> route that updates the name of the bakery in the database and returns its data as JSON. As with the previous POST block, the request will send data in a form. The form does not need to include values for all of the bakery's attributes.
    elif request.method == 'PATCH':
        for attr in request.form:
            setattr(bakery, attr, request.form.get(attr))
        db.session.add(bakery)
        db.session.commit()
        
        bakery_dict = bakery.to_dict()

        response = make_response(
            bakery_dict,
            200
        )
        return response
    


@app.route('/baked_goods/by_price')
def baked_goods_by_price():
    baked_goods_by_price = BakedGood.query.order_by(BakedGood.price.desc()).all()
    baked_goods_by_price_serialized = [
        bg.to_dict() for bg in baked_goods_by_price
    ]
    return make_response( baked_goods_by_price_serialized, 200  )
   

@app.route('/baked_goods/most_expensive')
def most_expensive_baked_good():
    most_expensive = BakedGood.query.order_by(BakedGood.price.desc()).limit(1).first()
    most_expensive_serialized = most_expensive.to_dict()
    return make_response( most_expensive_serialized,   200  )

# Define a POST block inside of a /baked_goods route that creates a new baked good in the database and returns its data as JSON. The request will send data in a form.
@app.route('/baked_goods', methods=['POST'])
def post():
    if request.method == 'POST':
        new_baked_good =  BakedGood(
            id= request.form.get('id'),
            name= request.form.get('name'),
            price = request.form.get('price'),
            created_at= request.form.get('created_at'),
            updated_at= request.form.get('updated_at'),
            bakery_id= request.form.get('bakery_id')
        )
        db.session.add(new_baked_good)
        db.session.commit()

        response_dict = new_baked_good.to_dict()
        response = make_response(
            response_dict,
            201
        )

        return response
    
# Define a DELETE block inside of a /baked_goods/<int:id> route that deletes the baked good from the database and returns a JSON message confirming that the record was successfully deleted.
@app.route('/baked_goods/<int:id>', methods = ['DELETE'])
def delete(id):
    bakery = BakedGood.query.filter(BakedGood.id==id).first()
    if request.method== 'DELETE':
        db.session.delete(bakery)
        db.session.commit()

        response_body = {
            "delete_successful": True,
            "message": "bakery Deleted."
        }

        response = make_response(
            response_body,
            200
        )

        return response

    

if __name__ == '__main__':
    app.run(port=5555, debug=True)
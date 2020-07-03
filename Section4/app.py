from flask import Flask,request
from flask_restful import Resource, Api, reqparse
from flask_jwt import JWT,jwt_required
from security import authenticate,identity

app = Flask(__name__)
api = Api(app)
app.secret_key = 'jose'
jwt = JWT(app,authenticate,identity) 

items = [
    {
        "name":"bag",
        "price":24
    }
]

class Item(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument("price",
        type=float,
        required=True,
        help="This field cannot be left blank!"
    )
    
    
    @jwt_required()
    def get(self,name):
        data=next(filter(lambda x: x["name"]==name,items),None)
        
        return data,200 if data is not None else 404
    def post(self,name):
        
        if next(filter(lambda x: x["name"]==name,items),None):
            return {"message":f"The item with name {name} alredy exists"},400
        data = Item.parser.parse_args()
        print(data["price"])
        item = {"name":name,"price":data["price"]}
        items.append(item)
        return item,201
    @jwt_required()
    def delete(self, name):
        global items
        items = list(filter(lambda x: x['name'] != name, items))
        return {'message': 'Item deleted'}
    def put(self,name):
#         data = request.get_json(force = True)
        data = Item.parser.parse_args()
        item = next(filter(lambda x: x["name"]==name,items),None)
        if item is None:
            item = {"name":name,"price":data["price"]}
            items.append(item)
        else:
            item.update(data)
        return item
            
    
class ItemList(Resource):
    
    def get(self):
        return {"item":items}
    def post(self):
        data = request.get_json(force = True)
        item = {"name":data["name"],"price":data["price"]}
        items.append(item)
        return item
#     def delete(self,name):
#         global items
#         items = list(filter(lambda x: x['name'] != name,items))
#         return {'message':"item deleted"}
    
    
api.add_resource(Item,"/item/<string:name>")
api.add_resource(ItemList,"/items")

app.run(port=1100,debug = True)
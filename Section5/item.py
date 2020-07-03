import sqlite3
from flask_restful import reqparse,Resource
from flask_jwt import jwt_required


class Item(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument("price",
        type=float,
        required=True,
        help="This field cannot be left blank!"
    )
    
    @classmethod
    def find_by_name(cls, name):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM items WHERE name=?"
        result = cursor.execute(query, (name,))
        row = result.fetchone()
        connection.close()

        if row:
            return {'item': {'name': row[0], 'price': row[1]}}

    @jwt_required()
    def get(self, name):
        item = self.find_by_name(name)
        if item:
            return item
        return {'message': 'Item not found'}, 404

    @classmethod
    def insert(cls,item):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "INSERT INTO items VALUES(?,?)"

        cursor.execute(query,(item["name"],item["price"]))

        connection.commit()
        connection.close()


    def post(self,name):
        row = Item.find_by_name(name)
        if row:
            return {"message":f"The item with name {name} alredy exists"},400
        data = Item.parser.parse_args()
        item = {"name":name,"price":data["price"]}
        
        try:
            Item.insert(item)
        except:
            return {"message":"An Error occured during inserting an item"},500
        return item,201
        
    @jwt_required()
    def delete(self, name):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "DELETE FROM items WHERE name=?"
        cursor.execute(query, (name,))

        connection.commit()
        connection.close()

        return {'message': 'Item deleted'}

    @classmethod
    def update(cls,item):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "UPDATE items SET price=? WHERE name=?"
        cursor.execute(query, (item["price"],item["name"]))

        connection.commit()
        connection.close()

        

    def put(self,name):
        data = Item.parser.parse_args()
        item = Item.find_by_name(name)
        updated_item = {"name":name,"price":data["price"]}
        
        if item is None:
            try:
                self.insert(updated_item)
            except:
                return {"message":"An Error occured during inserting an item"},500
        else:
            try:
                self.update(updated_item)
            except:
                return {"message":"An Error occured during inserting an item"},500
        return updated_item
            
    
class ItemList(Resource):


    @classmethod
    def return_items(cls,):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM items"
        item_list = []
        for row in cursor.execute(query):
            item_list.append({'name': row[0], 'price': row[1]})
        connection.close()

        return item_list

    def get(self):
        item_list = ItemList.return_items()
        return item_list

from flask import Flask,jsonify,request

app = Flask(__name__)

@app.route('/')
def home():
    return render_template("index.html")

# app.run()

stores = [
    {
    "name":"My Camy Store",
    "items":[
        {
            "name":"handbag",
            "price":200
        },
        {
            "name":"bag",
            "price":100
        }
    ]
    }
]


@app.route('/store',methods = ['POST'])
def build_store():
    request_data = request.get_json()
    new_store = {
        "name": request_data["name"],
        "items":[]
    }
    stores.append(new_store)
    return jsonify(new_store)
    

@app.route("/store/<string:name>")
def get_store_details(name):
    for i in stores:
        if(i["name"]==name):
            return jsonify(i)
    return jsonify({"message":"store not found"})

@app.route("/store")
def get_store():
    return jsonify({"stores":stores})

@app.route("/store/<string:name>/item",methods=["POST"])
def create_store_item(name):
    request_data = request.get_json()
    for i in stores:
        if(i["name"]==name):
            new_item = {
                "name":request_data["name"],
                "price":request_data["price"]
            }
            i["items"].append(new_item)
            return jsonify(new_item)
    return jsonify({"message":"store name don't exist"})

@app.route("/store/<string:name>/item")
def item(name):
    for i in stores:
        if(i["name"]==name):
            return jsonify({"item":i["items"]})
    return jsonify({"message":"some error found"})

@app.route("/store/<string:name>/item/<string:item>")
def get_item_price(name,item):
    for i in stores:
        if(i["name"]==name):
            for j in i["items"]:
                if j["name"]==item:
                    return jsonify(j)
            return jsonify({"message":"item not found"})
    return jsonify({"message":"store not found"})

app.run()

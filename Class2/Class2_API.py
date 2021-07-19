import flask
import pymongo
from flask import jsonify, request
from pymongo import results
from pymongo.message import query

conn = pymongo.MongoClient(host = '127.0.0.1', port = 27017)
db = conn['DataBase1']
newsdata = db['NewData']

app = flask.Flask(__name__)
app.config["DEBUG"] = True
app.config['JSON_AS_ASCII'] = False

#【男生可承租】且【位於新北】的租屋物件
@app.route('/rentApi/api1', methods=['GET'])
def api1():

    output = []
    for x in newsdata.find({ 'renterGender': { '$ne' : '女' }, 'area': '新北' }):
        output.append({"title": x['title'], "area": x['area'], "section": x['section'], "houseKind": x['houseKind']
        , "houseType'": x['houseType'], "mobile": x['mobile'], "price": x['price'], "renterGender": x['renterGender'] })

    return jsonify({'result' : output})

#以【聯絡電話】查詢租屋物件 , ex:http://127.0.0.1:5000/rentApi/api2?t=02-25569017
@app.route('/rentApi/api2', methods=['GET'])
def api2():

    query = ''
    if 't' in request.args:
        tel = request.args['t']
        query = {"$or":[{'mobile': tel}, {'phone': tel}]}

    output = []    
    for x in newsdata.find(query):
        output.append({"title": x['title'], "area": x['area'], "section": x['section'], "houseKind": x['houseKind']
        , "houseType'": x['houseType'], "mobile": x['mobile'], "phone": x['phone'], "price": x['price'], "lessor": x['lessor'], "lessor": x['lessor'] })

    return jsonify({'result' : output})

#所有【非屋主自行刊登】的租屋物件
@app.route('/rentApi/api3', methods=['GET'])
def api3():

    output = []
    for x in newsdata.find({ 'lessorRole': { '$ne' : '屋主' } }):
        output.append({"title": x['title'], "area": x['area'], "section": x['section'], "houseKind": x['houseKind']
        , "houseType'": x['houseType'], "mobile": x['mobile'], "price": x['price'], "lessor": x['lessor'] })

    return jsonify({'result' : output})

#【臺北】【屋主為女性】【姓氏為吳】所刊登的所有租屋物件
@app.route('/rentApi/api4', methods=['GET'])
def api4():

    output = []
    for x in newsdata.find({ 'area': '台北', 'lessorGender': '女', 'lessorLastname': '吳' }):
        output.append({"title": x['title'], "area": x['area'], "section": x['section'], "houseKind": x['houseKind']
        , "houseType'": x['houseType'], "mobile": x['mobile'], "price": x['price'], "lessor": x['lessor'], "renterGender": x['renterGender'], "lessorLastname": x['lessorLastname'] })

    return jsonify({'result' : output})

app.run()

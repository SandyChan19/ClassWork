import flask
import pymongo
from flask import jsonify, request
from pymongo import results
from pymongo.message import query
from flasgger import Swagger


conn = pymongo.MongoClient(host = '127.0.0.1', port = 27017)
db = conn['DataBase1']
newsdata = db['NewData']

app = flask.Flask(__name__)
app.config["DEBUG"] = True
app.config['JSON_AS_ASCII'] = False
app.config['SWAGGER'] = {
    "title": "Class API",
    "description": "Class API",
    "version": "1.0.0",
    "termsOfService": "",
    "hide_top_bar": True
}
Swagger(app)

#http://127.0.0.1:5000/apidocs/index.html 
#【男生可承租】且【位於新北】的租屋物件
@app.route('/rentApi/api1', methods=['GET'])
def api1():

    """
    This is the class API
    ---
    tags:
      - API-1
    produces: application/json,
    parameters:
      - name: sex
        in: query
        type: string
        required: true
        description: ex:男
      - name: area
        in: query
        type: string
        required: true
        description: ex:台北
    responses:
      490:
        description: Data not found!
      200:
        description: Rent Houst Data
        schema:
          id: API1-Response
          properties:
            result:
              type: array
              description: The list
              items:
                type: object
                properties:
                  title:
                    type: string
                    description: House title
                    default: 中山區1樓精美樓中樓
                  area:
                    type: string
                    description: Area
                    default: 台北
                  section:
                    type: string
                    description: Section
                    default: 中山區
                  houseKind:
                    type: string
                    description: House kind
                    default: 獨立套房
                  houseType:
                    type: string
                    description: House type
                    default: 公寓
                  mobile:
                    type: string
                    description: Mobile or phone number
                    default: 09xx-xxx-xxx
                  price:
                    type: string
                    description: House rent
                    default: 30000
                  renterGender:
                    type: string
                    description: Renter gender
                    default: 男                   
                  lessor:
                    type: string
                    description: Lessor
                    default: 張先生    

    """ 

    sex = ''
    area = ''
    if 'sex' in request.args:
        query_sex = request.args['sex']
        common_sex = {'男':'女', '女':'男'}
        sex = common_sex.get(query_sex)
    
    if 'area' in request.args:
        area = request.args['area']

    output = []
    for x in newsdata.find({ 'renterGender': { '$ne' : sex }, 'area': area }):
        output.append({"title": x['title'], "area": x['area'], "section": x['section'], "houseKind": x['houseKind']
        , "houseType'": x['houseType'], "mobile": x['mobile'], "price": x['price'], "renterGender": x['renterGender']
        , "lessor": x['lessor'] })

    return jsonify({'result' : output})

#以【聯絡電話】查詢租屋物件 , ex:http://127.0.0.1:5000/rentApi/api2/02-25569017
@app.route('/rentApi/api2/<string:phone_number>', methods=['GET'])
def api2(phone_number):
    """
    This is the class API
    ---
    tags:
      - API-2
    produces: application/json,
    parameters:
      - name: phone_number
        in: path
        type: string
        required: true
        description: ex:09xx-xxx-xxx
    responses:
      490:
        description: Data not found!
      200:
        description: Rent Houst Data
        schema:
          id: API2-Response
          properties:
            result:
              type: array
              description: The list
              items:
                type: object
                properties:
                  title:
                    type: string
                    description: House title
                    default: 中山區1樓精美樓中樓
                  area:
                    type: string
                    description: Area
                    default: 台北
                  section:
                    type: string
                    description: Section
                    default: 中山區
                  houseKind:
                    type: string
                    description: House kind
                    default: 獨立套房
                  houseType:
                    type: string
                    description: House type
                    default: 公寓
                  mobile:
                    type: string
                    description: Mobile or phone number
                    default: 09xx-xxx-xxx
                  price:
                    type: string
                    description: House rent
                    default: 30000
                  lessor:
                    type: string
                    description: Lessor
                    default: 張先生       

    """ 
    query = {"$or":[{'mobile' : phone_number}, {'phone' : phone_number}]}

    output = []
    for x in newsdata.find(query):
        output.append({"title": x['title'], "area": x['area'], "section": x['section'], "houseKind": x['houseKind']
        , "houseType'": x['houseType'], "mobile": x['mobile'], "price": x['price'], "lessor": x['lessor'] })

    return jsonify({'result' : output})

#所有【非屋主自行刊登】的租屋物件
@app.route('/rentApi/api3', methods=['GET'])
def api3():
    """
    This is the class API
    ---
    tags:
      - API-3
    produces: application/json,
    parameters:
      - name: isLessor
        in: path
        type: bool
        required: true
        description: ex:true
    responses:
      490:
        description: Data not found!
      200:
        description: Rent Houst Data
        schema:
          id: API3-Response
          properties:
            result:
              type: array
              description: The list
              items:
                type: object
                properties:
                  title:
                    type: string
                    description: House title
                    default: 中山區1樓精美樓中樓
                  area:
                    type: string
                    description: Area
                    default: 台北
                  section:
                    type: string
                    description: Section
                    default: 中山區
                  houseKind:
                    type: string
                    description: House kind
                    default: 獨立套房
                  houseType:
                    type: string
                    description: House type
                    default: 公寓
                  mobile:
                    type: string
                    description: Mobile or phone number
                    default: 09xx-xxx-xxx
                  price:
                    type: string
                    description: House rent
                    default: 30000
                  lessor:
                    type: string
                    description: Lessor
                    default: 張先生       

    """ 

    output = []
    for x in newsdata.find({ 'lessorRole': { '$ne' : '屋主' } }):
        output.append({"title": x['title'], "area": x['area'], "section": x['section'], "houseKind": x['houseKind']
        , "houseType'": x['houseType'], "mobile": x['mobile'], "price": x['price'], "lessor": x['lessor'] })

    return jsonify({'result' : output})

#【臺北】【屋主為女性】【姓氏為吳】所刊登的所有租屋物件
@app.route('/rentApi/api4', methods=['GET'])
def api4():
    """
    This is the class API
    ---
    tags:
      - API-4
    produces: application/json,
    parameters:
      - name: lessor_gender
        in: path
        type: string
        required: true
        description: ex:男
      - name: area
        in: path
        type: string
        required: true
        description: ex:台北
      - name: lessor_lastname
        in: path
        type: string
        required: true
        description: ex:吳
    responses:
      490:
        description: Data not found!
      200:
        description: Rent Houst Data
        schema:
          id: API4-Response
          properties:
            result:
              type: array
              description: The list
              items:
                type: object
                properties:
                  title:
                    type: string
                    description: House title
                    default: 中山區1樓精美樓中樓
                  area:
                    type: string
                    description: Area
                    default: 台北
                  section:
                    type: string
                    description: Section
                    default: 中山區
                  houseKind:
                    type: string
                    description: House kind
                    default: 獨立套房
                  houseType:
                    type: string
                    description: House type
                    default: 公寓
                  mobile:
                    type: string
                    description: Mobile or phone number
                    default: 09xx-xxx-xxx
                  price:
                    type: string
                    description: House rent
                    default: 30000
                  lessor:
                    type: string
                    description: Lessor
                    default: 張先生
                  lessorGender:
                    type: string
                    description: Lessor gender
                    default: 男       

    """ 

    output = []
    for x in newsdata.find({ 'area': '台北', 'lessorGender': '女', 'lessorLastname': '吳' }):
        output.append({"title": x['title'], "area": x['area'], "section": x['section'], "houseKind": x['houseKind']
        , "houseType'": x['houseType'], "mobile": x['mobile'], "price": x['price'], "lessor": x['lessor'], "lessorGender": x['lessorGender'], "lessorLastname": x['lessorLastname'] })

    return jsonify({'result' : output})

app.run()

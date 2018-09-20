import requests
import time
from flask import Flask
from pymongo import MongoClient
from flask_restplus import Resource, Api,reqparse
from bson.objectid import ObjectId

app = Flask(__name__)
api = Api(app)


@api.route('/collections/<string:indicator>')
class worldbank1(Resource):
    @api.response(200, 'OK')
    @api.response(201, 'Created')
    @api.response(400, 'input indicator id doesn\'t exist ')
    def post(self, indicator):
        #check whether the indicator exist in the Mongodb,if exist return 200
        x = [db.records.find_one({'indicator': indicator})]
        if x[0] != None:
            return {
                    "location" : "/<collections>/{}".format(x[0]['_id'].__str__()),
                     "collection_id" : x[0]['_id'].__str__(),
                     "creation_time":  x[0]["creation_time"],
                     "indicator" : indicator
                    },200
        #there are two page that we need to upload
        url1 = 'http://api.worldbank.org/v2/countries/all/indicators/{}?date=2012:2017&format=json'.format(indicator)
        url2 = 'http://api.worldbank.org/v2/countries/all/indicators/{}?date=2012:2017&format=json&page=2'.format(indicator)
        wb_data1 = requests.get(url1)
        wb_data2 = requests.get(url2)
        data1 = wb_data1.json()
        data2 = wb_data2.json()
        #check whether the indicator is the exist or not, exist keep going otherwise return 400
        if 'message' in data1[0] or 'message' in data2[0]:
            return {'message':'indicator id doesn\'t exist in the data source'}, 400

        user_record = db.records
        create_time = time.asctime(time.localtime(time.time()))
        record = {
            "collection_id": '_id',
            "indicator": indicator,
            "indicator_value": "GDP (current US$)",
            "creation_time": create_time,
            "entries": []}
        #iterating all the data and create the require format which in the discription
        for i in data1[1]:
            x = {"country": i['country']['value'], "date": i['date'], "value": i['value']}
            record["entries"].append(x)
        for i in data2[1]:
            x = {"country": i['country']['value'], "date": i['date'], "value": i['value']}
            record["entries"].append(x)
        #insert data to the Mongodb
        user_record.insert_one(record)
        x = [db.records.find_one({'creation_time': create_time})]
        #change the ObjectId to the string
        id = x[0]['_id'].__str__()
        return  { "location" : "/<collections>/{}".format(id),
                  "collection_id" : id,
                  "creation_time": create_time,
                  "indicator" : indicator
                  },201

@api.route('/collections/<string:collection_id>')
@api.response(200, 'OK')
class worldbank24(Resource):
    def delete(self, collection_id):
        #check wether the collection_id is existing in the database
        b = [db.records.find_one({'_id':  ObjectId(collection_id)})]
        if not b[0]:
            return {
                "message" :"Collection = {} is not exist in the database".format(collection_id)
               },200
        #if exist return message below
        db.records.delete_one({ "_id": ObjectId(collection_id)})
        return {
                "message" :"Collection = {} is removed from the database!".format(collection_id)
               },200

    def get(self,collection_id):
        try:
            x = [db.records.find_one({'_id': ObjectId(collection_id)})]
            x[0]['collection_id'] = x[0]['_id'].__str__()
            x[0].pop('_id')
            return x, 200
        except:
            return {
                "message" :"Collection = {} is not exist in the database".format(collection_id)
               },200



@api.route('/collections/')
@api.response(200, 'OK')
class worldbank3(Resource):
    def get(self):
        d = [doc for doc in db.records.find()]
        if not d:
            return {'message':'database is empty'},200
        lis =[]
        for i in d:
            segment = {
                "location": "/<collections>/{}".format(i["_id"].__str__()),
                "collection_id": i["_id"].__str__(),
                "creation_time": i['creation_time'],
                "indicator": i['indicator']
            }
            lis.append(segment)
        return lis, 200



@api.route('/collections/<string:collection_id>/<string:year>/<string:country>')
@api.response(200, 'OK')
class worldbank5(Resource):
    def get(self,collection_id,year,country):
        x = [db.records.find_one({'_id': ObjectId(collection_id)})]
        for i in x[0]['entries']:
            if i['country'] == country and i['date'] == year:
                return {
                    "collection_id": x[0]['_id'].__str__(),
                    "indicator": x[0]['indicator'],
                    "country": i['country'],
                    "year": i['date'],
                    "value": i['value']
                },200

#this route need to test in the browser by inputing
# eg: http://127.0.0.1:5000/collections/<collections_id>/2015?q=top20 in the Address Bar
parser = reqparse.RequestParser()
parser.add_argument('q')
@api.route('/collections/<string:collection_id>/<string:year>')
@api.response(200, 'OK')
@api.response(200, 'OK')
@api.response(400, 'quary format is not correct')
class worldbank6(Resource):
    def get(self, collection_id, year):
        # get quary as JSON string
        args = parser.parse_args()
        # retrieve the query parameters
        q = args.get('q')
        flag = False
        cut = 3
        if q[:3] == 'top' or q[:4] == 'down':
            if q[0] != 't':
                flag = True
                cut = 4
            try:
                x = [db.records.find_one({'_id': ObjectId(collection_id)})]
                buff = sorted(x[0]['entries'], key=lambda k: k['value'], reverse=flag)
                lis = []
                a = 1
                for i in range(len(buff)):
                    if a <= int(q[cut:]) and buff[i]['date'] == year:
                        lis.append(buff[i])
                        a += 1
                if q[0] == 'd':
                    lis = sorted(lis,key=lambda k:k['value'])
                segment = {
                    "indicator": x[0]['indicator'],
                    "indicator_value": x[0]['indicator_value'],
                    "entries": lis
                }
                return segment,200
            except:
                return{ "message" :"Collection = {} is not exist in the database".format(collection_id)},404
        return {"message": "quary format {} is not correct".format(q)}, 400


if __name__ == '__main__':
    conn = MongoClient('mongodb://us579:123456a@ds115472.mlab.com:15472/us579')
    db = conn.get_database("us579")
    app.run(debug=True)

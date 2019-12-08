import json
import pymongo
import datetime


class MongoHandler(object):

    def __init__(self):
        self.conf = json.load(open('mongoDB.conf', 'r'))  # config file
        self.client = pymongo.MongoClient(self.conf['MONGODB_URI'])
        self.db = self.client[self.conf['MONGODB_DATABASE']]
        self.collection = self.db[self.conf['MONGODB_COLLECTION']]

    def fetch_sensor_name_and_id(self):
        name_and_id = []
        cursor = self.collection.find({}, {'name': 1})  # data cursor, giving location its looking in; need to run loop
        for x in cursor:
            name_and_id.append({'label': x['name'], 'value': x['name']})  # label value is for dash (dropdown menu)
        return name_and_id

    def fetch_sensor_data(self, name, start_date=None, end_date=None):
        cursor = self.collection.find({'name': name})
        docs = [x for x in cursor]
        plot_data = []
        for doc in docs:
            label = doc['name']
            data = doc[label]
            timestamp = doc['timestamp']
            times = [datetime.datetime.strptime(x, '%c') for x in timestamp]
            time_in_range = [True for time in times]
            for i, time in enumerate(times):
                if start_date is not None and time < start_date:
                    time_in_range[i] = False
                if end_date is not None and time > end_date:
                    time_in_range[i] = False
            valid_times = [t for i, t in enumerate(times) if time_in_range[i]]
            valid_data = [d for i, d in enumerate(data) if time_in_range[i]]
            plot_data.append({'x': valid_times, 'y': valid_data, 'name': label})  # for plotly
        return plot_data

    def upload(self, docs):
        self.collection.insert_many(docs)

from rest_framework.views import APIView, Response
import datetime
import os
from dateutil import parser
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
import json
# Create your views here.
from os import path
import sys
sys.path.append(path.abspath('../group1/helpers'))
from database_manager import Manager
from arguments_manager import manage_arguments
sys.path.append(path.abspath('../group1'))
from container import Container

db_manager = Manager()
manager = Container()


from  bson.json_util import dumps

def generate_params_block_model():
    return ['mineral_deposit', 'headers', 'data_map', 'block_model']

def generate_params_blocks():

    return ['mineral_deposit', 'block_model', 'file_block_model', 'units']

def generate_params_metrics():

    return ['mineral_deposit', 'block_model', 'metric_wanted', 'coordinates']

class InsertBlockModel(APIView):
    queryset = ''
    def post(self, request):
        params = generate_params_block_model()
        values_params = {}
        for instance in params:
            value = request.data.get(instance)
            if instance == 'data_map' and value is not None:
               json_acceptable_string = value.replace("'", "\"")
               value = json.loads(json_acceptable_string)
            if instance =='headers' and value is not None:
                value = value.split(',')

            if instance == 'units' and value is not None:
               json_acceptable_string = value.replace("'", "\"")
               value = json.loads(json_acceptable_string)
            values_params[instance] = value
        if None not in values_params.values():
            db_manager.insert_new_block_model_with_name(values_params["mineral_deposit"], values_params["headers"] ,values_params["data_map"], values_params["block_model"] )

        return Response(values_params)


class InsertBlocks(APIView):
    queryset = ''
    def post(self, request):
        params = generate_params_blocks()
        values_params = {}

        for instance in params:
            value = request.data.get(instance)
            if instance == 'units' and value is not None:
               json_acceptable_string = value.replace("'", "\"")
               value = json.loads(json_acceptable_string)
            if instance == 'file_block_model' and value is not None:
               json_acceptable_string = value.replace("'", "\"")
               value = json.loads(json_acceptable_string)

            values_params[instance] = value
        if None not in values_params.values():
            db_manager.insert_blocks_from_url(values_params['mineral_deposit'],values_params['block_model'], values_params['file_block_model'], values_params['units'])

        return Response(True)


class GetMetrics(APIView):
    queryset = ''
    def post(self, request):
        params = generate_params_metrics()
        values_params = {}

        for instance in params:
            value = request.data.get(instance)
            if instance == 'metric_wanted' and value is not None:
                try:
                    value = int(value)
                except:
                    value = value
            elif instance == 'coordinates' and value is not None:
                value = tuple(map(int,value.split(',')))
            values_params[instance] = value

        if values_params['mineral_deposit'] is not None and values_params['block_model'] is not None:
            mineral_deposit = db_manager.fetch_mineral_deposit(values_params['mineral_deposit'])
            manager.set_mineral_deposit(mineral_deposit)
            if values_params['block_model']:
                block_model = db_manager.fetch_block_model(values_params['mineral_deposit'], values_params['block_model'])
                blocks = db_manager.get_all_blocks_from_block_model(values_params['mineral_deposit'], values_params['block_model'])
                manager.set_block_model(block_model, blocks)
            response_metric = manager.generate_action(values_params['metric_wanted'], values_params['coordinates'])
            values_params['response_metric'] = response_metric
        return Response(values_params)


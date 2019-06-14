from rest_framework.views import APIView, Response
import datetime
import os
from dateutil import parser
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
import json
from bson.json_util import dumps, loads
# Create your views here.
from os import path
import sys
sys.path.append(path.abspath('../group1/helpers'))
from database_manager import Manager
sys.path.append(path.abspath('../group1'))
from container import Container

db_manager = Manager()
manager = Container()


from  bson.json_util import dumps


def generate_params_block_model():
    return ['mineral_deposit', 'headers', 'data_map', 'block_model', 'file_block_model', 'units']

def generate_params_blocks():

    return ['mineral_deposit', 'block_model', 'file_block_model', 'units']

def generate_params_metrics():

    return ['mineral_deposit', 'block_model', 'metric_wanted', 'coordinates']

class DataMap(APIView):
    def get(self, request, id=-1):
        block_model = db_manager.fetch_block_model_from_id(id)
        response = {
            "data_map": block_model["data_map"]
        }
        return Response(response)

class MineralDeposit(APIView):
    def get(self,request,id=-1):
        if id == -1:
            cursor_all_minerals_deposit = db_manager.fetch_all_mineral_deposit()
            response = { "mineral_deposits": []}
            for mineral_deposit in cursor_all_minerals_deposit:
                mineral_deposit_hash={}
                id_mineral =  mineral_deposit.get('_id')
                name = mineral_deposit.get('name')
                mineral_deposit_hash['id'] = str(id_mineral)
                mineral_deposit_hash['name'] = name
                response["mineral_deposits"].append(mineral_deposit_hash)
        else:
            response = {}
            cursor_mineral_deposit_block_models = db_manager.fetch_mineral_deposit_by_id(id)
            list_block_models = []
            for block_model in cursor_mineral_deposit_block_models['block_models']:
                block_model_hash={}
                id_block_model =  block_model.get('_id')
                block_model_hash['id'] = str(id_block_model)
                block_model_hash['name'] = str(block_model.get('name'))
                list_block_models.append(block_model_hash)
            body = dict(cursor_mineral_deposit_block_models)
            body['block_models'] = list_block_models
            response['mineral_deposit'] = body
        return Response(response)

    def post(self, request, format=None):
        param = 'mineral_deposit'
        response = {'status': 'Failed the params delivered are not correct'}
        value = request.data.get(param)
        if value is not None:
            json_acceptable_string = value.replace("'", "\"")
            value = json.loads(json_acceptable_string)
            if list(value.keys()) == ['name','minerals']:
                db_manager.insert_new_mineral_deposit_from_name(value)
                response = {'status': 'Success'}
         
        return Response(response)


class BlockModel(APIView):
     def get(self,request,id=-1):
        if id == -1:
            cursor_all_block_models = db_manager.fetch_all_block_models()
            response = { "block_models": []}
            for block_model in cursor_all_block_models:
                block_model_hash={}
                id_block_model =  block_model.get('_id')                
                block_model_hash['id'] = str(id_block_model)
                block_model_hash['name'] =  block_model.get('name')
                block_model_hash['mineral_deposit'] =  block_model.get('mineral_deposit_name')
                response["block_models"].append(block_model_hash)
        else:
            response = { "block_model": {}}
            block_model_query = db_manager.fetch_block_model_from_id(id)
            mineral_deposit = db_manager.fetch_mineral_deposit(block_model_query['mineral_deposit_name'])
            manager.set_mineral_deposit(mineral_deposit)        
            block_model = db_manager.fetch_block_model(block_model_query['mineral_deposit_name'], block_model_query['name'])
            blocks = db_manager.get_all_blocks_from_block_model(block_model_query['mineral_deposit_name'], block_model_query['name'])
            manager.set_block_model(block_model, blocks)
            response_metric = manager.generate_action()     
            response["block_model"].update({'id':id})
            response["block_model"].update(response_metric)
            response["data_map"] = block_model["data_map"]


        return Response(response)

     def post(self, request):
        if request.data.get('block_model_reblock') is not None:
            #reblock
            value = request.data.get('block_model') 
            json_acceptable_string = value.replace("'", "\"")
            value = json.loads(json_acceptable_string)

            block_model_query = db_manager.fetch_block_model_from_id(value['base_block_model_id'])
            mineral_deposit = db_manager.fetch_mineral_deposit(block_model_query['mineral_deposit_name'])
            manager.set_mineral_deposit(mineral_deposit)        
            block_model = db_manager.fetch_block_model(block_model_query['mineral_deposit_name'], block_model_query['name'])
            blocks = db_manager.get_all_blocks_from_block_model(block_model_query['mineral_deposit_name'], block_model_query['name'])
            manager.set_block_model(block_model, blocks)
            rx = value['reblock_x']
            ry = value['reblock_y']
            rz = value['reblock_z']

            manager.block_model.reblock(rx, ry, rz, True)

            return Response(True)
        
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
            if instance == 'file_block_model' and value is not None:
               json_acceptable_string = value.replace("'", "\"")
               value = json.loads(json_acceptable_string)
            values_params[instance] = value
        if None not in values_params.values():
            db_manager.insert_new_block_model_with_name(values_params["mineral_deposit"], values_params["headers"] ,values_params["data_map"], values_params["block_model"] )
            db_manager.insert_blocks_from_url(values_params['mineral_deposit'],values_params['block_model'], values_params['file_block_model'], values_params['units'])
        
        
        return Response(values_params)
        
class Blocks(APIView):
     def get(self,request,id=-1, id_block_param=-1):
        if id_block_param==-1:
            block_model_query = db_manager.fetch_block_model_from_id(id)
            all_blocks = db_manager.get_all_blocks_from_block_model(block_model_query['mineral_deposit_name'], block_model_query['name'])
            response = { "blocks": []}
            for block in all_blocks[:4000]:
                block_hash={}
                id_block =  block.get('_id')
                block_hash['id'] = str(id_block)
                del block['_id']
                del block['id']
                block_hash.update(block)
                response["blocks"].append(block_hash)
            return Response(response)
        else: 
            block = db_manager.get_block_from_id(id_block_param)
            block['id']= id_block_param
            response = { "block": block}
            return Response(response)


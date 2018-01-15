import json

from django.http import JsonResponse

#from manpower.utils.constants import ERROR_DICT

__author__ = 'senthamilarasu'

from rest_framework.response import Response
from rest_framework import status

from street.code_msg import *

# Rest Response for Success
def success_response(code=3000, message='', data={}, status=status.HTTP_200_OK):
    if message == '':
        message = codes_msg[code]

    meta = {
        'status':'success', 
        'message': message, 
        'code': status
    }
    return Response({'meta':meta, 'data':data}, status=status)

# Rest Response for Fail
def fail_response(error_code, message='', data={}, status=status.HTTP_400_BAD_REQUEST):
    if message == '':
        message = codes_msg[error_code]

    meta = {
        'status':'fail', 
        'message': message, 
        'code': error_code
    }
    return Response({'meta':meta, 'data':data}, status=status)


def generate_failed_json(error_code, message, status=200, data={}):
    """
    Generates a failure response json message

    :param message:     The message to return as reason for failure
                        :type <type, 'str'>
    :param error_code:  The magical internal error code used by magical to identify and track common
                        known and uncommon unknown errors and or exceptions
                        :type <type, 'str'>
    :param status :     The status code that holds the http status code
    :return:            The collection object that holds the formatted key value collections
                        :type <type, 'dict'>
    """
    failed_json_data = load_failed_json_payload(data, error_code, message)
    failed_json_object = dict()

    failed_json_object['status'] = "fail"
    failed_json_object['message']=message
    failed_json_object['code']=error_code
    #failed_json_object['data']=dict()
    #failed_json_object['data'] = failed_json_data
    return JsonResponse({"meta":failed_json_object})

    #return JsonResponse({"meta":success_json,"data":data},status=status,  safe=False)

def generate_success_message(message,data, status=200):
    """
    Generates successful operation ,json message from the valid json resolvable :param `data`

    This :param `data` is what ends up as the value of the data key of all successful json responses
    this in line with the json schema chosen to represent all magical json responses
    :see http:\\www.jsonapi.com/schema for more information.

    :param data:            The data to be appended as the value of the json response key of the same
                            name i.e. `data`
                            :type <type, 'object'> limited to [str, int, list, None]
    :param code:
    :param message:
    :param status:
    :return success_json:   The fully parsed json response dict, might require additional wrapping by flask
                            json generating header function
                            :type <type, 'collections.OrderedDict'>
    """

    success_json = dict()

    success_json['status'] ='success'
    success_json['message']=message
    success_json['code']=200
    #success_json['data'] = data

    return JsonResponse({"meta":success_json,"data":data},status=status,  safe=False)


def load_failed_json_payload(data={}, error_code="", message=""):
    """
    Generates a failure response json dictionary

    :param message:     The message to return as reason for failure
                        :type <type, 'str'>
    :param error_code:  The magical internal error code used by magical to identify and track common
                        known and uncommon unknown errors and or exceptions
                        :type <type, 'str'>
    :return:            The collection object that holds the formatted key value collections
                        :type <type, 'dict'>
    """
    failed_json_info = dict()
    #failed_json_info['info'] = data
    failed_json_info['code'] = error_code
    failed_json_info['message'] = message
    return failed_json_info


def load_success_json_payload(data ="", code="", message=""):
    """
    Generates a failure response json dictionary

    :param message:     The message to return as reason for failure
                        :type <type, 'str'>
    :param code:  The magical internal code used by magical to identify and track common
                        known and uncommon unknown errors and or exceptions
                        :type <type, 'str'>
    :return:            The collection object that holds the formatted key value collections
                        :type <type, 'dict'>
    """
    success_json_info = dict()
    success_json_info['info'] = data
    success_json_info['code'] = code
    success_json_info['message'] = message
    return success_json_info

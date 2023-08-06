import requests
import json

from .api_results import *


class BaseFacade(object):

    baseURL = ""

    @classmethod
    def make_get_call(cls, url, result_type):
        response = requests.get(cls.baseURL + url)
        # print(response.json())

        json_str = json.dumps(response.json(), default=lambda o: o.__dict__, sort_keys=True, indent=4)
        print(json_str)
        # result = ApiResult(**json.loads(json_str))

        result = ApiResult.from_json(json.loads(json_str), result_type)

        return result

    @classmethod
    def make_post_call(cls, url, data, result_type):
        response = requests.post(cls.baseURL + url, json=data)

        json_str = json.dumps(response.json(), default=lambda o: o.__dict__, sort_keys=True, indent=4)
        # print(json_str)

        result = ApiResult.from_json(json.loads(json_str), result_type)

        return result

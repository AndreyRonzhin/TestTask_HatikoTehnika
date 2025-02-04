from typing import Any
import re
import requests
import json


class IMEI:

    __valid_formate = (r'\d{6}[-/.]\d{2}[-/.]\d{6}[-/.]\d{1}'
                       r'|\d{2}[-/.]\d{4}[-/.]\d{2}[-/.]\d{6}[-/.]\d{1}'
                       r'|\d{15}')
    imei:str

    def __init__(self, imei:str):
        self._imei = self.__valid_imei(imei)

    def __str__(self):
        return self.imei

    @property
    def imei(self):
        return self._imei

    @classmethod
    def __valid_imei(cls, value_imei:str)->str:
        if re.match(cls.__valid_formate, value_imei) is None:
            raise ValueError('Не верный формат IMEI')

        result = [int(v) for v in value_imei if v.isdigit()]

        if not cls.__valid_luhn(result):
            raise ValueError('Не верный номер IMEI')

        return ''.join(map(str, result))

    @classmethod
    def __valid_luhn(cls, imei:list[int])->bool:
        imei_copy = imei[:]

        for i in range(-(len(imei_copy) - 2), 1, 2):
            imei_copy[-i] = imei_copy[-i] * 2 if imei_copy[-i] * 2 <= 9 else imei_copy[-i] * 2 - 9

        return not sum(imei_copy) % 10


class IMEICheckNet:
    url = {'checks_imei': 'https://api.imeicheck.net/v1/checks'}

    def __init__(self, imei:str, token:str, service_id:int):
        self.imei = imei
        self.token = token
        self.service_id = service_id

    def post_check_imei(self)->dict[str, Any]:
        url = self.url.get('checks_imei', None)

        if url is None:
            raise requests.exceptions.RequestException('Ошибка POST запроса')

        headers = {
            'Authorization': 'Bearer ' + self.token,
            'Content-Type': 'application/json'
        }

        body = json.dumps({
            "deviceId": self.imei,
            "serviceId": self.service_id
        })

        try:
            response = requests.post(url, headers=headers, data=body)
        except requests.exceptions.RequestException as ex:
            raise requests.exceptions.RequestException(f'Ошибка POST запроса {ex}')

        if not response.status_code == 201:
            raise requests.exceptions.RequestException('Ошибка POST запроса')

        content = json.loads(response.content.decode(response.encoding))

        return {'response': response, 'content': content}




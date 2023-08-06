import sys
import json

import requests


class TranslatorException(Exception):
    """Exception for validation string type"""


class IsString(object):
    """Validator string type"""
    def isstring(value) -> bool:
        if isinstance(value, str):
            return True
        else:
            raise TranslatorException("Given value is not <class 'str'>")


class Translator(object):
    """
    Class makes object for connect to Yandex.Translate API.
    """

    def __init__(self, api_key=''):
        self._api_key = api_key
        self.__key = self._api_key or self.__get_trial_key()


    @property
    def api_key(self):
        """Get string value from api_key"""
        return self._api_key

    @api_key.setter
    def api_key(self, api_key: str):
        """Set string value to api_key"""
        if IsString.isstring(api_key):
            self._api_key = api_key
            self.__key = api_key

    @api_key.deleter
    def api_key(self):
        """Set trial_key to _api_key"""
        self._api_key = ''
        self.__key = self.__get_trial_key()


    def __get_trial_key(self): #  private function
        # return __trial_key only to test connection with api server
        # __trial_key maybe blocked anytime
        # please visit link below to get you free api_key
        # https://tech.yandex.com/translate/doc/dg/concepts/api-overview-docpage/

        __trial_key = 'trnsl.1.1.20190212T192502Z.6517b8749980b295.767053023db9b8116b29776755e6457da31b94ba'
        return __trial_key


    def _post_request(self, text='') -> str:
        """
        Send post request to Yandex.Translate API and return translated text
        """
        
        self.data = {
            'key': self.__key,
            'text': text,
            'lang': 'ru',
            'format': 'html'
        }

        r = requests.post(
                'https://translate.yandex.net/api/v1.5/tr.json/translate',
                self.data
        )

        try:
            result = str(*json.loads(r.text)['text'])
            return result
        except KeyError:
            raise TranslatorException(
                """
                No response from the server.
                Check the validity of your api_key.
                """
                )


    def get_translation(self, text='') -> str:
        """
        It makes text translation
        """
        if IsString.isstring(text) and text:
            return self._post_request(text)
        else:
            return ''

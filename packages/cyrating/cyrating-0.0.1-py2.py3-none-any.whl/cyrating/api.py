# -*- coding: utf-8 -*-

import requests
from requests.adapters import HTTPAdapter
import configparser
import jwt
import arrow
import json
import sys

PATH_MASTER_TOKEN = "./cyrating.ini"
APP_URL = "https://api.cyrating.com"
SIGNIN_ENDPOINT = '/signin'
COMPANY_ENDPOINT = '/company'
CLIENT_ENDPOINT = '/client'
CERTIFICATE_ENDPOINT = '/certificate'


class Cyrating(object):
  def __init__(self, **kwargs):
    """ Init a Cyrating context """

    self._requests = requests.Session()
    self._requests.mount('', HTTPAdapter(max_retries=5))

    if 'token' in kwargs:
      ptoken = kwargs.get('token')
    else:
      ptoken = self.get_personal_token()
    decoded_ptoken = jwt.decode(ptoken, verify=False)

    if 'debug' in kwargs:
      self.__app_url__ = 'http://localhost:5000'
    else:
      self.__app_url__ = APP_URL

    print("# Access Token expires in", self.__app_url__, "at",
          arrow.get(decoded_ptoken['exp']), end=' - ')
    self.signin(ptoken)

  def get_personal_token(self):
    """ Read personal token from configuration file """

    config = configparser.ConfigParser()
    config.read(PATH_MASTER_TOKEN)
    return config['cyrating']['token']

  def signin(self, ptoken):
    """ Sign in Cyrating with personal token and retrieve access token  """

    headers = {"Content-Type": "application/json",
               "Authorization": "Bearer " + ptoken}
    answer = requests.post(self.__app_url__ + SIGNIN_ENDPOINT,
                           '',
                           headers=headers)
    if not answer or not answer.ok:
      raise Exception('# Unauthorized token')

    self.__access_token__ = json.loads(answer.content)['token']
    self.__headers__ = {"Content-Type": "application/json",
                        "Authorization": "Bearer " + self.__access_token__}
    decoded_atoken = jwt.decode(self.__access_token__, verify=False)
    self.__current_user_id__ = decoded_atoken['sub']
    self.__current_client_id__ = decoded_atoken['ccs']
    self.load_client(self.__current_client_id__)

  def load_client(self, clientid):
    """ Retrieve client obj from API """

    answer = self.get(CLIENT_ENDPOINT, clientid)
    if not answer:
      self.__current_client__ = None
      return
    self.__current_client__ = dict(
        name=answer['name'] if 'name' in answer else None,
        company_id=answer['companyID'] if 'companyID' in answer else None,
        entities_id=answer['entitiesID'] if 'entitiesID' in answer else None,
        suppliers_id=answer['suppliersID'] if 'suppliersID' in answer else None,
    )

  def get_company(self, id):
    """ Retrieve company obj from API """

    projection = json.dumps({'name': 1, 'supersector': 1, 'score': 1})
    answer = self.get(COMPANY_ENDPOINT,
                      id,
                      {'projection': projection})
    if not answer:
      return None

    return dict(
        _id=answer['_id'],
        name=answer['name'],
        supersector=answer['supersector'],
        rating=int(answer['score']['CYRATING'] * 100)
    )

  def get_certificate(self, company, filename=None):
    """ Get certificate of a specific company from API """

    httpParams = dict(
        clientid=self.__current_client_id__,
        orgid=company['_id']
    )
    answer = self._requests.get(self.__app_url__ + CERTIFICATE_ENDPOINT,
                                params=httpParams,
                                headers=self.__headers__)

    if not answer.ok:
      raise Exception('Failed to retreive certificate for {}'.format(company['name']))

    if filename:
      try:
        with open(filename, 'wb') as f:
          f.write(answer.content)
      except Exception as e:
        raise Exception('Failed to save {}: {}'.format(filename, e))
    else:
      return answer.content

  def get(self, endpoint, id, extraHttpRequestParams=None):
    res = self._requests.get(self.__app_url__ + endpoint + '/' + id,
                             params=extraHttpRequestParams,
                             headers=self.__headers__)
    if res.ok:
      jData = json.loads(res.content)
      return jData
    return None

  def get_main_company(self):
    """ Get main company from API """

    return self.get_company(self.__current_client__['company_id'])

  def get_entities(self):
    """ Get list of entities from API """

    return [self.get_company(companyid) for companyid in self.__current_client__['entitiesID']]

  def get_suppliers(self):
    """ Get list of suppliers from API """

    return [self.get_company(companyid) for companyid in self.__current_client__['suppliersID']]

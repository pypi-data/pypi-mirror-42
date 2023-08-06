import os
import string
import requests
import json
import logging
import yaml
from ol_commons.constants.http_codes import HTTP_200_OK
from ol_commons.constants.messages import SECURITY_RESPONSE_MSG
from ol_commons.errors import AttributeControllerError, AppSecurityControllerError


def is_informational(code) -> bool:
    return 100 <= code <= 199


def is_success(code) -> bool:
    return 200 <= code <= 299


def is_redirect(code) -> bool:
    return 300 <= code <= 399


def is_client_error(code) -> bool:
    return 400 <= code <= 499


def is_server_error(code) -> bool:
    return 500 <= code <= 599


def standard_response(http_status, content, message) -> dict:
    response = {'status': http_status,
                'content': content,
                'message': message}
    return response


def get_attributes(str_attribute_name) -> dict:
    json_in = None
    url = os.environ.get('URL_ATTRIBUTES_SERVICE') + '?str_attribute_name=' + str_attribute_name

    service_resp = requests.get(url, json=json_in)
    json_out = json.loads(service_resp.text)

    if json_out.get('status') is not HTTP_200_OK:
        raise AttributeControllerError(json_out.get('message'), json_out.get('status'))

    content = json_out.get('content')

    result_dic = dict()

    if content is not None:
        attr_list = content.get('attributes')
        result_dic = dict([i.get('num_attr_member_id'), i.get('str_attr_member_value')] for i in attr_list)

    return result_dic


def get_auth_password(user_auth) -> string:
    try:
        json_in = {'oauth_user': {'user': user_auth, 'password': None}}
        service_resp = requests.post(os.environ.get('URL_OAUTH_SECURITY_SERVICE'), json=json_in)

        logging.debug('Response security service example: {}'.format(service_resp.status_code))

        if service_resp.status_code is not HTTP_200_OK:
            raise AppSecurityControllerError(service_resp.status_code)

        json_out = json.loads(service_resp.text)
        content = json_out.get('content')

        if content is None:
            raise AppSecurityControllerError(SECURITY_RESPONSE_MSG)

        oauth_user = content.get('oauth_user')

        if oauth_user is None:
            raise AppSecurityControllerError(SECURITY_RESPONSE_MSG)

        logging.debug("end get password")

        return oauth_user.get('str_oauth_cred_password')
    except requests.RequestException as e:
        raise AppSecurityControllerError(e)


def setup_logging(default_path='configs/logging.yaml', default_level=logging.INFO, env_key='LOG_CFG'):
    path = default_path
    value = os.getenv(env_key, None)
    if value:
        path = value
    if os.path.exists(path):
        with open(path, 'rt') as f:
            config = yaml.safe_load(f.read())
        logging.config.dictConfig(config)
        logging.getLogger().setLevel(level=default_level)
    else:
        logging.basicConfig(level=default_level)

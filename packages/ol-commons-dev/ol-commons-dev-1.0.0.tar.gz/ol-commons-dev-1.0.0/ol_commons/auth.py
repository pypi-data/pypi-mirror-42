import logging

from flask import jsonify
from flask_httpauth import HTTPBasicAuth
from ol_commons.constants.http_codes import HTTP_403_FORBIDDEN
from ol_commons.constants.messages import SECURITY_UNAUTHORIZED_MSG
from ol_commons.errors import AppSecurityControllerError
from ol_commons.helpers import standard_response, get_auth_password

auth = HTTPBasicAuth()


@auth.get_password
def get_password(oauth_user):
    try:
        resp = get_auth_password(oauth_user)
        logging.debug('type res: {}'.format(type(resp)))
        logging.debug('sending password ...')
        return resp

    except AppSecurityControllerError as e:
        logging.debug('bla bla bla')
        logging.error(e)
        return None


@auth.error_handler
def unauthorized():
    # return 403 instead of 401 to prevent browsers from displaying the default
    # auth dialog
    resp = standard_response(HTTP_403_FORBIDDEN, None, SECURITY_UNAUTHORIZED_MSG)
    return jsonify(resp)

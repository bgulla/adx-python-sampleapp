import os
import logging
from logging.handlers import RotatingFileHandler
from OpenSSL import SSL
from sampleapp import app
from mock import MagicMock

mock = MagicMock()

if __name__ == "__main__":
#    context = SSL.Context(SSL.SSLv23_METHOD)
#    cert_file = '/secret/cert/python-tls.crt'
#    key_file = '/secret/cert/python-tls.key'
#    if not os.path.exists('/secret/cert'):
#        cert_file = './python-tls.crt'
#        key_file = './python-tls.key'
    #application.run(host="0.0.0.0",port=8443,ssl_context=(cert_file,key_file))
#    with MagicMock.patch.object(getpass, "getuser", return_value='default'):
    with mock.patch.object('getpass', "getuser", return_value='default'):
        app.run(host="0.0.0.0",port=8080)




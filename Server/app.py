from flask import Flask
import base64
import datetime
import hashlib
import hmac
import json
from urllib.parse import urlparse
import ssl
from datetime import datetime
from time import mktime
from urllib.parse import urlencode
from wsgiref.handlers import format_date_time

# The following key information is obtained from the console
Appid = ""  # Fill in the APPID information obtained from the console
APISecret = ""  # Fill in the APISecret information obtained from the console
APIKey = ""  # Fill in the APIKey information obtained from the console

# Used to configure the large model version, default is "general/generalv2"
domain = "generalv3"   # Version 1.5
# domain = "generalv2"    # Version 2.0
# Service address for the cloud environment
Spark_url = "ws://spark-api.xf-yun.com/v3.1/chat"  # Address for version 1.5 environment
# Spark_url = "ws://spark-api.xf-yun.com/v2.1/chat"  # Address for version 2.0 environment
Spark_url1 = "ws://ws-api.xfyun.cn/v2/iat"  # Speech recognition
Spark_url2 = "ws://ws-api.xfyun.cn/v2/tts"  # Speech synthesis
Spark_url3 = "ws://tts-api.xfyun.cn/v2/tts"

app = Flask(__name__)

@app.route('/whf', methods=['GET'])
def handle_request():
    host = urlparse(Spark_url).netloc
    path = urlparse(Spark_url).path
    now = datetime.now()
    date = format_date_time(mktime(now.timetuple()))

    # Concatenate the string
    signature_origin = "host: " + host + "\n"
    signature_origin += "date: " + date + "\n"
    signature_origin += "GET " + path + " HTTP/1.1"
    # Perform HMAC-SHA256 encryption
    signature_sha = hmac.new(APISecret.encode('utf-8'), signature_origin.encode('utf-8'),
                             digestmod=hashlib.sha256).digest()
    signature_sha_base64 = base64.b64encode(
        signature_sha).decode(encoding='utf-8')
    authorization_origin = f'api_key="{APIKey}", algorithm="hmac-sha256", headers="host date request-line", signature="{signature_sha_base64}"'
    authorization = base64.b64encode(
        authorization_origin.encode('utf-8')).decode(encoding='utf-8')
    # Combine the request's authentication parameters into a dictionary
    v = {
        "authorization": authorization,
        "date": date,
        "host": host
    }
    # Concatenate the authentication parameters to generate the URL
    url = Spark_url + '?' + urlencode(v)
    return url  # Return a simple message example

@app.route('/whf1', methods=['GET'])
def handle_request1():
    host = urlparse(Spark_url1).netloc
    path = urlparse(Spark_url1).path
    now = datetime.now()
    date = format_date_time(mktime(now.timetuple()))

    # Concatenate the string
    signature_origin = "host: " + host + "\n"
    signature_origin += "date: " + date + "\n"
    signature_origin += "GET " + path + " HTTP/1.1"
    # Perform HMAC-SHA256 encryption
    signature_sha = hmac.new(APISecret.encode('utf-8'), signature_origin.encode('utf-8'),
                             digestmod=hashlib.sha256).digest()
    signature_sha_base64 = base64.b64encode(
        signature_sha).decode(encoding='utf-8')
    authorization_origin = f'api_key="{APIKey}", algorithm="hmac-sha256", headers="host date request-line", signature="{signature_sha_base64}"'
    authorization = base64.b64encode(
        authorization_origin.encode('utf-8')).decode(encoding='utf-8')
    # Combine the request's authentication parameters into a dictionary
    v = {
        "authorization": authorization,
        "date": date,
        "host": host
    }
    # Concatenate the authentication parameters to generate the URL
    url = Spark_url1 + '?' + urlencode(v)
    return url  # Return a simple message example

@app.route('/whf2', methods=['GET'])
def handle_request2():
    host = urlparse(Spark_url2).netloc
    path = urlparse(Spark_url2).path
    now = datetime.now()
    date = format_date_time(mktime(now.timetuple()))

    # Concatenate the string
    signature_origin = "host: " + host + "\n"
    signature_origin += "date: " + date + "\n"
    signature_origin += "GET " + path + " HTTP/1.1"
    # Perform HMAC-SHA256 encryption
    signature_sha = hmac.new(APISecret.encode('utf-8'), signature_origin.encode('utf-8'),
                             digestmod=hashlib.sha256).digest()
    signature_sha_base64 = base64.b64encode(
        signature_sha).decode(encoding='utf-8')
    authorization_origin = f'api_key="{APIKey}", algorithm="hmac-sha256", headers="host date request-line", signature="{signature_sha_base64}"'
    authorization = base64.b64encode(
        authorization_origin.encode('utf-8')).decode(encoding='utf-8')
    # Combine the request's authentication parameters into a dictionary
    v = {
        "authorization": authorization,
        "date": date,
        "host": host
    }
    # Concatenate the authentication parameters to generate the URL
    url = Spark_url3 + '?' + urlencode(v)
    return url  # Return a simple message example

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

import requests
import datetime
import hmac
import hashlib
import urllib
import json

# ----- EIR ----- #
PARTNER_ID  = 'eir'
SECRET      = '2496e15dcd02ef726daf4a7b10c39e5f1f10afb3276cbf64e453a4974de70652'
USER_ID     =  38830958 # EIRzattoo03@gmail.com/zattoo01 EIR prod 

# ----- 1UND1 ----- #
#PARTNER_ID  = '1und1'
#SECRET      = 'c497b39c332a3dbea8afea58341b78289b06faa91cdfb22b3ef27f8b74468552'
#USER_ID     =  1287 # 1110 zattoo10/zattoo 1&1 prod, # 1287 zattoo28/zattoo

ENCODING    = 'utf-8'
ENDPOINT    = ('https://qa.zattoo.com/partner/%s/zuya/' %(PARTNER_ID))
TIME_FORMAT = '%Y-%m-%dT%H:%M:%SZ'

# production:   https://zapi.zattoo.com/
# staging:      https://staging.zattoo.com/
# sandbox:      http://sandbox.zattoo.com/
# qa:           https://qa.zattoo.com/

# make sig for ZUYA Update POST requests
# check https://apidoc.zattoo.com/zuyaupdate/secure_requests
def signature (robj):
  #rstr   = bytes(robj).encode(ENCODING) for python2
  #secret = bytes(SECRET).encode(ENCODING) for python2
  rstr   = bytes(robj.encode(ENCODING))
  secret = bytes(SECRET.encode(ENCODING))
  return hmac.new(secret, rstr, hashlib.sha256).hexdigest()

# get an actual timestamp to sign the request
def timestamp ():
  return datetime.datetime.utcnow().replace(microsecond=0).strftime(TIME_FORMAT)

# generic post to zuya update
def post_to_api (path, robj):
  header  = {'Content-Type': 'application/x-www-form-urlencoded'}
  data    = {'request': robj, 'sig': signature(robj)}
  req     = requests.post(ENDPOINT+path, data=data, headers=header)

  status  = req.status_code
  try:
    body = req.json()
  except ValueError:
    body = ''

  print(ENDPOINT + path)
  print("\n",'HTTP Status: ' + str(status), "\n", sep="")
  print(json.dumps(body, indent=2, sort_keys= True))

### API calls ###

# ZUYA Update: trigger update
def trigger_update ():
  robj = {'partner_id': PARTNER_ID, 'creation_time': timestamp(), 'user_id': USER_ID}
  post_to_api('trigger_update', json.dumps(robj))

# device mgmt: List devices
def list_devices ():
  robj = {'partner_id': PARTNER_ID, 'creation_time': timestamp(), 'user_id': USER_ID}
  post_to_api('devices/list', json.dumps(robj))

# device mgmt: Update devices
def update_devices ():
  robj = {'partner_id': PARTNER_ID, 'creation_time': timestamp(), 'user_id': USER_ID, 'device_id': 67, 'name' : 'Test23MD DJsd'}
  post_to_api('device/update', json.dumps(robj))

# device mgmt: Deregiter devices
def deregister_devices ():
  robj = {'partner_id': PARTNER_ID, 'creation_time': timestamp(), 'user_id': USER_ID, 'device_id': 65}
  post_to_api('device/deregister', json.dumps(robj))

# device mgmt: Purge all devices
def purge_alldevices ():
  robj = {'partner_id': PARTNER_ID, 'creation_time': timestamp(), 'user_id': USER_ID}
  post_to_api('devices/purge', json.dumps(robj))

# activity feed
def activity_feed ():
  robj = {'partner_id': PARTNER_ID, 'creation_time': timestamp(), 'until': '2019-05-31T15:30:49Z', 'since' : '2019-05-24T15:30:49Z'}
  post_to_api('devices/feed.json', json.dumps(robj))

# Actions

list_devices()
# trigger_update()
# update_devices ()
# deregister_devices ()
# purge_alldevices ()
# activity_feed ()

# print (timestamp())
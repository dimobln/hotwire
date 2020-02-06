from __future__ import print_function
import hashlib
import hmac
import requests

PARTNER_ID = 'hotwire'
PARTNER_SECRET = 'bubblegum001'
STREAMAPI_URL = 'https://streamapi.fll.zattoo.com'
ENCODING = 'utf-8'

def request(method, path, params=None, data=None):
    url = STREAMAPI_URL + path
    # create a prepared request so we can sign the exact request path and body which gets sent
    prepped = requests.Request(method=method, url=url, params=params, json=data).prepare()
    prepped.headers['Z-Partner'] = PARTNER_ID
    signature_payload = prepped.path_url
    if prepped.body:
        signature_payload += str(prepped.body, encoding=ENCODING)
    signature = hmac.new(PARTNER_SECRET.encode(), signature_payload.encode(), digestmod=hashlib.sha256).hexdigest()
    prepped.headers['Z-Signature'] = signature
    with requests.Session() as session:
        resp = session.send(prepped)
        return resp.status_code, resp.json()

def main(channel):
    status, response = request('POST', '/stream/live', data={
        'channel': channel,
        'quality': 'hd',
        'stream_type': 'hls7',
        'https': True,
        'client_ip': '1.2.3.4',
        'uuid': 'abc123',
        'disable_geoblocking': True,
    })
    print(status, response) #response is used in file.write
    return response

if __name__ == '__main__':

    sender = ['cnn_us', 'msnbc_us', 'cnn_us', 'cnn_us']
    kannal = {'cnn_us':'tvg-id="" tvg-name="" tvg-logo="https://images.zattic.com/logos/njashdasdnaskbdkajsbd/black/640x360.png" group-title="US",',
             'msnbc_us':'tvg-id="" tvg-name="" tvg-logo="https://images.zattic.com/logos/232323/black/640x360.png" group-title="US",',
             'cnn_us':'tvg-id="" tvg-name="" tvg-logo="https://images.zattic.com/logos/njashdasdnaskbdkajsbd/black/640x360.png" group-title="US",',
        }

    with open("response.m3u8", "w") as file:
        try:
            file.write("#EXTM3U" + '\n')
            for channel in sender:
                url = main(channel)['stream_url']
                file.write("#EXTINF:-1 " + kannal.get(channel,["nicht gefunden"]) + '\n'+ url + '\n'+'\n')
        except ValueError:
            file.write('''
            ############## Check the VPN ##############
            ''' )
            print('\n' + "############## Check the VPN ##############"+'\n') 

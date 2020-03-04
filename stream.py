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
        'maxrate': 5000,
        'https': True,
        'client_ip': '1.2.3.4',
        'uuid': 'abc123',
        'disable_geoblocking': True,
    })
    print(status, response) #response is used in file.write
    return response

if __name__ == '__main__':

    kanaele = {
        'cnn_us':'tvg-id="" tvg-name="" tvg-logo="https://images.zattic.com/logos/9ff53034eab3535b79c7/black/640x360.png" group-title="US",CNN',
        'msnbc_us':'tvg-id="" tvg-name="" tvg-logo="https://images.zattic.com/logos/03e9f17e1e11033e6db4/black/640x360.png" group-title="US",MSNBC',
        'espn_mia':'tvg-id="" tvg-name="" tvg-logo="https://images.zattic.com/logos/6df04c3126e6914187ce/black/640x360.png" group-title="US",ESPN',
        'espn2_mia':'tvg-id="" tvg-name="" tvg-logo="https://images.zattic.com/logos/cafd3f3f1615f2e16a79/black/640x360.png" group-title="US",ESPN 2',
    }

    with open("response.m3u8", "w") as file:
        try:
            file.write("#EXTM3U" + '\n')
            for channel, link in kanaele.items():
                url = main(channel)['stream_url']
                file.write("#EXTINF:-1 " + link + '\n'+ url + '\n'+'\n')
        except ValueError:
            file.write('''
            ############## Check the VPN ##############
            ''' )
            print('\n' + "############## Check the VPN ##############"+'\n')
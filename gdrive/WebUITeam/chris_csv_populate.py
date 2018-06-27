
import json
import requests
import psycopg2
import time

class ApiRequest(object):
    def __init__(self, url, querystring, token):
        self.url = url
        self.querystring = querystring
        self.auth = token

    def get_Api_Request(self):
        header = {
            'Authorization': "Bearer " + self.auth,
            }
        response = requests.request("GET", self.url, headers=header, params=self.querystring)
        data = json.loads(str(response.text))

        return data
    def get_Token(self):
        response = requests.request("GET", self.url, params=self.querystring)
        token = (json.loads(str(response.text)))['token']

        return token
def get_Data():
    main_url = 'https://cam2-api.herokuapp.com'

    #Gets  Token
    url = main_url + "/auth"
    querystring = {"clientID":"34b9eb8afc032098bc96174ec38ca2dba940a401d03c311251af4d8b609f7272c91ed0aaef1ee4eddb4783bcaa3ead7d","clientSecret":"b0eaea176c29331149557b1c2fe54b82d335c8c30dbed9a50c5e4aa141b15dbefbbfd69"}
    token_request = ApiRequest(url, querystring, 0)
    token = token_request.get_Token()

    count = 0
    with open('cam_data.csv', 'w') as camera_data:
        camera_data.write('ID, Image, Latitude, Longitude, City, State, Country\n')
        for set in range(0,127):
            data = list()
            for set2 in range(0,9):
                count = count + 100
                url_2 = main_url + "/cameras/search"
                querystring_2 = {"offset": count}
                cameras_request = ApiRequest(url_2, querystring_2, token)
                cameras = cameras_request.get_Api_Request()
                data.append(cameras)
            try:
                for hundred in data:
                    for camera in hundred:
                        if camera['type'] == 'ip':
                            ip_address = camera['retrieval']['ip']
                            if ip_address is None:
                                ip_address = ''
                            video_path = camera['retrieval']['video_path']
                            if video_path is None:
                                video_path = ''
                            image = 'http://' + video_path + ip_address
                        elif camera['type'] == 'non_ip':
                            image = camera['snapshot_url']
                        elif d['type'] == 'stream':
                            image = camera['m3u8_url']
                        latitude = str(camera['latitude'])
                        longitude = str(camera['longitude'])
                        city = camera['city']
                        if city is None:
                            city = ''
                        state = camera['state']
                        if state is None:
                            state = ''
                        country = camera['country']
                        if country is None:
                            country = ''

                        camera_data.write(camera['cameraID'] + ',' + image + ',' + latitude + ',' + longitude + ',' + city + ',' + state + ',' + country)
                        camera_data.write('\n')
            except:
                continue

if __name__== '__main__':
    start_time = time.time()
    get_Data()
    print('%s seconds' % (time.time() - start_time))

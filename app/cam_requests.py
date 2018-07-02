import requests
import json
import time

client = '34b9eb8afc032098bc96174ec38ca2dba940a401d03c311251af4d8b609f7272c91ed0aaef1ee4eddb4783bcaa3ead7d'
secret = 'b0eaea176c29331149557b1c2fe54b82d335c8c30dbed9a50c5e4aa141b15dbefbbfd69'
#header = {'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJjbGllbnRJRCI6IjM0YjllYjhhZmMwMzIwOThiYzk2MTc0ZWMzOGNhMmRiYTk0MGE0MDFkMDNjMzExMjUxYWY0ZDhiNjA5ZjcyNzJjOTFlZDBhYWVmMWVlNGVkZGI0NzgzYmNhYTNlYWQ3ZCIsInBlcm1pc3Npb25MZXZlbCI6InVzZXIiLCJpYXQiOjE1MjgxMjkxNTAsImV4cCI6MTUyODEyOTQ1MH0.xaTv3iT7KJKoQlgZrlpm0d4RuhWjniL5QG6K_RqUWVQ'}
params = {'clientID': client, 'clientSecret': secret}
rauth = requests.get('https://cam2-api.herokuapp.com/auth', params=params)
"""tclient = 'user'
tsecret = 'user'
tparams = {'clientID': tclient, 'clientSecret': tsecret}
trauth = requests.get('https://cam2-api-test.herokuapp.com/auth', params=tparams)
token = trauth.json()['token']"""
token = rauth.json()['token']
headerval = 'Bearer ' + token
header = {'Authorization': headerval}
"""tr = requests.get('https://cam2-api-test.herokuapp.com/cameras/search', headers=header)
tdata = tr.json()"""
r = requests.get('https://cam2-api.herokuapp.com/cameras/search', headers=header)
#datalen = len(r.json())
data = r.json()
#print(data)
output = list()
for d in data:
    #info = {'cameraID': d['cameraID'], 'latitude': d['latitude'], 'longitude': d['longitude']}
    output.append(d)
"""for d in data:
    info = {'cameraID': d['cameraID'], 'latitude': d['latitude'], 'longitude': d['longitude']}
    output.append(info)"""
"""for count in range(100, 9900, 100):
    param2 = {'offset': count}
    r2 = requests.get('https://cam2-api.herokuapp.com/cameras/search', params=param2, headers=header)
    print(r2.status_code)
    x = 1
    while r2.status_code != 200:
        print(x)
        time.sleep(x)
        x = x * 2
        r2 = requests.get('https://cam2-api.herokuapp.com/cameras/search', params=param2, headers=header) # I'll cross the token expiring bridge when/if I come to it
        print(r2.status_code)
    data2 = r2.json()
    for d2 in data2:
        info2 = {'cameraID': d2['cameraID'], 'latitude': d2['latitude'], 'longitude': d2['longitude']}
        output.append(info2)"""
count = 0
#while True:
for x in range(1,4):
    time.sleep(60)
    count = count + 100
    param2 = {'offset': count}
    tr2 = requests.get('https://cam2-api.herokuapp.com/cameras/search', params=param2, headers=header)
    print(tr2.status_code)
    if tr2.status_code != 200:
        """while True:
            print('Sleeping for 120')
            time.sleep(120)
            tr2 = requests.get('https://cam2-api.herokuapp.com/cameras/search', params=param2, headers=header)
            print(tr2.status_code)
            if tr2.status_code == 200:
                break"""
        continue
    tdata2 = tr2.json()
    for d2 in tdata2:
        #tinfo2 = {'cameraID': d2['cameraID'], 'latitude': d2['latitude'], 'longitude': d2['longitude']}
        output.append(d2)
    if len(tr2.json()) < 100:
        break
with open('cam_data.json', 'w') as f:
    json.dump(output, f, ensure_ascii=False)

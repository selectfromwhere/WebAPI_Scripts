#!/usr/bin/env python                                                                                                                                             
# -*- coding:utf-8 -*-

import json, datetime, re, config
import urllib.request

url = 'https://map.yahooapis.jp/weather/V1/place?'
crient_id = config.crient_id
url_f = '{}coordinates={},{}&appid={}&output=json'

def Forecast(lat,lng):
    url_h = url_f.format(url, lng, lat, crient_id)
    res = urllib.request.urlopen(url_h).read()
    return json.loads(res.decode('utf-8'))

# f = open('test.json', 'w')
# json.dump(res_json, f)

def main():
    lat = [config.latlng["home"]["lat"],
           config.latlng["biz"]["lat"],
           config.latlng["brth"]["lat"]]
    lng = [config.latlng["home"]["lng"],
           config.latlng["biz"]["lng"],
           config.latlng["brth"]["lng"]]
    plc = ['【自宅】','【職場】','【地元】']
    pattern = "(.*)\)の(.*)"

    for i in range(0,3):
        res_json = Forecast(lat[i],lng[i])

        plc_nm = re.search(pattern,res_json['Feature'][0]['Name'])
        print('{}の{}'.format(plc[i], plc_nm.group(2)))

        fc = res_json['Feature'][0]['Property']['WeatherList']['Weather']

        for r in fc:
            dt = datetime.datetime.strptime(r['Date'], '%Y%m%d%H%M')
            if r['Rainfall'] == 0.0:
                rl = '晴れ'
            elif r['Rainfall'] < 20.0:
                rl = '雨'
            elif r['Rainfall'] >= 20.0:
                rl = '強い雨'
            print('{}時{}分 : {}（降水予雨量 : {}mm）'.format(str(dt.hour), str(dt.minute), rl, r['Rainfall']))

if __name__ == "__main__":
    main()
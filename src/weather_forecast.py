import sys
import rospy
from std_msgs.msg import String
import MeCab
import requests
import json

from speak_tools.srv import *

import voice2text

# API叩いで天気予報の情報を文字列で返す関数
def forecast_from_livedoor_api(ID)
	print("locationID :" + location_id)
	url = 'http://weather.livedoor.com/forecast/webservice/json/v1'
	response = requests.get(url, params={"city": location_id})
	weather_data = response.json()
	print(weather_data)
	ret = ""
	for forecast in weather_data['forecasts']:
	    print(forecast['telop'])
	    ret = ret + forecast['telop'] "。\n"
	return ret

# 発話ノードに対して喋らせたい内容をパブリッシュする関数
def speak(text):
    rospy.wait_for_service("speak_text")
    try:
        speak_text = rospy.ServiceProxy("speak_text", SpeakedText)
        resp = speak_text(text)
        return resp.message
    except rospy.ServiceException, e:
        print "Service call failed: %s" % e

def do():
	speak("どこの天気予報が知りたいですか。") # 喋る
	cityID = voice2text.get_cityID() # 喋っている音声をテキストに変換してIDにして返す
	result = forecast_from_livedoor_api(cityID) # APIを叩いて情報持ってくる
	speak(result) # 結果を喋る
	# 晴だったらダンスする
	# if '晴' in result:
	# 	return "lets dance"
	# else:
	# 	return "not"

def weather_forecast():
	def parse(text):
		m = MeCab.Tagger("-Ochasen")
        node = m.parseToNode(text)
        words_list = []
        while node:
            word = node.surface
            wclass = node.feature.split(',')
            if wclass[0] != 'BOS/EOS':
                words_list.append(word)
            node = node.next
        return words_list
    def callback(msg):
        words = parse(msg.data)
        if words == ['天気', '予報', 'モード', '開始']:
        	do() # 天気予報モード開始の端点
        else:
        	return
    rospy.Subscriber("/speech", String, callback) 
    rospy.spin() 

def main():
	rospy.init_node('weather_forecast')
	# dance = rospy.Publisher('/dance', String, queue_size=1)
	weather_forecast()

if __name__ == '__main__':
	sys.exit('main.py should not be called directory! use roslaunch instead.')

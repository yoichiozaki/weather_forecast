import sys
import rospy
from std_msgs.msg import String
import MeCab
import requests
import json

from speak_tools.srv import *

import voice2text

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

def speak(text):
    rospy.wait_for_service("speak_text")
    try:
        speak_text = rospy.ServiceProxy("speak_text", SpeakedText)
        resp = speak_text(text)
        return resp.message
    except rospy.ServiceException, e:
        print "Service call failed: %s" % e

def ask_where():
	speak("どこの天気予報が知りたいですか。")

def listen():
	cityID = voice2text.get_cityID()
	return cityID

def say_forecast(ID):
	# API叩いて結果を発話する。
	result = forecast_from_livedoor_api(ID)
	speak(result)
	# 晴だったらダンスする
	# if '晴' in result:
	# 	return "lets dance"
	# else:
	# 	return "not"

def do():
	ask_where()
	ID = listen()
	say_forecast(ID)

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
        	do()
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

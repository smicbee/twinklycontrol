#Copyright 2020 by peroxo
import json
import urllib.request as urllib2
import socket
import time
from PIL import Image, ImageDraw, ImageFont
import math
import numpy
import cv2 
import os 
from datetime import datetime

class twinkly:
	def __init__(self, ip = '192.168.0.13'):
		self.token = None
		self.ip = ip
		self.path = 'http://' + ip
		
	def postData(self, data,url):
		req = urllib2.Request(self.path+url)
		if self.token != None:
			req.add_header('X-Auth-Token',str(self.token))
		req.add_header('Content-Type','application/json')
		response = urllib2.urlopen(req, json.dumps(data).encode('utf-8'))
		if response.getcode() == 401:
			self.token = self.login()
			self.postData(data, url, self.token)
		elif response.getcode() == 200:
			return json.loads(response.read())
		else:
			self.postData(data, url, self.token)

	def postRaw(self, data,url):
		req = urllib2.Request(self.path+url)
		if self.token != None:
			req.add_header('X-Auth-Token',str(self.token))
		req.add_header('Content-Type','application/octet-stream')
		response = urllib2.urlopen(req, data)

		if response.getcode() == 401:
			self.token = self.login()
			postRaw(url, self.token)
		elif response.getcode() == 200:
			return json.loads(response.read())
		else:
			postRaw(url, self.token)

		return json.loads(response.read())

	def doGet(self, url):
		req = urllib2.Request(self.path+url)
		if self.token != None:
			req.add_header('X-Auth-Token',str(self.token))
		response = urllib2.urlopen(req)
		return json.loads(response.read())

	def login(self):
		challenge = 'A'*64
		data = {
		        'challenge': challenge
		}
		jResp = self.postData(data, '/xled/v1/login')
		self.token = jResp['authentication_token']
		chall = jResp['challenge-response']
		data = {"challenge-response": str(chall)}
		self.postData(data, '/xled/v1/verify')

	def get_mode(self):
		url = "/xled/v1/led/mode"
		return self.doGet(url)

	def set_mode(self, m):
		url = "/xled/v1/led/mode"
		data = {
		    'mode': m
		}
		return self.postData(data, url)

	def set_rt_mode(self):
		return self.set_mode('rt')

	def set_movie_mode(self):
		return self.set_mode('movie')

	def set_demo_mode(self):
		return self.set_mode('demo')

	def set_off_mode(self):
		return self.set_mode('off')

	def set_effect_mode(self):
		return self.set_mode('effect')

	def set_restart_mode(self):
		return self.set_mode('restart')

	def get_led_reset(self):
		url = "/xled/v1/led/reset"
		return self.doGet(url)

	def uploadMovie(self, data):
		url = "/xled/v1/led/movie/full"
		return self.postRaw(data, url)

	def set_movie_config(self, f_delay, leds, f_num):
		url = "/xled/v1/led/movie/config"
		data = {
		    'frame_delay': f_delay,
		    'leds_number': leds,
		    'frames_number': f_num
		}
		return self.postData(data, url)

	def get_movie_config(self):
		url = "/xled/v1/led/movie/config"
		return self.doGet(url)

	def get_gestalt(self):
		url = "/xled/v1/gestalt"
		return self.doGet( url)

	def get_fw_version(self):
		url = "/xled/v1/fw/version"
		return self.doGet( url)

	def logout(self):
		url = "/xled/v1/logout"
		data = {}
		return self.postData(data, url)

	def get_timer(self):
		url = "/xled/v1/timer"
		return self.doGet(url)

	def set_timer(self,time_on, time_now, timeoff):
		url = "/xled/v1/timer"
		data = {
				'time_on': time_on, 
				'time_now': time_now, 
				'time_off': time_off
				}
		return self.postData(data, url)

	def set_device_name(self, name):
		url = "/xled/v1/device_name"
		data = {
			'name' : name
		}
		return self.postData(data, url)

	def get_device_name(self):
		url = "/xled/v1/device_name"
		return self.doGet(url)


	def get_network_scan(self):
		url = "/xled/v1/network/scan"
		return self.doGet(url)

	def get_network_scan_results(self):
		url = "/xled/v1/network/scan_results"
		return self.doGet(url)

	def set_rt_frame(self, data):
		url = "/xled/v1/led/rt/frame"
		return self.postRaw(data, url)

	def udp_rt_frame(self, data, numLeds):
		header = [0] * 10
		frame[0] = 0x00
		frame = "".join(map(chr, frame))

	def get_driver_params(self):
		url = "/xled/v1/led/driver_params2"
		return self.doGet(url)

	def set_driver_params(self, timing_adjust_1=10, timing_adjust_2=62):
		url = "/xled/v1/led/driver_params2"
		data = {
				'timing_adjust_2': timing_adjust_2, 
				'timing_adjust_1': timing_adjust_1
				}
		return self.postData(data, url)

	def get_mqtt(self):
		url = "/xled/v1/mqtt/config"
		return self.doGet(url)

	def set_led_config(self, first_led_id = 0, length = 200):
		url = "/xled/v1/led/config"
		data = {'strings': [{'first_led_id': first_led_id, 'length': length}]}
		return self.postData(data,url)

	def get_led_config(self):
		url = "/xled/v1/led/config"
		return self.doGet(url)

	def get_network_status(self):
		url = "/xled/v1/network/status"
		return self.doGet(url)

	def set_echo(self, message):
		url = "/xled/v1/echo"
		data = message
		return self.postData(data, url)

	def get_production_info(self):
		url = "/xled/v1/production_info"
		return self.doGet(url)

	def get_status(self):
		url = "/xled/v1/status"
		return self.doGet(url)

	def get_reset_2(self):
		url = "/xled/v1/led/reset2"
		return self.doGet(url)

	def get_offsets(self):
		url = "/xled/v1/fw/offsets"
		return self.doGet(url)

	def draw_clock(self):
		now = datetime.now()
		mins = ""	
		
		self.set_rt_mode()
		while True:
			now = datetime.now()

			hours = now.strftime("%H")
			mins = now.strftime("%M")
			seconds = now.strftime("%S")

			font = ImageFont.truetype('/root/twinkly/small_pixel.ttf', size=8)

			(x, y) = (0, 0)

			#draw hours and mins


			color = 'rgba(0, 0, 0, 255)' 
			col = (int(seconds) / 60 * 255)

			#active Spot colors
			A = int((int(seconds) % 6)/5*255)
			R = int((int(seconds) % 6)/5*255)
			G = int((int(seconds) % 6)/5*255)
			B = int((int(seconds) % 6)/5*255)
			

			secondscolor = "rgba(" + str(255) + "," + str(255) + "," + str(255) + ",0)"
			bri = int(seconds)/60/ledwidth*255
			secondscoloractive = "rgba(" + str(R) + "," + str(G) + "," + str(B) + "," + str(A) + ")"
			# draw the message on the background

			t = 0

			while len(hours) < 2:
				hours = "0" + hours
			while len(mins) < 2:
				mins = "0" + mins


			mat = numpy.zeros([ledwidth,ledheight], dtype = tuple)

			#Stunden
			(x, y) = (1, 0)
			im = Image.new(mode = "RGBA", size = (ledwidth,ledheight), color = (0,0,0,0))
			draw = ImageDraw.Draw(im)
			draw.text((x, y), hours, fill=color, font=font)
			#Minuten
			(x, y) = (1, 11)
			draw.text((x, y), mins, fill=color, font=font)
			#Sekundenbalken
			(x,y) = (0,20)
			draw.line([(x,y),((int(seconds)/60)*ledwidth,y)],fill=secondscolor,width = 1)
			draw.line([((int(seconds)/60)*ledwidth,y),((int(seconds)/60)*ledwidth,y)],fill=secondscoloractive,width = 1)

			arr = image_to_bytestr(im,ledwidth,ledheight)

			self.set_rt_frame(arr)
			time.sleep(1)
			



	def draw_text(self, message):

		font = ImageFont.truetype('/root/twinkly/small_pixel.ttf', size=14)

		(x, y) = (0, 0)

		if message == "":
			message = input("Text: ")

		origcolor = 'rgb(255, 255, 255)' 

		# draw the message on the background

		self.set_rt_mode()
		t = 0

		for letter in message:
			
			if letter == "<" or letter == "3":
				color = 'rgb(255, 0, 0)'
			else:
				color = origcolor


			(x, y) = (0, 0)
			im = Image.new(mode = "RGB", size = (ledwidth,ledheight), color = (0,0,0))
			draw = ImageDraw.Draw(im)
			draw.text((x, y), letter, fill=color, font=font)

			arr = image_to_bytestr(im,ledwidth,ledheight)
			self.set_rt_frame(arr)

			time.sleep(1)
			arr = bytearray.fromhex("00"*4*ledwidth*ledheight)
			self.set_rt_frame(arr)
			t = t + 1
			time.sleep(0.02)


		self.set_off_mode()
		return True

	def play_video(self, filepath):

		self.set_rt_mode()

		# Read the video from specified path 
		cam = cv2.VideoCapture(filepath) 
		
		try: 
			
			# creating a folder named data 
			if not os.path.exists('data'): 
				os.makedirs('data') 
		
		# if not created then raise error 
		except OSError: 
			print ('Error: Creating directory of data') 
		
		# frame 
		currentframe = 0

		while(True): 

			# reading from frame 
			ret,frame = cam.read() 
			

			if ret: 
			# if video is still left continue creating images 

				print("Frame: " + str(currentframe))
				dimx = frame.shape[0]
				dimy = frame.shape[1]

				R = 0
				G = 0
				B = 0

				arr = bytearray()

				reframe = cv2.resize(frame,(ledwidth,ledheight),cv2.INTER_AREA)

				byteout = frame_to_bytestr(reframe,ledwidth,ledheight)

				self.set_rt_frame(byteout)

				#time.sleep(0.04)



				# increasing counter so that it will 
				# show how many frames are created 
				currentframe += 1
			else: 
				break
		
		# Release all space and windows once done 
		cam.release() 

	def play_movie(self, filepath):

		

		# Read the video from specified path 
		cam = cv2.VideoCapture(filepath) 
		
		try: 
			
			# creating a folder named data 
			if not os.path.exists('data'): 
				os.makedirs('data') 
		
		# if not created then raise error 
		except OSError: 
			print ('Error: Creating directory of data') 
		
		# frame 
		currentframe = 0
		byteout = bytearray()

		while(True): 

			# reading from frame 
			ret,frame = cam.read() 
			

			if ret: 
			# if video is still left continue creating images 

				print("Frame: " + str(currentframe))
				dimx = frame.shape[0]
				dimy = frame.shape[1]

				R = 0
				G = 0
				B = 0

				

				reframe = cv2.resize(frame,(ledwidth,ledheight),cv2.INTER_AREA)

				byteout = byteout + frame_to_bytestr(reframe,ledwidth,ledheight)

				
				currentframe += 1
			else: 
				break
		
		# Release all space and windows once done 
		cam.release() 
		
		self.uploadMovie(byteout)
		self.set_movie_mode()
		self.set_movie_config(42,ledwidth*ledheight,currentframe)
		self.get_led_reset()

	def play_image(self, filepath):


		im = cv2.imread(filepath) 
		
		byteout = bytearray()

		R = 0
		G = 0
		B = 0
		mat = numpy.zeros([ledheight,ledwidth], dtype = tuple)
		
		im = cv2.imread(filepath)
		origx = im.shape[0]
		origy = im.shape[1]
		ratio = origx/ledwidth
		stretchfactor = 1.5

		reframe = cv2.resize(im,(ledwidth,int(origy/ratio*stretchfactor)),cv2.INTER_AREA)
		
		t = 0
		rendimg = numpy.zeros([ledheight,ledwidth], dtype = tuple)
		for x in range(0,ledwidth):
			for y in range(0,ledheight):
				try:
					rendimg[y][x] = reframe[y][x]
				except:
					rendimg[y][x] = [0, 0, 0]

				t = t + 1

		 
		byteout = byteout + frame_to_bytestr(rendimg,ledwidth,ledheight)

		
		self.uploadMovie(byteout)
		self.set_movie_mode()
		self.set_movie_config(1,ledwidth*int(origy/ratio),1)
		self.get_led_reset()

def image_to_bytestr(img,dimx,dimy):

	mat = numpy.zeros([dimx,dimy], dtype = tuple)

	arr = bytearray()

	for x in range(dimx):
		for y in range(dimy):
			mat[x][y] = img.getpixel((x,y))
			A = '%02X' % mat[x][y][3]
			R = '%02X' % mat[x][y][0]
			G = '%02X' % mat[x][y][1]
			B = '%02X' % mat[x][y][2]

			arr = arr + bytearray.fromhex(A + R + G + B) #A R G B


	return arr
	
def frame_to_bytestr(frame,dimx,dimy):
	ledwidth = dimx
	ledheight = dimy
	arr = bytearray()
	mat = numpy.zeros([ledheight,ledwidth], dtype = tuple)

	for x in range(ledwidth):
		for y in range(ledheight):
			B = frame[y][x][0]
			G = frame[y][x][1]					
			R = frame[y][x][2]

			mat[y][x] = (R,G,B)


			A = '%02X' % 0
			R = '%02X' % mat[y][x][0]
			G = '%02X' % mat[y][x][1]
			B = '%02X' % mat[y][x][2]

			arr = arr + bytearray.fromhex(A + R + G + B) #A R G B
	return arr


twi = twinkly()
ledwidth = 10
ledheight = 21

twi.login()
#twi.draw_text("  Peroxo <3 ") #draw text to curtain
#twi.play_video("B:\Google Drive\Desktop\AC Biologen Zusammenfassung.mp4") #stream live to curtain
#twi.play_movie("B:\Google Drive\Desktop\Komp 1_1.mp4") #upload movie to curtain
#twi.play_image("B:\\Google Drive\\Desktop\\1200px-Flat_tick_icon.png") #draw image to curtain
twi.draw_clock()


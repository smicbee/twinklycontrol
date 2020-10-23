import twinklycontrol

ledwidth = 10
ledheight = 21
twi = twinklycontrol.twinkly('192.168.0.13',ledwidth,ledheight)
twi.login()

#twi.play_movie("arrowanimated.mp4")

while True:
	twi.draw_clock()
	twinklycontrol.time.sleep(0.05)

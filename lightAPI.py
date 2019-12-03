import pigpio

class lightAPI:
	pi = pigpio.pi()
	RED_PIN = 17
	GREEN_PIN = 22
	BLUE_PIN = 24
	colorQueue = []
	
	def getCurrentColor():
		currentColor = open("cc.txt", "r")
		pushCol = currentColor.read()
		currentColor.close()
		return pushCol

	def changeLights(hexCode):
		currentColor = open("cc.txt", "w+")
		currentColor.write(hexCode)
		currentColor.close()
		hexCodeReal = hexCode[1:7]
		slashedRGB = "/" + "/".join(str(i) for i in tuple(int(hexCodeReal[i:i + len(hexCodeReal) // 3], 16) for i in range(0, len(hexCodeReal), len(hexCodeReal) // 3)))
		slashedRGB = slashedRGB[1:len(slashedRGB)]
		rgbarray = slashedRGB.split('/')
		rgbarray = [int(x) for x in rgbarray]
		for i in range(0, 3):
			if(rgbarray[i] < 0):
				rgbarray[i] = 0;
			if(rgbarray[i] > 255):
				rgbarray[i] = 255;
		pi.set_PWM_dutycycle(RED_PIN, rgbarray[0])
		pi.set_PWM_dutycycle(GREEN_PIN, rgbarray[1])
		pi.set_PWM_dutycycle(BLUE_PIN, rgbarray[2])

	def changeLightsOR(hexCode, durration):
		pass

	def addToQueue(hexCode, user):
		pass

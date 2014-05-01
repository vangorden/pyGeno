import sys, time

class ProgressBar :
	"A very simple unthreaded progress bar, see ProgressBar  __name__ == '__main__' for an ex of utilisation"
	def __init__(self, nbEpochs = -1, width = 25, label = "progress", minRefeshTime = 0.1) :
		"if you don't know the maximum number of epochs you can enter nbEpochs < 1"
		
		self.width = width
		self.currEpoch = 0
		self.nbEpochs = float(nbEpochs)
		self.bar = ''

		self.label = label
		self.wheel = ["-", "\\", "|", "/"]
		self.startTime = time.time()
		self.lastPrintTime = 0
		self.minRefeshTime = minRefeshTime
		
		self.elTime = 0
		self.runtime = 0
		self.avg = 0
		self.remtime = -1
		
		self.bars = []
		self.miniSnake = '~-~-~-?:>' 
		
	def formatTime(self, val) :
		if val < 60 :
			return '%.3fsc' % val
		elif val < 3600 :
			return '%.3fmin' % (val/60)
		else :
			return '%dh %dmin' % (int(val)/3600, int(val/60)%60)

	def update(self, label = '', forceRefrech = False) :
		self.currEpoch += 1
		if (time.time() - self.lastPrintTime > self.minRefeshTime) or forceRefrech :
			wheelState = self.wheel[self.currEpoch%len(self.wheel)]
			self.elTime = time.time() - self.startTime
			self.runtime = self.formatTime(self.elTime)
			self.avg = self.elTime/self.currEpoch
			if label == '' :
				slabel = self.label
			else :
				slabel = label
			
			if self.nbEpochs > 1 :
				ratio = self.currEpoch/self.nbEpochs
				snakeLen = int(self.width*ratio)
				voidLen = int(self.width - (self.width*ratio))

				if snakeLen + voidLen < self.width :
					snakeLen = self.width - voidLen
				
				self.remtime = self.formatTime(self.avg * (self.nbEpochs-self.currEpoch))

				self.bar = "%s %s[%s:>%s] %.3f%% (%d/%d) runtime: %s, remaing: %s, avg: %s" %(wheelState, slabel, "~-" * snakeLen, "  " * voidLen, ratio*100, self.currEpoch, self.nbEpochs, self.runtime, self.remtime, self.formatTime(self.avg))
				if self.currEpoch == self.nbEpochs :
					self.close()
			else :
				w = self.width - len(self.miniSnake)
				v = self.currEpoch%(w+1)
				snake = "%s%s%s" %("  " * (v), self.miniSnake, "  " * (w-v))
				self.bar = "%s %s[%s] %s%% (%d/%s) runtime: %s, remaing: %s, avg: %s" %(wheelState, slabel, snake, '?', self.currEpoch, '?', self.runtime, '?', self.formatTime(self.avg))
			
			sys.stdout.write("\b" * (len(self.bar)+1))
			sys.stdout.write(" " * (len(self.bar)+1))
			sys.stdout.write("\b" * (len(self.bar)+1))
			sys.stdout.write(self.bar)
			sys.stdout.flush()
			self.lastPrintTime = time.time()
	
	def close(self) :
		self.update(forceRefrech = True)
		print
	
if __name__ == '__main__' :
	p = ProgressBar(nbEpochs = -1)
	for i in range(200000) :
		p.update(label = 'value of i %d' % i)
		time.sleep(0.5)
		

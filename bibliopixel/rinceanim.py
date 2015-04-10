import time
import log

from bibled import LEDMatrix
from bibled import LEDStrip
import colors

class BaseAnimation(object):
    def __init__(self, led):
        self._led = led
        self.animComplete = False
        self._step = 0
        self._timeRef = 0
        self._internalDelay = None

    def _msTime(self):
        return time.time() * 1000.0

    def preRun(self):
        pass

    def step(self, amt = 1):
        raise RuntimeError("Base class step() called. This shouldn't happen")

    def run(self, amt = 1, fps=None, sleep=None, max_steps = 0, untilComplete = False, max_cycles = 0):
        """
        untilComplete makes it run until the animation signals it has completed a cycle
        max_cycles should be used with untilComplete to make it run for more than one cycle
        """
        self.preRun()

        #calculate sleep time base on desired Frames per Second
        if sleep == None and fps != None:
            sleep = int(1000 / fps)


        initSleep = sleep

        self._step = 0
        cur_step = 0
        cycle_count = 0
        self.animComplete = False

        while (not untilComplete and (max_steps == 0 or cur_step < max_steps)) or (untilComplete and not self.animComplete):
            self._timeRef = self._msTime()

            start = self._msTime()
            self.step(amt)
            mid = self._msTime()

            if initSleep:
                sleep = initSleep
            elif self._internalDelay:
                sleep = self._internalDelay

            self._led._frameGenTime = int(mid - start)
            self._led._frameTotalTime = sleep
            
            self._led.update()
            now = self._msTime()

            if self.animComplete and max_cycles > 0:
                if cycle_count < max_cycles - 1:
                    cycle_count += 1
                    self.animComplete = False

            stepTime = int(mid - start)
            if self._led._threadedUpdate:
                updateTime = int(self._led.lastThreadedUpdate())
                totalTime = updateTime
            else:
                updateTime = int(now - mid)
                totalTime = stepTime + updateTime

            

            if self._led._threadedUpdate:
                log.logger.debug("Frame: {}ms / Update Max: {}ms".format(stepTime, updateTime))
            else:
                log.logger.debug("{}ms/{}fps / Frame: {}ms / Update: {}ms".format(totalTime, int(1000 / max(totalTime,1)), stepTime, updateTime))

            if sleep:
                diff = (self._msTime() - self._timeRef)
                t = max(0, (sleep - diff) / 1000.0)
                if t == 0:
                    log.logger.warning("Frame-time of %dms set, but took %dms!" % (sleep, diff))
                time.sleep(t)
            cur_step += 1

class BaseMatrixAnim(BaseAnimation):
    def __init__(self, led, width=0, height=0, startX=0, startY=0):
        super(BaseMatrixAnim, self).__init__(led)
        #if not isinstance(led, LEDMatrix):
        #    raise RuntimeError("Must use LEDMatrix with Matrix Animations!")

        if width == 0:
            self.width = led.width
        else:
            self.width = width

        if height == 0:
            self.height = led.height
        else:
            self.height = height

        self.startX = startX
        self.startY = startY

class LightningBibTest(BaseMatrixAnim):
    def __init__(self, led):
        super(LightningBibTest, self).__init__(led, 0, 0)
        self._internalDelay = 500
        self.colors =  [colors.Blue, colors.White]

    def step(self, amt = 1):
        
        self._led.drawLine(0, 0, 0, self.height - 1, colors.Blue)
        self._led.drawLine(1, 0, 1, self.height - 1, colors.White)
        self._led.drawLine(2, 0, 2, self.height - 1, colors.White)
        self._led.drawLine(3, 0, 3, self.height - 1, colors.Blue)
        self._led.drawLine(4, 0, 4, self.height - 1, colors.Blue)
        self._led.drawLine(5, 0, 5, self.height - 1, colors.Blue)

        color =  self._step % 4
#        self._led.fillRect(7, 0, 3, self.height, self.colors[color])

        self._step += 1

class LightningBibText(BaseMatrixAnim):
    def __init__(self, led):
        super(LightningBibText, self).__init__(led, 0, 0)
        self._internalDelay = 400
        self.colors =  [colors.Blue, colors.White]

    def step(self, amt = 1):

        mytext = 'Hello aa'
        mylen = len(mytext)
        mypos = mylen*5+5-self._step

	self._led.drawBibText(mytext,x=mypos,y=0,color=colors.White, bg=colors.Blue)

	self._step += 1
        


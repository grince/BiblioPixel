from bibliopixel.bibled import *
from bibliopixel.rinceanim import LightningBibText
#from bibliopixel.animation import StripChannelTest
#from bibliopixel.drivers.LPD8806 import *
from bibliopixel.drivers.visualizer import DriverVisualizer

#create driver for a 12x12 grid, use the size of your display
#driver = DriverLPD8806(9*9*4)
driver = DriverVisualizer(width = 9*4, height = 9, stayTop = True)
#led = LEDMatrix(driver, rotation = MatrixRotation.ROTATE_0, vert_flip = True, serpentine = False)
led = LEDMatrix(driver)
#led = LEDStrip(driver)

anim = LightningBibText(led)
#anim = StripChannelTest(led)
anim.run()

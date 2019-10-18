# Single Color RGB565 Blob Tracking Example
#
# This example shows off single color RGB565 tracking using the OpenMV Cam.

import sensor, image, time, math,pyb
from pyb import UART
import cpufreq
threshold_index = 0 # 0 for red, 1 for green, 2 for blue

# Color Tracking Thresholds (L Min, L Max, A Min, A Max, B Min, B Max)
# The below thresholds track in general red/green/blue things. You may wish to tune them...
#thresholds = [(((55, 0, 127, 26, -13, 127))) # generic_red_thresholds
#               # generic_green_thresholds
#] # generic_blue_thresholds
thresholds= [(42, 84, 42, 127, -13, 79)]

sensor.reset()
#sensor.set_auto_exposure(False,value = 1000)
cpufreq.set_frequency(216)
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.VGA)
sensor.set_windowing((0,200,600,110))
sensor.skip_frames(time = 2000)
sensor.set_auto_gain(False) # must be turned off for color tracking
sensor.set_auto_whitebal(False) # must be turned off for color tracking
#sensor.set_auto_exposure(False,9000)
clock = time.clock()

red=pyb.LED(1)
green=pyb.LED(2)
blue=pyb.LED(3)
uart = UART(3, 115200)
def find_max(blobs):
    max_size=0
    for blob in blobs:
        if blob[2]*blob[3] > max_size:
            max_blob=blob
            max_size = blob[2]*blob[3]
        return max_blob
# Only blobs that with more pixels than "pixel_threshold" and more area than "area_threshold" are
# returned by "find_blobs" below. Change "pixels_threshold" and "area_threshold" if you change the
# camera resolution. "merge=True" merges all overlapping blobs in the image.

while(True):
    clock.tick()
    blue.on()
    #img = sensor.snapshot()
    img = sensor.snapshot()
    #img.laplacian(1, sharpen=True)
    #print(sensor.get_exposure_us())
    #uart.write("123123\n")
    blobs=img.find_blobs([thresholds[threshold_index]],pixels_threshold=20, area_threshold=20, merge=True)
    if blobs:
        max_blob = find_max(blobs)
        size1=max_blob[2]*max_blob[3]
        #print(str(size1))
        if size1>500 and size1<1800:
            #print('1')
            # These values depend on the blob not being circular - otherwise they will be shaky.
            # These values are stable all the time.
            #img.draw_rectangle(blob.rect())
            img.draw_cross(max_blob.cx(), max_blob.cy())
            # Note - the blob rotation is unique to 0-180 only.
            #img.draw_keypoints([(blob.cx(), blob.cy(), int(math.degrees(blob.rotation())))])
            a=max_blob.cx()
            b=max_blob.cy()
            if max_blob.cx() >=100:
                uart.write(str(a))
                #print(str(a))
            elif max_blob.cx() >=10:
                uart.write('0'+str(a))
                #print('0'+str(a))
            else :
                uart.write('00'+str(a))
                #print('00'+str(a))
            if max_blob.cy() >=100:
    #           uart.write(" ")
                uart.write(str(b))
                #print(str(b))
            elif max_blob.cy() >=10:
                uart.write('0'+str(b))
                #print('0'+str(b))
            else :
                uart.write('00'+str(b))
                #print('00'+str(b))
            uart.write('\n')
            if max_blob.cx()>=295 and max_blob.cx()<305:
                green.on()
            else:
                green.off()
    #else:
        #uart.write("999999\n")
        #print('\n')

        #break
#        uart.write(str(b))
#        uart.write(str(a))
#        uart.write(" ")
#        uart.write(str(b))
#        uart.write("\r\n")
#    uart.write("fps=")
#    uart.write(str(clock.fps()))
#    uart.write("\r\n")
#    print(clock.fps())

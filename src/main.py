# This program is made to determine the ideal focal length for a camera to image an area of land from any altitude in any time with any sensor, and by product, the flight speed.
import math 
import sys
defaultFieldLength = 300 # in meters
defaultFieldWidth = 200 # in meters
idealSensorWidth = 13.2 # in millimeters; this is the ideal sensor width for us; Liang approved
idealSensorHeight = 8.8 # in millimeters; this is the ideal sensor height for us; Liang approved
defaultAltitude = 50 # in meters
defaultFocalLength = 30 # in millimeters
defaultOverlapPercentage = 65 # in percentage form without the percent sign, eg: 65 for 65%
defaultMinutes = 30 # in minutes

def fieldArea(fieldLength, fieldWidth):
    return fieldLength*fieldWidth

def widthOfImage(sensorWidth, altitude, focalLength): # gets the width of an image by multiplying the sensor width with the altitude and dividing it by the focal length
    if focalLength <= 0:
        print("You cannot have your focal length be 0 or less")
        sys.exit()
    return sensorWidth*altitude/focalLength

def heightOfImage(sensorHeight, altitude, focalLength): # same as widthOfImage but with height
    return sensorHeight*altitude/focalLength

def areaOfImage(sensorWidth, sensorHeight, altitude, focalLength): # gets the area of an image before accounting for overlap by multiplying the width and height
    return widthOfImage(sensorWidth, altitude, focalLength)*heightOfImage(sensorHeight, altitude, focalLength)
    
def areaOfImageWithOverlap(sensorWidth, sensorHeight, altitude, focalLength, overlapInPercentage): # gets the area of an image after accounting for overlap
    return areaOfImage(sensorWidth, sensorHeight, altitude, focalLength)*(1-overlapInPercentage/100)**2 # give the overlap as a percentage without the percent sign, such as 65 for 65% image overlap

def imagesNeeded(fieldLength, fieldWidth, sensorWidth, sensorHeight, altitude, focalLength, overlapInPercentage): # gets the number of images needed to map out the area by dividing the total area by the area of each image after accounting for overlap and then rounding up
    return rowsNeeded(fieldWidth, sensorWidth, altitude, focalLength, overlapInPercentage)*columnsNeeded(fieldLength, sensorHeight, altitude, focalLength, overlapInPercentage)

def rowsNeeded(fieldWidth, sensorWidth, altitude, focalLength, overlapInPercentage): # gets the number of rows needed by dividing the field's width by the effective width of each image
    return math.ceil(fieldWidth/(widthOfImage(sensorWidth, altitude, focalLength)*(1-overlapInPercentage/100))) # width of image is perpendicular to flight
    
def columnsNeeded(fieldLength, sensorHeight, altitude, focalLength, overlapInPercentage): # gets the number of columns needed by dividing the field's length by the effective height of each image
    return math.ceil(fieldLength/(heightOfImage(sensorHeight, altitude, focalLength)*(1-overlapInPercentage/100))) # height of image is parallel to flight

def transitionDistance(fieldWidth, sensorWidth, altitude, focalLength, overlapInPercentage): # finds the distance it takes to transition between rows
    return (rowsNeeded(fieldWidth, sensorWidth, altitude, focalLength, overlapInPercentage)-1)*((widthOfImage(sensorWidth, altitude, focalLength))*(1-overlapInPercentage/100))
    
def totalDistance(fieldLength, fieldWidth, sensorWidth, sensorHeight, altitude, focalLength, overlapInPercentage): # finds the total distance by multiplying the length of the field by the number of rows needed, then adding the transition distance
    return fieldLength*rowsNeeded(fieldWidth, sensorWidth, altitude, focalLength, overlapInPercentage)+transitionDistance(fieldWidth, sensorWidth, altitude, focalLength, overlapInPercentage)

def minimumSpeed(fieldLength, fieldWidth, sensorWidth, sensorHeight, altitude, focalLength, overlapInPercentage, minutesGiven):
    return totalDistance(fieldLength, fieldWidth, sensorWidth, sensorHeight, altitude, focalLength, overlapInPercentage)/(minutesGiven*60)
    
    # give the field length, field width, sensor width, sensor height, altitude, focal length, overlap of photos in percentage form without the percent sign (ex: 65 for 65%) and minutes given

print("Images needed: {}".format(imagesNeeded(defaultFieldLength, defaultFieldWidth, idealSensorWidth, idealSensorHeight, defaultAltitude, defaultFocalLength, defaultOverlapPercentage)))
print("Rows needed: {}".format(rowsNeeded(defaultFieldWidth, idealSensorWidth, defaultAltitude, defaultFocalLength, defaultOverlapPercentage)))
print("Columns needed: {}".format(columnsNeeded(defaultFieldLength, idealSensorHeight, defaultAltitude, defaultFocalLength, defaultOverlapPercentage)))
print("Minimum speed required: {}".format(minimumSpeed(defaultFieldLength, defaultFieldWidth, idealSensorWidth, idealSensorHeight, defaultAltitude, defaultFocalLength, defaultOverlapPercentage, defaultMinutes)))
    
    

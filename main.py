""" This will approimate lens shappe for aspheric lens to focus at a single point."""

from lenses import Lens1
from lenses import Lens2
from lenses import completeLens
from light import Light
from display import Display
from makeSVG import saveSVG


#numberLightRays = 00
lens1Front = 0
focalPoint = 250
lensHeight = 100
numSegments = 10
n1 = 1.0
n2 = 1.495

filename = "height" + str(lensHeight) + "fp" + str(focalPoint)
print(f"filename = {filename}")

light = []
lens1 = Lens1(focalPoint, lensHeight, numSegments, n1, n2)
finishLens = completeLens()

n1 = 1.495
n2 = 1.0
scaleFactor = 0.1
lens2 = Lens2(n1, n2, focalPoint, scaleFactor)

# Calculate coordinates for front lens
lens1.Inner()
# Add negative of coordinates to make complete front lens.
lens1XY = finishLens.lowerHalf(lens1.lensXY)
#print(lens1XY)



""" Set number light sources"""
numberLightRays = len(lens1.lensXY) -1
#print(numberLightRays)

# Light list for light objects

""" Create instance of light """
for rayNumber in range(numberLightRays):
    light.append(Light(rayNumber, lens1))

""" ADD LIGHT SOURCE POINTS """
for lightBeam in light:
    lightBeam.lightSource()

for lightBeam in light:
    lightBeam.rayLens1Intersection(lens1)

for lightBeam in light:
    lightBeam.refraction(lens1)

#print()
for lightBeam in light:
    lightBeam.rayExtension(5)
    #print(f"M52 lightBeam.angle {lightBeam.angle}")

#print()

#Find focal point to calculate second lens
lens2.findRayMidline(light)

lens2.formLens(light)

lens2XY = finishLens.lowerHalf(lens2.lensXY)
#print(lens2XY)

corners = []
corners = finishLens.lensCorners(lens1XY, lens2XY)

topCorner = [focalPoint + 25, lens1XY[-1][1]]
bottomCorner = [focalPoint + 25, lens1XY[0][1]]
print(f"focalLength = {focalPoint}")
#print(f"corners {corners}")


svgPoints = lens1XY
print(f"svgPoints {svgPoints}")

svgPoints.append(topCorner)
#lens2XY.reverse()

#for i in lens2XY:
#    svgPoints.append(i)

svgPoints.append(bottomCorner)
svgPoints.append(lens1XY[0])
print(f"svgPoints {svgPoints}")
#lens2XY.reverse()

minX, minY, maxX, maxY = svgPoints[0][0], svgPoints[0][1], svgPoints[0][0], svgPoints[0][1]
for i in svgPoints:
    if i[0] < minX:
        minX = i[0]
    if i[1] < minY:
        minX = i[1]
    if i[0] > maxX:
        maxX = i[0]
    if i[1] > maxY:
        maxY = i[1]

viewWidth = (maxX - minX)*1.1
viewHeight = (maxY - minY)*1.1
origX = minX - 0.05*viewWidth
origY = minY - 0.05*viewHeight

points = [[0,-90], [90,-30], [75,90], [-75,90], [-60,-30], [0,-90]]
laserImage = saveSVG(viewWidth, viewHeight, origX, origY, viewWidth, viewHeight, svgPoints)
print(f"filename {filename}")
laserImage.writeSVG(filename)



for lightBeam in light:
    lightBeam.rayLens2Intersection(lens2)
    pass



for lightBeam in light:
    lightBeam.refraction(lens2)
    #print(f"M73 lightBeam.angle {lightBeam.angle}")
    pass

#print(f"type(light): {type(light)}")
#print(f"light: {light[0].ray}")

for lightBeam in light:
    #lightBeam.rayExtension(100)
    pass


#******************************************8
toScreen = Display()



#drawLens
#toScreen.draw_Lens(lens1.lensXY, "RED") #***
#toScreen.drawLensLines(lens1.lensXY)

#toScreen.draw_Lens(lens2.lensXY, "RED") #***
#toScreen.drawLensLines(lens2.lensXY)

for lightBeam in light:
    #toScreen.draw_Source(lightBeam.ray)
    pass




# ************** COPY
toScreen.drawLensLines(lens1XY)
toScreen.drawLensLines(lens2XY)
toScreen.drawLensLines(corners[0])
toScreen.drawLensLines(corners[1])
toScreen.drawLensLines(corners[2])
toScreen.drawLensLines(corners[3])

#toScreen.draw_FocalPoint(lens1.fp)
toScreen.display_to_screen()



import math
from  calculations import LinAlg
class Lens1():

    def __init__(self, focalPoint, lensHeight, numSegments, n1, n2):
        self.fp = focalPoint
        self.lensHeight = lensHeight
        self.n1 = n1
        self.n2 = n2
        self.numSegs = numSegments
        self.segmentAngle = []
        self.dy = self.lensHeight / self.numSegs
        self.lensXY = [[0.0, 0.0]]
        self.lensXYMid = [[0.0, 0.0]]

    # print(f"30 thetaRay, theta1, theta2, segAngle, dx, x =  {thetaRay, self.theta1, self.theta2, self.segmentAngle[i]*180/math.pi, dx, x}")

    def findTheta1_Theta2(self, thetaR, n1, n2):
        """findTheta1_Theta2 documentation
        n1 sin(theta1) = n2 sin(theta(2)
        theta1 = theta2 - thetaR
        theta2 = theta1 + thetaR
        thetaR = theta2 - theta1
        n1 sint(theta1) = n2 sin(theta2)
        n1 sin(theta1) = n2 sin(theta1 + thetaR)
        n1 sin(theta1) = n2 sin(theta1) cos(thetaR) + n2 sin(thetaR) cos(theta1)
        n1 sin(theta1) - n2 sin(theta1) cos(thetaR) = n2 sin(thetaR) cos(theta1)
        sin(theta1) [ n1 - n2 cos(thetaR)] = n2 sin(thetaR) cos(theta1)
        sin(theta1) / cos(theta1) = [ n2 sin(thetaR) ] / [n1 - n2 cos(thetaR)]
        tan(theta1) = [ n2 sin(thetaR) ] / [n1 - n2 cos(thetaR)]
        theta1 = atan[ n2 sin(thetaR) ] / [n1 - n2 cos(thetaR)]
        ****
        n1 sin(theta1) = n2 sin(theta2)
        sin(theta2) = n1 sin(theta1) / n2
        theta2 = asin[ n1 sin(theta1) / n2 ]
        """

        theta1 = math.atan(n2 * math.sin(thetaR)  / (n1 - n2 * math.cos(thetaR)))
        theta2 = math.asin( n1 * math.sin(theta1) / n2 )
        return theta1, theta2


    def Inner(self):
        """Inner refers to lens closest to light source. *** I think***
        Calculate lens segment position and angle to focus to point fp
        Build lens segment by segment.
        1. dY = lens height / number of lens segments
        2. y = next point for calculating ray angles
            y = lens[-1][1] + dy/2
        3. xDist = dist from fp to middle of current segment
            middle current segment approx = lens[-1][0] + dy / tan(segmentAngle)
            xDist = fp = (lens[-1][0] + dy/2 / tan(segmentAngle[-1])
        4. final ray angle from to focal point to a point dy/2 directly above the top of last ray segment.
            Called in calculateAngles

            finalRayAngle = atan(atan(y / xDist)
        5. thetaR: change in angle from initialRayAngle to finalRayAngle
        6. Theta1 per double angle equation, n1, n2, thetaR
        7. Theta2 from theta1, n1, n2
        8. segment angle
        9. dX from dY and segment angle
        10. append [lens[-1][0] + dx, lens[-1][1] + dy] to lens
        """

        initialRayAngle = 0.0

        for segNum in range(self.numSegs):

            y = self.lensXY[-1][1] + self.dy / 2
            #print(f"segNum {segNum}    dy {self.dy}    lensXY[-1 {self.lensXY[-1]}    dy/2 {self.dy/2}")
            if len(self.segmentAngle) > 0:
                xDist = self.lensXY[-1][0] + self.dy / math.tan(self.segmentAngle[-1]) - self.fp
            else:
                xDist = (self.lensXY[-1][0] - self.fp)

            finalRayAngle = math.atan(y / xDist)

            thetaR = finalRayAngle - initialRayAngle
            n1, n2 = self.n1, self.n2
            theta1, theta2 = self.findTheta1_Theta2(thetaR, n1, n2)
            self.theta1, self.theta2 = theta1, theta2
            #print(f"theta1 = {theta1}   theta2 {theta2}")

            self.segmentAngle.append(initialRayAngle - self.theta1 + math.pi/2)
            #print(f"y = {y}   xDist = {xDist}   theta1 = {self.theta1*180/math.pi}   segmentAngle = {self.segmentAngle[-1]*180/math.pi}")
            # segment angle = initial ray angle - angle of incidence + 90


            dx = self.dy / math.tan(self.segmentAngle[segNum])
            # dx from dy and segment angle

            self.lensXY.append([self.lensXY[-1][0] + dx, self.lensXY[-1][1] + self.dy])
            #print(f"dx = {dx}   finalRayAngle = {finalRayAngle*180/math.pi}")
            #print()
            # print(f"segAngle = {self.segmentAngle[-1]*180/math.pi}")


class Lens2():


    def __init__(self, n1, n2, focalPoint, scaleFactor):

        self.n1 = n1
        self.n2 = n2
        self.fp = focalPoint
        self.scaleFactor = scaleFactor
        #self.position = position
        self.segmentAngle = []
        self.lensXY = []
        self.midRayLine = []


    def findRayMidline(self, light):
        """
        I. Find midline between adjacent rays
            A. midRay Angle, average angles ray[i] & ray[i+1]
            TO DO B. ray[i] and ray[i+1] intersection: midRX1, midY1
            C. midRay point 2, midRX2 = midRX1 + cos(midRAngle)...
            D. numRays - 1 midRayLine
            E. last midRayLine add angle"""

        midRayAngle = []
        for i in range(len(light)):
            # A. midRay Angle, average angles ray[i] & ray[i+1]
            if i <= len(light)-2:
                midRayAngle.append((light[i].angle[-1] + light[i+1].angle[-1]) / 2)
            if i == len(light)-2:
                deltaAngle = midRayAngle[i] - midRayAngle[i-1]
                midRayAngle.append(midRayAngle[i] + deltaAngle)

            # B. ray[i] and ray[i + 1] intersection: midRX1, midY1
            if i <= len(light) - 2:
                rayLine1 = [light[i].ray[-1], light[i].ray[-2]]
                rayLine2 = [light[i + 1].ray[-1], light[i + 1].ray[-2]]
                midRX1, midRY1 = LinAlg.line_intersection(rayLine1, rayLine2)
            if i == len(light) - 2:
                #print("xxx")
                midRX1, midRX1 = midRX1, midRX1
            #print(f"midRX1, midRY1 = {midRX1, midRY1}   i {i}")
            # C. midRay point midRX2 = midRX1 + cos(midRAngle)...
            midRX2 = midRX1 - 800 * math.cos(midRayAngle[i])
            midRY2 = midRY1 - 800 * math.sin(midRayAngle[i])
            # D. define midRayLine
            self.midRayLine.append([[midRX1, midRY1], [midRX2, midRY2]])
        #print(f"midRayAngle {midRayAngle}")
        #print(f"midRayLine {self.midRayLine}")


    def formLens(self, light):
        """Calculate lens segment position and angle to align light
                1. lENSxy[0][0] scaleFactor
                2. for i in range (len(rays)):
                    A. ThetaR = finalAngle - InitialAngle
                    B. theta1, theta2
                    C. Segment angle
                        i. midpointLens1Segment
                3 for j in range(len(middleRayLine)):
                    E. calculate segmentAngle
                3. for i in range (len(segmentAngle)):
                    A. segmentLine = [[x1, y1], [x2,y2]
                    B. segLine middleRay intersection

                    d. calculate lensSegment and ray intersection
                        i. rayLine
                        ii. segmentLine
                    """
        # 1. lENSxy[0][0] scaleFactor
        self.lensXY.append([self.fp - self.scaleFactor*self.fp, 0])
        #print(f"lensXY {self.lensXY}")
        # 2. for i in range (len(rays)):

        for i in range(len(light)):
            # A. ThetaR = finalAngle - InitialAngle
            initialRayAngle, finalRayAngle = light[i].angle[-1], 0.0
            thetaR = finalRayAngle - initialRayAngle
            # B. Calculate theta1, theta2
            self.theta1, self.theta2 = Lens1.findTheta1_Theta2(self, thetaR, self.n1, self.n2)
            #print(f"middleRay = {self.midRayLine[i]}  lightAngle {light[i].angle[1]*180/math.pi}")

            # C. calculate segmentAngle
            self.segmentAngle.append(initialRayAngle - self.theta1 + math.pi / 2)
            #print(f"segmentAngle {self.segmentAngle}")


        numsegs = len(self.segmentAngle)

        for i in range(len(self.segmentAngle)):
            # A. segmentLine
            segX = self.lensXY[i][0] + math.cos(self.segmentAngle[i])
            segY = self.lensXY[i][1] + math.sin(self.segmentAngle[i])
            segmentLine = [self.lensXY[i], [segX, segY]]
            #print(f"segLine = {segmentLine}")
            # B. segLine middleRay intersection
            lX, lY = LinAlg.line_intersection(segmentLine, self.midRayLine[i])
            self.lensXY.append([lX, lY])
            #print(f"lensXY = {self.lensXY}")
            #print(light[i].ray[-1])


class completeLens():
    def __init__(self):
        pass

    def lowerHalf(self, lensPts):
        """ from finishLens in main
            1. Create list copyLens to hold positive and negative values for complete lens
            2. Add (x, y) values of original lens to copyLens
            3. add (x, -y) values to copyLens for negative values
            """
        #1.  Create list copyLens to hold positive and negative values for complete lens
        copyLlens = []
        #2. Add (x, y) values of original lens to copyLens
        for pt in lensPts:
            copyLlens.append(pt)
        #3. add (x, -y) values to copyLens for negative values
        for i in range(1, len(lensPts)):
            # print(f"lensPts = {lensPts[i][0], -1*lensPts[i][1]}")
            copyLlens.insert(0, [lensPts[i][0], -1 * lensPts[i][1]])
        #print(copyLlens)
        return copyLlens


    def lensCorners(self, lens1XY, lens2XY):
        uX, uY = [lens2XY[-1][0] ,lens1XY[-1][1]]
        bX, bY = [lens2XY[0][0], lens1XY[0][1]]
        topLine = [[lens1XY[-1][0], lens1XY[-1][1]],[uX, uY]]
        topBack = [[uX, uY], [lens2XY[0][0], lens2XY[-1][1]]]
        lowBack = [[lens2XY[0][0], lens2XY[0][1]], [bX, bY]]
        lowLine = [[bX, bY], [lens1XY[0][0], lens1XY[0][1]]]
        return [topLine, topBack, lowBack, lowLine]

    def svgCorners(self, lens1XY, lens2XY):
        uX, uY = [lens2XY[-1][0] ,lens1XY[-1][1]]
        bX, bY = [lens2XY[0][0], lens1XY[0][1]]
        topCorner = [uX, uY]
        bottomCorner = [bX, bY]
        return topCorner, bottomCorner


#toScreen.copyAndDisplay(lens2)
"""Make a new function/method that creates two new lists for the points in lens1 and lens2
They will have copies of all the values except at y == 0.
This method will be called copyAndDisplay
"""

import math

import lenses
from lenses import Lens1
from calculations import LinAlg


class Light():
    """Light class for light objects"""
    def __init__(self, rayNumber, lens):
        self.rayNumber = rayNumber
        # print(f"10 rayNumber = {self.rayNumber}")
        # self.source = [-200, 0]
        # print(f"source = {self.source}")
        self.ray = []
        self.angle = [0.0]
        self.lensCoords = [lens.lensXY[self.rayNumber], lens.lensXY[self.rayNumber + 1]]
        self.segmentNumber = []


    """ LIGHT SOURCES """
    def lightSource(self):
        """First Lest Segment"""
        segmentCenter = (self.lensCoords[0][1] + self.lensCoords[1][1]) / 2
        self.ray.append([-200, segmentCenter])

        # self.ray.append([-100, segmentCenter])
        #print(self.ray)


    def rayLens1Intersection(self, lens):
        rX1, rY1 = self.ray[-1][0], self.ray[-1][1]
        rX2, rY2 = rX1 + 100 * math.cos(self.angle[-1]), rY1 + 100 * math.sin(self.angle[-1])
        lineR = [[rY1, rY1], [rX2, rY2]]
        for i in range(1, len(lens.lensXY)):
            lX1, lY1 = lens.lensXY[i-1][0], lens.lensXY[i-1][1]
            lX2, lY2 = lens.lensXY[i][0], lens.lensXY[i][1]
            lineL = [[lX1, lY1],[lX2, lY2]]
            intersectionPoint = LinAlg.line_intersection(lineR, lineL)
            if intersectionPoint[1] >= lY1 and intersectionPoint[1] <= lY2:
                self.ray.append([intersectionPoint[0], intersectionPoint[1]])
                self.segmentNumber.append(i-1) # i-1 because list starts at 0 and i starts at 1


    def refraction(self, lens):
        """rayNumber + 1 = lens Segment number."""
        #print(f"lens.XY = {lens.lensXY}")
        #print(f"self.segmentNumber[-1] = {self.segmentNumber[-1]}")
        #print(f"segnumbers = {self.segmentNumber}")
        #print(f"lens.segmentAngle[self.segmentNumber[-1]] = {lens.segmentAngle[self.segmentNumber[-1]]}")

        normalAngle = lens.segmentAngle[self.segmentNumber[-1]] - math.pi/2
        unitNormalVector = [math.cos(normalAngle), math.sin(normalAngle)]
        rayUnitVector = [math.cos(self.angle[-1]), math.sin(self.angle[-1])]
        dotProd = LinAlg.dotProd(self, unitNormalVector, rayUnitVector)
        # Compute dot product. if angle is obtuse unitNormalVectro wil be multiplied by -1
        if dotProd < 0:
            unitNormalVector = LinAlg.scalarMultiplication(self, -1, unitNormalVector)
        # Use cross product ot find sin(theta)
        crossProd = LinAlg.crossProd(self, unitNormalVector, rayUnitVector)
        angleOfIncidence = math.asin(crossProd)
        # Compute angle of refraction
        angleOfRefraction = lens.n1 * math.asin(math.sin(angleOfIncidence) / lens.n2)
        #light angle = normal angle + angle of refraction
        lightAngle = self.angle[-1] + normalAngle + angleOfRefraction
        self.angle.append(lightAngle)

        #print(f"51 segmentnumber = {self.segmentNumber[-1]},   segment angle = {lens.segmentAngle[self.segmentNumber[-1]] * 180 / math.pi},   normalAngle = {normalAngle*180/math.pi},    normVector = {unitNormalVector},   rayNormVector = {rayUnitVector}")
        #print(f"52 dotProd = {dotProd},   crossProd = {crossProd},   angleOfIncidence = {angleOfIncidence*180/math.pi},  n1 = {lens.n1}, n1 = {lens.n2},   angleOfRefraction = {angleOfRefraction*180/math.pi}   lightAngle = {lightAngle*180/math.pi}")


    def rayLens2Intersection(self, lens):
        """Intersection point of light and lens2
            1. lineRay: [ray[-2], ray[-1]]
            2. Loop through lens segments
                A. lineLens
                B. intersection rayLine lensLine
                C. check point is in lens segment
                    1. if yes append point to ray"""
        # 1. lineRay: [ray[-2], ray[-1]]
        lineRay = [self.ray[-2], self.ray[-1]]
        for i in range(1, len(lens.lensXY)):
            # A. lineLens lens
            if i < len(lens.lensXY):
                lineLens = [lens.lensXY[i-1], lens.lensXY[i]]
            # B. intersection rayLine lensLine
            x, y = LinAlg.line_intersection(lineRay, lineLens)
            # C. check point is in lens segment
            if y > lens.lensXY[i-1][1] and y < lens.lensXY[i][1]:
                # 1. if yes append point to ray"""
                self.ray.append([x, y])
                self.angle.append(self.refractionlens2(lineLens, lineRay, lens.n1, lens.n2))
                #print(f"angle = {self.angle}")
                self.rayExtension(100)
                #print(self.ray)

    def refractionlens2(self, lXY, rXY, n1, n2):
        """Refraction Lens 2
        A. normalLensVector
        B. unitNormalVector
        C. unitRayVector
        D. crossProduct(unitNormalVector, unitRayVector)
            1. if corssprod negative
                a. unitNormalVector = -1*unitNormalVector
        E. theta2 = asin(n1 * sin(theta1) / n2)
        F. ExtendRay."""
        # A. normalLensVector
        lensAngle = math.atan2((lXY[1][1] - lXY[0][1]), (lXY[1][0] - lXY[0][0]))
        normalAngle = lensAngle - math.pi / 2
        # B. unitNormalVector
        lensUnitVect = [math.cos(normalAngle), math.sin(normalAngle)]
        #print(f"lensUnitVect = {lensUnitVect}  lensAngle {lensAngle*180/math.pi}  normalAngle {normalAngle*180/math.pi}")
        # C. unitRayVector
        rayUnitVect = [math.cos(self.angle[-1]), math.sin(self.angle[-1])]
        #print(f"rayAngle {self.angle[-1]*180/math.pi}   rayUnitVect {rayUnitVect}")
        # D. crossProduct(unitNormalVector, unitRayVector)
        theta1 = math.asin(LinAlg.crossProd(self, lensUnitVect, rayUnitVect))
        #print(f"theta1 = {theta1*180/math.pi}")
        theta2 = math.asin(n1 * math.sin(theta1) / n2)
        #print(f"theta2 = {theta2*180/math.pi}")
        rayAngle = normalAngle + theta2
        #print("rayangle", rayAngle)
        return rayAngle


    def rayExtension(self, dist):
        dx = dist * math.cos(self.angle[-1])
        dy = dist * math.sin(self.angle[-1])
        self.ray.append([self.ray[-1][0] + dx, self.ray[-1][1] + dy])
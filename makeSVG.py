

class saveSVG():
    def __init__(self, width, height, minX, minY, viewBoxWidth, viewBoxHeight, points):
        self.width = str(width)
        self.height = str(height)
        self.vBox = [str(minX), str(minY), str(viewBoxWidth),str(viewBoxHeight)]
        self.path1 = ""
        for i in points:
            if self.path1 == "":
                self.path1 += 'M' + str(i[0]) + ',' + str(i[1])
            else:
                self.path1 += ' L' + str(i[0]) + ',' + str(i[1])






    def writeSVG(self, filename):

        f = open("FP250H100.svg", "a")
        f.truncate(0)
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
        f.write('<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink"\n')
        f.write(f'width="{self.width}" height="{self.height}" viewBox="{self.vBox[0]} {self.vBox[1]} {self.vBox[2]} {self.vBox[3]}">\n')
        f.write('<defs>\n')
        f.write('</defs>\n')
        f.write(f'<path d="{self.path1}" stroke="black" stroke-width="1.0" fill="none" />\n')
        f.write('</svg>')









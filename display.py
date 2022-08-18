import pygame

class Display():
    """Set colors, screeh size, display object, OFFSET_X, OFFSET_Y, to center displayed objects.
    Display caption, fill color
    """

    def __init__(self):
        pygame.init()

        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.RED = (255, 0, 0)
        self.GREEN = (0, 255, 0)
        self.BLUE = (0, 0, 255)

        self.width = 1620
        self.height = 900
        self.size = (self.width, self.height)
        self.display = pygame.display.set_mode(self.size)
        self.OFFSET_X =  int(self.width/2 - 100)
        self.OFFSET_Y = int(self.height/2)
        pygame.display.set_caption("Lens")
        self.display.fill(self.WHITE)

    def draw_Lens(self, surface, color):
        for point in surface:
            x = point[0]
            y = point[1]
            if color == "RED":
                pygame.draw.circle(self.display, self.RED,(x + self.OFFSET_X,-y + self.OFFSET_Y),1,1)
            elif color == "GREEN":
                pygame.draw.circle(self.display, self.BLUE, (x + self.OFFSET_X, -y + self.OFFSET_Y), 3, 3)
            else:
                pygame.draw.circle(self.display, self.BLACK, (x + self.OFFSET_X, -y + self.OFFSET_Y), 1, 1)


    def drawLensLines(self, lens):
        """display rays"""
        for p in range(len(lens)-1):
            #print(f"ray = {ray}")
            x1, y1 = lens[p][0], -lens[p][1]
            x2, y2 = lens[p+1][0], -lens[p+1][1]


            pygame.draw.line(self.display, self.BLUE, [x1 + self.OFFSET_X, y1 + self.OFFSET_Y], [x2 + self.OFFSET_X, y2 + self.OFFSET_Y])
            #print(x1 + self.OFFSET_X, y1 + self.OFFSET_Y)


    def draw_Source(self, ray):
        source = ray[0]
        x = source[0]  + self.OFFSET_X
        y = -source[1] + self.OFFSET_Y  # SET NEGATIVE TO MAKE SOURCE ON UPPER HALF IN IMAGE
        pygame.draw.circle(self.display, self.RED,( x, y), 2, 2)    #

    def draw_FocalPoint(self, fp):
        x = fp + self.OFFSET_X
        y = 0 + self.OFFSET_Y
        pygame.draw.circle(self.display, self.RED, (x, y), 4, 4)

    def draw_Rays(self, ray):
        """display rays"""
        for p in range(len(ray)-1):
            #print(f"ray = {ray}")
            x1, y1 = ray[p][0], -ray[p][1]
            x2, y2 = ray[p+1][0], -ray[p+1][1]


            pygame.draw.line(self.display, self.BLUE, [x1 + self.OFFSET_X, y1 + self.OFFSET_Y], [x2 + self.OFFSET_X, y2 + self.OFFSET_Y])
            #print(x1 + self.OFFSET_X, y1 + self.OFFSET_Y)


    def display_to_screen(self):
        """This is needed to display everything to the screen"""
        pygame.display.update()

        running = True
        while running:
            for event in pygame.event.get():  # this gets any event on the screen
                if event.type == pygame.QUIT:
                    running = False

                pygame.image.save(self.display, "image.jpg")
                pygame.image.save(self.display, "image.png")

        pygame.quit()
        quit()


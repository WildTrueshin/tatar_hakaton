EPS = 30
DELTA = 3


class Object:
    def __init__(self, cordL: tuple, cordR: tuple, material: bool, nextScene=None):
        self.cordMin = cordL
        self.cordMax = cordR
        self.material = material


class Scene:
    def __init__(self, objects: list, cord: tuple, isInteract):
        self.objects = objects
        self.cord = cord
        self.isInteractive = isInteract

    def inter(self):
        objp = None
        dst = EPS + 1
        for obj in self.objects:
            x1, y1 = obj.cordL
            x2, y2 = obj.cordR
            dist = (min(abs(self.cord[0] - x1), abs(self.cord[0] - x2))
                    + min(abs(self.cord[1] - y1), abs(self.cord[1] - y2)))
            if dist < dst and obj.nextScene:
                dst = dist
                objp = obj
        if objp:
            self.isInteractive = objp
        else:
            self.isInteractive = None

    def go(self, delta: tuple):
        self.cord[0] += delta[0]
        self.cord[1] += delta[1]
        self.inter()

    def forward(self):
        newcord = self.cord
        newcord[1] -= DELTA
        for obj in self.objects:
            x1, y1 = obj.cordL
            x2, y2 = obj.cordR
            if x1 <= newcord[0] <= x2 and y1 <= newcord[1] <= y2:
                return
        self.go(tuple({0, -DELTA}))

    def backward(self):
        newcord = self.cord
        newcord[1] += DELTA
        for obj in self.objects:
            x1, y1 = obj.cordL
            x2, y2 = obj.cordR
            if x1 <= newcord[0] <= x2 and y1 <= newcord[1] <= y2:
                return
        self.go(tuple({0, +DELTA}))

    def right(self):
        newcord = self.cord
        newcord[0] += DELTA
        for obj in self.objects:
            x1, y1 = obj.cordL
            x2, y2 = obj.cordR
            if x1 <= newcord[0] <= x2 and y1 <= newcord[1] <= y2:
                return
        self.go(tuple({+DELTA, 0}))

    def left(self):
        newcord = self.cord
        newcord[0] -= DELTA
        for obj in self.objects:
            x1, y1 = obj.cordL
            x2, y2 = obj.cordR
            if x1 <= newcord[0] <= x2 and y1 <= newcord[1] <= y2:
                return
        self.go(tuple({-DELTA, 0}))

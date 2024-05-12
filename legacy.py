import maya.cmds as m
import math
import time 
import random
from pymel.core.datatypes import Vector

global blacklist
global start 
global finish
global testNumbers

testNumbers = 20.0
start = [10, 0, -10]
finish = [-10, 0, 10]

blacklist = []
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 255, 255)
yellow = (255, 255, 0)
white = (255, 255, 255)
black = (0, 0, 0)
purple = (128, 0, 128)
orange = (255, 165, 0)
grey = (128, 128, 128)
turquoise = (64, 224, 208)

def parseToVal(str):
    ret = []
    spl = str.split("_")
    spl.pop(0)

    for i in spl:
        rep = i.replace("n", "-")
        rep = rep.replace("p", "+")
        ret.append(rep)

    return map(lambda x: int(x), ret )
def parseToStr(arr):
    ret = []
    for i in arr:
        if i < 0:
            rep = str(i).replace("-", "_n")
        else:
            rep = "_p"+ str(i)
        if i == 0:
            # rep.replact()
            rep = "_n0"
        ret.append(rep)

    return "".join(ret)

# spotNode = m.polyPlane(n="spot" , sx=1, sy=1)
class Spot:
    def __init__(self,x, y, z):
        self.x = x
        self.y = y
        self.z = z
        self.gDist = 0
        self.prev = None
        self.nodeArr = m.polyPlane(n= self.name(), sx=1, sy=1)
        self.color = white

        self.change_color(white)
        m.move(self.x, self.y, self.z, self.nodeArr[0])
        

    
    def name(self):
        return parseToStr([self.x, self.y, self.z])
    def change_color(self, color):
        self.color = color
        m.setAttr(str(self.name()) + ".overrideEnabled",1)
        m.setAttr(str(self.name()) + ".overrideRGBColors",1)
        m.setAttr(str(self.name()) + ".overrideColorR", color[0])
        m.setAttr(str(self.name()) + ".overrideColorG", color[1])
        m.setAttr(str(self.name()) + ".overrideColorB", color[2])
    def coord(self):
        return [self.x, self.y, self.z]
    
    def neighbors(self, current):
        ret = []
        for xAdd in range(3):
                for zAdd in range(3):
                        add = [self.x+xAdd-1, 0, self.z+zAdd-1]
                        ret.append(add)
        # generate all neighbor coords (x/y only

        ret = filter(lambda x : x not in blacklist, ret)
        def new(x):
            if x in blacklist or x[1] != 0:
                return "x"
            else:
                blacklist.append(x)
                mapSpot = Spot(x[0], x[1], x[2])
                mapSpot.prev = self
                return[mapSpot, mapSpot.fDist()]
        ret = map(lambda x: new(x), ret)
        ret = filter(lambda x : type(x) != str, ret)
        for i in ret:
            print(i)
            i[0].gDist = self.gDist + 1
        

        return ret  
    

    def hDist(self):
        dx = finish[0]
        dy = finish[1]
        dz = finish[2]
        vx = self.x
        vy = self.y
        vz = self.z
        c = math.sqrt(((dx-vx)**2)+((dy-vy)**2)+((dz-vz)**2))
        return c
    def fDist(self) :
        return self.hDist() + self.gDist

def lowest(arr):

    ret = [0, 10000]
    for i in arr:
        ret = i if i[1] < ret[1] and i[0] not in blacklist else ret
    return ret

def pathify(obj, testNumber):
    current = obj[0]
    pathLength = current.gDist
    vertexArr = []
    while pathLength > 0:
        vertexArr.append(current.coord())
        current = current.prev
        pathLength = pathLength - 1
    vertexArr.append(start)
    path = m.curve(p=vertexArr)
    m.setAttr(path + ".overrideEnabled", 1)
    m.setAttr(path + ".overrideColor", 17)
    return vertexArr

def blacklistIt():
    global blacklist
    cubes = m.ls("init*_instance*")
    m.select(cubes)
    blacklist = [[int(num) for num in m.xform(x, q=1, ws=1, t=1)] for x in cubes]
    print(blacklist)

def solve(testNumber=0):
    new = Spot(start[0], start[1], start[2])
    open =  new.neighbors(new)
    current = lowest(open)
    current[0].change_color(purple)
    running = 100
    while running > 0:
        if current[0].coord() == finish:
            current[0].change_color(red)
            running = 0
            ret = pathify(current, testNumber)
            print("finished")
            ls = m.ls("_*_*")
            m.group(ls, n="field")
            m.delete("field")
            return ret

        # time.sleep(.01)
        m.refresh()

        blacklist.append(current[0].coord())
        open = filter(lambda x : x[0].coord() != current[0].coord(), open)
        current[0].change_color(red)
        open = open + current[0].neighbors(current)
        current = lowest(open)
        running = running -1

def cleanup() :
    ls = m.ls("field")
    m.delete(ls)


blacklistIt()
cleanup()
solve()




# for testNumber in range(1):
#     print("-----------------------------------------Running test #" + str(testNumber) + " ----------------------------------")
#     cleanup(testNumber)
#     path = solve(testNumber)

#     complications = random.sample(path[5:-5], 10)
#     for coords in complications:
#         cube = m.duplicate("init1_instance1")
#         m.xform(cube, ws=1, a=1, t=coords)
#         m.setAttr(str(cube[0]) + "|init2Shape.overrideEnabled", 1)
#         m.setAttr(str(cube[0]) + "|init2Shape.overrideColor", 13)


def makeField():
    running = 0
    created = []

    while running < 700:
        coord = [random.randrange(-24, 24), 0, random.randrange(-24, 24)]

        if(coord in created):
            continue
        
        created.append(coord)
        cube = m.duplicate("init1_instance1")
        m.xform(cube, ws=1, a=1, t=coord)
        running+=1

# makeField()

# currentPosition = Spot(10,0,-10)

# currentPosition.neighbors(currentPosition)


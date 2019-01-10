

from copy import deepcopy  # copy 'target' to avoid modifying it
import utils  # it might be helpful to use 'utils.py'
from operator import add
from random import shuffle
import timeit

########################################
#Varible Bin!!!!



class point:
    def __init__(self,y,x):
        self.pos = (y,x) # rememeber grid is the other way round
        self.close = []
        for a in [[0,1],[1,0],[0,-1],[-1,0]]:
            if 0 <= self.pos[0] + a[0] < height and 0 <= self.pos[1] + a[1] < width:
                self.close.append((self.pos[0]+a[0],self.pos[1]+a[1]))
        self.state = 0 #0 is for needs to be filled  -1 is for nul and >0 is the shape id
        self.stateid = 0 #the placed order of the point

    def closenode(self):
        self.node = []
        for i in self.close:
            try:
                self.node.append(ogrid[i[0]][i[1]])
            except IndexError:
                continue

    def edgescore(self,target): #returns the edge score ie how many adacent empty squares
        try:
            if self.edge == 0:
                return
            self.old = self.edge
            #NumberCords[self.edge].remove(self.pos) #may slow it down
        except AttributeError:
            self.edge = 0
        if target[self.pos[0]][self.pos[1]] == 1:
            self.edge = 0
            for i in self.close:
                try:
                    if ogrid[i[0]][i[1]].state == -1:
                        self.edge += 1
                except IndexError:
                    pass

            try:
                NumberCords[self.edge].append(self.pos)
                return self.old - self.edge
            except AttributeError:
                pass

    def edgescore2(self,target):
        self.edge2 = 0
        if target[self.pos[0]][self.pos[1]] == 1:
            for i in self.close:
                try:
                    if target[i[0]][i[1]] == 1:
                        self.edge2 += ogrid[i[0]][i[1]].edge
                except IndexError:
                    pass
            try:
                NumberCords2[self.edge2].append(self.pos)
            except AttributeError:
                pass

class TreePoint():
    def __init__(self,cords):
        self.child = []
        self.id = ""
        self.cords = cords
    def genkids(self):
        new = set()
        if len(self.cords) < 4:
            for cord in self.cords:
                for i in [[0,1],[1,0],[0,-1],[-1,0]]:
                    new.add((cord[0]+i[0],cord[1]+i[1]))
            for item in self.cords:
                new.discard(item)
            if new:
                for i in new:
                    temp = []
                    for k in self.cords:
                        temp.append(k)
                    temp.append(i)
                    self.child.append(TreePoint(temp))
                    self.child[-1].genkids()
        else:
            for i in range(1,18):
                for cord in self.cords:
                    tempcords = []
                    for k in self.cords:
                        temp = [-cord[0] + k[0],-cord[1] + k[1]]
                        if temp not in utils.generate_shape(i):
                            break
                    else:
                        self.id = i
                        #print ("self.cords followed by true values",self.cords , utils.generate_shape(i))

def realcordsTest(pos,cord):
    tempy = pos[0] + cord[0]
    tempx = pos[1] + cord[1]
    if 0 <= tempy < height and 0 <= tempx < width:
        try:
            if ogrid[tempy][tempx].state == -1:
                return True
            else:
                return False
        except IndexError:
            return False
    else:
        return False

def nextLevel(node,pos):
    temp = node.cords
    if realcordsTest(pos,temp[-1]) == True:
        if len(temp) > 3:
            if  isinstance(node.id,int):
                #print("here",node.id,node.cords)
                if testParts[node.id] > 0:
                    n = doesitfit3(temp,pos)
                    #print("DoesItFit2",n)
                    if n != False:
                        truecords = []
                        for cord in node.cords:
                            truecords.append([pos[0]+cord[0],pos[1]+cord[1]])
                        return [n,truecords,node.id]

            return([20])
        else:
            best = [20,"nope"]
            for newnode in node.child:
                compare = nextLevel(newnode,pos)
                #print (compare,newnode.cords)
                if compare[0] < best[0]:
                    best = compare
            return best
    else:
        return([20])

def doesitfit3(cords,pos):
    output = 0
    for square in cords:
        try:
            #print ("does it fit cords",square[0]+pos[0],square[1]+pos[1])
            if ogrid[square[0]+pos[0]][square[1]+pos[1]].state == -1 and 0 <= square[0] + pos[0] < height and 0 <= square[1]+ pos[1] < width:
                output += int(ogrid[square[0]+pos[0]][square[1]+pos[1]].edge)
                continue
            else:
                break
        except IndexError:
            continue
    else:
        return output
    return False #returns a score based on how it simplifies the overall shape

def arroundTheShape(cords,target):
    aroundNodes = set()
    for sq in cords:
        aroundNodes.update(set(ogrid[sq[0]][sq[1]].node))
    for node in aroundNodes:
        node.edgescore(target) # updates nodes when something is placed

def placeshape2(shapeid,cords,stateid,target):
    global testParts
    for square in cords:
        ogrid[square[0]][square[1]].state = shapeid
        ogrid[square[0]][square[1]].stateid = stateid
    arroundTheShape(cords,target)
    testParts[shapeid] -= 1


def debugGrid(end): #this is a debug function. It takes a lower order lambda function then prints out a colour coded grid.
    for row in ogrid:
        line = ""
        for point in row:
            var = end(point)
            if var == 0:
                line += "\033[1;"+ "37;"+ str((var)%7 + 40)+ "m " + "0" + str(var)
            elif var < 0:
                line += "\033[1;"+ "37;"+ str((var)%6 + 41)+ "m " + str(var)
            elif var < 10:
                line += "\033[1;"+ "37;"+ str((var)%6 + 41)+ "m " + "0" + str(var)
            else:
                line += "\033[1;"+ "37;"+ str((var)%6 + 41)+ "m " + str(var)
        print (line)

def canitfit(shapeid,pos):
    shape = utils.generate_shape(shapeid)
    #print(shape)
    #print(shapeid)
    for sq in shape:
        output = [100,"a","a"]
        a = doesitfit2(shapeid,(pos[0]-sq[0],pos[1]-sq[1]))
        #print (pos[0]-sq[0],pos[1]-sq[1])
        #print("does it fit2 returns", a)
        if a != False and a < output[0]:
            output = (a,(pos[0]-sq[0],pos[1]-sq[1]),shapeid)
    return output #Unused at the moment

def setstate(target):
    for y, row in enumerate(ogrid):
        for x, sq in enumerate(row):
            if target[y][x] == 1:
                sq.state = -1

def closeAndEdge(target):
    for row in ogrid:
        for sq in row:
            sq.closenode()
            sq.edgescore(target)

def closeAndEdge2(target):
    for row in ogrid:
        for sq in row:
            sq.edgescore2(target)

def Tetris(target, limit_tetris):
    global height
    global width
    height = len(target)
    width = len(target[1])
    orderlist = "?" # ok so now this may be usefull
    #print("Running")
    global shapesPlaced
    global NumberCords
    global NumberCords2
    global testParts
    shapesPlaced = 1
    NumberCords = [[] for i in range(20)] # ok so this is a 2d array each sub array is a co-ords list in format (y,x) for the edge list
    NumberCords2 = [[] for i in range(20)]
    testParts = {}
    for item in limit_tetris:
        testParts[item] = limit_tetris[item]

    #print("main work point")
    start_time = timeit.default_timer()
    global ogrid
    ogrid = [[point(y,x) for x in range(width)]for y in range(height)]
    nodeTree = TreePoint([(0,0)])
    setstate(target)
    closeAndEdge(target)
    closeAndEdge2(target)
    nodeTree.genkids()

    elapsed = timeit.default_timer() - start_time
    beenPlaced = 0
    start_time = timeit.default_timer()
    placed = 1
    for i in NumberCords:
        if i:
            for pos in i:
                best = nextLevel(nodeTree,pos)
                if best[0] != 20 and best[1] != "nope":
                    #print(best)
                    placeshape2(best[2],best[1],placed,target)
                    placed += 1


    #print("second passs" , testParts)


    elapsed = timeit.default_timer() - start_time

    print("time for algoroythem = ",elapsed)



    #debugGrid(lambda x: x.state )
    #print(" ")
    #debugGrid(lambda x: x.state )
    #debugGrid(lambda x: x.edge)

    #debugGrid(lambda x : x.stateid)
    ############################
    #emptying the grid
    solution = []
    for y,row in enumerate(ogrid):
        solution.append([])
        for sq in row:
            if sq.state == 0 :
                solution[y].append((0,0))
            elif sq.state == -1:
                solution[y].append((0,0))
            else:
                solution[y].append((sq.state,sq.stateid))
    return solution


    #utils.visualisation(target,solution)

width = 20
height = 25
dencity = 0.8
target,a,TheSolution = utils.generate_target(width, height, dencity)

solution2 = Tetris(target,a)
valid, missing, excess, error_pieces, use_diff = utils.check_solution(target, solution2 ,a)
total_blocks = sum([sum(row) for row in target])
percent = (missing + excess)/ total_blocks
print (1 - percent)
print (a)

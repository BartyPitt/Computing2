# ####################################################
# DE2-COM2 Computing 2
# Individual project
#
# Title: MAIN
# Authors: Liuqing Chen
# Last updated: 25th July 2018
# ####################################################
######################################################
#Bartys big old notes that everyone gets annoyed at and completly ignores
# generate_target(width, height, density)
#visualisation(target, solution)
#generate_shape(shape_id)
# Co ordingate are done backwards y,x
#
#
#
from copy import deepcopy  # copy 'target' to avoid modifying it
import utils  # it might be helpful to use 'utils.py'
from operator import add
from random import shuffle
import timeit

########################################
#Varible Bin!!!!


width = 5
height = 5
dencity = 0.3
global target , testParts , TheSolution
target,a,TheSolution = utils.generate_target(width, height, dencity)
orderlist = "?" # ok so now this may be usefull

######################
#Running varibles
global shapesPlaced
shapesPlaced = 1
NumberCords = [[] for i in range(20)] # ok so this is a 2d array each sub array is a co-ords list in format (y,x) for the edge list


#####################################
#test
testgrid =  [
 [0, 1, 1, 0, 1, 0, 1, 0, 0, 1],
 [0, 1, 1, 0, 1, 0, 1, 1, 1, 1],
 [0, 1, 0, 1, 1, 1, 1, 1, 1, 1],
 [0, 1, 1, 1, 1, 0, 1, 1, 1, 1],
 [0, 1, 1, 0, 1, 1, 1, 0, 1, 0],
 [0, 0, 1, 1, 0, 1, 1, 1, 0, 0],
 [1, 1, 1, 1, 1, 1, 0, 1, 1, 0],
 [1, 1, 0, 1, 1, 0, 1, 1, 0, 1],
 [1, 1, 1, 0, 1, 1, 1, 0, 1, 1],
 [1, 0, 0, 1, 1, 1, 1, 0, 1, 0]
 ]

#testParts = {1: 4, 2: 0, 3: 1, 4: 1, 5: 1, 6: 0, 7: 1, 8: 1, 9: 1, 10: 0, 11: 0, 12: 2, 13: 0, 14: 1, 15: 0, 16: 1, 17: 1, 18: 1, 19: 1}

#target = testgrid
testParts = {}
for item in a:
    testParts[item] = a[item]



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

    def edgescore(self): #returns the edge score ie how many adacent empty squares
        try:
            if self.edge == 0:
                return
            self.old = self.edge
            NumberCords[self.edge].remove(self.pos) #may slow it down
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
                        temp = [cord[0] - k[0],cord[1] - k[1]]
                        if temp not in utils.generate_shape(i):
                            break
                    else:
                        self.id = i

def Tetris(target, limit_tetris):

    # #################################################
    # This is just a mock example showing how the solution is evaluated

    import random
    option = 4 #random.randint(1,4)

    if option == 1:  # this is not a perfect but acceptable answer
        M = [
                [(0, 0), (18, 1), (18, 1),  (0, 0),  (0, 0) ],
                [(0, 0), (0, 0),  (18, 1),  (18, 1), (0, 0) ],
                [(0, 0), (0, 0),  (1, 2),   (1, 2),  (8, 3)],
                [(0, 0), (13, 4), (1, 2),   (1, 2),  (8, 3) ],
                [(13,4), (13, 4), (13, 4),  (8, 3),  (8, 3) ]
            ]

    if option == 2:  # this is an invalid answer, resulting 0 score
        M = [
                [(0, 0),  (0, 0),  (0, 0),  (0, 0),   (0, 0)],
                [(0, 0),  (0, 0),  (1, 1),  (1, 1),   (0, 0)],
                [(0, 0),  (0, 0),  (1, 1),  (1, 1),   (0, 0)],
                [(0, 0),  (0, 0),  (1, 2),  (1, 2),   (0, 0)],
                [(0, 0),  (0, 0),  (1, 2),  (1, 2),   (0, 0)],
            ]


    if option == 3:  # this is an invalid answer, resulting 0 score
        M = [
                [(0, 0),  (0, 0),  (0, 0),  (0, 0),   (0, 0)],
                [(0, 0),  (0, 0),  (1, 1),  (0, 0),   (0, 0)],
                [(0, 0),  (0, 0),  (1, 1),  (0, 0),   (0, 0)],
                [(0, 0),  (0, 0),  (1, 1),  (0, 0),   (0, 0)],
                [(0, 0),  (0, 0),  (1, 1),  (0, 0),   (0, 0)],
             ]

    if option == 4:  # this is a perfect answer
        M = [
                [(0, 0),  (0, 0),  (8, 1),  (0, 0),   (0, 0)],
                [(0, 0),  (0, 0),  (8, 1),  (1, 2),   (1, 2)],
                [(0, 0),  (8, 1),  (8, 1),  (1, 2),   (1, 2)],
                [(0, 0),  (13, 3), (18, 4), (18, 4),  (0, 0)],
                [(13, 3), (13, 3), (13, 3), (18, 4),  (18, 4)]
            ]

    # Write your own solution generaton codes here instead of above
    # ######################################################

    return M #not me left in to sometimes test other functions


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
                print("here",node.id)
                if testParts[node.id] > 0:
                    n = doesitfit2(node.id,pos)
                    print("DoesItFit2",n)
                    if n != False:
                        truecords = []
                        for cord in node.cords:
                            truecords.append([pos[0]+cord[0],pos[1]+cord[1]])
                        return [n,truecords,node.id]

            return([-1])
        else:
            best = [-1,"nope"]
            for newnode in node.child:
                compare = nextLevel(newnode,pos)
                #print (compare,newnode.cords)
                if compare[0] > best[0]:
                    best = compare
            return best
    else:
        return([-1])

def shapepos(shapeid,pos): # takes the shape id and the starting possition and returns a list of the true cordinates
    output = []
    shape = utils.generate_shape(shapeid)
    for square in shape:
        testpos = [
            pos[0] + square[0]    ,
            pos[1] + square[1] ]  #getting position of the point of shape
        output.append(testpos)
        #if testpos[0] * testpos[1] < 0:
        #   return False Code that used to debug stuff but was not worth it
    return output

def doesitfit(shapeid,pos): #pos in form y,x. It takes the shape id , gets the true coordinates and then checks to see if all the spaces are empty
        for square in shapepos(shapeid,pos):
            try:
                if ogrid[square[0]][square[1]].state == -1:
                    continue
                else:
                    break
            except IndexError:
                break
        else:
            return True
        return False

def doesitfit2(shapeid,pos):
    output = 0
    for square in shapepos(shapeid,pos):
        try:
            if ogrid[square[0]][square[1]].state == -1 and 0 <= square[0] < height and 0 <= square[1] < width:
                output += int(ogrid[square[0]][square[1]].edge)
                continue
            else:
                break
        except IndexError:
            continue
    else:
        return output
    return False #returns a score based on how it simplifies the overall shape

def arroundTheShape(shapeid,pos):
    aroundNodes = set()
    for sq in shapepos(shapeid,pos):
        aroundNodes.update(set(ogrid[sq[0]][sq[1]].node))
    for node in aroundNodes:
        node.edgescore() # updates nodes when something is placed

def placeshape(shapeid,pos,stateid): #maybe some issue with this and findshape temp fix in placr
    global testParts
    for square in shapepos(shapeid,pos):
        ogrid[square[0]][square[1]].state = shapeid
        ogrid[square[0]][square[1]].stateid = stateid
    #arroundTheShape(shapeid,pos)
    testParts[shapeid] -= 1

def placeshape2(shapeid,cords,stateid):
    print(shapeid)
    global testParts
    for square in cords:
        ogrid[square[0]][square[1]].state = shapeid
        ogrid[square[0]][square[1]].stateid = stateid
    #arroundTheShape(shapeid,pos)
    testParts[shapeid] -= 1


def groupsize(livenode):#dead function but may be usefull in the future # Unused at the moment
    alive = []
    blive = []
    general = set()
    for sq in livenode.node:
        if sq.state == 0:
            alive.append(sq)
    while True:
        alive = set(alive)
        for sq in alive:
            for sqq in sq.node:
                if sq.state == 0:
                    blive.append(sq)
        general.union(set(alive))

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
    return output

def findshape(pos): # best in format (score , (pos) , shapeid)
    best = (20,False)
    global testParts
    for shape in testParts:
        if testParts[shape] > 0:
            test = canitfit(shape,pos)
            if best[0] > test[0]:
                best = test
    if best[0] != 20 :
        global shapesPlaced
        if doesitfit(best[2],best[1]):
            placeshape(best[2],best[1],shapesPlaced)
            shapesPlaced += 1
            #print(best)
        else:
            return False
        #print("fit shape at" ,pos)
        return True
    else:
        #print("cant fit shape" , pos)
        return False

######
#create the grid to put stuff in
ogrid = [[point(y,x) for x in range(width)]for y in range(height)]

def setstate():
    for y, row in enumerate(ogrid):
        for x, sq in enumerate(row):
            if target[y][x] == 1:
                sq.state = -1

def closeAndEdge():
    for row in ogrid:
        for sq in row:
            sq.closenode()
            sq.edgescore()


#print("setstate",timeit.timeit(setstate))
#print("Close and Edge",timeit.timeit(closeAndEdge))
#print("Edge2",timeit.timeit(Edge2f))
start_time = timeit.default_timer()

setstate()
closeAndEdge()
nodeTree = TreePoint([(0,0)])
nodeTree.genkids()

elapsed = timeit.default_timer() - start_time
#debugGrid(lambda x: x.state)
print(elapsed)
############
#proccess the gird xx
#debugGrid(lambda x: x.edge)
print("  ")
beenPlaced = 0

start_time = timeit.default_timer()
placed = 1
for i in NumberCords:
    if i:
        for pos in i:
            best = nextLevel(nodeTree,pos)
            #print (best)
            if best[0] != -1:
                #print("place item")
                placeshape2(best[2],best[1],placed)
                placed += 1

closeAndEdge()
print("second passs" , testParts)
for i in NumberCords:
    if i:
        for pos in i:
            best = nextLevel(nodeTree,pos)
            if best[0] != -1:
                print("place item")
                placeshape2(best[2],best[1],placed)
                placed += 1

elapsed = timeit.default_timer() - start_time
"""
for i in NumberCords:
    if i:
        for pos in i:
            findshape(pos)

"""

print("time for algoroythem = ",elapsed)



#debugGrid(lambda x: x.state )
print(" ")
#debugGrid(lambda x: x.stateid )
#debugGrid(lambda x: x.edge)
print (NumberCords)
#debugGrid(lambda x: x.edge2)

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


#utils.visualisation(target,solution)
valid, missing, excess, error_pieces, use_diff = utils.check_solution(target, solution ,a)
total_blocks = sum([sum(row) for row in target])
percent = (missing + excess)/ total_blocks
print (1 - percent)
print (a)

utils.visualisation(target,solution)
#debug print
#print(pieces, target)

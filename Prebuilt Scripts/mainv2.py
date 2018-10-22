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
import timeit

########################################
#Varible Bin!!!!
width = 1000
height = 1000
dencity = 0.7
target,testParts,TheSolution = utils.generate_target(width, height, dencity)
orderlist = "?" # ok so now this may be usefull

######################
#Running varibles
shapesPlaced = 1



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

    return M

def shapepos(shapeid,pos): # takes the shape id and the starting possition and returns a list of the true cordinates
    output = []
    shape = utils.generate_shape(shapeid)
    for square in shape:
        testpos = [
            square[0]   +pos[0] ,
            pos[1]      +square[1] ]  #getting position of the point of shape
        output.append(testpos)
        #if testpos[0] * testpos[1] < 0:
        #   return False Code that used to debug stuff but was not worth it
    return output

def doesitfit(shapeid,pos): #pos in form y,x. It takes the shape id , gets the true coordinates and then checks to see if all the spaces are empty
        for square in shapepos(shapeid,pos):
            try:
                if ogrid[square[0]][square[1]].state == -1:
                    #print ("square that was true",square)
                    continue
                else:
                    #print("no square",ogrid[square[0]][square[1]].state) # uncomment if you are having aslignment issues
                    break
            except IndexError:
                break
        else:
            return True
        return False

def placeshape(shapeid,pos,stateid):
    for square in shapepos(shapeid,pos):
        ogrid[square[0]][square[1]].state = shapeid
        ogrid[square[0]][square[1]].stateid = stateid

def groupsize(livenode):
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

def debugGrid(end):
    for row in ogrid:
        line = ""
        for point in row:
            var = end(point)
            if var == 0:
                line += "\033[1;"+ "37;"+ str((var)%7 + 40)+ "m " + "0" + str(var)
            elif var < 10:
                line += "\033[1;"+ "37;"+ str((var)%6 + 41)+ "m " + "0" + str(var)
            else:
                line += "\033[1;"+ "37;"+ str((var)%6 + 41)+ "m " + str(var)
        print (line)

def edge(target):
    output = []
    for y , row in enumerate(target):
        output.append([])
        for x , point in enumerate(row):
            pointlist = [[y,x+1],[y,x-1],[y+1,x],[y-1,x]]
            output[y].append(0)
            for sq in pointlist:
                try:
                    output[y][x] += target[sq[0]][sq[1]]
                except IndexError:
                    continue


    return output

######
#create the grid to put stuff in
start_time = timeit.default_timer()

edgegrid = edge(target)
edge2grid = edge(edgegrid)

elapsed = timeit.default_timer() - start_time
print(elapsed)
############
#proccess the gird xx

#debugGrid(lambda x: x.edge)
print ("      ")
#debugGrid(lambda x: x.edge2)

############################
#emptying the grid
solution = []


print (solution)
#utils.visualisation(target,TheSolution)
#debug print
#print(pieces, target)

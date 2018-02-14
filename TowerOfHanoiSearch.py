#Intro to AI -- EECS348 -- Fall 2017
#Assignment-1
#Done by Lakshman Pavan Kumar Boddoju (Student ID: 3082817 and Net ID: LPB8177)
#and Suman Maroja (Student ID: 2978953)




#Please provide the initial and target game states as a list of list. Example initial game state is [[3,2,1],[],[]] and target game state is [[],[],[3,2,1]]
#Please make sure that the inputs have them in descending order from left to right. Also works for any possible initial and target game states i.e. initial is [[1],[2],[3]] and target is [[3],[2],[1]]




from copy import deepcopy

#Funtion to check if a certain move is valid and if its valid, go through the move and change the state of the world
def checkmove(move):
    if move[1] and move[0]: #Check if we aren't placing a bigger disk over a smaller one and both from and to rod have something i.e. if there is no disk on the from rod, its not possible to move that
        if move[0][-1] < move[1][-1]:
            move[1].append(move[0][-1])
            move[0].pop()
          
    elif move[0]:           #If the to rod is empty , thus we dont have to compare the size of disks
        move[1].append(move[0][-1])
        move[0].pop()
        
#Function to check and calculate all the possible valid moves (non-illegal and non-possible moves eliminated)
def allpossiblemoves(gamestate):
    ret = []
    temp = []
    temp = deepcopy(gamestate)
    if temp[0]:
        checkmove([temp[0],temp[1]])
        if temp != gamestate:
            ret.append(temp)
        temp = deepcopy(gamestate)
        checkmove([temp[0],temp[2]])
        if temp != gamestate:
            ret.append(temp)
    temp = deepcopy(gamestate)
    if temp[1]:
        checkmove([temp[1],temp[0]])
        if temp != gamestate:
            ret.append(temp)
        temp = deepcopy(gamestate)
        checkmove([temp[1],temp[2]])
        if temp != gamestate:
            ret.append(temp)
    temp = deepcopy(gamestate)
    if temp[2]:
        temp = deepcopy(gamestate)
        checkmove([temp[2],temp[0]])
        if temp != gamestate:
            ret.append(temp)
        temp = deepcopy(gamestate)
        checkmove([temp[2],temp[1]])
        if temp != gamestate:
            ret.append(temp)
    print '\nThis is the currrent game state\n'                             #Printing the current game state
    print gamestate
    print '...........\n\n'
    print '\nAll possible next states of the moves in this state are\n'     # And Printing the next possible game states based on current game state
    for i in ret:
        print i
    return ret

#Function to find a path from current game state to target game state using Breadth First Search

def BFS(gamestate,final):
    queue = [gamestate]
    numiterations = 0
    visited = []
    path = []
    while queue:
        current = queue.pop(0)
        if current == final:
            print 'Final state reached'
            print 'Number of Iterations: ',
            print numiterations
            print 'The path taken by BREADTH FIRST SEARCH'
            for i in path:
                print i,
                print '--->',
            print current
            return current
        else:
            movesleft = allpossiblemoves(current)
            children = []
            for move in movesleft:
                children.append(move)
            visited.append(current)
            path.append(current)
            for child in children:
                if child not in visited or child not in queue:
                    queue.append(child)
            if children == []:
                path.pop()
        numiterations = len(path)

#Function to find a path from current game state to target game state using Depth First Search

def DFS(gamestate,final):
    queue = [gamestate]
    numiterations = 0
    visited = []
    triedmoves = [gamestate]
    path = []
    while queue:
        current = queue.pop()
        if current == final:
            print 'Final state reached'
            print 'Number of Iterations: ',
            print numiterations
            print 'The path taken by DEPTH FIRST SEARCH'
            for i in path:
                print i,
                print '--->',
            print current
            return current
        else:
            movesleft = allpossiblemoves(current)
            children = []
            for move in movesleft:
                if move not in triedmoves:
                    children.append(move)
                    triedmoves.append(move)
            visited.append(current)
            path.append(current)
            for child in children:
                if child not in visited or child not in queue:
                    queue.append(child)
            if children == []:
                path.pop()
        numiterations = len(path)

# Calculating a distance through a distance funtion to use as a parameter in Best First Search
# Taking the difference in the lengths of each of the rods between the current possible states and final states to determine which is closer

def calcdistance(gamestate,final):
    i = 0
    dist = 0
    distsq = 0
    while i < 3:
        if gamestate[i] and final[i]:
            dist = len(gamestate[i]) - len(final[i])
            distsq+= dist**2
        elif gamestate[i]:
            dist = len(gamestate[i])
            distsq+= dist**2
        elif final[i]:
            dist = len(final[i])
            distsq+= dist**2
        i+=1
    return distsq


#Function to find a path from current game state to target game state using Best First Search    
        
def BestFS(gamestate,final):
    queue = [gamestate]
    numiterations = 0
    visited = []
    triedmoves = [gamestate]
    path = []
    while queue:
        flag = 0
        distance = []
        if flag != 1:                                          #Finding the distances of all the queue objects from the target game state and then popping the one with the lowest distance
            for i in queue:
                distance.append(calcdistance(i,final))
            nextindex = distance.index(min(distance))
            if queue[nextindex]:    
                current = queue.pop(nextindex)
                flag = 1
            else:
                current = queue.pop()
                flag = 1
        if current == final:
            print 'Final state reached'
            print 'Number of Iterations: ',
            print numiterations
            print 'The path taken by BEST FIRST SEARCH'
            for i in path:
                print i,
                print '--->',
            print current
            return current
        else:
            movesleft = allpossiblemoves(current)
            children = []
            for move in movesleft:
                if move not in triedmoves:
                    children.append(move)
                    triedmoves.append(move)
            visited.append(current)
            path.append(current)
            for child in children:
                if child not in visited or child not in queue:
                    queue.append(child)
            if children == []:
                path.pop()
        numiterations = len(path)
            
# Main funtion which receives input from the user             
def main():
    print "Enter the Initial State:"
    initial = input()
    print "Enter the Target State:"
    target = input()
    print "Enter 1 for BFS, 2 for DFS and 3 for BestFS:"
    whichsearch = input()
    if whichsearch == 1:
        BFS(initial,target)
    elif whichsearch == 2:
        DFS(initial,target)
    elif whichsearch == 3:
        BestFS(initial,target)
    else:
        print 'Enter valid input'
        return
    
main()
import heapq
import copy
import time
import os
class Node:
    def __init__(self, state, parent=None, action=None, cost = 0, h = 0):
        self.state = state
        self.parent = parent
        self.action = action
        self.cost = cost
        self.heuristic = h
    
    def __lt__(self,other):
        return self.cost + self.heuristic < other.cost + other.heuristic
    
def heuristic(state,goal):
    return abs(state[0] - goal[0]) + abs(state[1] - goal[1])

def UCSSearch(problem,start,goal):
    explored = set()
    frontier = []

    startNode = Node(start,None,None,0)
    heapq.heappush(frontier,startNode)

    while frontier:
        curr_node = heapq.heappop(frontier)
        curr_state = curr_node.state

        if curr_state == goal:
            path = []
            while curr_node.parent:
                path.append(curr_node.action)
                curr_node = curr_node.parent
            return path[::-1]
        
        explored.add(curr_state)
        for action in problem.getActions(curr_state):
            succ_state = problem.getResult(curr_state,action)
            if succ_state not in explored:
                succ_cost = curr_node.cost + problem.getCost(curr_state,action)
                succ_node = Node(succ_state,curr_node,action,succ_cost)
                heapq.heappush(frontier,succ_node)
    return None

def AStarSearh(problem, start, goal):
    explored = set()
    frontier = []

    startNode = Node(start,None,None,0,heuristic(start,goal))
    heapq.heappush(frontier,startNode)

    while frontier:
        curr_node = heapq.heappop(frontier)
        curr_state = curr_node.state

        if curr_state == goal:
            path = []
            while curr_node.parent:
                path.append(curr_node.action)
                curr_node = curr_node.parent
            return path[::-1]
        explored.add(curr_state)

        for action in problem.getActions(curr_state):
            succ_state = problem.getResult(curr_state,action)
            if succ_state not in explored:
                succ_cost = curr_node.cost + problem.getCost(curr_state,action)
                succ_node = Node(succ_state,curr_node,action,succ_cost,heuristic(succ_state,goal))
                heapq.heappush(frontier,succ_node)
    return None

class problemPacman:
    def __init__(self,map):
        self.map = map

    def getActions(self,state):
        row, col = state
        actions = []
        if self.map[row-1][col] != '%':
            actions.append('North')
        if self.map[row+1][col] != '%':
            actions.append('South')
        if self.map[row][col-1] != '%':
            actions.append('West')
        if self.map[row][col+1] != '%':
            actions.append('East')
        return actions
    def getResult(self,state,action):
        row, col = state
        actions = []
        if action == 'North':
            return (row-1,col)
        elif action == 'South':
            return (row+1,col)
        elif action == 'West':
            return (row,col-1)
        elif action == 'East':
            return (row,col+1)
        return state
    def getCost(self,state,action):
        return 1

def readMapFile(file_path):
    with open(file_path,'r') as file:
        return [list(line.strip()) for line in file]
    
def findIndex(map,location):
    if location == 'P':
        for i in range(0,len(map)):
            for j in range(0,len(map[i])):
                if map[i][j] == location:
                    return i,j
    else:
        list_index_of_food = []
        for i in range(0,len(map)):
            for j in range(0,len(map[i])):
                if map[i][j] == location:
                    index = (i,j)
                    list_index_of_food.append(index)
        return list_index_of_food
            
def swap(arr,i,j,m,n):
    if(arr[m][n] == '.'):
        arr[m][n] = ' '
    tmp = arr[i][j]
    arr[i][j] = arr[m][n]
    arr[m][n] = tmp
    return arr

def printMap(curr_map):
    for i in range(0,len(curr_map)):
        for j in range(0,len(curr_map[i])):
            print(curr_map[i][j], end = '')
        print("")

def check_corner_isFood(map,index_of_corner):
    for index in index_of_corner:
        i,j = index
        if map[i][j] == '.':
            index_of_corner.remove((i,j))
    return index_of_corner
def list_index(a,b):
    for i in b:
        a.append(i)
    return a
def excution(file_path,name_of_algorithm):
    map = readMapFile(file_path)
    copy_map = copy.deepcopy(map)
    problem = problemPacman(map)
    path = []              
    path_cost = 0  

    index_of_corner = check_corner_isFood(map,[(1,1),(1,20),(8,20),(8,1)])
    index_of_food = findIndex(map,'.')
    index_need_to_move = list_index(index_of_corner,index_of_food)

    if name_of_algorithm == 'AStar':
        path = AStarSearh(problem,findIndex(map,'P'),index_need_to_move[0]) 
        i = 0
        j = 1
        while j < len(index_need_to_move):
            path = path + AStarSearh(problem,index_need_to_move[i],index_need_to_move[j])
            i += 1
            j += 1
    elif name_of_algorithm == 'UCS':
        path = UCSSearch(problem,findIndex(map,'P'),index_need_to_move[0]) 
        i = 0
        j = 1
        while j < len(index_need_to_move):
            path = path + UCSSearch(problem,index_need_to_move[i],index_need_to_move[j])
            i += 1
            j += 1
    else:  
        print("Not Found. There are two algorithms: 'AStar' and 'UCS'")
        exit()
    if path:
        #Visualization
        print("----Visualization----")
        # printMap(map)
        # print("\n")
        for act in path:
            i,j = findIndex(copy_map,'P')
            if act == 'North': 
                copy_map = swap(copy_map, i, j, i - 1, j)
            elif act == 'South':
                copy_map = swap(copy_map, i, j, i + 1, j)
            elif act == 'West':
                copy_map = swap(copy_map, i, j, i, j - 1)
            elif act == 'East':
                copy_map = swap(copy_map, i, j, i, j + 1)
            os.system('cls' if os.name == 'nt' else 'clear') 
            printMap(copy_map) 
            print("\n")
            time.sleep(0.2)
            
        print("List of actions:",path)
        for action in path:
            path_cost += problem.getCost(problem.getResult(findIndex(map,'P'),action),action)
        print("Path Cost:",path_cost)
    else:
        print("Not found.")
        
file_path_of_map = input("Enter the path of file contain map: ")
name_of_algorithm = input("Enter name of algorithm: ")
excution(file_path_of_map,name_of_algorithm)

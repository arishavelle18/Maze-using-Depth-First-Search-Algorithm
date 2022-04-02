
from os import stat
from os.path import exists
from collections import deque


# gagawa tayo ng Node
class Node:
    def __init__(self,state,parent = None,action = None):
        self.state = state
        self.parent = parent
        self.action = action


# gawa tayo ng stack
class StackFrontier():
    def __init__(self):
        self.frontier = deque()

    # insert 
    def add(self,state):
        self.frontier.append(state)
    
    # check if itis already inthe frontier
    def contain(self,state):
        return any(node.state == state for node in self.frontier)

    # check if it is empty
    def empty(self):
        return len(self.frontier) == 0

    def delete(self):
        #  check if it is empty or not if yes then you cannot delete in the list
        if self.empty():
            print("The list is empty")
            return
        else:
            node = self.frontier.pop()
            return node



# create a maze

# board
class Maze:
    def __init__(self,filename):
        
        self.filename = filename

        with open(filename) as filename:
            contents = filename.read()

        # check kung may staring point at ending point bato at dapat isa lang 
        if 'A' not in contents and contents.count('A') != 1:
            print("Error : Start point must be one ")
            return
        if 'B' not in contents and contents.count('B') != 1:
            print("Error : Final point must be one ")
            return

        board = contents.splitlines()
        self.height =  len(board)
        self.width =  max([len(i) for i in board])
        
        self.obstacle = []
        for i  in range(self.height):
            row = []
            for j in range(self.width):
                # if A
                if 'A' == board[i][j]:
                    self.start = (i,j)
                    row.append(True)
                # if B
                elif 'B' == board[i][j]:
                    self.end = (i,j)
                    row.append(True)
                # if path
                elif ' ' == board[i][j]:
                    row.append(True)
                # if wall
                else:
                    row.append(False)
            self.obstacle.append(row)
            # this will serve as the checker if the maze is not yet finish or maybe it is endless
            self.solution = None
    def neighbor(self,state):
        row , col = state
        movement=[
            ("up",(row - 1,col)),
            ("down",(row + 1,col)),
            ("left",(row,col - 1)),
            ("right",(row,col + 1)), 
        ]
        result = []
        for action , (r,c) in movement:
            # check na dapat di lalagpas yung height and width at hindi dpat wall yung tatamaan
            if 0 <= r < self.height and 0 <= c < self.width and self.obstacle[r][c] :
                result.append((action,(r,c)))
        return result        

    def print(self):
        solution = self.solution[1] if self.solution else None
        print(solution)  
        for i,row in enumerate(self.obstacle):
            for j,col in enumerate(row):
               
                if not col:
                    print("☒",end=" ")
                elif (i,j) == self.start:
                    print("A",end=" ")
                elif (i,j) == self.end:
                    print("B",end=" ")
                elif solution is not None and (i,j) in solution:
                    print("*",end=" ")
                else:
                    print(" ",end=" ")
              
            print()
        print()
    def solved(self):
        # declare number of exploration
        self.num_explored = 0
        
        # initial state
        start = Node(state=self.start,parent=None,action=None)
        
        # declare a stack
        frontier = StackFrontier()
        frontier.add(start)

        # add all the node that you explore in self.explored
        self.explored = set()

        while True:

            # check if it is empty
            if frontier.empty():
                print("No Solution")
                return

            node = frontier.delete()
            self.num_explored+=1
            
            # check if the state you delete is the one can equal to our final state
            if node.state == self.end:
                action=[]
                coordinate = [] 
                while node.parent is not None:
                    action.append(node.action)
                    coordinate.append(node.state)
                    node = node.parent
                action.reverse()
                coordinate.reverse()
                self.solution = (action,coordinate)
                return

            # add the node that you remove to the set that is being explored
            self.explored.add(node.state)

            # get its neighbor
            for action, state in self.neighbor(node.state):
                # check if the the frontier is equal to the state that we collect and it should not be in the explored set
                if not frontier.contain(state) and state not in self.explored:
                    # if the condition is true you can create a child node that is connected to the root node 
                    child = Node(state=state,parent=node,action=action)
                    frontier.add(child)
    def output_image(self, filename, show_solution=True, show_explored=False):
        from PIL import Image, ImageDraw
        cell_size = 50
        cell_border = 2

        # Create a blank canvas
        img = Image.new(
            "RGBA",
            (self.width * cell_size, self.height * cell_size),
            "black"
        )
        draw = ImageDraw.Draw(img)

        solution = self.solution[1] if self.solution is not None else None
        for i, row in enumerate(self.obstacle):
            for j, col in enumerate(row):

                # Walls
                if not col:
                    fill = (40, 40, 40)

                # Start
                elif (i, j) == self.start:
                    fill = (255, 0, 0)

                # Goal
                elif (i, j) == self.end:
                    fill = (0, 171, 28)

                # Solution
                elif solution is not None and show_solution and (i, j) in solution:
                    fill = (220, 235, 113)

                # Explored
                elif solution is not None and show_explored and (i, j) in self.explored:
                    fill = (212, 97, 85)

                # Empty cell
                else:
                    fill = (237, 240, 252)

                # Draw cell
                draw.rectangle(
                    ([(j * cell_size + cell_border, i * cell_size + cell_border),
                      ((j + 1) * cell_size - cell_border, (i + 1) * cell_size - cell_border)]),
                    fill=fill
                )

        img.save(filename)
            
        

try:
    filename = input("Enter the file name : ")
    if not exists(filename):
        exit(1)
except:
    print("Error : File is not Found")
    exit(1)


maze = Maze(filename=filename)
maze.print()
maze.solved()
print("Path : ",maze.solution[0])
print("Coordinate : ",maze.solution[1])
maze.print()
maze.output_image("maze.png", show_explored=True)

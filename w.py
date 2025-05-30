import random
import time
from tkinter import Tk, BOTH, Canvas

class Window:
    def __init__(self, width, height):
        self.root = Tk()
        self.root.title("maze solver")
        self.root.protocol("WM_DELETE_WINDOW", self.close)
        self.canvas = Canvas(self.root, bg="white", width=width, height=height)
        self.canvas.pack(fill=BOTH, expand=1)
        self.running = False
    
    def redraw(self):
        self.root.update_idletasks()
        self.root.update()

    def draw_line(self, line_obj, color="black"):
        line_obj.draw(self.canvas, color)

    def wait_for_close(self):
        self.running = True
        while self.running:
            self.redraw()

    def close(self):
        self.running = False
          
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Line:
    def __init__(self, point1, point2):
        self.point1 = point1 
        self.point2 = point2

    def draw(self, canvas, color="black"):
        canvas.create_line(self.point1.x, self.point1.y, self.point2.x, self.point2.y, fill=color, width=2)
        
class Cell:
    def __init__(self, window_obj=None):
        self.has_left_wall = True 
        self.has_right_wall = True 
        self.has_top_wall = True 
        self.has_bottom_wall = True 
        self.visited = False

        self.x1 = -1
        self.x2 = -1
        self.y1 = -1
        self.y2 = -1

        self.win = window_obj

    def draw(self, x1, y1, x2, y2):
        if self.win is None: return 
        self.x1 = x1
        self.x2 = x2
        self.y1 = y1
        self.y2 = y2

        if self.has_left_wall:
           point1 = Point(x1, y1)
           point2 = Point(x1, y2)
           line = Line(point1, point2)
           self.win.draw_line(line) 
        else:
           point1 = Point(x1, y1)
           point2 = Point(x1, y2)
           line = Line(point1, point2)
           self.win.draw_line(line, "white")

        if self.has_top_wall:
           point1 = Point(x1, y1)
           point2 = Point(x2, y1)
           line = Line(point1, point2)
           self.win.draw_line(line) 
        else:
           point1 = Point(x1, y1)
           point2 = Point(x2, y1)
           line = Line(point1, point2)
           self.win.draw_line(line, "white")

        if self.has_right_wall:
           point1 = Point(x2, y1)
           point2 = Point(x2, y2)
           line = Line(point1, point2)
           self.win.draw_line(line) 
        else:
           point1 = Point(x2, y1)
           point2 = Point(x2, y2)
           line = Line(point1, point2)
           self.win.draw_line(line, "white")

        if self.has_bottom_wall:
           point1 = Point(x1, y2)
           point2 = Point(x2, y2)
           line = Line(point1, point2)
           self.win.draw_line(line) 
        else:
           point1 = Point(x1, y2)
           point2 = Point(x2, y2)
           line = Line(point1, point2)
           self.win.draw_line(line, "white")

    def draw_move(self, to_cell, undo=False):
        half = abs(self.x2 - self.x1) // 2
        xc = half + self.x1
        yc = half + self.y1

        half2 = abs(to_cell.x2 - to_cell.x1) // 2
        xc2 = half2 + to_cell.x1
        yc2 = half2 + to_cell.y1

        color = "red"
        if undo == True: color = "gray"

        point1 = Point(xc, yc) 
        point2 = Point(xc2, yc2)
        line = Line(point1, point2)
        self.win.draw_line(line, color)

class Maze:
    def __init__(self, x1, y1, num_rows, num_cols, cell_size_x, cell_size_y, win=None, seed=None):
        self.x1 = x1
        self.y1 = y1
        self.num_rows = num_rows
        self.num_cols = num_cols
        self.cell_size_x = cell_size_x
        self.cell_size_y = cell_size_y
        self.cells = []
        self.win = win
        if seed: random.seed(seed)

        self.create_cells()
        self.break_entrance_and_exit()
        self.break_walls_r(0, 0)
        
    def create_cells(self):
        self.cells = [ [ Cell(self.win) for i in range(self.num_rows) ] for i in range(self.num_cols) ]        
        for i in range(self.num_cols):
            for j in range(self.num_rows):
                self.draw_cell(i, j)

    def break_entrance_and_exit(self):
        self.cells[0][0].has_top_wall = False
        self.draw_cell(0, 0)
        self.cells[self.num_cols - 1][self.num_rows - 1].has_bottom_wall = False
        self.draw_cell(self.num_cols - 1, self.num_rows - 1)

    def break_walls_r(self, i, j):
        self.cells[i][j].visited = True
        while 1: 
            next_index_list = []

            if i > 0 and not self.cells[i -1][j].visited:
                next_index_list.append((i-1, j))
            if i < self.num_cols - 1 and not self.cells[i + 1][j].visited:
                next_index_list.append((i + 1, j))
            if j > 0 and not self.cells[i][j - 1].visited:
                next_index_list.append((i, j - 1))
            if j < self.num_rows - 1 and not self.cells[i][j + 1].visited:
                next_index_list.append((i, j + 1))

            if len(next_index_list) == 0:
                self.draw_cell(i, j)
                return 

            direction_index = random.randrange(len(next_index_list))
            next_index = next_index_list[direction_index]

            if next_index[0] == i + 1:
                self.cells[i][j].has_right_wall = False
                self.cells[i + 1][j].has_left_wall = False

            if next_index[0] == i - 1:
                self.cells[i][j].has_left_wall = False
                self.cells[i - 1][j].has_right_wall = False
            
            if next_index[1] == j + 1:
                self.cells[i][j].has_bottom_wall = False
                self.cells[i][j + 1].has_top_wall = False
            
            if next_index[1] == j - 1:
                self.cells[i][j].has_top_wall = False
                self.cells[i][j - 1].has_bottom_wall = False

            self.break_walls_r(next_index[0], next_index[1])
            

    def draw_cell(self, i, j):
        if self.win is None: return 
        x1 = self.x1 + i * self.cell_size_x
        y1 = self.y1 + j * self.cell_size_y
        x2 = x1 + self.cell_size_x
        y2 = y1 + self.cell_size_y
        self.cells[i][j].draw(x1, y1, x2, y2)
        self.animate()

    def animate(self):
        if self.win is None: return
        self.win.redraw()
        time.sleep(0.05)

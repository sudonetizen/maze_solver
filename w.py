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
    def __init__(self, window_obj):
        self.has_left_wall = True 
        self.has_right_wall = True 
        self.has_top_wall = True 
        self.has_bottom_wall = True 

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
        if self.has_top_wall:
           point1 = Point(x1, y1)
           point2 = Point(x2, y1)
           line = Line(point1, point2)
           self.win.draw_line(line) 
        if self.has_right_wall:
           point1 = Point(x2, y1)
           point2 = Point(x2, y2)
           line = Line(point1, point2)
           self.win.draw_line(line) 
        if self.has_bottom_wall:
           point1 = Point(x1, y2)
           point2 = Point(x2, y2)
           line = Line(point1, point2)
           self.win.draw_line(line) 

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

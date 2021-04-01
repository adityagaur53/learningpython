from turtle import *

#SCREEN SETUP
win = Screen()
bgcolor = "white"
win.bgcolor(bgcolor)
win_height = 900
win_width = 1200
win.setup(win_width, win_height)
win.title("Whiteboard")
win.setworldcoordinates(0,0, win_width, win_height)
#COLORS
colors = {
    "black" : "#000000",
    "red" : "#FF0000",
    "blue" : "#0000FF",
    "green" : "#00FF00",
    "gold" : "#FFD700",
    "yellow" : "#FFFF00",
    "purple" : "#9370DB",
    "grey" : "#D3D3D3"
}

widths = [1,2,4,6,8,10,12,15,18,20, 25]

#CHOOSING COLOR OF PEN
class colorBtnTurtle(Turtle):

    def selectColor(self, x, y):
        pen.color(self.color()[0])

    def drawSquare(self, colors, color):
        self.penup()
        self.speed('fastest')
        self.shapesize(2,2,2)
        self.shape("square")
        self.color(colors[color])
        self.pencolor(colors[color])
        self.goto(win_width - 30 - colors.keys().index(color)*50, win_height - 20)
        self.onclick(self.selectColor)

for color in colors:
    newcolor = colorBtnTurtle()
    newcolor.drawSquare(colors, color)

#CHOOSING WIDTH OF PEN
class widthBtnTurtle(Turtle):
    def selectWidth(self, x, y):
        pen.width(self.width())

    def drawWidthSquare(self, widths, width):
        self.penup()
        self.speed('fastest')
        self.color("black")
        self.shape("square")
        self.goto(widths.index(width)*50, win_height - 20)
        self.write(width, move = False, align = "center", font = ("Arial", 20, "normal"))
        self.goto(widths.index(width)*50, win_height - 40)
        self.width(width)
        self.onclick(self.selectWidth)

for width in widths:
    newwidth = widthBtnTurtle()
    newwidth.drawWidthSquare(widths, width)

#CLEAR BUTTON
ClearBtn = Turtle()
ClearBtn.penup()
ClearBtn.speed('fastest')
ClearBtn.goto(win_width - 100, 0)
ClearBtn.write("Clear", align = "center", font = ("Arial", 20, "normal"))
ClearBtn.goto(win_width - 100, 50)
ClearBtn.shape("square")
ClearBtn.shapesize(2,2,2)

#ERASE BUTTON
EB = Turtle()
EB.penup()
EB.speed('fastest')
EB.goto(win_width - 200, 0)
EB.write("Eraser", align = "center", font = ("Arial", 20, "normal"))
EB.goto(win_width - 200, 50)
EB.shape("square")
EB.shapesize(2,2,2)
def eraser(x,y):
    pen.pencolor("black")
    pen.color(bgcolor)

EB.onclick(eraser)



def clearpen(x,y):
    pen.clear()
ClearBtn.onclick(clearpen)

#UNDO USING RIGHT CLICK
def undopen(x,y):
    for i in range(20):
        pen.undo()
win.onclick(undopen, btn=2)

topmargin  = 100
bottommargin = 100

#MAKING PEN
pen = Turtle()
pen.speed('fastest')
pen.shapesize(2,2,2)
pen.shape("circle")
pen.pendown()

def dragging(x, y):
    pen.ondrag(None)
    pen.setheading(pen.towards(x, y))

    if y < (win_height - topmargin) and y > (bottommargin):
        pen.goto(x, y)
    pen.ondrag(dragging)

pen.ondrag(dragging)

def newpos(x,y):
    pen.penup()
    pen.goto(x,y)
    pen.pendown()

win.onclick(newpos)

win.listen()
mainloop()

import time
from time import strftime
import datetime
from peewee import *
from tkinter import *

db = SqliteDatabase('max3.db')

class MaxScore(Model):

	id = IntegerField()
	maxdt = CharField()

	class Meta:
		database = db
		db_table = 'max3'

db.connect()

try:
	items =  MaxScore.select().where(MaxScore.id ==1)
	for item in items:
		print(item.maxdt)

except:
	MaxScore.create_table()
	diff2 = datetime.datetime.strptime(strftime('%H:%M:%S %p'), '%H:%M:%S %p')\
			- datetime.datetime.strptime(strftime('%H:%M:%S %p'),'%H:%M:%S %p')
	max1  = MaxScore.create(maxdt = "testing", id = 1)
	max1.save()
	items =  MaxScore.select().where(MaxScore.id == 1)
	for item in items:
		print(item.maxdt)







tk = Tk()
width = 400
height = 400
canvas = Canvas(tk, width=width, height=height)

textID = canvas.create_text(200, 30, text= " ")

x_speed = 10
y_speed = 10

class Ball:
	def __init__(self, paddle, id = None):
		self.id = canvas.create_oval(10, 10, 50, 50, fill="red")
		self.x_speed = 2
		self.y_speed = 1
		self.paddle = paddle.id

	def moveBall(self):

		canvas.move(self.id, self.x_speed, self.y_speed)
		k = canvas.coords(self.id)

		topleft_x = k[0]
		topleft_y = k[1]
		btmright_x = k[2]
		btmright_y = k[3]

		d = canvas.coords(self.paddle)

		#check bounce
		if topleft_x <= 0: #bouncing off left wall
			self.x_speed *= -1

		elif topleft_y <= 0: #bouncing off top wall
			self.y_speed *= -1

		elif btmright_x >= width: #bouncing off right wall
			self.x_speed *= -1

		elif topleft_x >= d[0] and btmright_x <= d[2] and btmright_y == 350: #x of ball is within left, rightx of paddle, y of ball is == y of paddle
			self.y_speed *= -1

	def gameplaying(self):
		if canvas.coords(self.id)[3] >= width:
			return False
		return True

	def restart(self):
		canvas.move(self.id, 0, -250)
		canvas.itemconfig(textID, text = " ")



class Paddle:

	def __init__(self, id = None):
		self.id = canvas.create_rectangle(50, 350, 150, 375, fill="blue")


	def movepaddle(self, event):
		l = canvas.coords(self.id)

		if event.keysym == 'Right' and l[2] <= width:
			canvas.move(self.id, 5, 0)
		elif event.keysym == 'Left' and l[0] >= 0:
			canvas.move(self.id, -5, 0)


class Score:
	def __init__(self, id=None):
		self.id = canvas.create_text(200, 60, text= "00:00")
		self.datetimeFormat = '%H:%M:%S %p'
		self.starttime = strftime('%H:%M:%S %p')
		self.current = 0

		items =  MaxScore.select().where(MaxScore.id ==1)
		for item in items:

			print(item.maxdt)
			self.max = item.maxdt


	def reset(self):
		self.starttime = strftime('%H:%M:%S %p')
		newtext = str(self.current)
		query = MaxScore.update(maxdt = newtext).where(MaxScore.id == 1)
		n = query.execute()

	def update(self):
		diff = datetime.datetime.strptime(strftime('%H:%M:%S %p'), self.datetimeFormat)\
				- datetime.datetime.strptime(self.starttime, self.datetimeFormat)
		self.current = diff

		getitems =  MaxScore.select().where(MaxScore.id == 1)
		for item in getitems:
			maxtext = item.maxdt


		string = "Current : " + str(self.current) + "\n Max: " + str(maxtext)
		canvas.itemconfig(self.id, text=string)

p = Paddle()
b = Ball(p)
s = Score()

def restart():
	b.restart()
	s.reset()

btn = Button(tk, text="Restart", command=restart)
btn.pack()

canvas.bind_all('<KeyPress-Left>', p.movepaddle)
canvas.bind_all('<KeyPress-Right>', p.movepaddle)

canvas.pack()

while 1:
	tk.update()
	time.sleep(0.01)
	tk.update_idletasks()

	if b.gameplaying():
		b.moveBall()
		s.update()
	else:
		canvas.itemconfig(textID, text = "Game over")

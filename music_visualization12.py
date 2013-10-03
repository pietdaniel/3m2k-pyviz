#
#	mv12 
#
#
import pygame, math, types, operator
from pygame.locals import *
from random import randint,choice,randrange
from math import pi, sin, asin, tan, cos
import os

# import cv2
width=1920
height=1080
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (0,0)
scr = pygame.display.set_mode((width,height))
w,h = scr.get_size()
white = (255,255,255)
black = (0,0,0)

def toggle_fullscreen():
    screen = pygame.display.get_surface()
    tmp = screen.convert()
    w,h = screen.get_width(),screen.get_height()
    flags = screen.get_flags()
    bits = screen.get_bitsize()
    pygame.display.init()
    screen = pygame.display.set_mode((w,h),flags^FULLSCREEN,bits)
    screen.blit(tmp,(0,0))
    pygame.key.set_mods(0) #HACK: work-a-round for a SDL bug??
    return screen

def ifquit(loop):
	(b1,b2,b3)=pygame.mouse.get_pressed()
	if b2:
		loop = 3
	for e in pygame.event.get():
		if e.type == KEYDOWN and e.key == K_ESCAPE or e.type == QUIT:
			loop = 3
		if e.type == KEYDOWN and e.key == K_SPACE:
			print "**** MARKER **** MARKER **** MARKER **** MARKER **** MARKER **** MARKER ****"
	return loop

def spf(samples_num,song_length,fps):
	print "--"
	print samples_num
	print song_length
	print fps
	print "--"
	return samples_num/song_length/fps

def function1(x):
	x=long(x)
	return abs(((255*(x*x))-999) / ((x*x) + 99999999))


class Box():
	def __init__(self, x=0,y=0,xv=0,yv=0,col=white,size=50):
		self.x=x
		self.y=y
		self.xv=xv
		self.yv=yv
		self.col=col
		self.size=size
	def draw(self,scr):
		d = math.sqrt(self.size*self.size)
		pygame.draw.polygon(scr,self.col,( (self.x,self.y),(self.x+self.size,self.y+self.size),(self.x,self.y+self.size*2),(self.x-self.size,self.y+self.size) ), 1 )
		y2 = self.y+self.size
		pygame.draw.polygon(scr,self.col,( (self.x,y2),(self.x+self.size,y2+self.size),(self.x,y2+self.size*2),(self.x-self.size,y2+self.size) ), 1 )
		pygame.draw.line(scr,self.col, (self.x,self.y) , (self.x,y2) )
		pygame.draw.line(scr,self.col, (self.x+self.size,self.y+self.size) , (self.x+self.size,y2+self.size) )
		pygame.draw.line(scr,self.col, (self.x-self.size,self.y+self.size) , (self.x-self.size,y2+self.size) )
		pygame.draw.line(scr,self.col, (self.x,self.y+2*self.size) , (self.x,y2+2*self.size) )
	def transport(self,x,y):
		self.x=x
		self.y=y
	def move(self):
		self.x+=self.xv
		self.y+=self.yv
	def push(self,x,y):
		self.xv+=x
		self.yv+=y
	def bounce_X(self):
		self.xv=self.xv*-1
	def bounce_Y(self):
		self.yv=self.yv*-1
	def contain(self):
		if (self.x+self.size>width or self.x-self.size<0):
			self.bounce_X()
			self.move()
		if (self.y+self.size*2>height or self.y<0):
			self.bounce_Y()
			self.move()

	def gravitate(self,x,y):
		difx = self.x - x
		dify = self.y - y
		self.xv -= int(.0025*difx) if (difx!=0) else 0
		self.yv -= int(.0025*dify) if (dify!=0) else 0

def randcol():
	return (randint(0,255),randint(0,255),randint(0,255))

class Ball():
	xv = 0
	yv = 0
	x = 0
	y = 0
	r=1
	prev = (x,y)
	col=white
	def move(self):
		self.prev = (self.x,self.y)
		self.x+=self.xv
		self.y+=self.yv
	def push(self,x,y):
		self.xv+=x
		self.yv+=y
	def draw(self,scr):
		pygame.draw.aaline(scr,self.col,self.prev,(self.x,self.y))
	def draw1(self,scr):
		pygame.draw.aaline(scr,self.col,self.prev,(self.x,self.y))
		pygame.draw.circle(scr,self.col,self.prev,5,1)
	def draw2(self,scr):
		pygame.draw.aaline(scr,self.col,self.prev,(self.x,self.y))
		pygame.draw.rect(scr,white,(self.x-12,self.y-12,25,25),1)
	def bounce_X(self):
		self.xv=self.xv*-1
	def bounce_Y(self):
		self.yv=self.yv*-1
	def contain(self):
		if (self.x>width or self.x<0):
			self.bounce_X()
			self.move()
		if (self.y>height or self.y<0):
			self.bounce_Y()
			self.move()
	def col_drift(self):
		(r1,b1,g1)=self.col
		r1=abs((r1+1)%255)
		b1=abs((b1+1)%255)
		g1=abs((g1+1)%255)
		self.col=(r1,b1,g1)
	def col_drift2(self):
		(r1,b1,g1)=self.col
		r1=abs((r1+6)%255)
		b1=abs((b1-1)%255)
		g1=abs((g1+4)%255)
		self.col=(r1,b1,g1)
	def __str__(self):
		return " x " + str(self.x) + " y " + str(self.y) + " xv " + str(self.xv) + " yv " + str(self.yv)



def main():
	pygame.mouse.set_visible(0)
	pygame.font.init()
	pygame.mixer.init()
	pygame.mixer.music.load("here.flac")
	# toggle_fullscreen()	
	sctr=0
	wait_time = 1
	loop = 0

	myfont = pygame.font.SysFont("", 300)
	myfont3 = pygame.font.SysFont("", 290)
	myfont2 = pygame.font.SysFont("arial", 10)
	label = myfont.render("3M2K", 1, (255,255,255))
	label2 = myfont.render("3M2K", 1, (0,0,0))
	label3 = myfont3.render("3M2K", 1, (255,0,250))
	label4 = myfont3.render("3M2K", 1, (0,255,250))

	pygame.mixer.music.play()
	ctr=0

	timestamp =0

	size = 500
	x = randint(0,width)
	y = randint(0,height)
	c = white

	ball = Ball()
	ball.x = 100
	ball.y = 100
	ball.push(15,15)

	ball2 = Ball()
	ball2.x = width-100
	ball2.y = height-100
	ball2.push(-15,-15)
	ball2.prev=(width,height)

	boxes = []
	for i in range(0,100):
		boxes.append(Box(randint(100,width-100),randint(0,100),randint(-4,4),40,randcol()))

	while not loop:
		# scr.fill(black)

		timestamp = pygame.mixer.music.get_pos()
		# print timestamp

		if timestamp>93428: #93428
			scr.scroll(randint(-10,10),700)
			if ctr%7==0:
				scr.fill(black)
			for box in boxes:
				box.push(randint(-1,1),randint(-1,1))
		elif timestamp>81623:
			scr.scroll(randint(-1,1),10)

		if timestamp>38039 and timestamp<76904: 
			scr.scroll(randint(-2,2),randint(-2,2))

		if (timestamp>=38039 and timestamp<=38439):
			ball2.col=(255,40,40)
			ball.col=(255,40,40)
			ball2.push(0,1)
			ball.push(-1,0)


		if (timestamp>76904):
			for box in boxes:
				box.draw(scr)
				box.move()
				box.contain()
		elif (timestamp>64970 and timestamp<66502):
			scr.scroll(50,randint(-2,2))
		elif (timestamp>66502):
			scr.fill(black)
			for box in boxes:
				box.draw(scr)
				box.move()
				box.contain()

			# ball.push(-1,-1)
			# ball.col_drift2()
			# ball2.push(1,1)
			# ball2.col_drift2()
			# ball.draw1(scr)
			# ball2.draw1(scr)
		elif (timestamp>38039):
			ball.push(2,2)
			ball2.push(-2,-2)


		if timestamp<64949:
			ball.draw(scr)
			ball.col_drift()
			ball.move()
			ball.contain()
			ball2.draw(scr)
			ball2.col_drift()
			ball2.move()
			ball2.contain()

		scr.blit(label2, (654, 442))
		scr.blit(label, (654, 440))

		ctr+=1
		if (pygame.mixer.music.get_pos()<0):
			loop=1
		
		pygame.display.flip()
		loop = ifquit(loop)
		pygame.time.wait(32)

main()
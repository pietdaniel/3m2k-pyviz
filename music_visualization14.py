#
#	mv14 uses ball to make flame looking things
#   theta log n
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

class Ball():
	def __init__(self, x=0,y=0,xv=0,yv=0,col=white):
		self.xv = xv
		self.yv = yv
		self.x = x
		self.y = y
		self.r=10
		self.prev = (self.x,self.y)
		self.col=col
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
	def gravitate(self,x,y):
		difx = self.x - x
		dify = self.y - y
		self.xv -= int(.0025*difx) if (difx!=0) else 0
		self.yv -= int(.0025*dify) if (dify!=0) else 0

def randcol():
	return (randint(0,255),randint(0,255),randint(0,255))


def main():
	pygame.mouse.set_visible(0)
	pygame.font.init()
	pygame.mixer.init()
	pygame.mixer.music.load("theta.flac")
	sound = pygame.mixer.Sound("theta.flac")
	samples = pygame.sndarray.array(sound)
	# toggle_fullscreen()	
	sctr=0
	wait_time = 1
	loop = 0

	myfont = pygame.font.SysFont("", 300)
	myfont3 = pygame.font.SysFont("", 290)
	myfont2 = pygame.font.SysFont("arial", 10)
	myfont4 = pygame.font.SysFont("", 320)
	label = myfont.render("3M2K", 1, (255,255,255))
	label2 = myfont.render("3M2K", 1, (0,0,0))
	label3 = myfont3.render("3M2K", 1, (255,0,250))
	label4 = myfont3.render("3M2K", 1, (0,255,250))
	label5 = myfont4.render("3M2K", 1, (5,0,0))

	pygame.mixer.music.play()
	ctr=0
	increment = len(samples)/1816

	timestamp =0

	size = 500
	x = randint(0,width)
	y = randint(0,height)
	c = white
	screen = 0
	l=0
	r=0

	qx = 2
	qy1 = 0
	qy2 = 50
	threshold = 27000;

	scr.blit(label2, (654, 442))
	scr.blit(label, (654, 440))

	balls=[]
	for i in range(0,100):
		balls.append(Ball(randint(0,width),randint(0,height),randint(-10,10),randint(-10,10),randcol()))

	while not loop:

		if timestamp%74579 <= 100 and timestamp>100:
			qx = 10
			qy1 = -50
			qy2 = 0
		if timestamp>112755:
			qx = 2
			qy1 = 0
			qy2 = 50
			threshold = 22000;

		if timestamp>5300 and timestamp<5400:
			scr.fill((100,0,0))

		
		screen = scr.copy()
		if (screen):
			scr.set_alpha(128)
			scr.blit(screen,(randint(-qx,qx),randint(qy1,qy2)), None,5)



		timestamp = pygame.mixer.music.get_pos()
		# print timestamp
		# print "ctr: " + str(ctr) + " timestamp: " + str(timestamp) + " sctr: " + str(sctr)
		# if l and r:
		# 	# print "l: " + str(l) + " r: " + str(r)

		if (abs(l)>threshold):
			scr.fill((0,0,0))


		for ball in balls:
			ball.draw(scr)
			ball.move()
			ball.contain()

		if (sctr<len(samples)):
			(l,r) = samples[sctr]


			
		sctr+=increment
		ctr+=1
		if (pygame.mixer.music.get_pos()<0):
			loop=1
		# pygame.draw.rect(scr,black,(650,441,590,180))
		screen = scr.copy()
		scr.blit(label5, (640, 440))
		scr.blit(label2, (654, 442))
		scr.blit(label, (654, 440))
		pygame.display.flip()
		
		loop = ifquit(loop)
		pygame.time.wait(1)

main()

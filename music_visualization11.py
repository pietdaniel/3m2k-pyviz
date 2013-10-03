#
#	mv11 sky
#
#
import pygame, math, types
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



def main():
	pygame.mouse.set_visible(0)
	pygame.font.init()
	pygame.mixer.init()
	# sound = pygame.mixer.Sound("luvin.wav")
	pygame.mixer.music.load("sky.mp3")
	# samples = pygame.sndarray.array(sound)
	
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

	# prev = samples[0]

	pygame.mixer.music.play()
	ctr=0
	# increment = len(samples)/11681

	timestamp =0

	size = 500
	x = randint(0,width)
	y = randint(0,height)
	c = white

	
	while not loop:
		# scr.fill(black)

		screen = scr.copy()
		if timestamp >= 3656:#3656:
			scr.blit(label2, (654, 442))
			scr.blit(label, (654, 440))
			pygame.display.flip()
		if (screen):
			screen.set_alpha(254)
			scr.blit(label2, (654, 442))
			scr.blit(label, (654, 440))
			scr.blit(screen,(-10,0))



		timestamp = pygame.mixer.music.get_pos()
		print timestamp
		if timestamp >= 3656:#3656:
			(r1,g1,b1)=c
			r1-=1
			g1-=2
			b1-=3
			c=(abs(r1%255),abs(g1%255),abs(b1%255))
			pygame.draw.rect(scr,c,(x+size,y-size/2,size,size),1)
			size-=10

			if (size<=-500):
				size = 500
				x = randint(0,width)
				y = randint(200,height)
				# c = white


		ctr+=1
		# sctr+=increment
		# timestamp = pygame.mixer.music.get_pos()
		if (pygame.mixer.music.get_pos()<0):
			loop=1
		# if (sctr<len(samples)):
		# 	(l,r) = samples[sctr]
		
		pygame.display.flip()
		loop = ifquit(loop)
		# pygame.time.wait(2)

main()
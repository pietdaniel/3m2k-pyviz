#
#	mv9 uses sound levels and draws scenes
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
	sound = pygame.mixer.Sound("novalue.flac")
	pygame.mixer.music.load("novalue.flac")
	samples = pygame.sndarray.array(sound)
	
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

	x=564
	y=642

	prev = samples[0]

	pygame.mixer.music.play()
	ctr=0
	increment = len(samples)/11681

	timestamp =0
	
	while not loop:
		ctr+=1
		if (timestamp>0):
			if timestamp>72501:
				scr.scroll(0,10)
			else:
				scr.scroll(-5,0)

		sctr+=increment
		timestamp = pygame.mixer.music.get_pos()
		# print ctr
		print timestamp

		if (timestamp>27627 and timestamp<87729):
			pygame.draw.rect(scr, (randint(0,255),0,randint(0,255)) , (0,height/3,width,height/3 ) )
		if (timestamp>39597 and timestamp<57200):
			if (l>10000):
				scr.fill((0,0,0))

		if (pygame.mixer.music.get_pos()<0):
			loop=1

		if (sctr<len(samples)):
			(l,r) = samples[sctr]
		
			# print str(l)+" "+str(r)+" "+str(sctr)
			# print str(l)+" "+str(function1(l))+" function1"
			if (function1(l)<0 or function1(l)>255):
				print str(l)+" "+str(function1(l))+" function1"

			if timestamp<72501: 
				pygame.draw.rect(scr,(255,function1(l),255),(width-20,height/4,2,l/100));
				pygame.draw.rect(scr,(255,function1(r),255),(width-20,(3*height)/4,2,r/100));
				pygame.draw.rect(scr,black,(650,441,590,180))
			else:
				pygame.draw.rect(scr,(255,function1(l),function1(l)),(width/4,20,l/100,2));
				pygame.draw.rect(scr,(function1(r),function1(r),255),((3*width)/4,20,r/100,2));

		scr.blit(label3, (650, 441+l/5000))
		scr.blit(label4, (668, 441+l/5000))
		scr.blit(label2, (654, 442+l/5000))
		scr.blit(label, (654, 440+l/5000))


		pygame.display.flip()
		loop = ifquit(loop)
		pygame.time.wait(2)

main()
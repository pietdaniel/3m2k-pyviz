#
#	mv4 uses sound levels of left and right
#	channels to place anti aliased lines
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
	return samples_num/song_length/fps

def main():
	pygame.mouse.set_visible(0)
	pygame.font.init()
	pygame.mixer.init()
	sound = pygame.mixer.Sound("ROLLING.wav")
	samples = pygame.sndarray.array(sound)
	# pygame.time.wait(5000)
	# len(samples)/len(song)/fps = samples per frame

	# toggle_fullscreen()	
	ctr=0
	sctr=1;
	wait_time = 20
	fps = 1000/wait_time
	myspf = spf(len(samples),sound.get_length(),fps-8)
	loop = 0

	delta0=0.
	delta1=0.
	p=0.
	q=0.

	myfont = pygame.font.SysFont("", 300)
	myfont2 = pygame.font.SysFont("arial", 10)
	label = myfont.render("3M2K", 1, (255,255,255))
	label2 = myfont.render("3M2K", 1, (0,0,0))

	x=564
	y=642

	prev = samples[0]
	
	
	while not loop:
		if (ctr%3==0):
			scr.fill((0,0,0,.9))		
		ctr+=1

		if (sctr<len(samples)):
			(l,r) = samples[sctr]
		
			

			if (sctr>0):
				(n,m)=prev
				pygame.draw.aaline(scr, (255-(ctr%255),255-(ctr%255),255-(ctr%255)), ((l+15)%width,r%height),((l+15)%width,height-440))
				for i in range(1,25,5):
					pygame.draw.aaline(scr, (0,0,255), ((n+i)%width,m%height),((l+i)%width,r%height))
				
			else:
				pygame.draw.aaline(scr,((254-ctr/11)%255,(254-ctr/10)%255,255),(0,0),(l%width,r%height))
				pygame.draw.aaline(scr,((254-ctr/11)%255,(254-ctr/10)%255,255),(width,0),(l%width,r%height))
				pygame.draw.aaline(scr,((254-ctr/11)%255,(254-ctr/10)%255,255),(0,height),(l%width,r%height))
				pygame.draw.aaline(scr,((254-ctr/11)%255,(254-ctr/10)%255,255),(width,height),(l%width,r%height))


			# pygame.draw.circle(scr,(255,255,255),(400,100),abs(l/200))
			# pygame.draw.circle(scr,(255,255,255),(500,100),abs(r/200))
			if (ctr%113==0):
				delta0=p-q	
			q = round((sctr/len(samples))*sound.get_length(),10)
			p = round(pygame.time.get_ticks()/1000.,10)
			delta1=p-q

			if (abs(p-q)>1 and ctr%7==0):
				if ((p-q)<0):
					myspf*=.99
				elif ((p-q)>0):
					myspf*=1.01
			else:
				if (ctr%57==0):
					if ((p-q)<-0.1):
						if (abs(delta1-delta0)<.1):
							myspf-=1
					elif ((p-q)>0.1):
						if (abs(delta1-delta0)<.1):
							myspf+=1

			scr.blit(myfont2.render(str(round(q,3)), 1, (255,255,255)), (5, 5))
			scr.blit(myfont2.render(str(round(p,3)), 1, (255,255,255)), (5, 20))
			scr.blit(myfont2.render(str(round(p-q,3)), 1, (255,255,255)), (5, 35))
			scr.blit(myfont2.render(str(round(delta1-delta0,3)), 1, (255,255,255)), (5, 50))
			scr.blit(myfont2.render(str(round(myspf,3)), 1, (255,255,255)), (5, 65))
			

			scr.blit(label2, (654, 442))
			scr.blit(label, (654, 440))
		else:
			scr.blit(label2, (654, 442))
			scr.blit(label, (654, 440))

		pygame.display.flip()
		if (sctr==1):
			channel = sound.play()
		loop = ifquit(loop)
		sctr+=myspf
		pygame.time.wait(wait_time)
		prev = (l,r)

main()
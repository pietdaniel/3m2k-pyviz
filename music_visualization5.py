#
#	mv5 looks like vomit in a good way
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

def toggle_fullscreen():
    screen = pygame.display.get_surface()
    tmp = screen.convert()
    w,h = screen.get_width(),screen.get_height()
    flags = screen.get_flags()
    bits = screen.get_bitsize()
    pygame.display.init()
    screen = pygame.display.set_mode((w,h),flags^FULLSCREEN,bits)
    screen.blit(tmp,(0,0))
    pygame.key.set_mods(0) 
    return screen

def ifquit(loop):
	(b1,b2,b3)=pygame.mouse.get_pressed()
	if b2:
		loop = 3
	for e in pygame.event.get():
		if e.type == KEYDOWN and e.key == K_ESCAPE or e.type == QUIT:
			loop = 3
	return loop

def play_song(song):
	pygame.mixer.init()
	pygame.mixer.music.load(song)
	pygame.mixer.music.play()

def main():
	pygame.mouse.set_visible(0)
	pygame.font.init()
	# toggle_fullscreen()	
	ctr=0
	loop = 0

	myfont = pygame.font.SysFont("", 300)
	myfont3 = pygame.font.SysFont("", 290)
	label = myfont.render("3M2K", 1, (255,255,255))
	label2 = myfont.render("3M2K", 1, (0,0,0))
	label3 = myfont3.render("3M2K", 1, (255,0,250))
	label4 = myfont3.render("3M2K", 1, (0,255,250))

	x=-10
	y=10

	play_song("crazy_noise.wav")

	scr.blit(label2, (654, 442))
	scr.blit(label, (654, 440))
	pygame.display.flip()

	t=0
	q=0
	while not loop:
		# scr.fill((0,0,0))
		ctr+=80
		# q+=1
		# if (q%2==0):
		# 	t=scr.copy()
		# 	scr.fill((q%255,0,0))
		# else:
		# 	if (t):
		# 		scr.blit(t,(0,0))

		timestamp = pygame.mixer.music.get_pos()
		if timestamp >= 55300 and timestamp<=78043:
			l = randint(0,10)
			m = randint(11,150)
			scr.fill((m+l,m-l,m))
			scr.blit(label3, (650, 441+l/5000))
			scr.blit(label4, (668, 441+l/5000))
			scr.blit(label2, (654, 442+l/5000))
			scr.blit(label, (654, 440+l/5000))
		if timestamp >= 78044 and timestamp<=78144:
			scr.fill((0,0,0))

		# print timestamp
		
		for i in range(0,100):
			q=randint(0,width)
			p=randint(0,height)
			if (i%3==0):
				pygame.draw.aaline(scr,( (254-(ctr/700))%255,(254-(ctr/500))%255,(254-(ctr/900))%255 ),(x+q,y+p),(x+100+q,y-100+p+(ctr/10000)),True)
			elif (i%2==0):
				pygame.draw.circle(scr,( (254-(ctr/1000))%255,(254-(ctr/800))%255,(254-(ctr/900))%255 ),(x+q,y+p),1)
			elif (i%5==0):
				pygame.draw.rect(scr,( (254-(ctr/600))%255,(254-(ctr/800))%255,(254-(ctr/900))%255 ),(x+q,y+p,10,10),1)
			else:
				pygame.draw.rect(scr,( 0,0,randint(0,255) ),(x+q,y+p,5,5),1)

		# print timestamp

		if (pygame.mixer.music.get_pos()<0):
			loop=1		
	
		# if (ctr%10000==0):
		# 	y+=5;

		scr.blit(label2, (654, 442))
		scr.blit(label, (654, 440))
		pygame.display.flip()
		loop = ifquit(loop)
		pygame.time.wait((100000-ctr)/ctr)
		pygame.time.wait(40)

main()












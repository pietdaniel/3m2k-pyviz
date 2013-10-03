#
#	mv3 draws squares on a sine function
#	while changing the colors
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
	label = myfont.render("3M2K", 1, (255,255,255))
	label2 = myfont.render("3M2K", 1, (0,0,0))

	play_song("Pulp.wav")

	scr.blit(label2, (654, 442))
	scr.blit(label, (654, 440))
	pygame.display.flip()
	pygame.time.wait(300)
	x=500
	y=500

	while not loop:
		# scr.fill((0,0,0))		
		ctr+=1


		pygame.draw.rect(scr,( x%255, (x+(ctr/100))%255, (x+(ctr/50))%255 ),(x,y,10,10),1)

		x=(sin(x)+.6)*width
		y=(sin(y)+.6)*height

	
		scr.blit(label2, (654, 442))
		scr.blit(label, (654, 440))

		pygame.display.flip()
		loop = ifquit(loop)
		if (ctr<200):
			pygame.time.wait(200-ctr)

		pygame.time.wait(0)

main()
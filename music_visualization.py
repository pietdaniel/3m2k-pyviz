#
#	mv1 contains some dead functions
#	draws aalines and moves them
# 	[lostinthecrowd]
import pygame, math, types
from pygame.locals import *
from random import randint,choice,randrange
import os
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

def bossImg(pos):
		(x,y)=pos
		def loop(x,y,rad,color):
			x1=x
			ctr=1
			while rad > 1:
				pygame.draw.circle(scr,color,(x,y),rad)
				moreCirc(x,y,rad,color)
				moreCirc(x1,y,rad,color)
				pygame.draw.circle(scr,color,(x1,y),rad)
				x+=rad
				x1-=rad
				rad=int(rad/2)
				x+=rad
				x1-=rad
				
		def moreCirc(x,y,rad,color):
			if rad > 2: moreCirc(x-rad,y,rad/2,color), moreCirc(x+rad,y,rad/2,color)
			while rad>1:
				y+=rad
				rad=int(rad/1.9)
				y+=rad
				pygame.draw.circle(scr,color,(x,y),rad)
				
		for i in range(1,150,25):
			loop(x,y,150-i,pygame.Color(randint(1,255),randint(1,255),randint(1,255)))

# can really take any x and y
def collatz(pos):
	(x,y)=pos
	if (x%2==0):
			x=x/2
	else:
		x=x*3+1
	if (x<=1):
		x=randint(0,1079)

	if (y%2==0):
		y=y/2
	else:
		y=y*3+1
	if (y<=1):
		y=randint(0,1919)
	pygame.draw.circle(scr,(255,255,255),(x,y),4)
	pygame.draw.circle(scr,(0,0,0),(x+1,y+1),2)
	return (x,y)

def cornerLines(pos,ctr):
	(x,y)=pos
	pygame.draw.aaline(scr,( (x+(ctr/100))%255, x%255, (x-(ctr/50))%255  ),(0,0),(x,y),True)
	pygame.draw.aaline(scr,( (x+(ctr/100))%255, x%255, (x-(ctr/50))%255  ),(0,0),(y,x),True)
	pygame.draw.aaline(scr,( (x+(ctr/100))%255, x%255, (x-(ctr/50))%255  ),(width,height),(width-x,height-y),True)
	pygame.draw.aaline(scr,( (x+(ctr/100))%255, x%255, (x-(ctr/50))%255  ),(width,height),(width-y,height-x),True)
	pygame.draw.aaline(scr,( (x+(ctr/100))%255, x%255, (x-(ctr/50))%255  ),(width,0),(width-x,y),True)
	pygame.draw.aaline(scr,( (x+(ctr/100))%255, x%255, (x-(ctr/50))%255  ),(width,0),(width-y,x),True)
	pygame.draw.aaline(scr,( (x+(ctr/100))%255, x%255, (x-(ctr/50))%255  ),(0,height),(x,height-y),True)
	pygame.draw.aaline(scr,( (x+(ctr/100))%255, x%255, (x-(ctr/50))%255  ),(0,height),(y,height-x),True)
	if (x>10):
		x-=4
	else:
		x=width
	if (y>10):
		y-=4
	else:
		y=width
	y+=3
	return (x,y)

def play_song(song):
	pygame.mixer.init()
	pygame.mixer.music.load(song)
	pygame.mixer.music.play()

def keyListener():
	key=pygame.key.get_pressed()
	if key[pygame.K_r]:
		return 1
	if key[pygame.K_e]:
		return 2
	if key[pygame.K_w]:
		return 3
	if key[pygame.K_q]:
		return 4
	else:
		return 0

def ifquit(loop):
	(b1,b2,b3)=pygame.mouse.get_pressed()
	if b2:
		loop = 3
	for e in pygame.event.get():
		if e.type == KEYDOWN and e.key == K_ESCAPE or e.type == QUIT:
			loop = 3
	return loop

def main():
	pygame.mouse.set_visible(0)
	pygame.font.init()
	# toggle_fullscreen()

	pygame.mixer.init()
	sound = pygame.mixer.Sound("smooth.wav")
	samples = pygame.sndarray.array(sound)

	ctr=0
	loop = 0

	myfont = pygame.font.SysFont("", 300)
	label = myfont.render("3M2K", 1, (255,255,255))
	label2 = myfont.render("3M2K", 1, (0,0,0))

	x=width
	y=0
	x2 = 100
	y2 = 100
	play_song("smooth.wav")
	# sound.play()
	while not loop:
		# scr.fill((0,0,0))
		ctr+=1
		# bossImg((680,400))	
		(x,y) = cornerLines((x,y),ctr)
		# (x2,y2) = collatz((x2,y2))
		scr.blit(label2, (654, 442))
		scr.blit(label, (654, 440))
		if (pygame.mixer.music.get_pos()<0):
			loop=1	
		pygame.display.flip()
		loop = ifquit(loop)
		pygame.time.wait(80)

main()












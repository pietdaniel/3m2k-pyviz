#
#	mv6 uses motherfucking midi
#		
#
import pygame, math, types
import pygame.midi
from pygame.locals import *
from random import randint,choice,randrange
from math import pi, sin, asin, tan, cos
import os
from pprint import pprint
import midi

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

# len(samples)/len(song)/fps = samples per frame
def spf(samples_num,song_length,fps):
	return samples_num/song_length/fps

def ms_per_tick(bpm):
	return 60000 / (bpm*120)

def data_from_midi(array):
	data=[]
	for i in range(0,len(array)):
		if (type(array[i])==midi.NoteOnEvent):
			if array[i].velocity!=0:
				data.append((array[i].tick,array[i].pitch,array[i].velocity,array[i].length))
	return data

# returns an array tracks where each track is array(tick,pitch,vel,len)
def create_tracks(midifile):
	z = midi.read_midifile(midifile)
	z.make_ticks_abs()
	data=[]
	for i in range(0,len(z)):
		data.append(data_from_midi(z[i]))
	data = filter(lambda x: len(x)!=0,data)
	pprint(z[0])
	return data

def note_feed(track,ctr):
	if (len(track)>0 and track[0][0]<=ctr):
		return track.pop(0)

def get_clock_divisor(midifile):
	z = midi.read_midifile(midifile)
	return z[0][1].mpqn/(z.resolution*1000.)

def draw_data(temp,i,scr):
	scr.blit(myfont3.render(str(temp[1]), 1, (255,(i*113)%255,(i*57)%255)), ((20+150*i)%width, 100))
	scr.blit(myfont3.render(str(temp[0]), 1, (255,(i*113)%255,(i*227)%255)), ((20+150*i)%width, 150))
	scr.blit(myfont3.render(str(temp[2]), 1, (255,(i*113)%255,(i*1053)%255)), ((20+150*i)%width, 200))
	scr.blit(myfont3.render(str(temp[3]), 1, (255,(i*113)%255,(i*1001)%255)), ((20+150*i)%width, 250))


def main2():
	pygame.mouse.set_visible(0)
	pygame.font.init()
	# toggle_fullscreen()
	loop = 0
	ctr=0
	myfont = pygame.font.SysFont("", 300)
	myfont2 = pygame.font.SysFont("arial", 10)
	myfont3 = pygame.font.SysFont("arial", 50)
	label = myfont.render("3M2K", 1, (255,255,255))
	label2 = myfont.render("3M2K", 1, (0,0,0))
	pygame.mixer.init()
	pygame.mixer.music.load("Drumb.wav")

	t = create_tracks("drumb.mid")
	divisor =  get_clock_divisor("drumb.mid")

	pygame.mixer.music.play()

	screen = 0
	x=10
	y=10


	while not loop:
		scr.fill((0,0,0))
		if (screen):
			screen.set_alpha(254)
			scr.blit(screen,(0,10))

		pygame.draw.rect(scr,( x%255, (x+(ctr/100))%255, (x+(ctr/50))%255 ),(x,y,10,10),1)

		screen = scr.convert()
		for i in range(0,len(t)):
			temp = note_feed(t[i],ctr)
			if (temp):
				if (screen):
					pygame.draw.rect(scr,(((i+1)*5153+30)%255,((i+1)*153+30)%100,((i+1)*100+30)%255),((i*50)+600+temp[1]*2,10,10,25))				
				pygame.draw.rect(screen,(((i+1)*5153)%255,((i+1)*153)%100,((i+1)*113)%255),((i*50)+600+temp[1]*2,10,10,25))


		x=(sin(x)+.6)*width
		y=(sin(y)+.6)*height


		scr.blit(label2, (654, 442))
		scr.blit(label, (654, 440))
		# scr.blit(myfont2.render(str(ctr), 1, (255,255,255)), (5, 65))

		ctr=pygame.mixer.music.get_pos()/divisor # in miliseconds

		loop = ifquit(loop)

		pygame.display.flip()
		if (ctr<0):
			#hold on a second
			pygame.time.wait(900)
			#ok quit
			loop=1

		pygame.time.wait(50)

main2()

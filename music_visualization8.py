#
#	mv8 has perspective, brutes
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

def color_1(i,o):
	return ( ((i+1)*5153+o)%255 , ((i+1)*153+o)%100 , ((i+1)*100+o)%255 )

def trap(scr, size,direction,pos,col):
	(x,y)=pos
	if (direction):
		pygame.draw.polygon(scr,col,[ (x,y),(x,y+size),(x-size,y+(3*size/4)),(x-size,y+size/4) ])
	else:
		pygame.draw.polygon(scr,col,[ (x,y),(x,y+size),(x+size,y+(3*size/4)),(x+size,y+size/4) ])

def trap_theta(scr,pos,direction,col):
	(x,y)=pos
	col = (randint(0,255),randint(0,255),randint(0,255))
	if (direction):
		wdth = ((.5*width) - x )/20
		pygame.draw.polygon(scr,col, [ (x,y*.70) , (x,y+wdth), (x-wdth,y), (x-wdth,y*.75)  ]    )
	else:
		wdth = ((.5*width) - x )/20
		pygame.draw.polygon(scr,col, [ (x,y*.70) , (x,y+wdth), (x+wdth,y), (x+wdth,y*.75)  ]    )


def main2():
	pygame.time.wait(2000)
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
	pygame.mixer.music.load("Brutes.wav")

	t = create_tracks("brutes.mid")
	divisor =  get_clock_divisor("brutes.mid")

	pygame.mixer.music.play()

	screen = 0
	x=10
	y=10

	poly_array=[]
	appendable=[]

	screen=0

	while not loop:
		scr.fill((0,0,0))
		pygame.draw.line(scr,white,(width/2,100),(width-100,height/2))
		pygame.draw.line(scr,white,(width/2,height-100),(width-100,height/2))
		pygame.draw.line(scr,white,(width/2,100),(100,height/2))
		pygame.draw.line(scr,white,(width/2,height-100),(100,height/2))
		pygame.draw.line(scr,white,(width/2,height-100),(width/2,100))

		index=0
		for item in poly_array:
			(s,(x,y),d,c) = item
			x-=10
			trap_theta(s,(x,y),d,c)
			trap_theta(s,(width-x,y),abs(d-1),c)
			poly_array[index] = (s,(x,y),d,c)
			index+=1
			

		for i in range(0,len(t)):
			temp = note_feed(t[i],ctr)
			if (temp):
				trap_theta(scr,(width/2,height/4+i*50),1,white)
				poly_array.append((scr,(width/2,height/4+i*50+(temp[1]-20)),1,white))


		scr.blit(label2, (654, 442))
		scr.blit(label, (654, 440))


		pygame.display.flip()
		ctr=pygame.mixer.music.get_pos()/divisor # in miliseconds
		if (ctr<0):
			#hold on a second
			pygame.time.wait(900)
			#ok quit
			loop=1
		loop = ifquit(loop)

		pygame.time.wait(30)

main2()

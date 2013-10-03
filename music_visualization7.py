#
#	mv7 has scenes
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
	myfont3 = pygame.font.SysFont("arial", 50)
	scr.blit(myfont3.render(str(i), 1, (255,(i*113)%255,(i*57)%255)), ((20+150*i)%width, 50))
	scr.blit(myfont3.render(str(temp[1]), 1, (255,(i*113)%255,(i*57)%255)), ((20+150*i)%width, 100))
	scr.blit(myfont3.render(str(temp[0]), 1, (255,(i*113)%255,(i*227)%255)), ((20+150*i)%width, 150))
	scr.blit(myfont3.render(str(temp[2]), 1, (255,(i*113)%255,(i*1053)%255)), ((20+150*i)%width, 200))
	scr.blit(myfont3.render(str(temp[3]), 1, (255,(i*113)%255,(i*1001)%255)), ((20+150*i)%width, 250))

def tri_list((x,y,w,h)):
	q=[]
	q.append((x+w/2,y))
	q.append((x+w,y+h))
	q.append((x,y+h))
	return q


def main():
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
	pygame.mixer.music.load("taint.wav")

	t = create_tracks("taint.mid")
	divisor =  get_clock_divisor("taint.mid")

	pygame.mixer.music.play()

	screen = 0
	x=10
	y=10
	flipper=1
	track_1_note=0

	circle_array=[]
	z=0

	tri=tri_list((622,400,160,160))

	while not loop:
		time = pygame.mixer.music.get_pos()/1000
		track_5_note = note_feed(t[5],ctr)
		track_4_note = note_feed(t[4],ctr)
		track_3_note = note_feed(t[3],ctr)
		track_1_note = note_feed(t[1],ctr)
		track_0_note = note_feed(t[0],ctr)
		scr.fill((0,0,0))

		if (screen):
			screen.set_alpha(254)
			scr.blit(screen,(-10,0))

		if (track_0_note and ctr>0):
			pygame.draw.rect(scr,(255,225,225),(width-1,0,1,height))

		if (track_1_note):
			z=track_1_note

		if (z):
			q = 15-(z[1]-71)
			for i in range(0,100):
				pygame.draw.rect(scr,(98,0,255),(width-15,(i*40+10*q)-100,10,10),5)

		screen = scr.copy()


		if (track_4_note):
			pygame.draw.polygon(scr,(40,0,0),tri)
		if (track_3_note):
			pygame.draw.polygon(scr,(150,0,0),tri,1)

		if (time*10<255):
			pygame.draw.circle(scr,(time*10,time*10,time*10),(700,500),100,1)
		else:
			pygame.draw.circle(scr,(255,255,255),(700,500),100,1)
		
		scr.blit(label2, (654, 442))
		scr.blit(label, (654, 440))

		ctr=pygame.mixer.music.get_pos()/divisor # in miliseconds

		loop = ifquit(loop)

		pygame.display.flip()
		if (ctr<0):
			#hold on a second
			pygame.time.wait(900)
			#ok quit
			loop=1

		pygame.time.wait(50)

main()
# else:
			# 	scr.fill((0,0,0))
			# if (screen):
			# 	screen.set_alpha(100)
			# 	flipper*=-1
			# 	scr.blit(screen,(flipper,10),None,2)
			# if (track_5_note):
			# 	circle_array.append(pygame.draw.ellipse(scr,(100,100,150-time),(952-(time*14),525-(time*14),10+time*27,10+time*27),1))
			# for rect in circle_array:
			# 	(x,y,w,h) = rect 
			# 	pygame.draw.ellipse(scr,(0,0,0),(x+1,y+1,w,h),1)
			# 	pygame.draw.ellipse(scr,(randint(0,time),randint(0,time),abs(randint(150,180)-5*time)),rect,1)
			# 	pygame.draw.aaline(scr,(10+time,0,0),(0,450+randint(0,200)),(width,450+randint(0,200)),0)
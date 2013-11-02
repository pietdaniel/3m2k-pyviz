from random import randint,choice,randrange
from math import pi, sin, asin, tan, cos
from pprint import pprint
import pygame, math, types, operator, os, midi, sys
import pygame.midi
print sys.argv
var = raw_input("Enter something: ")
print "you entered ", var#
white = (255,255,255)
black = (0,0,0)
width=1920
height=1080
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (0,0)
scr = pygame.display.set_mode((width,height))
w,h = scr.get_size()
#	mv1 contains some dead functions
#	draws aalines and moves them
# 	[lostinthecrowd]
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
		if e.type == KEYDOWN and e.key == K_SPACE:
			print "**** MARKER **** MARKER **** MARKER **** MARKER **** MARKER **** MARKER ****"
	return loop
def main1():
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
#
#	mv10 luvin
#
#
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
def function1(x):
	x=long(x)
	return abs(((255*(x*x))-999) / ((x*x) + 99999999))
def main2():
	pygame.mouse.set_visible(0)
	pygame.font.init()
	pygame.mixer.init()
	
	pygame.mixer.music.load("luvin.wav")
	
	
	
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
	
	pygame.mixer.music.play()
	ctr=0
	
	timestamp =0
	x = randint(0,width-10)
	y = randint(0,height-10)
	a=.5
	b=.9
	c=(255,255,255)
	
	while not loop:
		
		pygame.draw.arc(scr, white, (0,50,width,2*height+100),0,pi,1)

		if (x>width and y>height):
			x = randint(0,width-10)
			y = randint(0,height-10)
			c=(255,255,255)
		pygame.draw.rect(scr,c,(x,y,1,1),1)
		(r2,g2,b2)=c
		pygame.draw.rect(scr,(b2,r2,g2),(y,x,1,1),1)
		x = a*x+b*y
		y = a*y+b*x
		(r1,g1,b1)=c
		r1-=25
		b1-=25
		r1=abs(r1%255)
		b1=abs(b1%255)
		c=(r1,g1,b1)

		scr.blit(label2, (654, 442))
		scr.blit(label, (654, 440))
		ctr+=1
		
		
		if (pygame.mixer.music.get_pos()<0):
			loop=1
		
		
		
		pygame.display.flip()
		loop = ifquit(loop)
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
def main3():
	pygame.mouse.set_visible(0)
	pygame.font.init()
	pygame.mixer.init()
	
	pygame.mixer.music.load("sky.mp3")
	
	
	
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
	
	pygame.mixer.music.play()
	ctr=0
	
	timestamp =0
	size = 500
	x = randint(0,width)
	y = randint(0,height)
	c = white
	
	while not loop:
		
		screen = scr.copy()
		if timestamp >= 3656:
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
		if timestamp >= 3656:
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
				

		ctr+=1
		
		
		if (pygame.mixer.music.get_pos()<0):
			loop=1
		
		
		
		pygame.display.flip()
		loop = ifquit(loop)
class Box():
	def __init__(self, x=0,y=0,xv=0,yv=0,col=white,size=50):
		self.x=x
		self.y=y
		self.xv=xv
		self.yv=yv
		self.col=col
		self.size=size
	def draw(self,scr):
		d = math.sqrt(self.size*self.size)
		pygame.draw.polygon(scr,self.col,( (self.x,self.y),(self.x+self.size,self.y+self.size),(self.x,self.y+self.size*2),(self.x-self.size,self.y+self.size) ), 1 )
		y2 = self.y+self.size
		pygame.draw.polygon(scr,self.col,( (self.x,y2),(self.x+self.size,y2+self.size),(self.x,y2+self.size*2),(self.x-self.size,y2+self.size) ), 1 )
		pygame.draw.line(scr,self.col, (self.x,self.y) , (self.x,y2) )
		pygame.draw.line(scr,self.col, (self.x+self.size,self.y+self.size) , (self.x+self.size,y2+self.size) )
		pygame.draw.line(scr,self.col, (self.x-self.size,self.y+self.size) , (self.x-self.size,y2+self.size) )
		pygame.draw.line(scr,self.col, (self.x,self.y+2*self.size) , (self.x,y2+2*self.size) )
	def transport(self,x,y):
		self.x=x
		self.y=y
	def move(self):
		self.x+=self.xv
		self.y+=self.yv
	def push(self,x,y):
		self.xv+=x
		self.yv+=y
	def bounce_X(self):
		self.xv=self.xv*-1
	def bounce_Y(self):
		self.yv=self.yv*-1
	def contain(self):
		if (self.x+self.size>width or self.x-self.size<0):
			self.bounce_X()
			self.move()
		if (self.y+self.size*2>height or self.y<0):
			self.bounce_Y()
			self.move()
	def gravitate(self,x,y):
		difx = self.x - x
		dify = self.y - y
		self.xv -= int(.0025*difx) if (difx!=0) else 0
		self.yv -= int(.0025*dify) if (dify!=0) else 0
def randcol():
	return (randint(0,255),randint(0,255),randint(0,255))
class Ball():
	xv = 0
	yv = 0
	x = 0
	y = 0
	r=1
	prev = (x,y)
	col=white
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
def main33():
	pygame.mouse.set_visible(0)
	pygame.font.init()
	pygame.mixer.init()
	pygame.mixer.music.load("here.flac")
	
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
	pygame.mixer.music.play()
	ctr=0
	timestamp =0
	size = 500
	x = randint(0,width)
	y = randint(0,height)
	c = white
	ball = Ball()
	ball.x = 100
	ball.y = 100
	ball.push(15,15)
	ball2 = Ball()
	ball2.x = width-100
	ball2.y = height-100
	ball2.push(-15,-15)
	ball2.prev=(width,height)
	boxes = []
	for i in range(0,100):
		boxes.append(Box(randint(100,width-100),randint(0,100),randint(-4,4),40,randcol()))
	while not loop:
		
		timestamp = pygame.mixer.music.get_pos()
		
		if timestamp>93428: 
			scr.scroll(randint(-10,10),700)
			if ctr%7==0:
				scr.fill(black)
			for box in boxes:
				box.push(randint(-1,1),randint(-1,1))
		elif timestamp>81623:
			scr.scroll(randint(-1,1),10)
		if timestamp>38039 and timestamp<76904: 
			scr.scroll(randint(-2,2),randint(-2,2))
		if (timestamp>=38039 and timestamp<=38439):
			ball2.col=(255,40,40)
			ball.col=(255,40,40)
			ball2.push(0,1)
			ball.push(-1,0)

		if (timestamp>76904):
			for box in boxes:
				box.draw(scr)
				box.move()
				box.contain()
		elif (timestamp>64970 and timestamp<66502):
			scr.scroll(50,randint(-2,2))
		elif (timestamp>66502):
			scr.fill(black)
			for box in boxes:
				box.draw(scr)
				box.move()
				box.contain()
			
			
			
			
			
			
		elif (timestamp>38039):
			ball.push(2,2)
			ball2.push(-2,-2)

		if timestamp<64949:
			ball.draw(scr)
			ball.col_drift()
			ball.move()
			ball.contain()
			ball2.draw(scr)
			ball2.col_drift()
			ball2.move()
			ball2.contain()
		scr.blit(label2, (654, 442))
		scr.blit(label, (654, 440))
		ctr+=1
		if (pygame.mixer.music.get_pos()<0):
			loop=1
		
		pygame.display.flip()
		loop = ifquit(loop)
		pygame.time.wait(32)
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
def main4():
	pygame.mouse.set_visible(0)
	pygame.font.init()
	pygame.mixer.init()
	pygame.mixer.music.load("god.wav")
	
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
	pygame.mixer.music.play()
	ctr=0
	timestamp =0
	size = 500
	x = randint(0,width)
	y = randint(0,height)
	c = white
	ball = Ball()
	ball.x = 100
	ball.y = 100
	ball.push(15,15)

	balls=[]
	for i in range(0,1000):
		balls.append(Ball(randint(0,width),randint(0,width),randint(-10,10),randint(-10,10),randcol()))
	while not loop:
		scr.fill(black)
		timestamp = pygame.mixer.music.get_pos()
		

		for b in balls:
			b.draw(scr)
			b.draw1(scr)
			b.col_drift2()
			b.move()
			b.contain()
			if (timestamp>116519 and timestamp<189621):
				b.gravitate(width/2,height/2)
			else:
				b.push(randint(-1,1),randint(-1,1))
				if (ctr%9==0):
					if (b.xv>1):
						b.xv-=1
					elif (b.xv<1):
						b.xv+=1
					if (b.yv>1):
						b.yv-=1
					elif (b.yv<1):
						b.yv+=1
		scr.blit(label2, (654, 442))
		scr.blit(label, (654, 440))
		ctr+=1
		if (pygame.mixer.music.get_pos()<0):
			loop=1
		
		pygame.display.flip()
		loop = ifquit(loop)
		pygame.time.wait(20)
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
def main6():
	pygame.mouse.set_visible(0)
	pygame.font.init()
	pygame.mixer.init()
	pygame.mixer.music.load("theta.flac")
	sound = pygame.mixer.Sound("theta.flac")
	samples = pygame.sndarray.array(sound)
	
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
		
		screen = scr.copy()
		scr.blit(label5, (640, 440))
		scr.blit(label2, (654, 442))
		scr.blit(label, (654, 440))
		pygame.display.flip()
		
		loop = ifquit(loop)
		pygame.time.wait(1)
class Box():
	def __init__(self, x=0,y=0,xv=0,yv=0,col=white,size=50):
		self.x=x
		self.y=y
		self.xv=xv
		self.yv=yv
		self.col=col
		self.size=size
	def draw(self,scr):
		d = math.sqrt(self.size*self.size)
		pygame.draw.polygon(scr,self.col,( (self.x,self.y),(self.x+self.size,self.y+self.size),(self.x,self.y+self.size*2),(self.x-self.size,self.y+self.size) ), 1 )
		y2 = self.y+self.size
		pygame.draw.polygon(scr,self.col,( (self.x,y2),(self.x+self.size,y2+self.size),(self.x,y2+self.size*2),(self.x-self.size,y2+self.size) ), 1 )
		pygame.draw.line(scr,self.col, (self.x,self.y) , (self.x,y2) )
		pygame.draw.line(scr,self.col, (self.x+self.size,self.y+self.size) , (self.x+self.size,y2+self.size) )
		pygame.draw.line(scr,self.col, (self.x-self.size,self.y+self.size) , (self.x-self.size,y2+self.size) )
		pygame.draw.line(scr,self.col, (self.x,self.y+2*self.size) , (self.x,y2+2*self.size) )
	def transport(self,x,y):
		self.x=x
		self.y=y
	def move(self):
		self.x+=self.xv
		self.y+=self.yv
	def push(self,x,y):
		self.xv+=x
		self.yv+=y
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
	def gravitate(self,x,y):
		difx = self.x - x
		dify = self.y - y
		self.xv -= int(.0025*difx) if (difx!=0) else 0
		self.yv -= int(.0025*dify) if (dify!=0) else 0
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
def main5():
	pygame.mouse.set_visible(0)
	pygame.font.init()
	pygame.mixer.init()
	pygame.mixer.music.load("faith.wav")
	sound = pygame.mixer.Sound("faith.wav")
	samples = pygame.sndarray.array(sound)
	
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
	pygame.mixer.music.play()
	ctr=0
	increment = len(samples)/16837
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
	box = Box(50,0)
	
	size_var=10.
	alpha_var = 200

	
	
	
	boxes=[]
	for i in range(0,50):
		boxes.append(Box(randint(0,width),randint(0,height),randint(-10,10),randint(-10,10),randcol()))
	while not loop:
		
		
		
		
		scr.fill(black)
		if (screen):
			screen.set_alpha(alpha_var)
			scr.blit(screen,(0,10))
		
		sin_var = int(size_var*(sin(ctr/5.)+1.1))
		timestamp = pygame.mixer.music.get_pos()
		
		
		
		

		for box in boxes:
			box.draw(scr)
			box.contain()
			box.move()
			box.gravitate(width/2,height/2)
			if timestamp>13000:
				box.size=sin_var
			if timestamp>19445 and timestamp<19545:
				box.push(randint(-40,40),randint(-40,40))
			if timestamp>19445 and timestamp<45358:
				box.xv= box.xv/2
				box.yv= box.yv/2
			if timestamp>45358 and timestamp<45458:
				pass
			if timestamp>70691 and timestamp<70791:
				box.push(randint(-40,40),randint(-40,40))
				box.col=(255,0,0)
				size_var = 20.
			if timestamp>83714 and timestamp<83914:
				box.push(randint(-40,40),randint(-40,40))
				box.col=(240,0,0)
			if timestamp>96506 and timestamp<96706:
				
				box.xv/=2
				box.yv/=2
				sin_var = 5.
				box.col=randcol()
			if timestamp>96506:
				box.col=randcol()
				alpha_var+=0.1
				alpha_var=int(alpha_var%255)
			if timestamp>112229:
				if box.x>width/2:
					box.x-=1
				else:
					box.x+=1
				if box.y>height/2:
					box.y-=1
				else:
					box.y+=1

		
		
		
		
		# if (sctr<len(samples))
		

		(l,r) = samples[sctr]
		screen = scr.copy()
			
		sctr+=increment
		ctr+=1
		if (pygame.mixer.music.get_pos()<0):
			loop=1
		
		scr.blit(label2, (654, 442))
		scr.blit(label, (654, 440))
		pygame.display.flip()
		
		loop = ifquit(loop)
		pygame.time.wait(20)
def play_song(song):
	pygame.mixer.init()
	pygame.mixer.music.load(song)
	pygame.mixer.music.play()
def main7():
	pygame.mouse.set_visible(0)
	pygame.font.init()
	
	ctr=0
	loop = 0
	myfont = pygame.font.SysFont("", 300)
	label = myfont.render("3M2K", 1, (255,255,255))
	label2 = myfont.render("3M2K", 1, (0,0,0))
	x=500
	y=500
	w=500
	h=500
	a=0
	b=pi/2
	scr.blit(label2, (654, 442))
	scr.blit(label, (654, 440))
	pygame.display.flip()

	play_song("Xor.mp3")
	while not loop:
		timestamp = pygame.mixer.music.get_pos()
		print timestamp
		
		if (ctr<13409):
			t = scr.convert()
			t.fill((0,0,0))
			t.set_alpha(254)
			scr.blit(t,(0,0))
		ctr+=1

		if (w>1000):
			w-=1
		elif (w>200):
			w+=1
		else:
			w=500
		x=width*(sin(x)+.8)
		y=height*(sin(y)+.8)
		if (abs(x-y)>300):
			pygame.draw.aaline(scr,( (x+(ctr/100))%255, x%255, (w-(ctr/50))%255 ),(x,y),(y,x+ctr/100),True)
	
		scr.blit(label2, (654, 442))
		scr.blit(label, (654, 440))
		pygame.display.flip()
		loop = ifquit(loop)
		pygame.time.wait(20)
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
def play_song(song):
	pygame.mixer.init()
	pygame.mixer.music.load(song)
	pygame.mixer.music.play()
def main8():
	pygame.mouse.set_visible(0)
	pygame.font.init()
	
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
def spf(samples_num,song_length,fps):
	return samples_num/song_length/fps
def main9():
	pygame.mouse.set_visible(0)
	pygame.font.init()
	pygame.mixer.init()
	sound = pygame.mixer.Sound("ROLLING.wav")
	samples = pygame.sndarray.array(sound)
	
	
	
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
def play_song(song):
	pygame.mixer.init()
	pygame.mixer.music.load(song)
	pygame.mixer.music.play()
def main13():
	pygame.mouse.set_visible(0)
	pygame.font.init()
	
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
		
		ctr+=80
		
		
		
		
		
		
		
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
		
		if (pygame.mixer.music.get_pos()<0):
			loop=1		
	
		
		
		scr.blit(label2, (654, 442))
		scr.blit(label, (654, 440))
		pygame.display.flip()
		loop = ifquit(loop)
		pygame.time.wait((100000-ctr)/ctr)
		pygame.time.wait(40)
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
def main21():
	pygame.mouse.set_visible(0)
	pygame.font.init()
	
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
		
		ctr=pygame.mixer.music.get_pos()/divisor 
		loop = ifquit(loop)
		pygame.display.flip()
		if (ctr<0):
			
			pygame.time.wait(900)
			
			loop=1
		pygame.time.wait(50)
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
def main10():
	pygame.mouse.set_visible(0)
	pygame.font.init()
	
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
		ctr=pygame.mixer.music.get_pos()/divisor 
		loop = ifquit(loop)
		pygame.display.flip()
		if (ctr<0):
			
			pygame.time.wait(900)
			
			loop=1
		pygame.time.wait(50)
def main22():
	pygame.time.wait(2000)
	pygame.mouse.set_visible(0)
	pygame.font.init()
	
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
		ctr=pygame.mixer.music.get_pos()/divisor 
		if (ctr<0):
			
			pygame.time.wait(900)
			
			loop=1
		loop = ifquit(loop)
		pygame.time.wait(30)
def main11():
	pygame.mouse.set_visible(0)
	pygame.font.init()
	pygame.mixer.init()
	sound = pygame.mixer.Sound("novalue.flac")
	pygame.mixer.music.load("novalue.flac")
	samples = pygame.sndarray.array(sound)
	
	
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

			
			
			
			
			
			
			
			
			
			
			
			
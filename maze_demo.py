
import random

import pygame,sys
from pygame.locals import *

import easygui as g

import pickle

# thanks to 迷夏牛 for the algorithm, 
# link: http://blog.csdn.net/homer1984/article/details/3891780

class Maze:
	direction_num=4
	north,south,west,east=(0,2,1,3)


	def __init__(self,row,col):		
		self.rows=row
		self.cols=col
		self.cell_num=self.rows*self.cols
		self.cells=[]
		self.maze=[]

		self.path=[]
		self.debug_cells=[]
		self.debug_maze=[]

	def init(self):
		self.cells=[]
		self.maze=[]
		
		self.path=[]
		self.debug_cells=[]
		self.debug_maze=[]

	def create_Maze(self):
		self.init_Maze()
		check_step=0
		while True:

			c1=random.randint(0,self.cell_num-1)
			direction=random.randint(0,self.direction_num-1)

			if direction==self.east:
				if c1%self.cols==(self.cols-1):
					c2=-1
				else:
					c2=c1+1
			elif direction==self.south:
				if (self.rows-1)==c1//self.cols:
					c2=-1
				else:
					c2=c1+self.cols
			elif direction==self.west:
				if c1%self.cols==0:
					c2=-1
				else:
					c2=c1-1
			else:
				if c1//self.cols==0:
					c2=-1
				else:
					c2=c1-self.cols
			if c2<0:
				continue

			if self.is_Connect(c1,c2):
				continue
			else:
				self.union_Cells(c1,c2)
				self.maze[c1][direction]=1
				self.maze[c2][(direction+2)%self.direction_num]=1
			if(self.all_Connect()):
				break
			

	def init_Maze(self):
		for i in range(self.cell_num):
			self.maze.append([0]*4)

		self.maze[0][self.west]=1	#entry
		self.maze[self.cell_num-1][self.east]=1	#exit

		for j in range(self.cell_num):
			self.cells.append(-1)
			self.debug_cells.append(0)
        
		self.path=[]
		self.debug_maze=[]

	def is_Connect(self,c1,c2):
		while self.cells[c1]>=0:
			c1=self.cells[c1]

		while self.cells[c2]>=0:
			c2=self.cells[c2]

		if c1==c2:
			return True
		else:
			return False

	def union_Cells(self,c1,c2):
		while self.cells[c1]>=0:
			c1=self.cells[c1]

		while self.cells[c2]>=0:
			c2=self.cells[c2]

		if self.cells[c1]>self.cells[c2]:
			self.cells[c1]=c2
		else:
			if self.cells[c1]==self.cells[c2]:
				self.cells[c1]-=1
			self.cells[c2]=c1		

	def all_Connect(self):
		count_root=0
		for i in range(self.cell_num):
			if self.cells[i]<0:
				count_root+=1
		if count_root==1:
			return True
		else:
			return False

	def find_path(self):
		for i in self.maze:
			temparray=i[:]
			self.debug_maze.append(temparray)

		_sum=0;_oldsum=-1;temp=0;tempdirection=-1
		
		while _sum!=_oldsum:

			_oldsum=_sum; _sum=0

			for i in range(self.cell_num):
				temp=0
				for j in range(self.direction_num):
					temp+=self.debug_maze[i][j]
					if self.debug_maze[i][j]==1:
						tempdirection=j
					
				if temp==1:
					self.debug_cells[i]=1
					
					if tempdirection==0:
						self.debug_maze[i-self.cols][2]=0
					elif tempdirection==2:
						self.debug_maze[i+self.cols][0]=0
					elif tempdirection==1:
						self.debug_maze[i-1][3]=0
					else:
						self.debug_maze[i+1][1]=0
					
					self.debug_maze[i]=[0,0,0,0]

			for i in self.debug_cells:
				_sum+=i
		# print("debug:%d"%(_sum))
		for i in range(self.cell_num):
			if self.debug_cells[i]==0:
				self.path.append(i)

	def print_path(self):
		index=0
		for i in self.path:
			print("(%d,%d)\t"%(i//self.cols+1,i%self.cols+1),end="")
			index+=1
			if index>=4:
				print("\n",end="")
				index=0

	
	def print_path_debug(self):
		index=0
		for i in range(self.rows):
			for j in range(self.cols):
				print("%d\t"%(self.debug_cells[index]),end="")
				index+=1
			print("\n",end="")
	

def _add(a,b):
	return (a[0]+b[0],a[1]+b[1])


class Player:
	dirs_pace=([0,-1],[-1,0],[0,1],[1,0])

	def __init__(self,maze_pace):
		# self.dirs=-1
		self.pace=maze_pace
		self.alive=False
		self.position=[0,0]
		self.trace=[]



	def init(self):
		self.alive=True
		self.moving=False
		self.position=[0,0]
		self.trace=[[0,0]]
	
	
	def update(self,Maze_object,width,key_dir):
		if self.position[0]==Maze_object.cols-1 and self.position[1]==Maze_object.rows-1:
			return True

		if key_dir!=-1:
			# self.moving=True
			_position=_add(self.position,self.dirs_pace[key_dir])
			if _position[0]<0 or _position[0]>Maze_object.cols or _position[1]<0 or _position[1]>Maze_object.rows:
				return 	False
                      
			if(Maze_object.maze[self.position[0]+width*self.position[1]][key_dir]):
				self.position=_position
				self.trace.append(self.position)
		# else:
		# 	self.moving=False

	# def die(self):
	# 	self.alive=False


class Game:
	gamestatus=(0,1,2,3,4)
	init_time,player_time,ai_time,win_time,newmaze_time=gamestatus

	def __init__(self,rows,cols,pace):
		self.rows=rows
		self.cols=cols
		self.maze_num=rows*cols

		self.pace=pace

		self.status=self.init_time
	
	# def update(self,need_update):
	# 	pass

# def Is_ButtonPress(pos,buttonrect):
# 	if pos[0]>buttonrect[0] and pos[0]<buttonrect[0]+buttonrect[2] and pos[1]>buttonrect[1] and pos[1]<buttonrect[1]+buttonrect[3]:
# 		return True
# 	else:
# 		return False

# def write_maze_debug(mazeObj,index):
# 	filehandle=open('demo'+str(index)+'.txt','a')
# 	itemindex=0
# 	for i in mazeObj.path:
# 		rows=i//mazeObj.cols;cols=i%mazeObj.cols
# 		filehandle.write("("+str(rows)+","+str(cols)+")\t")
# 		if itemindex>4:
# 			filehandle.write("\n")
# 			itemindex=0
# 		itemindex+=1

def draw_maze(surface,mazeObj,maze_pace):
	for i in range(mazeObj.cell_num):
		rows=i//mazeObj.cols;cols=i%mazeObj.cols
		if mazeObj.maze[i][0]==0:
			pygame.draw.line(surface,BLACK,(cols*maze_pace+delt_x,rows*maze_pace+delt_y),(cols*maze_pace+maze_pace+delt_x,rows*maze_pace+delt_y))
		if mazeObj.maze[i][2]==0:
			pygame.draw.line(surface,BLACK,(cols*maze_pace+delt_x,rows*maze_pace+maze_pace+delt_y),(cols*maze_pace+maze_pace+delt_x,rows*maze_pace+maze_pace+delt_y))	
		if mazeObj.maze[i][1]==0:
			pygame.draw.line(surface,BLACK,(cols*maze_pace+delt_x,rows*maze_pace+delt_y),(cols*maze_pace+delt_x,rows*maze_pace+maze_pace+delt_y))
		if mazeObj.maze[i][3]==0:
			pygame.draw.line(surface,BLACK,(cols*maze_pace+maze_pace+delt_x,rows*maze_pace+delt_y),(cols*maze_pace+maze_pace+delt_x,rows*maze_pace+maze_pace+delt_y))



def draw_player(surface,playerObj,maze_pace):
	pygame.draw.rect(surface,YELLOW,pygame.Rect(playerObj.position[0]*maze_pace+delt_x,playerObj.position[1]*maze_pace+delt_y,maze_pace,maze_pace))

# 	pygame.draw.line(sue)
# 	pass

def draw_trace(surface,playerObj,color,maze_pace):
	index=0
	while(index<len(playerObj.trace)-1):
		pygame.draw.line(surface,color,(playerObj.trace[index][0]*maze_pace+maze_pace//2+delt_x,playerObj.trace[index][1]*maze_pace+maze_pace//2+delt_y),(playerObj.trace[index+1][0]*maze_pace+maze_pace//2+delt_x,playerObj.trace[index+1][1]*maze_pace+maze_pace//2+delt_y))
		index+=1



def draw_answer(surface,mazeObj,maze_pace):
	for i in mazeObj.path:
		posy=i//mazeObj.cols;posx=i%mazeObj.cols
		pygame.draw.rect(surface,GREEN,pygame.Rect(posx*maze_pace+delt_x,posy*maze_pace+delt_y,maze_pace,maze_pace))

# def is_a_num(str):
# 	try:
# 		num=int(str)
# 	except ValueError:
# 		return False
# 	else:
# 		return num

def wait_for_paras(old_paras):

	# while(not (rows=is_a_num(input("请输入迷宫的长度（整数）：")))):
	# 	pass
	# while(not (cols=is_a_num(input("请输入迷宫的宽度（整数）：")))):
	# 	pass	
	# while(not (pace=is_a_num(input("请输入迷宫的步长（格宽，整数）：")))):
	# 	pass
	rows=g.integerbox("请输入迷宫的高度（整数 >5而且<30）：","请输入",5,5,30)
	if rows==None :
		rows=old_paras[0]

	cols=g.integerbox("请输入迷宫的宽度（整数 >10而且<45)：","请输入",10,10,45)
	if cols==None :
		cols=old_paras[1]

	pace=g.integerbox("请输入迷宫的步长（格宽，整数 必须是10，。.。）：","请输入",10,10,10)
	if pace==None :
		pace=old_paras[2]


	paras=[rows,cols,pace]

	etc=open("etc","wb")
	# paras_str=[str(i)+'\n' for i in paras]
	# etc.writelines(paras_str)
	pickle.dump(paras,etc)
	etc.close()

	return paras


def new_maze_init():

	global paras
	paras=wait_for_paras(paras)

	global game
	game=Game(paras[0],paras[1],paras[2])
	global demo
	demo=Maze(game.rows,game.cols)
	global player
	player=Player(game.pace)
	
	demo.create_Maze()
	demo.find_path()

	global maze_rect
	maze_rect=pygame.Rect(0,0,paras[1]*paras[2],paras[0]*paras[2])
	maze_rect.centerx=windowSurface.get_rect().centerx
	maze_rect.centery=windowSurface.get_rect().centery

	global delt_x,delt_y
	delt_x=maze_rect[0]
	delt_y=maze_rect[1]

def game_rule():
	print("键A,D,W,S 或者 方向键 控制方向")
	print("键N 刷新迷宫")
	print("键F 寻找出口")
	print("键I 重启迷宫")
	print("easy game by python, have fun ：D")

# -------------------------------------------------------------main-----------------------------------------------------------------------------
game_rule()

key_dir=-1
old_key_dir=-1

# inited=True
paras=[]

try:
	etc = open('etc','rb')
except FileNotFoundError:
	inited=False
else:
	# for line in etc.readlines():
	# 	paras.append(int(line))
	paras=pickle.load(etc)
	if len(paras)!=3:
		inited=False
	inited=True
# finally:
# 	etc.close()

if not inited:
	paras=wait_for_paras([5,10,10])

game=Game(paras[0],paras[1],paras[2])
demo=Maze(game.rows,game.cols)
player=Player(game.pace)

	
mainClock=pygame.time.Clock()


demo.create_Maze()
demo.find_path()

pygame.init()
windowSurface=pygame.display.set_mode((500,400),0,32)
pygame.display.set_caption('mazedemo')

BLACK=(0,0,0)
WHITE=(255,255,255)
RED=(255,0,0)
GREEN=(0,255,0)
BLUE=(0,0,255)
ORANGE=(231,179,37)
YELLOW=(255,255,0)
FONT=pygame.font.SysFont('miriam',48)

#字体居中
text = FONT.render('You Win !',True,ORANGE,WHITE)
textRect = text.get_rect()
textRect.centerx=windowSurface.get_rect().centerx
textRect.centery=windowSurface.get_rect().centery

#迷宫居中
maze_rect=pygame.Rect(0,0,paras[1]*paras[2],paras[0]*paras[2])
maze_rect.centerx=windowSurface.get_rect().centerx
maze_rect.centery=windowSurface.get_rect().centery
delt_x=maze_rect[0]
delt_y=maze_rect[1]
##render
# for i in test.path:
# 	rows=i//20;
# 	pygame.draw.rect(windowSurface,GREEN,())
# 	pygame.draw.rect(windowSurface,)

# north,south,west,east=(0,2,1,3)



presstime=0
key_sensi=15#按键灵敏度

while True:
	#render the surface

	windowSurface.fill(WHITE)

	if game.status==0:
		pass

	elif game.status==1:
		draw_player(windowSurface,player,game.pace)
		draw_trace(windowSurface,player,BLUE,game.pace)

	elif game.status==2:
		draw_answer(windowSurface,demo,game.pace)
		draw_trace(windowSurface,player,RED,game.pace)

	else :
		windowSurface.blit(text,textRect)

	if game.status!=3:
		draw_maze(windowSurface,demo,game.pace)

	#key event
	old_key_dir=key_dir
	for event in pygame.event.get():
		if event.type==QUIT:
			pygame.quit()
			sys.exit()
		elif event.type==KEYDOWN:
			presstime=0
			if event.key==K_LEFT or event.key== ord('a'):
				key_dir=1
			elif event.key==K_RIGHT or event.key== ord('d'):
				key_dir=3			
			elif event.key==K_UP or event.key== ord('w'):
				key_dir=0
			elif event.key==K_DOWN or event.key== ord('s'):
				key_dir=2

			elif event.key== ord('n'):
				game.status=0
				key_dir=-1

			elif event.key==ord('f'):
				game.status=2
				key_dir=-1
			
			elif event.key==ord('i'):
				game.status=4
				key_dir=-1
			else:
				key_dir=-1
		elif event.type==KEYUP:
			key_dir=-1

	# logic update
	if game.status==0:
		demo.init()
		demo.create_Maze()
		demo.find_path()

		# write_maze_debug(demo,1)

		player.init()

		game.status=1
		
	elif game.status==1:
		if key_dir!=old_key_dir:
			if player.update(demo,game.cols,key_dir):
				#print("you win!")
				game.status=3
				continue
		else:
			if key_dir!=-1:
				presstime+=1
				if presstime>=key_sensi and player.update(demo,game.cols,key_dir):
					#print("you win!")
					game.status=3
					presstime=0
					continue
	
	elif game.status==4:
		new_maze_init()

		game.status=0
			
	else:
		pass


	pygame.display.update()
	mainClock.tick(40)

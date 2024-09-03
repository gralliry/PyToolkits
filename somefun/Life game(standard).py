import pygame,sys,random
width,height,size,density = 100,60,10,10
pygame.init()
screen,standard = pygame.display.set_mode((width*size,height*size)),[(a,b) for a in range(width) for b in range(height)]#弹窗屏幕
pygame.display.set_caption("Life Game")#标题

terrain=[]
for i in range(height):
	x_put = []
	for j in range(width):
		x_put.append(True if random.randint(1,101) < density else False)
	terrain.append(x_put)
while True:#进入游戏主循环
	situation = terrain[:]
	for event in pygame.event.get():#检测事件
		if event.type == pygame.QUIT:#结束
			sys.exit()
	for x,y in standard:#处理游戏数据
		yes = 0
		for x_s,y_s in [(-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1)]:
			if 0 <= x+x_s < width and 0 <= y+y_s < height:
				if terrain[y+y_s][x+x_s]:
					yes += 1
		if terrain[y][x]:
			if yes < 2:
				situation[y][x] = False
			elif yes > 3:
				situation[y][x] = True
		else:
			if yes == 3:
				situation[y][x] = True
	for x,y in standard:#更新屏幕
		pygame.draw.rect(screen,[0,0,0] if situation[y][x] else [255,255,255],[x*size,y*size,10,10],0)
	terrain = situation[:]
	pygame.display.flip()#刷新游戏

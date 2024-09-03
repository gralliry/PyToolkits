import random,sys,pygame,time
#
def initial_model():
	global fishes,fishes_s,grade,speed,x,y,size
	grade = 10
	speed = 1
	x = 500
	y = 400
	size = 4
	fishes,fishes_s = {},{}
#
def develop():
	while True:#创造小鱼
		name = random.randint(0,9999)
		if name not in fishes:
			fish = {}
			fish['x'] = random.randint(0,1000)
			fish['y'] = random.randint(0,600)
			fish['grade'] = random.randint(1,round(grade/10))
			fishes_s[name] = fish
			break
#
def run_game():
	global fishes
	pygame.init()
	screen = pygame.display.set_mode((1000,600))#弹窗屏幕
	pygame.display.set_caption("玩家大鱼吃小鱼")#标题
	initial_model()
	for i in range(1,51):
		develop()
	fishes = fishes_s.copy()#更新游戏数据
	while True:#进入游戏主循环
		#
		screen.fill((230,230,230))#背景颜色
		for i in fishes.keys():#打印网点
			pygame.draw.circle(screen,[0,0,255],[fishes[i]["x"],fishes[i]["y"]],size,0)
			#                                          字体 大小                  信息              抗锯齿 颜色    位置
			#screen.blit(pygame.font.Font(None,15).render(str(fishes[i]["grade"]),False,(0,0,0)),(fishes[i]["x"],fishes[i]["y"]))
		pygame.draw.circle(screen,[225,0,0],[x,y],size,0)
		screen.blit(pygame.font.Font(None,45).render("Grade:"+str(grade),True,(0,0,0)),(0,0))
		#
		for event in pygame.event.get():#检测结束事件
			if event.type == pygame.QUIT:
				sys.exit()
		#
		time.sleep(0.001)
		#处理全局数据
		deal()#处理玩家数据
		#
		pygame.display.flip()#更新屏幕
	#
def deal():
	global fishes,fishes_s,grade,speed,x,y
	fishes_s = fishes.copy()
	#
	decrease = 0.0003
	grade -= round(grade*decrease)
	#检测距离是否够近可以吃
	for i in fishes.keys():
		if ( ( fishes[i]['x'] - x )**2 + ( fishes[i]['y'] - y )**2 )**0.5 < size:#是否够距离吃
			develop()
			grade += fishes[i]['grade']
			del fishes_s[i]
			continue
	###################
	choose_object,value = "",0
	for i in fishes.keys():
		value_do = fishes[i]["grade"]/((fishes[i]["x"] - x)**2 + (fishes[i]["y"] - y)**2)**0.5
		if value_do >= value:
			choose_object,value = i,value_do
	###################
	set_x,set_y = fishes[choose_object]["x"] - x,fishes[choose_object]["y"] - y#进入位移调整
	if set_x != 0 or set_y != 0:#移动(坐标x,坐标y)
		proportion = speed/(set_x**2+set_y**2)**0.5
		x += set_x*proportion#进行位移
		y += set_y*proportion
	fishes = fishes_s.copy()#更新游戏数据
	return








while True:
	run_game()
	

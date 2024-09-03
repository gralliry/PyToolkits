import random
import sys
import time

import pygame
width, height, size, density = 200, 120, 5, 50
pygame.init()
screen = pygame.display.set_mode((width * size, height * size))
font = pygame.font.Font(None, 45)
terrain = [[random.randint(1, 101) < density for _ in range(width + 2)] for _ in range(height + 2)]
yes = [[0 for _ in range(width + 2)] for _ in range(height + 2)]
direction = ((-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1))
# 弹窗屏幕
pygame.display.set_caption("Life Game")  # 标题
while True:  # 进入游戏主循环
    start_time = time.time()
    for e in pygame.event.get():  # 检测事件
        if e.type == pygame.QUIT:  # 结束
            sys.exit()
    # 处理游戏数据
    for x in range(1, width + 1):
        for y in range(1, height + 1):
            if terrain[y][x]:
                for x_s, y_s in direction:
                    yes[y + y_s][x + x_s] += 1
    for x in range(1, width + 1):
        for y in range(1, height + 1):
            ye = yes[y][x]
            if terrain[y][x]:
                if ye < 2 or 3 < ye:
                    terrain[y][x] = False
            else:
                if ye == 3:
                    terrain[y][x] = True
            yes[y][x] = 0
    for x in range(width + 2):
        yes[0][x] = 0
        yes[height + 1][x] = 0
    for y in range(height + 2):
        yes[y][0] = 0
        yes[y][width + 1] = 0
    for x in range(1, width + 1):
        for y in range(1, height + 1):
            # 更新屏幕
            pygame.draw.rect(
                surface=screen,
                color=[0, 0, 0] if terrain[y][x] else [255, 255, 255],
                rect=[(x - 1) * size, (y - 1) * size, size, size],
            )
    end_time = time.time()
    screen.blit(font.render(f"FPS:{int(1/(end_time-start_time))}", True, (255, 0, 0)), (0, 0))
    pygame.display.flip()  # 刷新游戏

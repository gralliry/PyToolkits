import os
import sys
import time

import pygame

# 初始化Pygame
pygame.init()
# 设置屏幕长宽
screen = pygame.display.set_mode((1000, 800), 0, 23)
# 设置标题
pygame.display.set_caption("PHYSIC")
#


# 进入Pygame循环
count = 2
pause = False
while True:
    pygame.time.Clock().tick(20)
    # Pygame过程检测
    for event in pygame.event.get():
        # 退出
        if event.type == pygame.QUIT:
            pygame.quit()
            os.system("taskkill /f /im cmd.exe")
        # 按键按下
        if event.type == pygame.KEYDOWN:
            # esc键完全退出
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                os.system("taskkill /f /im cmd.exe")
                sys.exit()
            # q键结束进程
            elif event.key == pygame.K_SPACE:
                pause = False if pause else True
    # 清空屏幕
    screen.fill((255, 255, 255))
    # 对系统进行操作运行
    if not pause:
        pygame.draw.circle(screen, (0, 0, 0), (500, 200), 45, 0)
        pygame.draw.polygon(screen, (0, 0, 0), [(450, 250), (550, 250), (550, 450), (450, 450)], 0)
        pygame.draw.polygon(screen, (0, 0, 0), [(400, 250), (435, 250), (435, 450), (400, 450)], 0)
        pygame.draw.polygon(screen, (0, 0, 0), [(565, 250), (600, 250), (600, 450), (565, 450)], 0)
        if count % 2 == 0:
            pygame.draw.polygon(screen, (0, 0, 0), [(450, 445), (490, 445), (490, 625), (450, 625)], 0)
            pygame.draw.polygon(screen, (0, 0, 0), [(510, 445), (550, 445), (550, 625), (510, 625)], 0)
        else:
            pygame.draw.polygon(screen, (0, 0, 0), [(450, 465), (490, 465), (490, 675), (450, 675)], 0)
            pygame.draw.polygon(screen, (0, 0, 0), [(510, 465), (550, 465), (550, 675), (510, 675)], 0)
        count += 1
    else:
        pygame.draw.circle(screen, (0, 0, 0), (500, 200), 45, 0)
        pygame.draw.polygon(screen, (0, 0, 0), [(450, 250), (550, 250), (550, 450), (450, 450)], 0)
        pygame.draw.polygon(screen, (0, 0, 0), [(400, 250), (435, 250), (435, 450), (400, 450)], 0)
        pygame.draw.polygon(screen, (0, 0, 0), [(565, 250), (600, 250), (600, 450), (565, 450)], 0)
        pygame.draw.polygon(screen, (0, 0, 0), [(450, 445), (490, 445), (490, 625), (450, 625)], 0)
        pygame.draw.polygon(screen, (0, 0, 0), [(510, 445), (550, 445), (550, 625), (510, 625)], 0)
    # 更新屏幕
    pygame.display.update()

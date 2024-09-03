import pygame
import sys
import time

import keyboard

width, height = 800, 250
white = (0, 0, 0)
black = (255, 255, 255)
pygame.init()
font = pygame.font.SysFont("arial", 20)
screen = pygame.display.set_mode((width, height))  # 弹窗屏幕
pygame.display.set_caption("键盘展示")  # 标题
percX = (
    (2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2),
    (2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 4),
    (3, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2),
    (4, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 4),
    (5, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 3),
    (3, 2, 2, 2, 10, 2, 2, 2, 2, 2)
)
percY = (
    1,
    2,
    2,
    2,
    2,
    2
)
keys = (
    ('esc', 'f1', 'f2', 'f3', 'f4', 'f5', 'f6', 'f7', 'f8', 'f9', 'f10', 'f11', 'f12', 'insert', 'print_Screen','delete'),  # 16
    ('~', '!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '-', '=', 'backspace'),  # 14
    ('tab', 'q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p', '[', ']', '|'),  # 14
    ('capsLock', 'a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', ';', '"', 'enter'),  # 13
    ('shift', 'z', 'x', 'c', 'v', 'b', 'n', 'm', ',', '.', '/', 'up', 'shift'),  # 13
    ('ctrl', '0', 'cmd', 'alt', 'space', 'alt', 'ctrl', 'left', 'down', 'right')  # 10
)

keyboards = []
sumValueY, sumY = 0, sum(percY)
for yIndex, row in enumerate(keys):
    sumValueX, sumX = 0, sum(percX[yIndex])
    keyboardsRow = []
    for xIndex, keyValue in enumerate(row):
        pos = (
            int(sumValueX / sumX * width),
            int(sumValueY / sumY * height),
        )
        shape = (
            int(percX[yIndex][xIndex] / sumX * width),
            int(percY[yIndex] / sumY * height)
        )
        fontPos = (
            int(pos[0] + shape[1] / 2),
            int(pos[1] + shape[1] / 2)
        )
        keyfaceobs = pygame.Surface(shape)
        keyfaceobs.fill(white)
        keyfaceobs.blit(font.render(keyValue, True, black), (0, 0))

        keyfacehid = pygame.Surface(shape)
        keyfacehid.fill(black)
        keyfacehid.blit(font.render(keyValue, True, white), (0, 0))

        keyboardsRow.append(
            {
                'pos': pos,
                'obs': keyfaceobs,
                'hid': keyfacehid
            }
        )
        sumValueX += percX[yIndex][xIndex]
    keyboards.append(keyboardsRow)
    sumValueY += percY[yIndex]
state = [[False for _ in range(len(row))] for row in keys]
print("创建成功")
if __name__ == "__main__":
    for yIndex, row in enumerate(keys):
        for xIndex, keyValue in enumerate(row):
            screen.blit(keyboards[yIndex][xIndex]['obs'], keyboards[yIndex][xIndex]['pos'])
    pygame.display.flip()
    while True:  # 进入游戏主循环
        for event in pygame.event.get():  # 检测结束事件
            if event.type == pygame.QUIT:
                sys.exit()
        flag = False
        for yIndex in range(len(keys)):
            for xIndex in range(len(keys[yIndex])):
                press = keyboard.is_pressed(keys[yIndex][xIndex])
                if state[yIndex][xIndex] != press:
                    state[yIndex][xIndex] = press
                    if press:
                        screen.blit(keyboards[yIndex][xIndex]['hid'], keyboards[yIndex][xIndex]['pos'])
                    else:
                        screen.blit(keyboards[yIndex][xIndex]['obs'], keyboards[yIndex][xIndex]['pos'])
                    flag = True
        if flag:
            print("update")
            pygame.display.flip()

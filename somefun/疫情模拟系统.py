import random, sys, pygame, time

positions_numbers = 100  # 全国网点数
goods_numbers = 100  # 货物数
goods_speed = 1  # 货物运输速度
epidemic_severity = 50  # 疫情传染几率性
epidemic_probabililty = 10  # %疫情产生几率
foresee_value = 4  # 预警值


def initial_model():
    global positions_sort, goods_sort, positions_names, goods_names
    positions_names = [i for i in range(1, positions_numbers + 1)]
    goods_names = [i for i in range(1, goods_numbers + 1)]
    positions_names_copy = positions_names[:]
    goods_names_copy = goods_names[:]
    # 创建网点
    positions_sort = {}
    while len(positions_names_copy) != 0:
        positions = {}
        positions["x"] = random.randint(0, 1000)  # 网点坐标x
        positions["y"] = random.randint(0, 600)  # 网点坐标y
        if random.randint(1, 101) <= epidemic_probabililty:  # 疫情情况
            positions["nature"] = 10
        else:
            positions["nature"] = 0
        positions_sort[positions_names_copy.pop(random.randint(0, len(positions_names_copy) - 1))] = positions  # 把网点写入
    # 创建货物
    goods_sort = {}
    while len(goods_names_copy) != 0:
        goods = {}
        goods["n_x"] = random.randint(0, 1000)  # 货物坐标x
        goods["n_y"] = random.randint(0, 600)  # 货物坐标y
        goods["nature"] = 0  # 感染情况
        net_xy = positions_names[random.randint(0, len(positions_names) - 1)]
        goods["destination"] = net_xy
        goods["e_x"] = positions_sort[net_xy]["x"]  # 选择终点
        goods["e_y"] = positions_sort[net_xy]["y"]
        goods_sort[goods_names_copy.pop(random.randint(0, len(goods_names_copy) - 1))] = goods  # 把货物写入


def deal():
    for i in goods_sort.keys():  # 遍历货物
        if goods_sort[i]["e_x"] == goods_sort[i]["n_x"] and goods_sort[i]["e_y"] == goods_sort[i]["n_y"]:  # 判断货物是否到底目的地
            # 判断到了哪个地方
            # 处理感染
            if random.randint(1, 101) <= epidemic_severity:  # 是否传染
                if goods_sort[i]["nature"] < positions_sort[goods_sort[i]["destination"]]["nature"]:  # 环境传染
                    if goods_sort[i]["nature"] == 2:  # 货物污染等级2则继续污染环境
                        positions_sort[goods_sort[i]["destination"]]["nature"] += 1
                    if positions_sort[goods_sort[i]["destination"]]["nature"] >= foresee_value:  # 大于预警值就污染货物+等级2
                        goods_sort[i]["nature"] = 2
                    else:  # 小于则污染货物+等级1
                        if goods_sort[i]["nature"] != 2:  # 如果等级不是2，则设置成等级1（等级在污染中不能回退）
                            goods_sort[i]["nature"] = 1
                else:  # 货物传染
                    positions_sort[goods_sort[i]["destination"]]["nature"] += goods_sort[i]["nature"]
            # 修正位置
            goods_sort[i]["n_x"] = goods_sort[i]["e_x"]  # 在此设置起点
            goods_sort[i]["n_y"] = goods_sort[i]["e_y"]
            net_xy = positions_names[random.randint(0, len(positions_names) - 1)]  # 重新选择终点
            goods_sort[i]["destination"] = net_xy
            goods_sort[i]["e_x"] = positions_sort[net_xy]["x"]
            goods_sort[i]["e_y"] = positions_sort[net_xy]["y"]
        else:
            distance = round(((goods_sort[i]["n_x"] - goods_sort[i]["e_x"]) ** 2 + (
                        goods_sort[i]["n_y"] - goods_sort[i]["e_y"]) ** 2) ** 0.5)  # 判断目的地距离
            if distance <= goods_speed:  # 简易修正
                goods_sort[i]["n_x"] = goods_sort[i]["e_x"]
                goods_sort[i]["n_y"] = goods_sort[i]["e_y"]
            else:
                if goods_sort[i]["e_x"] - goods_sort[i]["n_x"] <= 0:
                    goods_sort[i]["n_x"] -= goods_speed  # 朝左
                else:
                    goods_sort[i]["n_x"] += goods_speed  # 朝右
                if goods_sort[i]["e_y"] - goods_sort[i]["n_y"] <= 0:
                    goods_sort[i]["n_y"] -= goods_speed  # 朝下
                else:
                    goods_sort[i]["n_y"] += goods_speed  # 朝上
    return


def run_game():
    pygame.init()
    screen = pygame.display.set_mode((1000, 600))  # 弹窗屏幕
    pygame.display.set_caption("疫情模拟系统")  # 标题
    bg_color = (230, 230, 230)  # 背景颜色
    while True:  # 进入游戏主循环
        screen.fill(bg_color)
        for event in pygame.event.get():  # 检测结束事件
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:  # 测试
                for i in goods_sort.keys():
                    print(f"{i} : {goods_sort[i]}")
                for i in positions_sort.keys():
                    print(f"{i} : {positions_sort[i]}")
        time.sleep(0.01)
        deal()  # 处理游戏数据
        for i in positions_sort:  # 打印网点
            if positions_sort[i]["nature"] == 0:  # 绿色
                color = [0, 100, 0]
            elif 0 < positions_sort[i]["nature"] < foresee_value:  # 黄色
                color = [255, 255, 0]
            elif positions_sort[i]["nature"] >= foresee_value:  # 红色
                color = [255, 0, 0]
            pygame.draw.circle(screen, color, [positions_sort[i]["x"], positions_sort[i]["y"]], 3, 0)
        for i in goods_sort:  # 打印货物
            if goods_sort[i]["nature"] == 0:  # 蓝色
                color = [0, 0, 225]
            elif goods_sort[i]["nature"] == 1:  # 紫色
                color = [128, 0, 128]
            elif goods_sort[i]["nature"] == 2:  # 黑色
                color = [0, 0, 0]
            pygame.draw.circle(screen, color, [goods_sort[i]["n_x"], goods_sort[i]["n_y"]], 1, 0)
        pygame.display.flip()  # 更新屏幕


initial_model()
run_game()

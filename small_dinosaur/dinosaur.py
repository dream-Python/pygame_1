# _*_ coding  ：  UTF-8 _*_
# 开发团队    ：  dream
# 开发人员    ：  刘育彬
# 开发时间    ：  2020/1/19  15:34
# 文件名称    ：  dinosaur.py
# 开发工具    ：  PyCharm


import pygame
from pygame.locals import *                 # 导入 pygame 中的常量
from itertools import cycle
import random


SCREENWIDTH = 822                           # 窗体宽度
SCREENHEIGHT = 260                          # 窗体高度
FPS = 30                                    # 更新画面的时间


# 障碍物类
class Obstacle:
    score = 1                # 分数

    def __init__(self):
        # 初始化障碍物矩形
        self.rect = pygame.Rect(0, 0, 0, 0)
        # 加载障碍物图片
        self.stone = pygame.image.load('image/stone.png').convert_alpha()
        self.cacti = pygame.image.load('image/cacti.png').convert_alpha()
        # 加载分数图片
        self.numbers = (
            pygame.image.load('image/0.png').convert_alpha(),
            pygame.image.load('image/1.png').convert_alpha(),
            pygame.image.load('image/2.png').convert_alpha(),
            pygame.image.load('image/3.png').convert_alpha(),
            pygame.image.load('image/4.png').convert_alpha(),
            pygame.image.load('image/5.png').convert_alpha(),
            pygame.image.load('image/6.png').convert_alpha(),
            pygame.image.load('image/7.png').convert_alpha(),
            pygame.image.load('image/8.png').convert_alpha(),
            pygame.image.load('image/9.png').convert_alpha(),
        )
        # 加载加分音效
        self.score_audio = pygame.mixer.Sound('audio/score.wav')       # 加分
        # 0 和 1 随机数
        r = random.randint(0, 1)
        if r == 0:             # 如果随机数为 0 显示石头障碍物相反显示仙人掌
            self.image = self.stone
        else:
            self.image = self.cacti
        # 根据障碍物位图的宽高来设置矩形
        self.rect.size = self.image.get_size()
        # 获取位图宽高
        self.width, self.height = self.rect.size
        # 障碍物绘制坐标
        self.x = 800
        self.y = 200 - (self.height / 2)
        self.rect.center = (self.x, self.y)

    # 障碍物移动
    def obstacle_move(self):
        self.rect.x -= 5

    # 绘制障碍物
    def draw_obstacle(self):
        SCREEN.blit(self.image, (self.rect.x, self.rect.y))

    # 获取分数
    def get_score(self):
        self.score
        tmp = self.score
        if tmp == 1:
            self.score_audio.play()                        # 播放加分音乐
        self.score = 0
        return tmp

    # 显示分数
    def show_score(self, score):
        '''在窗体顶部中间的位置显示分数'''
        self.scorDigits = [int(x) for x in list(str(score))]
        totalWidth = 0
        for digit in self.scorDigits:
            # 获取积分图片的宽度
            totalWidth += self.numbers[digit].get_width()
        # 分数横向位置
        Xoffset = (SCREENWIDTH - totalWidth) / 2
        for digit in self.scorDigits:
            # 绘制分数
            SCREEN.blit(self.numbers[digit], (Xoffset, SCREENHEIGHT * 0.1))
            # 随着数字增加改变位置
            Xoffset += self.numbers[digit].get_width()


# 恐龙类
class Dinosaur:
    def __init__(self):
        # 初始化小恐龙矩形
        self.rect = pygame.Rect(0, 0, 0, 0)
        self.jumpState = False              # 跳跃的状态
        self.jumpHeight = 130               # 跳跃的高度
        self.lowest_y = 140                 # 最低坐标
        self.jumpValue = 0                  # 跳跃增变量
        # 小恐龙动图索引
        self.dinosaurIndex = 0
        self.dinosaurIndexGen = cycle([0, 1, 2])
        # 加载小恐龙图片
        self.dinosaur_img = (
            pygame.image.load('image/dinosaur1.png').convert_alpha(),
            pygame.image.load('image/dinosaur2.png').convert_alpha(),
            pygame.image.load('image/dinosaur3.png').convert_alpha(),
        )
        self.jump_audio = pygame.mixer.Sound('audio/jump.wav')          # 跳跃音乐
        self.rect.size = self.dinosaur_img[0].get_size()
        self.x = 50                           # 绘制恐龙的 x 坐标
        self.y = self.lowest_y                # 绘制恐龙的 y 坐标
        self.rect.topleft = (self.x, self.y)

    # 跳状态
    def jump(self):
        self.jumpState = True

    # 小恐龙移动
    def move(self):
        if self.jumpState:                     # 当起跳的时候
            if self.rect.y >= self.lowest_y:    # 如果站在地上
                self.jumpValue = -5            # 以 5 个像素值向上移动
            if self.rect.y <= self.lowest_y - self.jumpHeight:         # 恐龙到达顶部回落
                self.jumpValue = 5             # 以 5 个像素向下移动
            self.rect.y += self.jumpValue      # 通过循环改变恐龙的 y 坐标
            if self.rect.y >= self.lowest_y:   # 如果恐龙回到地面
                self.jumpState = False         # 关闭跳跃状态

    # 绘制恐龙
    def draw_dinosaur(self):
        # 匹配恐龙动图
        dinosaurIndex = next(self.dinosaurIndexGen)
        # 绘制小恐龙
        SCREEN.blit(self.dinosaur_img[dinosaurIndex], (self.x, self.rect.y))


class MyMap:
    def __init__(self, x, y):
        # 加载背景图片
        self.bg = pygame.image.load('image/bg.png').convert_alpha()        # 加载图片
        self.x = x
        self.y = y

    def map_rolling(self):
        if self.x < -800:              # 小于 -790 说明地图已经移动完毕
            self.x = 800               # 给地图一个新的坐标点
        else:
            self.x -= 5                # 5 个像素向左移动

    def map_update(self):
        SCREEN.blit(self.bg, (self.x, self.y))              # 将图片画到窗口上


# 游戏结束的方法
def game_over():
    bump_audio = pygame.mixer.Sound('audio/bump.wav')        # 撞击
    bump_audio.play()
    # 获取窗体宽度、高度
    screen_w = pygame.display.Info().current_w
    screen_h = pygame.display.Info().current_h
    # 加载游戏结束的图片
    over_img = pygame.image.load('image/gameover.png').convert_alpha()
    # 将游戏结束的图片绘制在窗体的中间位置
    SCREEN.blit(over_img, ((screen_w - over_img.get_width()) / 2,
                           (screen_h - over_img.get_height()) / 2))


def main_game():
    score = 0                               # 得分
    over = False
    global SCREEN, FPSCLOCK
    pygame.init()                           # 经过初始化以后我们就可以尽情地使用 pygame 了
    # 使用 pygame 时钟之前，必须先创建 Clock 对象的一个实例
    # 控制每个循环多长时间一次
    FPSCLOCK = pygame.time.Clock()
    # 通常来说我们需要先创建一个窗体，方便我们与程序的交互
    SCREEN = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
    pygame.display.set_caption('小恐龙')            # 设置窗体标题

    # 创建地图对象
    bg1 = MyMap(0, 0)
    bg2 = MyMap(800, 0)

    # 创建恐龙对象
    dinosaur = Dinosaur()

    addObstacleTime = 0                   # 添加障碍物的时间
    lists = []                             # 障碍物对象列表

    while True:

        # 判断是否单机了关闭窗体
        for event in pygame.event.get():            # 遍历所有事件
            # 如果单机了关闭窗体就将窗体关闭
            if event.type == pygame.QUIT:
                exit()               # 关闭窗体
            # 单击键盘空格键，开启跳的状态
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                if dinosaur.rect.y >= dinosaur.lowest_y:          # 如果恐龙在地面上
                    dinosaur.jump()                               # 开启恐龙跳的状态
                    dinosaur.jump_audio.play()                    # 播放小恐龙跳跃音效
                if over is True:             # 判断游戏结束的开关是否开启
                    main_game()              # 如果开启将调用 main_game() 方法重新启动游戏

        if over is False:
            # 绘制地图起到更新地图的作用
            bg1.map_update()
            # 地图移动
            bg1.map_rolling()
            bg2.map_update()
            bg2.map_rolling()
            # 恐龙移动
            dinosaur.move()
            # 绘制恐龙
            dinosaur.draw_dinosaur()

            # 计算障碍物间隔时间
            if addObstacleTime >= 1300:
                r = random.randint(0, 100)
                if r > 40:
                    # 创建障碍物对象
                    obstacle = Obstacle()
                    # 将障碍物对象添加到列表中
                    lists.append(obstacle)
                # 重置添加障碍物时间
                addObstacleTime = 0

            # 循环遍历障碍物
            for i in range(len(lists)):
                # 障碍物移动
                lists[i].obstacle_move()
                # 绘制障碍物
                lists[i].draw_obstacle()

                # 判断恐龙与障碍物是否碰撞
                if pygame.sprite.collide_rect(dinosaur, lists[i]):
                    over = True                        # 碰撞后开启结束开关
                    game_over()                        # 调用游戏结束的方法
                else:
                    # 判断小恐龙是否越过了障碍物
                    if (lists[i].rect.x + lists[i].rect.width) < dinosaur.rect.x:
                        # 加分
                        score += lists[i].get_score()
                # 显示分数
                lists[i].show_score(score)

        addObstacleTime += 20       # 增加障碍物时间
        pygame.display.update()      # 更新整个窗体
        FPSCLOCK.tick(FPS)


if __name__ == '__main__':
    main_game()

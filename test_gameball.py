import pygame
import sys
from pygame.locals import *
import random
import math
import traceback


# 继承动画精灵类
class Ball(pygame.sprite.Sprite):

    def __init__(self, image, position, speed, bg_site):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load(image).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = position
        self.speed = speed
        self.bg_width, self.bg_height = bg_site[0], bg_site[1]
        self.radius = self.rect.width / 2

    # 小球自动移动，出界后处理
    def ball_move(self):
        self.rect = self.rect.move(self.speed)

        if self.rect.right < 0:
            self.rect.left = self.bg_width
        elif self.rect.left > self.bg_width:
            self.rect.right = 0

        elif self.rect.top > self.bg_height:
            self.rect.bottom = 0
        elif self.rect.bottom < 0:
            self.rect.top = self.bg_height


# 碰撞检测
def collide_check(item, target):
    coll_balls = []
    for each in target:
        distance = math.sqrt( \
            math.pow((item.rect.center[0] - each.rect.center[0]), 2) + \
            math.pow((item.rect.center[1] - each.rect.center[1]), 2))
        if distance <= (item.rect.width + each.rect.width) / 2:
            coll_balls.append(each)
    return coll_balls


def main():
    pygame.init()
    pygame.mixer.init()

    # 背景图片及小球图片存储位置
    ball_image = r"E:\python_file\ballgame\gray_ball.png"
    bg_image = r"E:\python_file\ballgame\ball_bg.png"

    # 背景音乐
    pygame.mixer.music.load(r"E:\python_file\ballgame\G.E.M.mp3")
    pygame.mixer.music.set_volume(0.2)
    pygame.mixer.music.play()

    # 运行标志位
    runing = True
    BALL_NUM = 5
    music_pause = False

    # 界面尺寸
    bg_site = width, height = 1024, 681
    # 创建界面及标题
    screen = pygame.display.set_mode(bg_site)
    pygame.display.set_caption('Play ball game')
    # 为界面加载背景图片
    back_ground = pygame.image.load(bg_image).convert_alpha()

    # 加载音乐控制图片
    pause_image = pygame.image.load(r"E:\python_file\ballgame\pause.JPG").convert_alpha()
    start_image = pygame.image.load(r"E:\python_file\ballgame\start.jpg").convert_alpha()
    pause_rect = pause_image.get_rect()
    pause_rect.left, pause_rect.top = (width - pause_rect.width), (height - pause_rect.height)
    start_rect = start_image.get_rect()
    start_rect.left, start_rect.top = (width - start_rect.width), (height - start_rect.height)

    # 小球对象列表
    balls = []
    group = pygame.sprite.Group()

    # 创建5个小球
    for i in range(BALL_NUM):
        # 随机选取小球位置
        position = random.randint(0, width - 100), random.randint(0, height - 100)
        # 随机设定小球运行速度及方向
        speed = [random.randint(-5, 5), random.randint(-5, 5)]
        # 实例化小球
        ball = Ball(ball_image, position, speed, bg_site)
        # 碰撞检测
        while pygame.sprite.spritecollide(ball, group, False, pygame.sprite.collide_circle):
            ball.rect.left, ball.rect.top = random.randint(0, width - 100), \
                                            random.randint(0, height - 100)
        balls.append(ball)
        group.add(ball)

    # 实例化帧率
    clock = pygame.time.Clock()

    # 运行
    while runing:

        for event in pygame.event.get():
            # 退出
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            # 空格键
            if event.type == KEYDOWN:
                if event.key == K_SPACE:
                    music_pause = not music_pause

            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1 and (
                        (pause_rect.left + pause_rect.width) >= pygame.mouse.get_pos()[0] >= pause_rect.left \
                        and (pause_rect.top + pause_rect.height) >= pygame.mouse.get_pos()[1] >= pause_rect.top):
                    music_pause = not music_pause

        screen.blit(back_ground, (0, 0))

        if music_pause:
            screen.blit(pause_image, pause_rect)
            pygame.mixer.music.pause()
        else:
            screen.blit(start_image, start_rect)
            pygame.mixer.music.unpause()

        for each in balls:
            each.ball_move()
            screen.blit(each.image, each.rect)

        for i in group:
            group.remove(i)

            if pygame.sprite.spritecollide(i, group, False, pygame.sprite.collide_circle):
                i.speed[0] = -i.speed[0]
                i.speed[1] = -i.speed[1]
            group.add(i)

        pygame.display.flip()
        clock.tick(30)


def play_music():
    pygame.init()
    pygame.mixer.init()

    pygame.mixer.music.load(r"E:\python_file\ballgame\G.E.M.mp3")
    pygame.mixer.music.set_volume(0.2)
    pygame.mixer.music.play()

    bg_size = width, height = 300, 200
    screen = pygame.display.set_mode(bg_size)
    pygame.display.set_caption("泡沫播放器")

    pause_image = pygame.image.load(r"E:\python_file\ballgame\pause.JPG").convert_alpha()
    start_image = pygame.image.load(r"E:\python_file\ballgame\start.jpg").convert_alpha()
    pause_rect = pause_image.get_rect()
    pause_rect.left, pause_rect.top = (width - pause_rect.width) // 2, (height - pause_rect.height) // 2
    start_rect = start_image.get_rect()
    start_rect.left, start_rect.top = (width - start_rect.width) // 2, (height - start_rect.height) // 2
    clock = pygame.time.Clock()
    pause = False

    while True:

        for event in pygame.event.get():

            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_SPACE:
                    pause = not pause
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1 and (
                        (pause_rect.left + pause_rect.width) >= pygame.mouse.get_pos()[0] >= pause_rect.left \
                        and (pause_rect.top + pause_rect.height) >= pygame.mouse.get_pos()[1] >= pause_rect.top):
                    pause = not pause

        screen.fill((255, 255, 255))

        if pause:
            screen.blit(pause_image, pause_rect)
            pygame.mixer.music.pause()
        else:
            screen.blit(start_image, start_rect)
            pygame.mixer.music.unpause()

        pygame.display.flip()

        clock.tick(30)


if __name__ == "__main__":
    try:
        main()
    except SystemExit:
        pass
    except:
        traceback.print_exc()
        pygame.quit()
        input()

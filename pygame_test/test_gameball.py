import pygame
import sys
from pygame.locals import *
import random
import math
import traceback


# 球类，继承动画精灵类
class Ball(pygame.sprite.Sprite):

    def __init__(self, image, control_ball_image, position, speed, bg_site,target):
        pygame.sprite.Sprite.__init__(self)

        self.red_ball = pygame.image.load(control_ball_image).convert_alpha()
        self.image = pygame.image.load(image).convert_alpha()
        self.rect = self.image.get_rect()
        #将小球放在指定position
        self.rect.left, self.rect.top = position
        #小球速度
        self.speed = speed
        #小球方向
        self.side = [random.choice([-1,1]),random.choice([-1,1])]
        #小球目标
        self.target = target
        #小球是否被控制
        self.control = False
        #是否碰撞
        self.collide = False
        #背景长宽
        self.bg_width, self.bg_height = bg_site[0], bg_site[1]
        #小球半径
        self.radius = self.rect.width / 2

    # 小球自动移动，出界后处理
    def ball_move(self):
        if self.control:
            self.rect = self.rect.move(self.speed)
        else:
            self.rect = self.rect.move((self.speed[0]*self.side[0],\
                                        self.speed[1]*self.side[1]))

        if self.rect.right <= 0:
            self.rect.left = self.bg_width
        elif self.rect.left >= self.bg_width:
            self.rect.right = 0

        elif self.rect.top >= self.bg_height:
            self.rect.bottom = 0
        elif self.rect.bottom <= 0:
            self.rect.top = self.bg_height

    def ball_check(self,motion):
        
        if self.target < motion < self.target + 5:
            return True
        else:
            return False

        
#控制面板类      
class Panel(pygame.sprite.Sprite):
    def __init__(self,panel_image,mouse_image,bg_size):
        pygame.sprite.Sprite.__init__(self)

        self.panel_image = pygame.image.load(panel_image).convert_alpha()
        self.panel_rect = self.panel_image.get_rect()
        self.panel_rect.left,self.panel_rect.top = \
                             (bg_size[0]-self.panel_rect.width)//2,\
                             bg_size[1] - self.panel_rect.height
        self.mouse_image = pygame.image.load(mouse_image).convert_alpha()
        self.mouse_rect = self.mouse_image.get_rect()
        self.mouse_rect.left,self.mouse_rect.top = \
                             self.panel_rect.left,self.panel_rect.top
        
        pygame.mouse.set_visible(False)
    

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
    control_ball_image = r"E:\python_file\ballgame\control_ball.png"
    bg_image = r"E:\python_file\ballgame\ball_bg.png"
    panel_image = r"E:\python_file\ballgame\panel.gif"
    mouse_image = r"E:\python_file\ballgame\mouse.jpg"

    
    # 添加背景音乐
    pygame.mixer.music.load(r"E:\python_file\ballgame\G.E.M.mp3")
    pygame.mixer.music.set_volume(0.2)
    pygame.mixer.music.play()
    #添加音效
    win_sound = pygame.mixer.Sound(r"E:\python_file\ballgame\win.wav")
    lose_sound = pygame.mixer.Sound(r"E:\python_file\ballgame\loser.wav")
    
    # 运行标志位
    runing = True
    BALL_NUM = 5
    music_pause = False

    # 界面尺寸
    bg_size = width, height = 1024, 681
    # 创建界面及标题
    screen = pygame.display.set_mode(bg_size)
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

    #背景图片中黑洞左上角位置
    hole = [(117,119,199,201),(225,227,390,392),\
            (503,505,320,322),(698,700,192,194),\
            (906,908,419,421)]
    # 小球对象列表
    balls = []
    group = pygame.sprite.Group()
   
    # 创建5个小球
    for i in range(BALL_NUM):
        # 随机选取小球位置
        position = random.randint(0, width - 100), random.randint(0, height - 100)
        # 随机设定小球运行速度及方向
        speed = [random.randint(1, 10), random.randint(1, 10)]
        # 实例化小球
        ball = Ball(ball_image, control_ball_image,\
                    position, speed, bg_size, 5*(i+1))
        # 碰撞检测
        while pygame.sprite.spritecollide(ball, group, False, pygame.sprite.collide_circle):
            ball.rect.left, ball.rect.top = random.randint(0, width - 100), \
                                            random.randint(0, height - 100)
        balls.append(ball)
        group.add(ball)

    #控制面板对象
    panel = Panel(panel_image,mouse_image,bg_size)

    #鼠标每秒在玻璃面板产生的事件数量
    motion =0

    #添加自定义事件游戏结束，背景音乐停止游戏结束
    GAMEOVER = USEREVENT
    pygame.mixer.music.set_endevent(GAMEOVER)
    
    #添加自定义事件计数器
    MYTIMER = USEREVENT + 1
    pygame.time.set_timer(MYTIMER,1*1000)

    #设置按键后响应延迟100毫秒
    pygame.key.set_repeat(100,100)
    
    # 实例化帧率
    clock = pygame.time.Clock()

    # 运行
    while runing:

        for event in pygame.event.get():
            # 退出
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            #游戏结束
            if event.type == GAMEOVER:
                lose_sound.play()
                lose_sound.play()
                runing = False
            
            #键盘按键
            if event.type == KEYDOWN:
                # 空格键控制小球消失
                if event.key == K_SPACE:
                    for each in group:
                        if each.control:
                            for i in hole:
                                if i[0]<=each.rect.left<=i[1] and i[2]<=each.rect.top<=i[3]:
                                    win_sound.play()
                                    each.speed = [0,0]
                                    group.remove(each)
                                    temp = balls.pop(balls.index(each))
                                    balls.insert(0,temp)
                                    hole.remove(i)
                            if not hole:
                                pygame.mixer.music.stop()
                                win_sound.play()
                                win_sound.play()
                                pygame.time.delay(3000)
                                #打印胜利图片
                                
                                

                    
                #控制红色小球方向
                if event.key == K_w or event.key ==K_UP:
                    for each in group:
                        if each.control:
                            each.speed[1] -= 1
                if event.key == K_s or event.key ==K_DOWN:
                    for each in group:
                        if each.control:
                            each.speed[1] += 1
                if event.key == K_a or event.key ==K_LEFT:
                    for each in group:
                        if each.control:
                            each.speed[0] -= 1
                if event.key == K_d or event.key ==K_RIGHT:
                    for each in group:
                        if each.control:
                            each.speed[0] += 1
                    
            #背景音乐播放控制
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1 and (
                        (pause_rect.left + pause_rect.width) >= pygame.mouse.get_pos()[0] >= pause_rect.left \
                        and (pause_rect.top + pause_rect.height) >= pygame.mouse.get_pos()[1] >= pause_rect.top):
                    music_pause = not music_pause

            #事件计数
            if event.type == MYTIMER:
                if motion:
                    for each in group:
                        if each.ball_check(motion):
                            each.speed = [0,0]
                            each.control = True
                    motion = 0
            if event.type == MOUSEMOTION:
                motion += 1

        screen.blit(back_ground, (0, 0))
        screen.blit(panel.panel_image,panel.panel_rect)

        panel.mouse_rect.left,panel.mouse_rect.top = pygame.mouse.get_pos()
        if panel.mouse_rect.left<panel.panel_rect.left:
            panel.mouse_rect.left = panel.panel_rect.left
        if panel.mouse_rect.left>panel.panel_rect.right -\
           panel.mouse_rect.width:
            panel.mouse_rect.left = panel.panel_rect.right -panel.mouse_rect.width
        if panel.mouse_rect.top<panel.panel_rect.top:
            panel.mouse_rect.top = panel.panel_rect.top
        if panel.mouse_rect.top>panel.panel_rect.bottom-panel.mouse_rect.height:
            panel.mouse_rect.top = panel.panel_rect.bottom-panel.mouse_rect.height


        screen.blit(panel.mouse_image,panel.mouse_rect)
            

        if music_pause:
            screen.blit(pause_image, pause_rect)
            pygame.mixer.music.pause()
        else:
            screen.blit(start_image, start_rect)
            pygame.mixer.music.unpause()


        for each in balls:
            each.ball_move()
            if each.collide:
                each.speed = [random.randint(1,10),\
                               random.randint(1,10)]
                each.collide = False
            if each.control:
                #将选中的小球变为带标记的小球
                screen.blit(each.red_ball,each.rect)
            else:
                screen.blit(each.image, each.rect)

        for i in group:
            group.remove(i)

            if pygame.sprite.spritecollide(i, group, False, pygame.sprite.collide_circle):
                #i.speed[0] = -i.speed[0]
                #i.speed[1] = -i.speed[1]
                i.side[0] = -i.side[0]
                i.side[1] = -i.side[1]
                i.collide = True
                if i.control:
                    each.side[0] = -1
                    each.side[1] = -1
                    i.control = False
                
            group.add(i)

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

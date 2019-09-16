#config
image_adds="E:\python_file\yu.png"
image_bg = "E:\python_file\sea.jpg"
import pygame
import sys
from pygame.locals import*

        
        

#测试对象移动
def test_game1():
        
        #初始化pygame
        pygame.init()
        #实例化帧率设置对象
        clock = pygame.time.Clock()
        size = width,height = 500,500
        #速度，每次向左移动2个单位，向上移动1个单位
        speed = [2,1]
        #鱼头方向
        fish_head = 1
        #全屏标志，默认为非全屏
        fullscreen = False
        #背景颜色RGB格式
        bg = pygame.image.load(image_bg)
        #bg = (255,255,255)
        #创建窗口并设置窗口的大小，返回一个surface对象
        screen = pygame.display.set_mode(size,RESIZABLE)
        
        #设置窗口标题
        pygame.display.set_caption('pygame第一个测试游戏')

        #加载图片,返回一个surface对象
        image_actor = pygame.image.load(image_adds)
        #获得图片的位置矩形
        position = image_actor.get_rect()
        
        
        while True:
                #检测是否点击关闭按钮，查看是否需要结束事件
                for event in pygame.event.get():
                        if event.type == QUIT:
                                sys.exit()
                        #键盘输入     
                        if event.type == KEYDOWN:
                                if event.key == K_LEFT:
                                        
                                        if fish_head>0:
                                                image_actor = pygame.transform.flip(image_actor,True,False)
                                                fish_head = -fish_head
                                        speed = [-1,0]
                                if event.key == K_RIGHT:
                                        if fish_head<0:
                                                image_actor = pygame.transform.flip(image_actor,True,False)
                                                fish_head = -fish_head 
                                        speed =[1,0]
                                if event.key == K_UP:
                                        if fish_head>0:
                                                fish_head = -fish_head
                                                image_actor = pygame.transform.flip(image_actor,True,False)
                                        speed =[0,-1]
                                if event.key == K_DOWN:
                                        if fish_head>0:
                                                fish_head = -fish_head
                                                image_actor = pygame.transform.flip(image_actor,True,False)
                                        speed =[0,1]
                                #全屏设置(F11)
                                if event.key == K_F11:
                                        fullscreen = not fullscreen
                                        if fullscreen:
                                                size_new = width,height = pygame.display.list_modes()[0]
                                                position[0]=int((position[0]/screen.get_width())*size_new[0])
                                                position[1]=int((position[1]/screen.get_height())*size_new[1])
                                                screen = pygame.display.set_mode(size_new,FULLSCREEN)
                                                
                                        else:
                                                size_new = width,height = 500,500
                                                position[0]=int((position[0]/screen.get_width())*size_new[0])
                                                position[1]=int((position[1]/screen.get_height())*size_new[1])
                                                screen = pygame.display.set_mode(size_new,RESIZABLE)
                                                
                                
                        #调整窗口大小
                        if event.type == VIDEORESIZE:
                                
                                size_new = width,height = event.size
                                position[0]=int((position[0]/screen.get_width())*size_new[0])
                                position[1]=int((position[1]/screen.get_height())*size_new[1])
                                screen = pygame.display.set_mode(size_new,RESIZABLE)
                                
                                
                                        
                
                #移动主角图像
                position = position.move(speed)
                #当图片x方向到达边界时，图片翻转，并反方向移动
                if  position.left <0 or position.right >width:
                        image_actor = pygame.transform.flip(image_actor,True,False)
                        speed[0] = -speed[0]
                #当图片y方向到达边界时，图片反方向移动
                if position.top<0 or position.bottom > height:
                        speed[1] = -speed[1]
                
                #填充背景
                #screen.fill(bg)
                screen.blit(bg,(0,0))
                #更新图片位置
                screen.blit(image_actor,position)
                #更新界面
                pygame.display.flip()
                #延迟10毫秒
                pygame.time.delay(10)
                #设置帧率为1
                clock.tick(30)
if __name__=='__main__':

        test_game1()

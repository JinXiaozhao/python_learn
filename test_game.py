#config
image_adds="E:\python_file\yu.png"
image_bg = "E:\python_file\sea.jpg"
import pygame
import sys
from pygame.locals import*
import math

#基本图形绘制
def test_figure():
        pygame.init()
        clock = pygame.time.Clock()
        
        bg = (255,255,255)
        BLACK = (0,0,0)
        GREEN = (0,255,0)
        RED = (255,0,0)
        BLUE = (0,0,255)
        
        size = width,height = 700,700
        screen = pygame.display.set_mode(size,RESIZABLE)
        pygame.display.set_caption('基本图形绘制测试')

        #多边形顶点坐标
        pointlist1 = [(50,200),(100,200),(100,220),(100,250),(50,250),(50,220)]
        pointlist2 = [(150,200),(200,200),(200,220),(200,250),(150,250),(150,220)]
        pointlist3 = [(250,200),(300,200),(300,220),(300,250),(250,250),(250,220)]
        point1=(250,75)
        pointlist4 = [(point1[0]-200,point1[1]),(point1[0]-100,point1[1]-50),point1,(point1[0]+50,point1[1]-50),(point1[0]+50,point1[1]+50),point1,(point1[0]-100,point1[1]+50)]
        left_button_move = False
        
        #圆形圆心位置
        position = (450,450)
        right_button_move = False
        
        #椭圆中点位置
        position1 = (175,350)
        
        #线段坐标
        pointlist_line1 = [(500,60),(600,100),(650,60)]
        pointlist_line2 = [(500,160),(600,200),(650,160)]

        
        while True:

                for event in pygame.event.get():
                        if event.type == QUIT:
                                pygame.quit()
                                sys.exit()

                        
                        if event.type == MOUSEBUTTONDOWN:
                                if event.button ==1:
                                        left_button_move = True
                                if event.button == 3:
                                        right_button_move = True

                        
                        if event.type == MOUSEBUTTONUP:
                                if event.button == 1:
                                        left_button_move = False
                                if event.button == 3:
                                        right_button_move = False
                                        

                #使用鼠标右键控制椭圆的位置
                if right_button_move:
                        position1 = pygame.mouse.get_pos()
                #使用鼠标左键控制多边形某一点位置，从而移动多边形
                if left_button_move:
                        point1 = pygame.mouse.get_pos()
                        pointlist4 = [(point1[0]-200,point1[1]),(point1[0]-100,point1[1]-50),point1,(point1[0]+50,point1[1]-50),(point1[0]+50,point1[1]+50),point1,(point1[0]-100,point1[1]+50)]               
                                        
                        
                screen.fill(bg)

                #绘制矩形
                pygame.draw.rect(screen,BLACK,(50,300,50,50),0)
                pygame.draw.rect(screen,BLACK,(150,300,50,50),1)
                pygame.draw.rect(screen,BLACK,(250,300,50,50),5)

                #绘制多边形
                pygame.draw.polygon(screen,BLACK,pointlist1,0)
                pygame.draw.polygon(screen,BLACK,pointlist2,1)
                pygame.draw.polygon(screen,BLACK,pointlist3,5)
                pygame.draw.polygon(screen,RED,pointlist4,0)

                #绘制圆形
                pygame.draw.circle(screen,RED,position,25,1)
                pygame.draw.circle(screen,GREEN,position,75,1)
                pygame.draw.circle(screen,BLUE,position,100,1)
                pygame.draw.circle(screen,BLACK,position,125,1)
                
                #绘制椭圆形
                pygame.draw.ellipse(screen,RED,(position1[0]-150,position1[1]+50,300,100),1)
                pygame.draw.ellipse(screen,RED,(position1[0]-100,position1[1],200,200),1)
                #绘制弧线
                pygame.draw.arc(screen,RED,(300,50,300,100),math.pi*1.5,math.pi*2,1)
                #绘制线段
                pygame.draw.line(screen,RED,(500,50),(500,100),1)
                pygame.draw.lines(screen,RED,1,pointlist_line1,1)
                pygame.draw.lines(screen,RED,0,pointlist_line2,1)

                pygame.draw.aaline(screen,BLUE,(500,10),(600,60),1)
                pygame.draw.aaline(screen,BLUE,(400,10),(500,60),0)
                
                pygame.display.flip()
                clock.tick(100)


                

#测试对象移动
def test_game1():
        
        #初始化pygame
        pygame.init()
        #实例化帧率设置对象
        clock = pygame.time.Clock()
        
        #速度，每次向左移动2个单位，向上移动1个单位
        speed = [2,1]
        #鱼头方向
        fish_head = 1
        #全屏标志，默认为非全屏
        fullscreen = False
        
        #创建窗口并设置窗口的大小，返回一个surface对象
        size = width,height = 500,500
        screen = pygame.display.set_mode(size,RESIZABLE)
        #背景颜色RGB格式
        bg = pygame.image.load(image_bg).convert()
        #bg = (255,255,255)
        #设置窗口标题
        pygame.display.set_caption('pygame第一个测试游戏')


        #加载主要处理图片,返回一个surface对象
        image_actor = pygame.image.load(image_adds).convert()
        #获得图片的位置矩形
        position = image_actor.get_rect()
        
        
        while True:
                #检测是否点击关闭按钮，查看是否需要结束事件
                for event in pygame.event.get():
                        if event.type == QUIT:
                                pygame.quit()
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
                                                size_new = width,height = size
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
                        fish_head = -fish_head
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
        try:
                #test_game1()
                test_figure()
        except SystemExit:
                pass
        except:
                traceback.print_exc()
                pygame.quit()
                input()

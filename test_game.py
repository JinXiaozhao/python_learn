import pygame
import sys
def test_game1():
	#测试对象移动
	
	
	#初始化pygame
	pygame.init()

	size = width,height = 400,600
	#速度，每次向左移动2个单位，向上移动1个单位
	speed = [-2,1]
	#背景颜色RGB格式
	bg = (255,255,255)
	#创建窗口并设置窗口的大小，返回一个surface对象
	screen = pygame.display.set_mode(size)
	#设置窗口标题
	pygame.display.set_caption('pygame第一个测试游戏')

	#加载图片,返回一个surface对象
	image_actor = pygame.image.load("E:\python_file\gray_ball.png")
	#获得图片的位置矩形
	position = image_actor.get_rect()
	
	while True:
		#检测是否点击关闭按钮，查看是否需要结束事件
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				sys.exit()
		
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
		screen.fill(bg)
		#更新图片位置
		screen.blit(image_actor,position)
		#更新界面
		pygame.display.flip()
		#延迟10毫秒
		pygame.time.delay(10)
		
if __name__=='__main__':

	test_game1()

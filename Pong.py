import pygame
import random
import math

pygame.init()

# Values for colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0 ,0)  
BLUE = (0, 102, 255)
LBLUE = (0, 100, 150)

# sizes of the screen & other stuff
WIDTH, HEIGHT = 900, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong")

# Clock pygame setup stuff
clock = pygame.time.Clock() 
FPS = 60

# Function that makes it easy to get fonts
def font(size, font = 'freesansbold.ttf'):
	font = pygame.font.Font(font, size)
	return font

# I tried to make a function that would draw me an arrow but it really sucked so I gave up
# It works for like 0, 45, and 90 degrees but it just sucks for everythin in between
def arrow(pos, direct, l, w, color = WHITE):
	print(pos, direct, l, w)
	x = pos[0]
	y = pos[1]
	dx = math.cos((direct*math.pi)/180)
	dy = math.sin((direct*math.pi)/180)
	perp = direct + 90
	perpx = math.cos((perp*math.pi)/180)
	perpy = math.sin((perp*math.pi)/180)
	p1 = (x+perpx*(w//2), y-perpy*(w//2))
	p2 = (p1[0]+4*(dx*l)/5, p1[1]-4*(dy*l)/5)
	p3 = (p2[0]+dx*w, p2[1]+dy*w)
	p4 = (x+dx*l, y-dy*l)
	p6 = (p2[0]-perpx*w, p2[1]+perpy*w)
	p5 = (p6[0]-dx*w, p6[1]-dy*w)
	p7 = (p6[0]-4*(dx*l)/5, p6[1]+4*(dy*l)/5)
	arrow = pygame.draw.polygon(screen, color, (p1, p2, p3, p4, p5, p6, p7))
	return arrow

# The code for the side striker things	
class Striker:
	def __init__(self, posx, posy, width, height, speed, color):
		self.posx = posx
		self.posy = posy
		self.width = width
		self.height = height
		self.speed = speed
		self.color = color
		self.shoot = False
		self.rect = pygame.Rect(posx, posy, width, height)
		self.player = pygame.draw.rect(screen, self.color, self.rect)

	# Displays the rectangle
	def display(self):
		self.player = pygame.draw.rect(screen, self.color, self.rect)

	# Changes the position 
	def update(self, yFac):
		self.posy = self.posy + self.speed*yFac

		# Stops the thing from going too low or too high
		if self.posy <= 0:
			self.posy = 0
		elif self.posy + self.height >= HEIGHT:
			self.posy = HEIGHT-self.height

		# Updates the rect
		self.rect = (self.posx, self.posy, self.width, self.height)

	# Displays score for the rects
	def displayScore(self, text, score, x, y, color):
		text = font(20).render(text+str(score), True, color)
		textRect = text.get_rect()
		textRect.center = (x, y)

		screen.blit(text, textRect)

	# For collision
	def getRect(self):
		return self.rect

	# Get x & y are just useful sometimes
	def getPosY(self):
		return int(self.posy)

	def getPosX(self):
		return self.posx

	# Gives a value if the rect has shot
	def getToggle(self):
		return self.shoot

	# Freezes the rect (just changes the color)
	def freeze(self):
		self.color = LBLUE
  
	def unfreeze(self):
		self.color = GREEN
  
	# Used for genious collision detection math
	def getCenter(self):
		cords = (self.posx+self.width//2, self.posy+self.height//2)
		return cords

	# Makes it so that holding space or control doesn't spam bullets
	def toggle(self):
		if self.shoot:
			self.shoot = False
		else:
			self.shoot = True

# The ball that bounces around
class Ball:
	def __init__(self, posx, posy, radius, speed, color, timer = 3):
		self.posx = posx
		self.posy = posy
		self.radius = radius
		self.ogspeed = speed
		self.speed = speed
		self.color = color
		self.timer = timer
		# Sets the direction as an angle between [10,80], [100, 170], [190, 260], or [280, 350]
		self.direct = random.randint(10, 80)+random.randint(0,3)*90
		# Figures out the rise and run (slope) if the ball with a hypotenuse of the speed
		self.yFac = math.sin((self.direct*math.pi)/180)*self.speed
		self.xFac = math.cos((self.direct*math.pi)/180)*self.speed
		self.ball = pygame.draw.circle(screen, self.color, (self.posx, self.posy), self.radius)
		# Used for drawing the initial arrow
		self.ap1 = (self.posx+math.cos((self.direct*math.pi)/180)*20, self.posy-math.sin((self.direct*math.pi)/180)*20)
		self.ap2 = (self.posx+math.cos((self.direct*math.pi)/180)*10, self.posy-math.sin((self.direct*math.pi)/180)*10)
		# Used to avoid giving multiple points in one score
		self.count1 = 1
		# Used to avoid glitching into the rect and getting stuck on the striker
		self.count2 = 0
		# Used to count seconds for the initial timer
		self.count3 = 0
		# Used to avoid glitching into the top and bottom of the screen.
		self.count4 = 0

	def display(self):
		self.ball = pygame.draw.circle(
			screen, self.color, (self.posx, self.posy), self.radius)

	def update(self):
		if self.timer >> 0:
			pygame.draw.line(screen, BLUE, self.ap1, self.ap2, 3)
			text = font(50).render(str(self.timer), True, WHITE)
			textRect = text.get_rect()
			textRect.center = (WIDTH//2, HEIGHT//2-50)
			screen.blit(text, textRect)
			if self.count3 <= FPS:
				self.count3 +=1
			else:
				self.count3 = 0
				self.timer -= 1

		else:
			self.posx += self.xFac
			self.posy -= self.yFac

			if WIDTH//2-10 <= self.posx <= WIDTH//2+10:
				self.count2 = 0

			if HEIGHT//2-10 <= self.posy <= HEIGHT//2+10:
				self.count4 = 0

			# Bounces it off the top
			if self.posy <= 0 or self.posy >= HEIGHT:
				if self.count4 == 0:
					self.yFac *= -1
					self.count4 = 1

			# Checks if the ball has scored, return where it scored
			if self.posx <= 0 and self.count1:
				self.count1 = 0
				return 1
			elif self.posx >= WIDTH and self.count1:
				self.count1 = 0
				return -1
			else:
				return 0

	def reset(self):
		self.posx = WIDTH//2
		self.posy = HEIGHT//2
		self.xFac *= -1
		self.count1 = 1
		self.count4 = 0
		self.speed = self.ogspeed
		self.yFac = math.sin((self.direct*math.pi)/180)*self.speed
		self.xFac = math.cos((self.direct*math.pi)/180)*self.speed

	# Sadly took me the longest, it bounces the ball of a rect in a kinda controlable way 
	def hit(self, cords):
		self.count4 = 0
		if self.count2 != 1:
			# Speeds it up a bit every hit
			self.speed *= 1.02
			self.count2 = 1
			if cords[0] == 25:
				# (Angle of reflection)
				aor = (180*(math.atan((self.posy-cords[1])/(cords[0]-self.posx-20))/math.pi))
				if aor <= 0:
					aor += 360
			else:
				aor = 180+(180*(math.atan((self.posy-cords[1])/(cords[0]-self.posx+20))/math.pi))
			self.direct = aor
			self.yFac = math.sin((self.direct*math.pi)/180)*self.speed
			self.xFac = math.cos((self.direct*math.pi)/180)*self.speed
   
	def getdirect(self):
		return self.direct

	def getRect(self):
		return self.ball

# I added bullets because I got bored (it was before I started the math for the ball so I wasn't yet angry)
class Bullet:
	# Litteraly all the same as the ball, just simpler and red
	def __init__(self, posx, posy, radius, speed, color):
		self.posx = posx
		self.posy = posy
		self.radius = radius
		self.speed = speed
		self.color = color
		self.xFac = 1
		self.bullet = pygame.draw.circle(
			screen, self.color, (self.posx, self.posy), self.radius)

	def display(self):
		self.bullet = pygame.draw.circle(
			screen, self.color, (self.posx, self.posy), self.radius)

	def update(self):
		self.posx += self.speed*self.xFac

		if self.posx <= 0:
			return 1
		elif self.posx >= WIDTH:
			return 1
		else:
			return 0

	def hit(self):
		self.xFac *= -1

	def getRect(self):
		return self.bullet

# This was what I worked on when I was sick of messing with the values of the bullet's bounce
class Button:
	def __init__(self, posx, posy, width, height, frame):
		self.posx = posx
		self.posy = posy
		self.width = width
		self.height = height
		self.frame = frame
		self.backcolor = WHITE
		# I went with two rects because I didn't feel like using a sprite or png
		self.backRect = pygame.Rect(posx, posy, width, height)
		self.backButton = pygame.draw.rect(screen, self.backcolor, self.backRect)
		self.frontRect = pygame.Rect(posx+self.frame, posy+self.frame, width-2*self.frame, height-2*self.frame)
		self.frontButton = pygame.draw.rect(screen, BLACK, self.frontRect)
  
	def update(self):
		self.backRect = pygame.Rect(self.posx, self.posy, self.width, self.height)
		self.frontRect = pygame.Rect(self.posx+self.frame, self.posy+self.frame, self.width-2*self.frame, self.height-2*self.frame)
 
	def display(self):
		self.backButton = pygame.draw.rect(screen, self.backcolor, self.backRect)
		self.frontButton = pygame.draw.rect(screen, BLACK, self.frontRect)

	def displayTextPos(self, text, size, x, y, color, list=[], listsize = 0):
		text = font(size).render(text, True, color)
		textRect = text.get_rect()
		textRect.center = (x, y)
		screen.blit(text, textRect)
		count = 1
		for string in list:
			text2 = font(listsize).render(string, True, WHITE)
			textRect2 = text2.get_rect()
			textRect2.center = (x, y+2*listsize*count)
			screen.blit(text2, textRect2)
			count += 1
  
	def displayText(self, text, size, color, value = ""):
		text = font(size).render(text+str(value), True, color)
		textRect = text.get_rect()
		textRect.center = (self.posx+(self.width//2), self.posy+(self.height//2))
		screen.blit(text, textRect)
	
	def select(self):
		self.backcolor = GREEN
  
	def unselect(self):
		self.backcolor = WHITE

# I just copy and pasted Bullet Pong and removed some stuff
def Pong():
	running = True
 
	# Spawning that objects
	player1 = Striker(20, 250, 10, 100, 10, GREEN)
	player2 = Striker(WIDTH-30, 250, 10, 100, 10, GREEN)
	ball = Ball(WIDTH//2, HEIGHT//2, 7, 10, WHITE)

	# (List of players) Didn't make this till later and it is great, used for collision detection
	lop = [player1, player2]
 

	# Initial values of the players
	player1Score, player2Score = 0, 0
	player1YFac, player2YFac = 0, 0
	
	while running:
		screen.fill(BLACK)

		# Event handling
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_UP:
					player2YFac = -1
				if event.key == pygame.K_DOWN:
					player2YFac = 1
				if event.key == pygame.K_w:
					player1YFac = -1
				if event.key == pygame.K_s:
					player1YFac = 1

			if event.type == pygame.KEYUP:
				if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
					player2YFac = 0
				if event.key == pygame.K_w or event.key == pygame.K_s:
					player1YFac = 0


		# Collision detection
		for player in lop:
			if pygame.Rect.colliderect(ball.getRect(), player.getRect()):
				xy = player.getCenter()
				ball.hit(xy)
	

		# Updating the objects
		player1.update(player1YFac)
		player2.update(player2YFac)
		point = ball.update()


		# -1 -> player1 scored, +1 -> player2 scored, 0 -> Nothing interesting happened
		if point == -1:
			player1Score += 1
		elif point == 1:
			player2Score += 1

		# Someone scored so reset the ball
		if point: 
			ball.reset()

		# Displaying the objects on the screen
		player1.display()
		player2.display()
		ball.display()


		# Displays the scores of each player
		player1.displayScore("Player 1 : ", 
						player1Score, 100, 20, WHITE)
		player2.displayScore("Player 2 : ", 
						player2Score, WIDTH-100, 20, WHITE)

		# Boring pygame stuff
		pygame.display.update()
		clock.tick(FPS)	 
  
# This code + the menu made main() too big and confusing so I started to split it into funtions
def BulletPong():
	running = True
 
	# Spawning all dem objects
	player1 = Striker(20, 250, 10, 100, 10, GREEN)
	player2 = Striker(WIDTH-30, 250, 10, 100, 10, GREEN)
	ball = Ball(WIDTH//2, HEIGHT//2, 7, 10, WHITE)

	# (List of players) Didn't make this till later and it is great, used for collision detection
	lop = [player1, player2]
 

	# Initial values of the players
	player1Score, player2Score = 0, 0
	player1YFac, player2YFac = 0, 0
	shoot1 = 0
	shoot2 = 0
	freeze1 = 0
	freeze2 = 0
	bullets = []
	
	while running:
		screen.fill(BLACK)

		# Event handling
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False
			if event.type == pygame.KEYDOWN:
				if freeze2 == 0:
					if event.key == pygame.K_UP:
						player2YFac = -1
					if event.key == pygame.K_DOWN:
						player2YFac = 1
				if freeze1 == 0:
					if event.key == pygame.K_w:
						player1YFac = -1
					if event.key == pygame.K_s:
						player1YFac = 1
				if event.key == pygame.K_SPACE:
					if shoot1 == 0:
						shoot1 = 1
						# I guess python doesn't like just putting player1.getPosY() into a class ):<
						gety1 = player1.getPosY()
						bullets.append(Bullet(40, gety1+50, 7, 20, RED))
				if event.key == pygame.K_RCTRL:
					if shoot2 == 0:
						shoot2 = 1
						gety2 = player2.getPosY()
						bullets.append(Bullet(WIDTH-40, gety2+50, 7, -20, RED))

			if event.type == pygame.KEYUP:
				if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
					player2YFac = 0
				if event.key == pygame.K_w or event.key == pygame.K_s:
					player1YFac = 0

		if shoot1 >> 0:
			shoot1 += 1
		if shoot1 >= 30:
			shoot1 = 0
		if shoot2 >> 0:
			shoot2 += 1
		if shoot2 >= 30:
			shoot2 = 0
					

		# Collision detection, couldn't find a better way to detect bullets without try
		for player in lop:
			if pygame.Rect.colliderect(ball.getRect(), player.getRect()):
				xy = player.getCenter()
				ball.hit(xy)
			for bullet in bullets:
				if pygame.Rect.colliderect(bullet.getRect(), player2.getRect()):
					freeze2 = 1
				if pygame.Rect.colliderect(bullet.getRect(), player1.getRect()):
					freeze1 = 1
	
		# Counts 30 frames (1 second) before unfreezing the player
		if freeze1 == 30:
			player1.unfreeze()
			freeze1 = 0
		elif freeze1 >= 1:
			player1.freeze()
			player1YFac = 0
			freeze1 += 1
   
		if freeze2 == 30:
			player2.unfreeze()
			freeze2 = 0
		elif freeze2 >= 1:
			player2.freeze()
			player2YFac = 0
			freeze2 += 1

		# Updating the objects
		player1.update(player1YFac)
		player2.update(player2YFac)
		point = ball.update()
		for bullet in bullets:
			bullet.display()
			bullet.update()

		# -1 -> player1 scored, +1 -> player2 scored, 0 -> Nothing interesting happened
		if point == -1:
			player1Score += 1
		elif point == 1:
			player2Score += 1

		# Someone scored so reset the ball
		if point: 
			ball.reset()

		# Displaying the objects on the screen
		player1.display()
		player2.display()
		ball.display()
		# Again was out of ideas

		# Displays the scores of each player
		player1.displayScore("Player 1 : ", 
						player1Score, 100, 20, WHITE)
		player2.displayScore("Player 2 : ", 
						player2Score, WIDTH-100, 20, WHITE)

		# Boring pygame stuff
		pygame.display.update()
		clock.tick(FPS)	 

def Menu():
	running = True
	
  
	bulletPong = Button(WIDTH//2-100, HEIGHT//2, 200, 80, 3)
	pong = Button(WIDTH//2-100, HEIGHT//2-80, 200, 80, 3)
 
	quitButton = Button(WIDTH//2-30, HEIGHT-60, 60, 30, 3)
  
	# List of Buttons
	lob = [pong, bulletPong, quitButton]

	# Dictionary of Texts and font sizes
	dot = {"Pong": 30,
		"Bullet Pong": 30,
		"Quit": 15}
 
	# Lists of each buttons description
	mains = ["Pong",
		  "Bullet Pong",
		  ""]
	descs = [["This is just regular Pong.",
			"The left player uses W and S",
			"to move and the right player",
			"uses Up and Down arrows"],
			["This is Pong with bullets.",
			"Same controls and Pong except",
			"the left player uses space and",
			"the right player uses left control",
			"to shoot a bullet that freezes",
			"the other player for a second."],
		   []]
	
	selected = 0

	while running:

		screen.fill(BLACK)

		# Counts which button is being displayed
		count = 0

		for obj in lob:
			obj.display()
			obj.update()
			lob[selected].select()
			lob[selected].displayTextPos(mains[selected], 20, WIDTH-150, 100, GREEN, descs[selected], 15)
			obj.displayText(list(dot)[count], list(dot.values())[count], WHITE)
			count += 1

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False
				return 0
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_k:
					piss += 10
				if event.key == pygame.K_UP:
					for obj in lob:
						obj.unselect()
					selected -= 1
					if selected >= len(lob):
						selected = 0
				if event.key == pygame.K_DOWN:
					for obj in lob:
						obj.unselect()
					selected += 1
					if selected >= len(lob):
						selected = 0
				if event.key == pygame.K_RETURN:
					if list(dot)[selected] == "Bullet Pong":
						running = False
						return "BP"
					elif list(dot)[selected] == "Pong":
						running = False	
						return "P"
					else:
						return 0

  
		pygame.display.update()
		clock.tick(FPS)

def main():
	menu = Menu()
	if menu == "BP":
		BulletPong()
	elif menu == "P":
		Pong()

# Read about how this makes it so when you call this file from another file it doesn't run or something
if __name__ == "__main__":
	main()
	pygame.quit()

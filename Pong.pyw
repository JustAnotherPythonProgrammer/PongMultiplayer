import pygame
from pygame.locals import *
from Client import Client
from sys import argv, exit
from random import randint, random
pygame.init()

try:
    me = Client(argv[1], int(argv[2]), int(argv[3]), int(argv[4]), int(argv[5]), int(argv[6]))
except IndexError:
    me = Client(input("Host: "), 8080, 4444, 5555, 10, 0)
me.connect()


pygame.key.set_repeat(1, 1)

Black = (  0,   0,   0)
White = (255, 255, 255)

class screen():
    def __init__(self, Width, Height, Color, FPS):
        self.Width = Width
        self.Height = Height
        self.Clock = pygame.time.Clock()
        self.FPS = FPS
        self.Display = pygame.display.set_mode((self.Width, self.Height))
        pygame.display.set_caption('Pong: Player ' + str(me.player))

    def Clear(self):
        self.Display.fill(Black)
        pygame.draw.rect(self.Display, White, (((self.Width / 2) - 2), 0, 4, self.Height), 0)
        self.Clock.tick(self.FPS)



class paddle():
    def __init__(self, Width, Height, Color, x_coord, Speed):
        self.Width = Width
        self.Height = Height
        self.Color = Color
        self.x = x_coord
        self.y = 200
        self.Speed = Speed

    def Update(self, KEY):
        if KEY == K_UP:
            if self.y > 0:
                self.y -= self.Speed
        if KEY == K_DOWN:
            if self.y < Screen.Height - self.Height:
                self.y += self.Speed

    def Move(self, KEY):
        self.Update(KEY)

    def Draw(self):
        pygame.draw.rect(Screen.Display, self.Color, (self.x, self.y, self.Width, self.Height), 0)


class ball():
    def __init__(self, Color, Radius):
        self.x = 195
        self.y = 195
        self.Color = Color
        self.Radius = Radius
        self.DeltaX = 2
        self.DeltaY = None


    def Draw(self):
        pygame.draw.circle(Screen.Display, self.Color, (self.x, self.y), self.Radius, 0)


    def Update(self):
        Ball.Dead()
        Ball.Bounce()
        self.x += self.DeltaX
        self.y += self.DeltaY


    def Bounce(self):
        if self.y > Screen.Height - self.Radius:
            self.DeltaY *= -1
            return
        if self.y < self.Radius:
            self.DeltaY *= -1
            return
        if self.y > UserPaddle.y and self.y < UserPaddle.y + UserPaddle.Height and self.x > UserPaddle.x - self.Radius:
            self.DeltaX *= -1
            return

    def Dead(self):
        if self.x > Screen.Width - self.Radius or self.x < self.Radius:
            self.x = 195
            self.y = 195
            self.DeltaX = 2
            self.DeltaY = randint(1, 2) * 1 if random() < 0.5 else -1



class game():
    def __init__(self):
        pass

    def Inputs(self):
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_UP or event.key == K_DOWN:
                    UserPaddle.Update(event.key)
            if event.type == QUIT:
                me.close()
                pygame.quit()
                exit(0)

    def Draw(self):
        Screen.Clear()
        UserPaddle.Draw()
        OtherPaddle.Draw()
        Ball.Draw()



def getGameData():
    gameData = me.recieve()
    ballData, playerData = gameData.split("/")
    ballData = ballData.split("|")
    playerData = playerData.split("|")
    ballData = [int(x) for x in ballData]
    playerData = [int(y) for y in playerData]
    newBallx = ballData[0]
    newBally = ballData[1]
    newBallDeltaX = ballData[2]
    newBallDeltaY = ballData[3]
    newUserPaddley = playerData[me.player - 1]
    newOtherPaddley = playerData[int(not me.player - 1)]
    return newBallx, newBally, newBallDeltaX, newBallDeltaY, newUserPaddley, newOtherPaddley




def Main():
    global Screen, UserPaddle, OtherPaddle, Ball, Game

    Screen = screen(400, 300, White, 60)
    UserPaddle = paddle(10, 30, White, 370, 3)
    OtherPaddle = paddle(10, 30, White, 20, 3)
    Ball = ball(White, 6)

    Game = game()

    try:
        ballx, bally, ballDeltaX, ballDeltaY, UserPaddley, OtherPaddley = getGameData()
        Ball.x, Ball.y, Ball.DeltaX, Ball.DeltaY = ballx, bally, ballDeltaX, ballDeltaY
        UserPaddle.y, OtherPaddle.y = UserPaddley, OtherPaddley



        flip = 200
        if me.player == 1:
            while True:
                Game.Inputs()
                Game.Draw()
                me.send(f"{Ball.x}|{Ball.y}|{Ball.DeltaX}|{Ball.DeltaY}/{UserPaddle.y}")
                pygame.display.update()

                ballData, paddleData =  me.recieve().split("/")
                OtherPaddle.y = int(paddleData)
                Ball.x, Ball.y, Ball.DeltaX, Ball.DeltaY = [int(num) for num in ballData.split("|")]
                Ball.x = flip - abs(flip - Ball.x) if Ball.x >= flip else flip + abs(flip - Ball.x)
                Ball.DeltaX *= -1
                Ball.Update()




        else:
            while True:
                Game.Inputs()
                ballData, paddleData = me.recieve().split("/")
                OtherPaddle.y = int(paddleData)
                Ball.x, Ball.y, Ball.DeltaX, Ball.DeltaY = [int(num) for num in ballData.split("|")]
                Ball.x = flip - abs(flip - Ball.x) if Ball.x >= flip else flip + abs(flip - Ball.x)
                Ball.DeltaX *= -1
                Ball.Update()

                me.send(f"{Ball.x}|{Ball.y}|{Ball.DeltaX}|{Ball.DeltaY}/{UserPaddle.y}")
                Game.Draw()
                pygame.display.update()



    except Exception as e:
        print(f"\n\n\nError: {e}\n")
        me.close()
        pygame.quit()
        exit(0)



if __name__ == '__main__':
    Main()

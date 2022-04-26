from graphics import *
import random
import time

FIELD_HEIGHT = 150
FIELD_WIDTH = 150
PLAYER_SIZE = 4
PLAYER_SPEED = 4

COOKIE_POINT1 = 10
COOKIE_POINT2 = 30
COOKIE_POINT3 = 50
COOKIE_POINT4 = 100

enemies = []
cookies = []

SPEED_SLOW = [-3, -2, -1, 1, 2, 3]
SPEED_FAST = [-4, -3, 5, 6, 7]



class Enemy:
    def __init__(self, x, y, speed, image_src):
        self.x = x
        self.y = y
        self.dx = 0
        self.dy = 0
        self.move_counter = 0
        self.image =  Image(Point(self.x, self.y), image_src)
        self.speed = speed
        enemies.append(self)


def draw_enemy(list, win):
    for enemy in list:
        enemy.image.draw(win)

def move_enemy(list):
        for circle in list:
            if(circle.move_counter == 0):
                circle.dx = random.choice(circle.speed)
                circle.dy = random.choice(circle.speed)
                if(circle.dx == 0 or circle.dy == 0):
                    circle.dx = random.random.choice(circle.speed)
                    circle.dy = random.random.choice(circle.speed)
                circle.dx = circle.dx /10
                circle.dy = circle.dy /10

                circle.image.move(circle.dx,circle.dy)
                circle.x+=circle.dx
                circle.y+=circle.dy
                circle.move_counter+=1
            else:
                circle.image.move(circle.dx,circle.dy)
                circle.x+=circle.dx
                circle.y+=circle.dy
                
                if(circle.x >= FIELD_HEIGHT):
                    circle.dx = circle.dx * -1
                if(circle.x <= 0):
                    circle.dx = circle.dx * -1
                if(circle.y >= FIELD_WIDTH):
                    circle.dy = circle.dy * -1
                if(circle.y <= 0):
                    circle.dy = circle.dy * -1
        

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.image = Image(Point(self.x, self.y), "player.png")
        self.alive = True

    def move(self, key, win):
        if key=="w":
            self.y+= PLAYER_SPEED
            self.y = min(self.y, FIELD_HEIGHT)
            if self.y != FIELD_HEIGHT:
                self.image.move(0, PLAYER_SPEED)
            else:
                self.image.undraw()
                self.image = Image(Point(self.x, self.y), "player.png")
                self.image.draw(win)

        if key=="a":
            self.x-= PLAYER_SPEED
            self.x = max(self.x, 0)
            if self.x != 0:
                self.image.move(-PLAYER_SPEED, 0)
            else:
                self.image.undraw()
                self.image = Image(Point(self.x, self.y), "player.png")
                self.image.draw(win)

        if key=="d":
            self.x+= PLAYER_SPEED
            self.x = min(self.x, FIELD_WIDTH)
            if self.x != FIELD_WIDTH:
                self.image.move(PLAYER_SPEED, 0)
            else:
                self.image.undraw()
                self.image = Image(Point(self.x, self.y), "player.png")
                self.image.draw(win)

        if key=="s":
            self.y-= PLAYER_SPEED
            self.y = max(self.y, 0)
            if self.y != 0:
                self.image.move(0, -PLAYER_SPEED)
            else:
                self.image.undraw()
                self.image = Image(Point(self.x, self.y), "player.png")
                self.image.draw(win)

    
    def draw(self, win):
        self.image.draw(win)

    def undraw(self):
        self.image.undraw()

    def hit(self, list):
        for enemy in list:
            if((self.x - PLAYER_SIZE < enemy.x and self.x + PLAYER_SIZE > enemy.x ) and (self.y - PLAYER_SIZE < enemy.y and self.y + PLAYER_SIZE > enemy.y)):
                self.alive = False

class  Packman:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.point = COOKIE_POINT1
        self.circ = Circle(Point(self.x, self.y), 0.8)
        self.circ.setFill("BROWN")
        cookies.append(self)   
      
def eat(list, x, y, win):
    score = 0
    for cookies in list:
        if((x - PLAYER_SIZE < cookies.x and x + PLAYER_SIZE > cookies.x ) and (y - PLAYER_SIZE < cookies.y and y + PLAYER_SIZE > cookies.y)):
            cookies.circ.undraw()
            if(cookies.point==COOKIE_POINT1):
                score += COOKIE_POINT1          
            if(cookies.point==COOKIE_POINT2):
                score += COOKIE_POINT2
            if(cookies.point==COOKIE_POINT3):
                score += COOKIE_POINT3   
            if(cookies.point==COOKIE_POINT4):
                score += COOKIE_POINT4
            cookies.x = random.randint(1, FIELD_WIDTH)
            cookies.y = random.randint(10, FIELD_HEIGHT)
            ramdom = random.randint(1, 10)
            flag = 0

            #茶(10)->緑(30)->50%の確率で青(50)->50%の確率で黄色(100)になる。
            if(cookies.point == COOKIE_POINT1):
                cookies.circ = Circle(Point(cookies.x,cookies.y),1.2)
                cookies.circ.setFill("Green")
                cookies.point =COOKIE_POINT2
                flag = 1
            elif(cookies.point == COOKIE_POINT3 and ramdom >= 6 and flag ==0):
                cookies.circ = Circle(Point(cookies.x,cookies.y),2.0)
                cookies.circ.setFill("Yellow")
                cookies.point =COOKIE_POINT4
                flag = 1
            elif(cookies.point == COOKIE_POINT2 and ramdom >= 6 and flag ==0):
                cookies.circ = Circle(Point(cookies.x,cookies.y),1.7)
                cookies.circ.setFill("Blue")
                cookies.point =COOKIE_POINT3
                flag = 1
            else:
                cookies.circ = Circle(Point(cookies.x,cookies.y),0.8)
                cookies.circ.setFill("Brown")
                cookies.point =COOKIE_POINT1
            cookies.circ.draw(win)
    return score      


def draw_cookie(list, win):
    for cookies in list:
        cookies.circ.draw(win)

def main():
    win = GraphWin("Escape from enemies", 600, 600)
    win.setCoords(0, 0, FIELD_WIDTH, FIELD_HEIGHT)
    background = Image(Point(75,75), "background.png")
    background.draw(win)

    bomb = Image(Point(5,145), "canon.png")
    bomb.draw(win)

    for i in range(5):
        x1 = random.randint(1, FIELD_WIDTH-1)
        y1 = random.randint(1, FIELD_HEIGHT-1)
        Enemy(x1, y1, SPEED_SLOW, "enemy_red.png")

    for i in range(30):
        x1 = random.randint(1, FIELD_WIDTH-1)
        y1 = random.randint(1, FIELD_HEIGHT-1)
        Packman(x1, y1)

    player = Player(FIELD_WIDTH / 2, FIELD_HEIGHT / 2)


    draw_enemy(enemies, win)
    draw_cookie(cookies, win)
    player.draw(win)

    label_score = Text(Point(125, 140), "Score")
    label_score.setSize(20)
    label_score.draw(win)

    score = 0
    score_point = Text(Point(142, 140), score)
    score_point.setSize(20)
    score_point.draw(win)

#ゲームの開始のカウントダウン
    time_sta = time.time()
    time_now = 5
    label_time = Text(Point(FIELD_WIDTH / 2, FIELD_HEIGHT * 0.75), str(5))
    label_time.setSize(36)
    label_time.draw(win)

    while(time_now > 0):
        time_now = 5 - int(time.time() - time_sta)
        label_time.setText(str(time_now))
        key = win.checkKey()
        if(key == "w" or key == "a" or key == "d" or key == "s"):
            player.move(key, win)

    label_time.undraw()

    time_sta = time.time()
    
    while(1):
        move_enemy(enemies)

        key = win.checkKey()
        if(key == "w" or key == "a" or key == "d" or key == "s"):
            player.move(key, win)

        score += eat(cookies,player.x,player.y,win)
        score_point.setText(str(score))
        
                    
        player.hit(enemies)
        if not player.alive:
            break

        time_now = time.time()
        if(time_now - time_sta > 5):
            Enemy(10 , 140, SPEED_FAST, "enemy_black.png")
            enemies[len(enemies)-1].image.draw(win)
            score_point.setText(str(score))
            time_sta+=5
        
        update(80)


        
#Gameover後 ゲームの結果を表示
    rect = Rectangle(Point(FIELD_WIDTH * 0.25, FIELD_HEIGHT * 0.25), Point(FIELD_WIDTH * 0.75, FIELD_HEIGHT * 0.75))
    
    rect.draw(win)

    tmp_str = Text(Point(FIELD_WIDTH / 2, 80), "Your score").draw(win)
    tmp_str.setSize(30)
    tmp_str = Text(Point(FIELD_WIDTH / 2, 65), score).draw(win)
    tmp_str.setSize(30)

    win.getMouse()
    win.close()

main()
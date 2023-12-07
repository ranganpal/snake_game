import pygame, sys, random
from pygame.math import Vector2

class Food:
    def __init__(self):
        self.create_food()
    
    def create_food(self):
        self.__x_food = random.randint(0, cell_num - 1)
        self.__y_food = random.randint(0, cell_num - 1)
        self.__pos = Vector2(self.__x_food, self.__y_food)

    def pos(self):
        return self.__pos

    def draw_food(self):
        x_pos = self.__pos.x * cell_size
        y_pos = self.__pos.y * cell_size
        weidth = height = cell_size
        food_rect = pygame.Rect(x_pos, y_pos, weidth, height)
        pygame.draw.rect(screen, (126, 166, 114), food_rect)

class Snake:
    def __init__(self):
        self.__body = [Vector2(7, 10), Vector2(6, 10), Vector2(5, 10)]
        self.__direction = Vector2(1, 0)
        self.__grow = False

    def head_pos(self):
        return self.__body[0]
    
    def body(self):
        return self.__body
    
    def direction(self):
        return self.__direction

    def draw_snake(self):
        for block in self.__body:
            x_pos = block.x * cell_size
            y_pos = block.y * cell_size
            weidth = height = cell_size
            block_rect = pygame.Rect(x_pos, y_pos, weidth, height)
            pygame.draw.rect(screen, (77, 100, 250), block_rect)

    def move_snake(self):
        if self.__grow: 
            self.__body.insert(0, self.__body[0] + self.__direction)
            self.__grow = False
        else:
            self.__body.pop()
            self.__body.insert(0, self.__body[0] + self.__direction)
            
    def change_direction(self, x, y):
        if self.__direction.x == 0 and y == 0: # left and right
            self.__direction.x = x 
            self.__direction.y = y

        if self.__direction.y == 0 and x == 0: # up and down
            self.__direction.x = x 
            self.__direction.y = y

    def grow_snake(self):
        self.__grow = True

class Main:
    def __init__(self):
        self.food = Food()
        self.snake = Snake()

    def draw_elements(self):
        self.food.draw_food()
        self.snake.draw_snake()

    def update(self):
        self.snake.move_snake()
        self.check_collision()
        self.check_fail()

    def check_collision(self):
        if self.food.pos() == self.snake.head_pos():
            self.food.create_food()
            self.snake.grow_snake()

    def check_fail(self):
        head = self.snake.head_pos()
        in_x_range = 0 <= head.x <= cell_num - 1
        in_y_range = 0 <= head.y <= cell_num - 1
        if not in_x_range or not in_y_range:
            self.game_over()

        snake = self.snake.body()
        for block in snake[1:]:
            if block == snake[0]:
                self.game_over()

    def game_over():
        pygame.quit()
        sys.exit()


pygame.init()

cell_size = 20
cell_num = 30
screen = pygame.display.set_mode((cell_size * cell_num, cell_size * cell_num))
clock = pygame.time.Clock()

main_game = Main()

SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE, 150)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == SCREEN_UPDATE:
            main_game.update()

        if event.type == pygame.KEYDOWN:
            
            if event.key == pygame.K_UP:
                main_game.snake.change_direction(0, -1)
            if event.key == pygame.K_DOWN:
                main_game.snake.change_direction(0, 1)
            if event.key == pygame.K_LEFT:
                main_game.snake.change_direction(-1, 0)
            if event.key == pygame.K_RIGHT:
                main_game.snake.change_direction(1, 0)

    
    screen.fill((175, 215, 70))
    main_game.draw_elements()
    pygame.display.update()
    clock.tick(60)

pygame.quit()
sys.exit()
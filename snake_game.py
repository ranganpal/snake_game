import pygame, sys, random
from pygame.math import Vector2

class Food:
    def __init__(self):
        self.create_food()
        self.__apple = pygame.image.load('Graphics/apple.png').convert_alpha()
    
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
        screen.blit(self.__apple, food_rect)

class Snake:
    def __init__(self):
        self.create_snake()
        self.__grow = False

        self.__head_up = pygame.image.load('Graphics/head_up.png').convert_alpha()
        self.__head_down = pygame.image.load('Graphics/head_down.png').convert_alpha()
        self.__head_right = pygame.image.load('Graphics/head_right.png').convert_alpha()
        self.__head_left = pygame.image.load('Graphics/head_left.png').convert_alpha()
		
        self.__tail_up = pygame.image.load('Graphics/tail_up.png').convert_alpha()
        self.__tail_down = pygame.image.load('Graphics/tail_down.png').convert_alpha()
        self.__tail_right = pygame.image.load('Graphics/tail_right.png').convert_alpha()
        self.__tail_left = pygame.image.load('Graphics/tail_left.png').convert_alpha()

        self.__body_vertical = pygame.image.load('Graphics/body_vertical.png').convert_alpha()
        self.__body_horizontal = pygame.image.load('Graphics/body_horizontal.png').convert_alpha()

        self.__body_tl = pygame.image.load('Graphics/body_tl.png').convert_alpha()
        self.__body_tr = pygame.image.load('Graphics/body_tr.png').convert_alpha()
        self.__body_bl = pygame.image.load('Graphics/body_bl.png').convert_alpha()
        self.__body_br = pygame.image.load('Graphics/body_br.png').convert_alpha()

        self.__point_gain_sound = pygame.mixer.Sound('Sounds/point_gain.wav')
        self.__turn_snake_sound = pygame.mixer.Sound('Sounds/turn_snake.wav')
        self.__game_over_sound = pygame.mixer.Sound('Sounds/game_over.wav')

    def create_snake(self):
        self.__blocks = [Vector2(5, 4), Vector2(4, 4), Vector2(3, 4)]
        self.__direction = Vector2(1, 0)

    def head(self):
        return self.__blocks[0]
    
    def body(self):
        return self.__blocks[1:]
    
    def direction(self):
        return self.__direction
    
    def play_point_gain_sound(self):
        self.__point_gain_sound.play()
    
    def play_turn_sound(self):
        self.__turn_snake_sound.play()

    def play_game_over_sound(self):
        self.__game_over_sound.play()
    
    def update_head_block(self):
        head_body_rtln = self.__blocks[0] - self.__blocks[1]
        if   head_body_rtln == Vector2(1, 0): self.__head_block = self.__head_right
        elif head_body_rtln == Vector2(-1,0): self.__head_block = self.__head_left
        elif head_body_rtln == Vector2(0, 1): self.__head_block = self.__head_down
        elif head_body_rtln == Vector2(0,-1): self.__head_block = self.__head_up
    
    def update_tail_block(self):
        tail_body_rtln = self.__blocks[-1] - self.__blocks[-2]
        if   tail_body_rtln == Vector2(1, 0): self.__tail_block = self.__tail_right
        elif tail_body_rtln == Vector2(-1,0): self.__tail_block = self.__tail_left
        elif tail_body_rtln == Vector2(0, 1): self.__tail_block = self.__tail_down
        elif tail_body_rtln == Vector2(0,-1): self.__tail_block = self.__tail_up

    def update_body_block(self, index, block):
        prev_block_rtln = self.__blocks[index - 1] - block
        next_block_rtln = self.__blocks[index + 1] - block

        horizontal = prev_block_rtln.y == next_block_rtln.y == 0
        vertical = prev_block_rtln.x == next_block_rtln.x == 0

        top_left = prev_block_rtln.x == -1 and next_block_rtln.y == -1 or prev_block_rtln.y == -1 and next_block_rtln.x == -1
        top_right = prev_block_rtln.x == 1 and next_block_rtln.y == -1 or prev_block_rtln.y == -1 and next_block_rtln.x == 1
        
        btm_left = prev_block_rtln.x == -1 and next_block_rtln.y == 1 or prev_block_rtln.y == 1 and next_block_rtln.x == -1
        btm_right = prev_block_rtln.x == 1 and next_block_rtln.y == 1 or prev_block_rtln.y == 1 and next_block_rtln.x == 1
        
        if horizontal  : self.__body_block = self.__body_horizontal
        elif vertical  : self.__body_block = self.__body_vertical
        elif top_left  : self.__body_block = self.__body_tl
        elif top_right : self.__body_block = self.__body_tr
        elif btm_left  : self.__body_block = self.__body_bl
        elif btm_right : self.__body_block = self.__body_br

    def draw_snake(self):
        for index, block in enumerate(self.__blocks):
            x_pos = block.x * cell_size
            y_pos = block.y * cell_size
            weidth = height = cell_size
            block_rect = pygame.Rect(x_pos, y_pos, weidth, height)

            if index == 0:
                self.update_head_block()
                screen.blit(self.__head_block, block_rect)
            elif index == len(self.__blocks) - 1:
                self.update_tail_block()
                screen.blit(self.__tail_block, block_rect)
            else:
                self.update_body_block(index, block)
                screen.blit(self.__body_block, block_rect)

    def move_snake(self):
        if self.__grow: 
            self.__blocks.insert(0, self.__blocks[0] + self.__direction)
            self.__grow = False
        else:
            self.__blocks.pop()
            self.__blocks.insert(0, self.__blocks[0] + self.__direction)
            
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
        self.__food = Food()
        self.__snake = Snake()
        self.__score_font = pygame.font.Font('Font\PoetsenOne-Regular.ttf', 25)
        self.__instruction_font = pygame.font.Font('Font\PoetsenOne-Regular.ttf', 55)

    def game_start(self):
        instruction_text = "Press SPACE to Start"
        instruction_surface = self.__instruction_font.render(instruction_text, True, (56, 74, 12))
        x_pos = (cell_size * cell_num) / 2
        y_pos = (cell_size * cell_num + 40) / 2
        instruction_rect = instruction_surface.get_rect(center = (x_pos, y_pos))
        screen.blit(instruction_surface, instruction_rect)

    def control_snake(self, event):
        # if event.key == pygame.K_SPACE:
        #     pass
        if event.key == pygame.K_UP: 
            self.__snake.play_turn_sound()
            self.__snake.change_direction(0,-1)
        if event.key == pygame.K_DOWN: 
            self.__snake.play_turn_sound()
            self.__snake.change_direction(0, 1)
        if event.key == pygame.K_LEFT: 
            self.__snake.play_turn_sound()
            self.__snake.change_direction(-1,0)
        if event.key == pygame.K_RIGHT: 
            self.__snake.play_turn_sound()
            self.__snake.change_direction(1, 0)

    def create_grass1(self, row, col):
        grass_color = (167, 209, 61)
        x_pos = col * cell_size
        y_pos = row * cell_size
        weidth = height = cell_size
        grass_rect = pygame.Rect(x_pos, y_pos, weidth, height)
        pygame.draw.rect(screen, grass_color, grass_rect)

    def create_grass2(self, row, col):
        grass_color = (175, 215, 70)
        x_pos = col * cell_size
        y_pos = row * cell_size
        weidth = height = cell_size
        grass_rect = pygame.Rect(x_pos, y_pos, weidth, height)
        pygame.draw.rect(screen, grass_color, grass_rect)
    
    def draw_grass(self):
        for row in range(cell_num):
            for col in range(cell_num):
                if row % 2 == 0 and col % 2 == 0: self.create_grass1(row, col)
                if row % 2 == 0 and col % 2 != 0: self.create_grass2(row, col)
                if row % 2 != 0 and col % 2 == 0: self.create_grass2(row, col)
                if row % 2 != 0 and col % 2 != 0: self.create_grass1(row, col)

    def draw_score(self):
        score_text = str(len(self.__snake.body()) - 2)
        score_surface = self.__score_font.render(score_text, True, (56, 74, 12))
        score_x = cell_size * cell_num - 40
        score_y = cell_size * cell_num + 35
        score_rect = score_surface.get_rect(bottomright = (score_x, score_y))

        apple_surface = pygame.image.load('Graphics/apple.png').convert_alpha()
        apple_rect = apple_surface.get_rect(midright = score_rect.midleft)

        bg_x = apple_rect.left
        bg_y = apple_rect.top
        weidth = apple_rect.width + score_rect.width + 6
        height = apple_rect.height
        bg_rect = pygame.Rect(bg_x, bg_y, weidth, height)

        pygame.draw.rect(screen, (167, 209, 61), bg_rect)
        pygame.draw.rect(screen, (56, 74, 12), bg_rect, 2)
        screen.blit(apple_surface, apple_rect)
        screen.blit(score_surface, score_rect)

    def draw_elements(self):
        self.draw_grass()
        self.__food.draw_food()
        self.__snake.draw_snake()
        self.draw_score()

    def update_game_elements(self):
        self.__snake.move_snake()
        self.check_collision()

    def check_collision(self):
        if self.__food.pos() == self.__snake.head():
            self.__snake.play_point_gain_sound()
            self.__snake.grow_snake()
            self.__food.create_food()

        for block in self.__snake.body():
            while self.__food.pos() == block:
                self.__food.create_food()

    def check_game_over(self):
        snake_head = self.__snake.head()
        in_x_range = 0 <= snake_head.x <= cell_num - 1
        in_y_range = 0 <= snake_head.y <= cell_num - 1

        if not in_x_range or not in_y_range:
            self.__snake.play_game_over_sound()
            return True

        snake_body = self.__snake.body()
        for block in snake_body:
            if block == snake_head:
                self.__snake.play_game_over_sound()
                return True
            
        return False

    def game_restart(self):
        x_pos = 0
        y_pos = 0
        weidth = cell_num * cell_size
        height = cell_num * cell_size + 40
        restart_rect = pygame.Rect(x_pos, y_pos, weidth, height)
        pygame.draw.rect(screen, background_color , restart_rect)

        score = len(self.__snake.body()) - 2
        instruction_text1 = "GAME OVER   Score: " + str(score)
        instruction_text2 = "Press SPACE to Restart"
        instruction_surface1 = self.__instruction_font.render(instruction_text1, True, (56, 74, 12))
        instruction_surface2 = self.__instruction_font.render(instruction_text2, True, (56, 74, 12))

        x_pos = restart_rect.centerx
        y_pos = restart_rect.centery
        instruction_rect1 = instruction_surface1.get_rect(midbottom = (x_pos, y_pos))
        instruction_rect2 = instruction_surface2.get_rect(midtop = (x_pos, y_pos))

        screen.blit(instruction_surface1, instruction_rect1)
        screen.blit(instruction_surface2, instruction_rect2)

    def recreate_snake(self):
        self.__snake.create_snake()



pygame.init()

cell_size = 40
cell_num = 16
background_color = (126, 159, 60)
screen = pygame.display.set_mode((cell_size * cell_num, cell_size * cell_num + 40))
clock = pygame.time.Clock()
main_game = Main()

SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE, 150)

game_start = False
game_over = False
running = True
while running:
    screen.fill(background_color)
    if not game_start:
        main_game.game_start()
    else:
        main_game.draw_elements()
        if game_over:
            main_game.game_restart()
        
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if game_over:
                    main_game.recreate_snake()
                game_start = True
                game_over = False
            else:
                main_game.control_snake(event)
    
        if game_start and not game_over and event.type == SCREEN_UPDATE:
            main_game.update_game_elements()
            game_over = main_game.check_game_over()

    pygame.display.update()
    clock.tick(60)

pygame.quit()
sys.exit()
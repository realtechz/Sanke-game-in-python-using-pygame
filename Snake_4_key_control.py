import sys
import pygame
import random
import os
import time

pygame.font.init()
WIN_WIDTH = 800
WIN_HEIGHT = 800

frame_size_x = WIN_WIDTH
frame_size_y = WIN_HEIGHT

grid_size_x = 20
grid_size_y = 20
# Colors (R, G, B)
black = pygame.Color(0, 0, 0)
white = pygame.Color(255, 255, 255)
red = pygame.Color(255, 0, 0)
green = pygame.Color(0, 255, 0)
blue = pygame.Color(0, 0, 255)
print(pygame.font.get_fonts())
STAT_FONT = pygame.font.SysFont("bahnschrift", 50)
win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT + 100))
deaths = 0
blockSize_x = int(frame_size_x / grid_size_x)
blockSize_y = int(frame_size_y / grid_size_y)


def drawGrid():
    # Set the size of the grid block
    for x in range(0, frame_size_x, blockSize_x):
        for y in range(0, frame_size_y, blockSize_y):
            rect = pygame.Rect(x, y, blockSize_x, blockSize_y)
            pygame.draw.rect(win, black, rect, 1)


class Snake:
    def __init__(self):
        self.direction = 'RIGHT'
        self.change_to = 'RIGHT'
        self.score = 0
        self.food_spawn = True
        self.snake_pos = [blockSize_x * 5, blockSize_y * 5]
        self.snake_body = [[100, 50]]
        self.food_pos = [random.randrange(1, (frame_size_x // blockSize_x)) * blockSize_x,
                         random.randrange(1, (frame_size_y // blockSize_y)) * blockSize_y]

    def move(self):
        # Making sure the snake cannot move in the opposite direction instantaneously
        if self.change_to == 'UP' and self.direction != 'DOWN':
            self.direction = 'UP'
        if self.change_to == 'DOWN' and self.direction != 'UP':
            self.direction = 'DOWN'
        if self.change_to == 'LEFT' and self.direction != 'RIGHT':
            self.direction = 'LEFT'
        if self.change_to == 'RIGHT' and self.direction != 'LEFT':
            self.direction = 'RIGHT'

        # Moving the snake
        if self.direction == 'UP':
            self.snake_pos[1] -= blockSize_y
        if self.direction == 'DOWN':
            self.snake_pos[1] += blockSize_y
        if self.direction == 'LEFT':
            self.snake_pos[0] -= blockSize_x
        if self.direction == 'RIGHT':
            self.snake_pos[0] += blockSize_x

    def grow(self):
        # Snake body growing mechanism
        self.snake_body.insert(0, list(self.snake_pos))
        if snake.snake_pos[0] == snake.food_pos[0] and snake.snake_pos[1] == snake.food_pos[1]:
            self.score += 1
            self.food_spawn = False
        else:
            self.snake_body.pop()

    def boundary(self):
        global snake
        if self.snake_pos[0] < 0 or self.snake_pos[0] > frame_size_x - blockSize_x:
            snake = Snake()
            game_over(self.score)
        if self.snake_pos[1] < 0 or self.snake_pos[1] > frame_size_y - blockSize_y:
            snake = Snake()
            game_over(self.score)
        # Touching the snake body
        for block in snake.snake_body[1:]:
            if self.snake_pos[0] == block[0] and self.snake_pos[1] == block[1]:
                snake = Snake()
                game_over(self.score)

    def food_spawning(self):
        # Spawning food on the screen
        if not self.food_spawn:
            x, y = [random.randrange(1, (frame_size_x // blockSize_x)) * blockSize_x,
                    random.randrange(1, (frame_size_y // blockSize_y)) * blockSize_y]
            for body in self.snake_body:
                while body[0] == x and body[1] == y:
                    x, y = [random.randrange(1, (frame_size_x // blockSize_x)) * blockSize_x,
                            random.randrange(1, (frame_size_y // blockSize_y)) * blockSize_y]
                self.food_pos = x, y
        self.food_spawn = True

    def update(self):
        self.move()
        self.grow()
        self.boundary()
        self.food_spawning()


snake = Snake()


def draw_window(win, snake, score, deaths):
    win.fill(black)

    for pos in snake.snake_body:
        pygame.draw.rect(win, green, pygame.Rect(pos[0], pos[1], blockSize_x, blockSize_y))
    if snake.food_spawn:
        pygame.draw.rect(win, red, pygame.Rect(snake.food_pos[0], snake.food_pos[1],
                                               blockSize_x, blockSize_y))
    drawGrid()

    pygame.draw.rect(win, white, pygame.Rect(0, WIN_HEIGHT,
                                             WIN_WIDTH, 200))
    text = STAT_FONT.render("Score:" + str(score), True, black)
    win.blit(text, (WIN_WIDTH - 50 - text.get_width(), WIN_HEIGHT + 40))
    # generations
    score_label = STAT_FONT.render("Deaths: " + str(deaths - 1), True, black)
    win.blit(score_label, (50, WIN_HEIGHT + 40))
    pygame.display.update()


# Score
def show_score(color, score):
    score_surface = STAT_FONT.render('Score : ' + str(score), True, color)
    score_rect = score_surface.get_rect()
    score_rect.midtop = (frame_size_x / 2, frame_size_y / 1.25)
    win.blit(score_surface, score_rect)
    # pygame.display.flip()


def game_over(score):
    my_font = pygame.font.SysFont('"bahnschrift"', 90)
    game_over_surface = my_font.render('YOU DIED', True, red)
    win.fill(black)
    win.blit(game_over_surface, (frame_size_x/3.7, frame_size_y / 4))
    show_score(red, score=score)
    pygame.display.flip()
    time.sleep(5)
    pygame.quit()
    sys.exit()


def main():
    # genomes, config
    global win, deaths
    deaths += 1
    run = True
    score = 0

    clock = pygame.time.Clock()
    while run:
        clock.tick(5)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
                sys.exit()
            # Whenever a key is pressed down
            elif event.type == pygame.KEYDOWN:
                # W -> Up; S -> Down; A -> Left; D -> Right
                if event.key == pygame.K_UP or event.key == ord('w'):
                    snake.change_to = 'UP'
                if event.key == pygame.K_DOWN or event.key == ord('s'):
                    snake.change_to = 'DOWN'
                if event.key == pygame.K_LEFT or event.key == ord('a'):
                    snake.change_to = 'LEFT'
                if event.key == pygame.K_RIGHT or event.key == ord('d'):
                    snake.change_to = 'RIGHT'
                # Esc -> Create event to quit the game
                if event.key == pygame.K_ESCAPE:
                    pygame.event.post(pygame.event.Event(pygame.QUIT))

        snake.update()
        draw_window(win, snake, snake.score, deaths=deaths)


if __name__ == "__main__":
    main()

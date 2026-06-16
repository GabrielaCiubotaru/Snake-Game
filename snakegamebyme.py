import pygame
import random

pygame.init()

#Screen
width = 800
height = 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Snake Game 🐍")

#Colours
red = (255, 0, 0)
green = (0, 255, 0)
white = (255, 255, 255)
black = (0, 0, 0)

#Snake
snake_block = 20
snake_speed = 8

clock = pygame.time.Clock()

#Font
font_style = pygame.font.SysFont("Arial", 30)

def message(msg, color):
    text_surface = font_style.render(msg, True, color)
    screen.blit(text_surface, [width / 6, height / 2])

#Draw the snake
def draw_snake(snake_list):
    for block in snake_list:
        pygame.draw.rect(screen, green, [block[0], block[1], snake_block, snake_block])

def game_loop():

    #Start the snake as the same grid as the food
    x = random.randrange(0, width - snake_block, snake_block)
    y = random.randrange(0, height - snake_block, snake_block)

    #The snakes stays still at the start
    x_changed = 0
    y_changed = 0

    #Create snakes's body by starting with just one block
    snake_list = []
    snake_length = 1

    #Position the food in the same grid as the snake
    foodx = random.randrange(0, width - snake_block, snake_block)
    foody = random.randrange(0, height - snake_block, snake_block)

    #Still playing
    game_over = False
    game_close = False

    while not game_over:
        
        #Game Over screen
        while game_close:
            screen.fill(black)
            message("Game Over! Press Q to Quit or C to Continue", red)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_over = True
                    game_close = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        game_loop()
                        return
         #Main event loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    x_changed = 0
                    y_changed = -snake_block
                elif event.key == pygame.K_DOWN:
                    x_changed = 0
                    y_changed = +snake_block
                elif event.key == pygame.K_RIGHT:
                    x_changed = +snake_block
                    y_changed = 0
                elif event.key == pygame.K_LEFT:
                    x_changed = -snake_block
                    y_changed = 0

        # Move snake
        x += x_changed
        y += y_changed        

        #Wall collision
        if x < 0 or x >= width or y < 0 or y >= height:
            game_close = True
        
        # Clear screen before drawing the new frame
        screen.fill(black)


        #Draw food
        pygame.draw.rect(screen, red,[foodx, foody, snake_block, snake_block])

        #Create snake head and and add it to the body
        snake_head = [x, y]
        snake_list.append(snake_head)

        #Keep correct length (remove tail when a new head is added)
        if len(snake_list) > snake_length:
            del snake_list[0]

        #Self collision
        for block in snake_list[:-1]: #(for every block except the last one which is the head)
            if block == snake_head: #(if the snake eats itself)
                game_close = True
        draw_snake(snake_list)

        #Eat the food
        if snake_head == [foodx, foody]:
            while True:
                foodx = random.randrange(0, width - snake_block, snake_block) #make the food appear anywhere starting from the beginning of the screen, stay inside the screen, and stay in the same grid as the snake on the horizontal axis
                foody = random.randrange(0, height - snake_block, snake_block) #same thing but on the vertical axis
                if [foodx, foody] not in snake_list:
                    break
            snake_length += 1
      

        pygame.display.update()
        clock.tick(snake_speed)

    pygame.quit()
    quit()

game_loop()
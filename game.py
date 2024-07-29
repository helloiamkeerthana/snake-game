import pygame
import random
import math

pygame.init()

# Define colors
white = (255, 255, 255)
black = (0, 0, 0)
red = (213, 50, 80)
green = (0, 255, 0)
blue = (50, 153, 213)

# Set up the display
dis_width = 800
dis_height = 600

dis = pygame.display.set_mode((dis_width, dis_height))
pygame.display.set_caption('Snake Game')

# Define clock and snake block size
clock = pygame.time.Clock()
snake_block = 20  # Increase snake block size
snake_speed = 8  # Decrease snake speed

# Define font styles
font_style = pygame.font.SysFont("bahnschrift", 25)
score_font = pygame.font.SysFont("comicsansms", 35)

# Initialize variables for food
foodx = 0
foody = 0
food_radius = 10  # Radius of food circle
food_color = (0, 0, 0)

# Initialize snake color variables
snake_color_timer = 0
snake_color_interval = 1000  # 1000 milliseconds = 1 second
snake_color = black  # Initial snake color

def our_snake(snake_block, snake_list):
    for i, segment in enumerate(snake_list):
        if i == 0:  # Head of the snake
            pygame.draw.circle(dis, segment[2], (segment[0] + snake_block // 2, segment[1] + snake_block // 2), snake_block // 2)
        else:  # Body segments
            pygame.draw.circle(dis, segment[2], (segment[0] + snake_block // 2, segment[1] + snake_block // 2), snake_block // 2)

def message(msg, color):
    mesg = font_style.render(msg, True, color)
    dis.blit(mesg, [dis_width / 6, dis_height / 3])

def generate_food():
    global foodx, foody, food_color
    foodx = round(random.randrange(0, dis_width - 2*food_radius) / 10.0) * 10.0
    foody = round(random.randrange(0, dis_height - 2*food_radius) / 10.0) * 10.0
    food_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

generate_food()

def is_collision(x1, y1, x2, y2, radius):
    distance = math.sqrt((x1 - x2)**2 + (y1 - y2)**2)
    if distance < radius:
        return True
    else:
        return False

def gameLoop():
    global foodx, foody, food_color, snake_color, snake_color_timer

    game_over = False
    game_close = False

    x1 = dis_width / 2
    y1 = dis_height / 2

    x1_change = 0
    y1_change = 0

    snake_List = []
    Length_of_snake = 1

    while not game_over:

        while game_close == True:
            dis.fill(blue)
            message("You Lost! Press P-Play Again or Q-Quit", red)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_p:
                        generate_food()
                        gameLoop()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x1_change = -snake_block
                    y1_change = 0
                elif event.key == pygame.K_RIGHT:
                    x1_change = snake_block
                    y1_change = 0
                elif event.key == pygame.K_UP:
                    y1_change = -snake_block
                    x1_change = 0
                elif event.key == pygame.K_DOWN:
                    y1_change = snake_block
                    x1_change = 0

        if x1 >= dis_width or x1 < 0 or y1 >= dis_height or y1 < 0:
            game_close = True
        x1 += x1_change
        y1 += y1_change
        dis.fill(blue)
        pygame.draw.circle(dis, food_color, (int(foodx) + food_radius, int(foody) + food_radius), food_radius)

        snake_Head = []
        snake_Head.append(x1)
        snake_Head.append(y1)
        snake_Head.append(snake_color)  # Head color
        snake_List.append(snake_Head)
        if len(snake_List) > Length_of_snake:
            del snake_List[0]

        for x in snake_List[:-1]:
            if x == snake_Head:
                game_close = True

        our_snake(snake_block, snake_List)
        pygame.display.update()

        # Check if snake eats food
        if is_collision(x1, y1, foodx + food_radius, foody + food_radius, snake_block):
            # Add new segment with food color
            snake_List.append([x1, y1, food_color])
            Length_of_snake += 1
            generate_food()  # Generate new food

        clock.tick(snake_speed)  # Adjust game speed

    pygame.quit()
    quit()

def main_menu():
    while True:
        dis.fill(blue)
        title_font = pygame.font.SysFont("Times New Roman", 50)
        title = title_font.render("SNAKE GAME", True, white)
        dis.blit(title, [dis_width / 3, dis_height / 3])

        play_button = pygame.Rect(dis_width / 2 - 50, dis_height / 2, 100, 50)
        pygame.draw.rect(dis, green, play_button)
        play_text = font_style.render("START", True, black)
        dis.blit(play_text, [dis_width / 2 - play_text.get_width() / 2, dis_height / 2 + (50 - play_text.get_height()) / 2])

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_button.collidepoint(event.pos):
                    gameLoop()

if __name__ == "__main__":
    main_menu()

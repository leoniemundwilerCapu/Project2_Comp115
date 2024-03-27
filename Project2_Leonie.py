import pygame
import random

# Initialize Pygame
pygame.init()

# Setting up the game window
width = 500
height = 600
screen_y = -1410
screen_change = 0
background_bmp = pygame.image.load('Images/background.bmp')
background_pos = (0, screen_y)
background = background_bmp
crab = pygame.transform.scale(pygame.image.load('Images/Crab.bmp'), (100, 60))
Brown = (165, 42, 42)
Black = (0, 0, 0)
font = pygame.font.Font('freesansbold.ttf', 16)
font_go = pygame.font.Font('freesansbold.ttf', 30)
fps = 60
timer = pygame.time.Clock()

# Game variables
crab_x = 205
crab_y = 450
platform_width = 70
platform_height = 10
platforms_lst = [[220, 580, platform_width, platform_height], [120, 480, platform_width, platform_height],
                 [320, 480, platform_width, platform_height], [220, 380, platform_width, platform_height],
                 [120, 280, platform_width, platform_height], [320, 280, platform_width, platform_height],
                 [220, 180, platform_width, platform_height], [120, 80, platform_width, platform_height],
                 [320, 80, platform_width, platform_height]]
jump = False
y_change = 0
x_change = 0
crabs_speed = 3
score = 0
high_score = 0
game_over = False
super_jump = 2
jump_last = 0

# Create the game screen
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Mr. Crab on his big adventure by Leonie")

# Function to draw the start screen
def draw_start_screen():
    screen.blit(background, background_pos)
    title = font_go.render("Mr. Crab on his big adventure", True, Black)
    description_text = font.render("Mr. Crab always wanted to come close to the stars", True, Black)
    description_text2 = font.render("therefore he got on the way to come them closer.", True, Black)
    description_text3 = font.render("Help him to get closer, by press A to go left", True, Black)
    description_text4 = font.render("and D to go right, as well as press SPACE for a super jump", True, Black)
    description_text5 = font.render("To start his adventure press W.", True, Black)
    screen.blit(title, (40, 150))
    screen.blit(description_text, (60, 200))
    screen.blit(description_text2, (65, 220))
    screen.blit(description_text3, (85, 240))
    screen.blit(description_text4, (30, 260))
    screen.blit(description_text5, (130, 280))
    screen.blit(crab, (crab_x, crab_y))

# Function to update the crab's y position
def crab_update_y(crab_y):
    global jump
    global y_change
    jump_height = 8
    gravity = 0.3
    if jump:
        y_change = -jump_height
        jump = False
    crab_y += y_change
    y_change += gravity
    return crab_y

# Function to check for collision
def check_collisions(rect_lst, j):
    global crab_x
    global crab_y
    global y_change
    for rect in rect_lst:
        if pygame.Rect(rect).colliderect((crab_x + 20, crab_y + 50, 70, 10)) and not jump and y_change > 0:
            return True
    return j

# Function to handle movement of the platforms
def update_platforms(my_lst, crab_y, change):
    global score
    if crab_y < 250 and change < 0:
        for i in range(len(my_lst)):
            my_lst[i][1] -= change
    else:
        pass
    for item in range(len(my_lst)):
        if my_lst[item][1] > 600:
            my_lst[item] = [random.randint(10, 420), random.randint(-50, -10), platform_width, platform_height]
            score += 1
    return my_lst

# Main game loop
running = True
start_screen = True
while running:
    timer.tick(fps)

    # Set the background color and draw the start screen if necessary
    if start_screen:
        draw_start_screen()
    else:
        screen.blit(background, background_pos)
        screen.blit(crab, (crab_x, crab_y))
        blocks_lst = []
        score_text = font.render('Score:' + str(score), True, Black)
        screen.blit(score_text, (410, 25))
        highscore_text = font.render('High Score:' + str(high_score), True, Black)
        screen.blit(highscore_text, (370, 5))
        super_jump_text = font.render('Super Jumps:' + str(super_jump), True, Black)
        screen.blit(super_jump_text, (370, 580))
        
        # Draw platforms
        for i in range(len(platforms_lst)):
            block = pygame.draw.rect(screen, Brown, platforms_lst[i], 0, 3)
            blocks_lst.append(block)

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if start_screen == True:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    start_screen = False
        else:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and game_over:
                    game_over = False
                    screen_y = -1410
                    screen_change = 0
                    score= 0
                    crab_x = 205
                    crab_y = 450
                    super_jump = 2
                    jump_last = 0
                    platforms_lst = [[220, 580, platform_width, platform_height], [120, 480, platform_width, platform_height], [320, 480, platform_width, platform_height], [220, 380, platform_width, platform_height], [120, 280, platform_width, platform_height], [320, 280, platform_width, platform_height], [220, 180, platform_width, platform_height], [120, 80, platform_width, platform_height], [320, 80, platform_width, platform_height]]
                if event.key == pygame.K_SPACE and not game_over and super_jump > 0:
                    super_jump -= 1
                    y_change = -12
                if event.key == pygame.K_a:
                    x_change = -crabs_speed
                if event.key == pygame.K_d:
                    x_change = crabs_speed
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_a:
                    x_change = 0
                if event.key == pygame.K_d:
                    x_change = 0

    # Check for collisions and update crab's position
    jump = check_collisions(platforms_lst, jump)
    crab_x += x_change

    if crab_y < 540:
        crab_y = crab_update_y(crab_y)
    
    else: 
        # Game over scenario
        game_over = True
        y_change = 0
        x_change = 0
        gameover_text = font_go.render('Game Over!', True, Black)
        screen.blit(gameover_text, (170, 290))
        your_score_text = font.render('Your Score:' + str(score), True, Black)
        screen.blit(your_score_text, (210, 320))
        restart_text = font.render('To restart press SPACE', True, Black)
        screen.blit(restart_text, (170, 340))

    # Update platforms
    platforms = update_platforms(platforms_lst, crab_y, y_change)

    # Ensure crab stays within the screen boundaries
    if crab_x < -30:
        crab_x = -30
    if crab_x > 430:
        crab_x = 430

    # Update high score
    if score > high_score:
        high_score = score

    # Add more super jumps as score increases
    if score - jump_last > 50:
        jump_last = score
        super_jump += 1

    # Scroll the background as score increases
    if score - screen_change > 1:
        screen_change = score
        screen_y += 1
        background_pos = (0, screen_y)

    # Check if Mr. Crab has reached space
    if screen_y == 0:
        y_change = 0
        x_change = 0
        win_text = font_go.render('Mr. Crab arrived in Space', True, Black)
        screen.blit(win_text, (75, 290))
        con_text = font.render('Congratulations!', True, Black)
        screen.blit(con_text, (200, 270))
        thank_text = font.render('Thank you for your help!', True, Black)
        screen.blit(thank_text, (170, 320))

    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()
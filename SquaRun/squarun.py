import pygame
import random

pygame.init()

screen_width = 800
screen_height = 600

black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)

floor_height = 40
ceiling_height = 40

square_size = 50
square_x = 50
square_y = screen_height - floor_height - square_size
square_speed = 10

obstacle_width = 80
obstacle_height = 20
obstacle_speed = 5
obstacles = []

score = 0

def create_obstacle():
    x = screen_width
    if random.choice([True, False]):
        y = screen_height - floor_height - obstacle_height
    else:
        y = ceiling_height
    return pygame.Rect(x, y, obstacle_width, obstacle_height)

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("SquaRun")

moving_up = False
moving_down = False

clock = pygame.time.Clock()
game_running = True
game_over = False

while game_running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_running = False
        if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
            if not moving_up and not moving_down:
                if square_y >= screen_height - square_size - floor_height:
                    moving_up = True
                elif square_y <= ceiling_height:
                    moving_down = True
        if event.type == pygame.KEYDOWN and game_over:
            if event.key == pygame.K_SPACE:
                game_over = False
                score = 0
                obstacles = []
                square_y = screen_height - floor_height - square_size

    if not game_over:
        if moving_up:
            square_y -= square_speed
            if square_y <= ceiling_height:
                square_y = ceiling_height
                moving_up = False
        elif moving_down:
            square_y += square_speed
            if square_y >= screen_height - square_size - floor_height:
                square_y = screen_height - square_size - floor_height
                moving_down = False

        new_obstacles = []
        for obstacle in obstacles:
            obstacle.x -= obstacle_speed
            if obstacle.x < -obstacle_width:
                score += 1
            else:
                new_obstacles.append(obstacle)
        
        obstacles = new_obstacles

        if len(obstacles) == 0 or obstacles[-1].x < screen_width - 200:
            new_obstacle = create_obstacle()
            
            if len(obstacles) > 0 and new_obstacle.x - obstacles[-1].x < 70:
                obstacles[-1].width += new_obstacle.width
            else:
                obstacles.append(new_obstacle)

        square_rect = pygame.Rect(square_x, square_y, square_size, square_size)
        for obstacle in obstacles:
            if square_rect.colliderect(obstacle):
                game_over = True

    screen.fill(black)

    pygame.draw.rect(screen, white, (0, screen_height - floor_height, screen_width, floor_height))
    pygame.draw.rect(screen, white, (0, 0, screen_width, ceiling_height))

    pygame.draw.rect(screen, white, (square_x, square_y, square_size, square_size))

    for obstacle in obstacles:
        pygame.draw.rect(screen, white, obstacle)

    font = pygame.font.Font(None, 36)
    score_text = font.render(f"Score: {score}", True, black)
    score_x = screen_width - score_text.get_width() - 10
    score_y = 10
    screen.blit(score_text, (score_x, score_y))

    if game_over:
        game_over_font = pygame.font.Font(None, 72)
        game_over_text = game_over_font.render("GAME OVER", True, red)
        game_over_x = screen_width // 2 - game_over_text.get_width() // 2
        game_over_y = screen_height // 2 - game_over_text.get_height() // 2
        screen.blit(game_over_text, (game_over_x, game_over_y))
        
        restart_font = pygame.font.Font(None, 36)
        restart_text = restart_font.render("Press SPACE to restart", True, white)
        restart_x = screen_width // 2 - restart_text.get_width() // 2
        restart_y = game_over_y + game_over_text.get_height() + 20
        screen.blit(restart_text, (restart_x, restart_y))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()

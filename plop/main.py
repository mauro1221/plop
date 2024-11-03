import pygame
import math
import random 

# Initialize Pygame
pygame.init()
pygame.display.set_caption("Plop!")

# Set screen dimensions
SCREEN_WIDTH = 720
SCREEN_HEIGHT = 480

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()

# Colors
WHITE = (255, 255, 255)
YELLOW = (255, 255, 50)
GOLD = (255,215,0)
BLACK = (0, 0, 0)
BLUE = (0, 0, 224)
GREEN = (0, 250, 20)
RED = (255, 10, 10)

button_surface = pygame.Surface.fill

background_surface = pygame.image.load('backgrounds/background_1a.png').convert()  # Replace with your image file
background_surface = pygame.transform.scale(background_surface, (SCREEN_WIDTH, SCREEN_HEIGHT))

# Game classes

class button:
    def __init__(self, button_xy, radius, color, text):
        self.button_xy = button_xy
        self.radius = radius
        self.color = color
        self.text = text
        

#Game Variables 

plop_button = button((SCREEN_WIDTH/1.55, SCREEN_HEIGHT/1.7 ), 80, BLUE, "Plop!")
pass_button = button((SCREEN_WIDTH/1.15, SCREEN_HEIGHT/1.3 ), 70, GOLD, "Pass")

def draw_button(button):
    pygame.draw.circle(screen, button.color , button.button_xy, button.radius)
    
    if button.color == BLUE:
        button_name = font_button.render(button.text , True, WHITE)
    else:
        button_name = font_button.render(button.text , True, BLACK)
    
    screen.blit(button_name, (button.button_xy[0]-50,button.button_xy[1]-20)) # hier kompliziert an die Werte zu kommen 

def check_click_button(mouse_pos, button):
    # Abstand zwischen Maus und Button-Mittelpunkt berechnen       
    dist_x = mouse_pos[0] - button.button_xy[0]
    dist_y = mouse_pos[1] - button.button_xy[1]
    distance = math.sqrt(dist_x**2 + dist_y**2)
                
    # Prüfen, ob der Klick innerhalb des Kreises ist
    if distance <= button.radius:
        return True 

# Fonts
font_button = pygame.font.Font("fonts/eracake.ttf", 40)
font_score = pygame.font.Font("fonts/eracake.ttf", 44)
font_dividend = pygame.font.Font("fonts/eracake.ttf", 58)
font_board = pygame.font.Font("fonts/eracake.ttf", 150)
font_answer = pygame.font.Font("fonts/Starshines.ttf", 80)
font_inst = pygame.font.Font(None, 36)
font_inst_bold = pygame.font.Font(None, 38)

class board:
    def __init__(self, number, color, font):
        self.number = number
        self.color = color
        self.font = font
        
def draw_board(board):
    number = board.number
    board_show = font_board.render(f"{number} ", True, board.color)
    screen.blit(board_show, (100 , 170))

def board_set_color(board, color):
    board.color = color
    

show_text = False
start_time = 0
text_duration = 1000  # Zeit in Millisekunden (2 Sekunden)
fade_in_duration = 500  # Dauer des Fade-In (0,5 Sekunde)
text = ""
text_color = GREEN

# Funktion, um den Text anzuzeigen
def display_text_effect(text, color, duration=800):
    global show_text, start_time, text_color
    show_text = True
    start_time = pygame.time.get_ticks()
    text_color = color
    return text, duration


# Game loop
def game():
    
    global show_text, scaled_text
    score = 0
    number = random.randint(3,50)
    dividend = 3
    counter = 0
    
    #screen.blit(background_surface, (0, 0)) 
    running = True
    game_over = False
    
    while running:
        #screen.fill(WHITE) 
        
        board1 = board(number, RED, font_score)

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE or event.type == pygame.QUIT:
                running = False
                
            if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
                if event.button == 1:  # Linke Maustaste
                    if check_click_button(pygame.mouse.get_pos(), plop_button):
                        if number % dividend == 0:
                            score +=3
                            text, text_duration = display_text_effect("Right!", GREEN)
                            counter +=1
                        else:
                            score -=2
                            text, text_duration = display_text_effect("Wrong!", RED)
                        number += 1
                        
                    if check_click_button(pygame.mouse.get_pos(), pass_button):
                        if number % dividend != 0:
                            score +=1
                            text, text_duration = display_text_effect("Right!", GREEN)
                            counter +=1
                        else:
                            score -=2
                            text, text_duration = display_text_effect("Wrong!", RED)
                        number += 1

        if counter >= 7 :
            counter = 0 
            dividend = random.randint(3,17)
            number = number + random.randint(3, 99)
        
        if not game_over:
            # Draw background first
            #screen.fill(WHITE)
            screen.blit(background_surface, (0, 0)) 
            # Draw score
            score_text = font_dividend.render(f"Score: {score}", True, BLUE)
            screen.blit(score_text, ((SCREEN_WIDTH/2)-100 , 30))
            # Draw dividend
            
            dividend_text = font_dividend.render(f"dividend: {dividend}", True, BLUE)
            screen.blit(dividend_text, (50 , 400))      
            
            #score_text = font_score.render(f"Highscore: ", True, BLUE)
            #screen.blit(score_text, (SCREEN_WIDTH - 180 , 30))

            #Draw board
            draw_board(board1)

            #Draw buttons 
            draw_button(plop_button)
            draw_button(pass_button)
            
            
            # Text anzeigen, wenn er aktiv ist
            if show_text:
        
                elapsed_time = pygame.time.get_ticks() - start_time
        
             # Fade-In- und Scale-Effekt
                if elapsed_time < fade_in_duration:
                    alpha = int(255 * (elapsed_time / fade_in_duration))  # Transparenz
                    scale_factor = 1 + 0.5 * (elapsed_time / fade_in_duration)  # Skalierung
                else:
                    alpha = 255
                    scale_factor = 1.5  # Endgröße für den Effekt
        
                # Text rendern mit Skalierung und Transparenz
                rendered_text = font_answer.render(text, True, text_color)
                rendered_text.set_alpha(alpha)
                scaled_text = pygame.transform.scale(rendered_text, (int(rendered_text.get_width() * scale_factor), int(rendered_text.get_height() * scale_factor)))
        
            # Text auf den Bildschirm zentrieren
                screen.blit(scaled_text, (300 - scaled_text.get_width() // 2, 150 - scaled_text.get_height() // 2))
        
            # Text entfernen, wenn die Anzeigezeit abgelaufen ist
                if elapsed_time > text_duration:
                    show_text = False
            else:
                scaled_text = None

            #check for highscore
            #update_highscore(score)

        #if game_over:
            
            #display_game_over()

        # Update display and set frame rate
        pygame.display.update()
        #clock.tick(60)

    #pygame.quit()

# Start game after pressing Enter
def main_menu():
    screen.fill(GREEN)
    #screen.blit(start_text ,(0, 0))
    start_text = font_inst.render("Press ENTER to Start", True, BLUE)
    screen.blit(start_text, (SCREEN_WIDTH // 2 - 120, SCREEN_HEIGHT // 2 - 20))
    pygame.display.update()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE or event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                waiting = False
                pass

# Start the game
main_menu()  # Show the start menu
game()  # Start the game loop after pressing Enter
# Ideen: 


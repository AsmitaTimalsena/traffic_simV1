import pygame
import sys


pygame.init()


# Screen dimensions
screen_width = 1280  
screen_height = 800


# Create the screen
screen = pygame.display.set_mode((screen_width, screen_height))


background_image = pygame.image.load("dedicated_laneIMG.png")


background_image = pygame.transform.scale(background_image, (screen_width, screen_height))


pygame.display.set_caption("Pygame with Background Image")


oval_coordinates = [
    #north road
    (760, 0), (795,0),
    (680, 0), (850, 0),
    #north road
    (680, 690), (760, 690),
    # East road 
    #Ease Movement(path A) for bus
    (845, 470),(880, 470), 
    #East Movement, (path B)left turn  for bike
    (880, 530),(800, 470),(800, 530),
    # West road
    (400, 590), (400, 650),
    
    #Traffic lights
    #east road
    (905, 420),(935, 420), 
    #south road 
     (825, 710),(855, 710),
     #west road
     (425, 710),(455, 710),
     #north road
     (345, 420),(375, 420)
     
]


oval_width, oval_height = 20, 20  
oval_color = (255, 0, 0)  


# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False


    screen.blit(background_image, (0, 0))


    for x, y in oval_coordinates:
        pygame.draw.ellipse(screen, oval_color, (x - oval_width // 2, y - oval_height // 2, oval_width, oval_height))


    pygame.display.flip()


pygame.quit()
sys.exit()




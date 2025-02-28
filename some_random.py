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
    # # #north road
    # # (760, 0), (795,0),
    # # (680, 0), (850, 0),
    # # #south road
    # # (680, 690), (760, 690),
    # # # East road
    # # (880, 470), (880, 530),
    # #  # West road
    # # (400, 590), (400, 650),




    # # #Traffic lights
    # # #north road
    # # (760,420),(680,420),
    # # #East road
    # # (880, 590),
    # # (1280,590), (1280,650),
    # # #South road
    # # (600, 690),
    # # #West road
    # # (400, 520), 

    # # (0,520),(0,620),
    # # (760,0),(800,0), 
    # # (680,0),(850,0),
    # # (520,790),(600,790), (520,520), (600,480),
    # # (600,540),

    # (1280,590), (1280,650),(750,660),(530,590), (600,590),
    # # West road
    # # (0,520),(0,620),
    # # (440,520),(490,520),
    # # (680,620),
    # # (590,590),
    # (700,600),(720,530),
    (680,620),(680,530), 
    
   
# (680,530),
#     (1280,650),(530,590),
#     (845,470), (520,640),




#     # #north road
#  "motorcycle_lanes": [760, 795],  # x positions for motorcycle lanes going south
#         "car_lanes": [680, 850],    



    # #east road
    # (905, 420),(935, 420),
    # #south road
    #  (825, 710),(855, 710),
    #  #west road
    #  (425, 710),(455, 710),
    #  #north road
    #  (345, 420),(375, 420)
     
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



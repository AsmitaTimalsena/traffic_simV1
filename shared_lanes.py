import pygame 
import random

pygame.init()

width, height = 300, 700
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Shared lanes vehicle simulation')

WHITE = (255, 255, 255)
BLUE = (0, 0, 100)
YELLOW = (255, 255, 0)

# Speed conversion , here we used logic(1 pixel = 5 meters, 60 FPS)
FPS = 60
METERS_PER_PIXEL = 5  

#speed ranges in km/h
BIKE_SPEED_KMH = random.randint(35, 40)  
CAR_SPEED_KMH = random.randint(30, 35)   

BIKE_SPEED_PIXELS = (BIKE_SPEED_KMH * 1000) / (60 * 60 * METERS_PER_PIXEL)
CAR_SPEED_PIXELS = (CAR_SPEED_KMH * 1000) / (60 * 60 * METERS_PER_PIXEL)

lanes = [45, 120, 180, 240]
SEPARATION_DISTANCE = 70
LANE_CHANGE_DISTANCE = 120
OVERTAKE_DISTANCE = 50  


total_vehicles_passed = 0

class Vehicle:
    def __init__(self, x, y, lane, vtype):
        self.x = x
        self.y = y
        self.lane = lane
        self.vtype = vtype
        
        self.speed = (random.randint(35, 40) if vtype == "bike" else random.randint(30, 35)) * 1000 / (60 * 60 * METERS_PER_PIXEL)
        
        if vtype == "car":
            self.width = random.randint(18, 22)
            self.height = random.randint(30, 32)
        else:
            self.width = random.randint(12, 15)
            self.height = random.randint(25, 30)
        
        self.target_lane = self.lane
        self.lane_change_progress = 1

    def draw(self, screen):
        if self.vtype == "car":
            pygame.draw.rect(screen, WHITE, (self.x, self.y, self.width, self.height))
        else:
            pygame.draw.ellipse(screen, YELLOW, (self.x, self.y, self.width, self.height))

    def move(self):
        if self.lane_change_progress < 1:
            self.x += (self.target_lane - self.x) * 0.1
            if abs(self.x - self.target_lane) < 1:
                self.x = self.target_lane
                self.lane = self.target_lane
                self.lane_change_progress = 1
        self.y += self.speed

    def adjust_speed(self, vehicles):
        for other in vehicles:
            if other != self and other.lane == self.lane:
                distance = other.y - self.y
                if 0 < distance < SEPARATION_DISTANCE:
                    self.speed = max(self.speed * 0.5, 1)
                    return
                elif 0 < distance < LANE_CHANGE_DISTANCE:
                    self.speed = max(self.speed * 0.8, 1)
                    return
        self.speed = (random.randint(35, 40) if self.vtype == "bike" else random.randint(30, 35)) * 1000 / (60 * 60 * METERS_PER_PIXEL)

    def attempt_lane_change(self, vehicles):
        if self.vtype != "bike":
            return  
        
        for other in vehicles:
            if other != self and other.lane == self.lane:
                distance = other.y - self.y
                if 0 < distance < OVERTAKE_DISTANCE:
                    random.shuffle(lanes)  # Shuffle lanes to avoid biased selection
                    for target_lane in lanes:
                        if target_lane != self.lane and self.can_change_lane(vehicles, target_lane):
                            self.target_lane = target_lane
                            self.lane_change_progress = 0
                            return
                    self.speed = max(self.speed * 0.5, 1)
                    return
    
    def can_change_lane(self, vehicles, target_lane):
        for other in vehicles:
            if other.lane == target_lane and abs(other.y - self.y) < SEPARATION_DISTANCE:
                return False  
        return True

vehicles = []
for i in range(10):
    lane = random.choice(lanes)
    vtype = random.choices(["bike", "car"], weights=[65, 35])[0]
    x = lane
    y = random.randint(-height, 0)
    vehicles.append(Vehicle(x, y, lane, vtype))

running = True
clock = pygame.time.Clock()
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(BLUE)
    dash_length = 20
    gap_length = 10
    start_x = 150

    for y in range(0, height, dash_length + gap_length):
        pygame.draw.line(screen, WHITE, (start_x, y), (start_x, y + dash_length), 2)

    for vehicle in vehicles:
        vehicle.adjust_speed(vehicles)
        vehicle.attempt_lane_change(vehicles)
        vehicle.move()
        if vehicle.y > height:
            vehicle.y = random.randint(-height, 0)
            total_vehicles_passed += 1
        vehicle.draw(screen)

    font = pygame.font.Font(None, 28)
    text = font.render(f"Vehicles Passed: {total_vehicles_passed}", True, WHITE)
    screen.blit(text, (10, 10))
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()

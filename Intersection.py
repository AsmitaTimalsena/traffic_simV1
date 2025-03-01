import pygame
import random
import math
import sys

pygame.init()

screen_width = 1280
screen_height = 800
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Multi-Lane Vehicle Simulation")

# Colors
WHITE = (255, 255, 255)
BLUE = (0, 0, 100)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

background_image = pygame.image.load("dedicated_laneIMG.png")
background_image = pygame.transform.scale(
    background_image, (screen_width, screen_height)
)

total_vehicles_passed = 0

dedicated_passed_south = 0
shared_passed_south = 0

dedicated_lanes = {"North-Car-Outer", "North-Bike-Middle"}


motorcycle_safe_threshold = 50
car_safe_threshold = 100
max_vehicles_per_lane = 5


directions_data = {
    # Top approach traveling downward
    "S": {"traffic_lights": [(760, 420), (680, 420)], "stop_line_y": 415},
    # Right approach traveling left
    "W": {"traffic_lights": [(880, 590)], "stop_line_x": 875},
    # Bottom approach traveling upward
    "N": {"traffic_lights": [(600, 690)], "stop_line_y": 670},
    # Left approach traveling right
    "E": {"traffic_lights": [(400, 600)], "stop_line_x": 405},
}

# Initialize for drawing the traffic lights
dash_colors = {}
for direction, ddata in directions_data.items():
    for coord in ddata["traffic_lights"]:
        dash_colors[coord] = RED


direction_order = ["N", "W", "S", "E"]
direction_index = 0

light_state = "green"
light_state_start = pygame.time.get_ticks()

light_durations = {
    "green": 13000,
    "orange": 2000,
    "allred": 2000,
    "green_west": 13000,
    "orange_west": 2000,
    "green_east": 6000,
    "orange_east": 3000,  
}


def get_light_color_for_direction(dir_name):
    """Return the color for the given direction depending on the current state."""
    if light_state == "allred":
        return RED
    active_direction = direction_order[direction_index]
    if dir_name == active_direction:
        if dir_name == "W":
            return GREEN if light_state == "green_west" else ORANGE
        elif dir_name == "E":
            return GREEN if light_state == "green_east" else ORANGE 
        else:
            return GREEN if light_state == "green" else ORANGE
    else:
        return RED

def is_direction_green(dir_name):
    """Return True if this direction is currently green/orange, otherwise False."""
    if light_state == "allred":
        return False
    active_direction = direction_order[direction_index]
    if dir_name == active_direction:
        if dir_name == "W":
            return light_state in ["green_west"]
        elif dir_name == "E":
            return light_state in ["green_east"]  
        else:
            return light_state in ["green"]
    else:
        return False


lanes_data = [
    # NORTH ROAD (travel_dir = "S")
    {
        "name": "North-Bike-Middle",
        "spawn": (800, 0),
        "vehicle_types": ["bike"],
        "travel_dir": "S",
        "stop_for_red": False,
        "max_vehicles": 9,
        "possible_paths": [
            [
                {
                    "trigger_point": (800, 510),
                    "action": "turn_left",  # S->E
                    "new_direction": "E",
                }
            ]
        ],
    },
    {
        "name": "North-Car-Outer",
        "spawn": (850, 0),
        "vehicle_types": ["car"],
        "travel_dir": "S",
        "stop_for_red": False,
        "max_vehicles": 4,
        "possible_paths": [
            [
                {
                    "trigger_point": (845, 470),
                    "action": "turn_left",  # S->E
                    "new_direction": "E",
                }
            ]
        ],
    },
    {
        "name": "North-Lane-3",
        "spawn": (755, 0),
        "vehicle_types": ["bike"],
        "travel_dir": "S",
        "stop_for_red": True,
        "max_vehicles": 8,
        "possible_paths": [
            [],  # Straight
        ],
    },
    {
        "name": "North-Lane-4",
        "spawn": (680, 0),
        "vehicle_types": ["car"],
        "travel_dir": "S",
        "stop_for_red": True,
        "max_vehicles": 5,
        "possible_paths": [
            [],
        ],
    },
    # SOUTH ROAD
    {
        "name": "South-Branching-Lane",
        "spawn": (515, 790),
        "vehicle_types": ["car", "bike"],
        "travel_dir": "N",
        "stop_for_red": False,
        "max_vehicles": 3,
        "possible_paths": [
            [{"trigger_point": (515, 520), "action": "branch", "new_direction": "N"}]
        ],
    },
    {
        "name": "South-Lane-StopForRed",
        "spawn": (600, 790),
        "vehicle_types": ["car", "bike"],
        "travel_dir": "N",
        "stop_for_red": True,
        "max_vehicles": 2,
        "possible_paths": [
            [
                {
                    "trigger_point": (600, 540),
                    "action": "turn_right",  # N->E
                    "new_direction": "E",
                }
            ]
        ],
    },
    # EAST ROAD
    {
        "name": "East-NoStop",
        "spawn": (1280, 650),
        "vehicle_types": ["car", "bike"],
        "travel_dir": "W",
        "stop_for_red": False,
        "max_vehicles": 6,  # Shorter lane
        "possible_paths": [
            [
                {
                    "trigger_point": (770, 650),
                    "action": "turn_left",  # W->S
                    "new_direction": "S",
                }
            ],
        ],
    },
    {
        "name": "East-StopThenBranch",
        "spawn": (1280, 590),
        "vehicle_types": ["car", "bike"],
        "travel_dir": "W",
        "stop_for_red": True,
        "max_vehicles": 5,  # Standard lane
        "possible_paths": [
            [
                {
                    "trigger_point": (625, 590),
                    "action": "branch_east",
                    "new_direction": "N",
                }
            ],
        ],
    },
    # WEST ROAD
    {
        "name": "West-LeftTurn",
        "spawn": (0, 520),
        "vehicle_types": ["car", "bike"],
        "travel_dir": "E",
        "stop_for_red": False,
        "max_vehicles": 6,
        "possible_paths": [
            [
                {
                    "trigger_point": (440, 520),
                    "action": "turn_left",  
                    "new_direction": "N",
                }
            ]
        ],
    },
    {
        "name": "West-StopThenMultiTurn",
        "spawn": (0, 600),
        "vehicle_types": ["car", "bike"],
        "travel_dir": "E",
        "stop_for_red": True,
        "max_vehicles": 6,
        "possible_paths": [
            [
                {
                    "trigger_point": (680, 600),
                    "action": "turn_right",  # E->S
                    "new_direction": "S",
                }
            ],
            [
                {
                    "trigger_point": (720, 600),
                    "action": "move_west_to_east",
                    "new_direction": "E",
                }
            ],
        ],
    },
]

##PER LANE TIMER AND data stracture
lane_vehicles_map = {}


def get_new_event_id():
    get_new_event_id.counter += 1
    return pygame.USEREVENT + get_new_event_id.counter


get_new_event_id.counter = 0

timers = []
for lane_def in lanes_data:
    lane_name = lane_def["name"]
    lane_vehicles_map[lane_name] = []
    for vtype in lane_def["vehicle_types"]:
        event_id = get_new_event_id()
        # Adjust spawn intervals if needed
        spawn_interval = 2300 if vtype == "bike" else 2500
        pygame.time.set_timer(event_id, spawn_interval)
        timers.append((event_id, lane_name, vtype))


# defining the directions/angles
def angle_for_dir(direction):
    """Return angle for direction: 0=S, 90=W, 180=N, 270=E."""
    if direction == "N":
        return 180
    elif direction == "S":
        return 0
    elif direction == "E":
        return 270
    elif direction == "W":
        return 90
    return 0


def move_coords(x, y, speed, direction):
    if direction == "N":
        return x, y - speed
    elif direction == "S":
        return x, y + speed
    elif direction == "E":
        return x + speed, y
    elif direction == "W":
        return x - speed, y
    return x, y


def distance_in_travel_dir(pos1, pos2, direction):
    """
    for distance calculation and collison avoidance
    """
    x1, y1 = pos1
    x2, y2 = pos2
    if direction == "S":
        return y2 - y1
    elif direction == "N":
        return y1 - y2
    elif direction == "E":
        return x2 - x1
    elif direction == "W":
        return x1 - x2
    return 999999


class Vehicle:
    
    def __init__(self, lane_def, vehicle_type, turn_instructions):
        global screen_width, screen_height

        self.lane_def = lane_def
        self.vehicle_type = vehicle_type

        # Current direction (N,S,E,W)
        self.direction = lane_def["travel_dir"]
        self.stop_for_red = lane_def["stop_for_red"]

        # The instructions that define this vehicle’s route (picked randomly).
        self.turn_instructions = turn_instructions

        # Initial position
        self.x, self.y = lane_def["spawn"]

        # Random scaling factor for vehicle size
        size_scale = random.uniform(0.8, 1.2)  # Random scaling between 80% and 120%

        if vehicle_type == "bike":
            self.width = int(10 * size_scale)  # Random width between 8 and 12
            self.height = int(25 * size_scale)  # Random height between 20 and 30
            self.max_speed = 2.5
        else:
            self.width = int(20 * size_scale)  # Random width between 16 and 24
            self.height = int(40 * size_scale)  # Random height between 32 and 48
            self.max_speed = 2.0

        self.speed = random.uniform(self.max_speed * 0.8, self.max_speed)
        self.angle = angle_for_dir(self.direction)
        self.turn_index = 0
        self.has_been_counted = False

    def yield_for_left_turn(self, all_vehicles):
        """
        If the next action is a left turn, yield to the traffic on the right
        if they have green/orange. This is an example logic.
        """
        if self.turn_index >= len(self.turn_instructions):
            return  # no turns => do nothing

        instr = self.turn_instructions[self.turn_index]
        if instr["action"] != "turn_left":
            return  # only yield on left turns

        # Mapping to find which direction is on your right:
        dir_to_right = {"N": "W", "E": "N", "S": "E", "W": "S"}
        right_side_dir = dir_to_right[self.direction]

        # Check if we are close enough to the turn point to consider yielding
        trigger_x, trigger_y = instr["trigger_point"]
        dist_to_trigger = math.hypot(self.x - trigger_x, self.y - trigger_y)

        if dist_to_trigger < 30:
            # If the road to your right has green/orange, yield if conflict
            if is_direction_green(right_side_dir):
                conflict_found = False
                for other in all_vehicles:
                    if other is self:
                        continue
                    d = math.hypot(self.x - other.x, self.y - other.y)
                    if d < 60:
                        self.speed = 0
                        conflict_found = True
                        break
                if not conflict_found:
                    self.speed = min(self.speed + 0.2, self.max_speed)
            else:
                # If the road to your right is red, just go/accelerate
                self.speed = min(self.speed + 0.2, self.max_speed)

    def move_and_collide(self, lane_vehicles, all_vehicles):
        global total_vehicles_passed
        global dedicated_passed_south, shared_passed_south

        # logic for south directional lane (520, 790)
        if self.lane_def["name"] == "South-Branching-Lane":
            west_light_color = get_light_color_for_direction("E")

            # If west has green or orange (is_direction_green includes both states)
            if get_light_color_for_direction("E") in [GREEN, ORANGE]:
                dist_to_stop = math.hypot(self.x - 520, self.y - 690)

                # If we're approaching the stop point, gradually slow down
                if dist_to_stop < 50 and self.y < 690:
                    self.speed = max(self.speed - 0.4, 0)
                    return False  # Don't remove the vehicle
                # If we're exactly at y=690, stop completely
                elif (
                    abs(self.y - 690) < 1
                ):  # Using small threshold for floating point comparison
                    self.speed = 0
                    self.y = 690
                    return False
                # If we're past y=690, continue moving normally
                elif self.y > 690:
                    self.speed = min(self.speed + 0.2, self.max_speed)
            else:
                # If west has green/orange, resume normal speed
                self.speed = min(self.speed + 0.2, self.max_speed)

        # 1) Handle red/stop line if needed
        if self.stop_for_red:
            # figure out the stop line
            dir_config = directions_data.get(self.direction, {})
            if self.direction in ("N", "S"):
                stop_line = dir_config.get("stop_line_y", None)
            else:
                stop_line = dir_config.get("stop_line_x", None)

            if stop_line is not None:
                dist_to_stop = self.distance_to_stop_line(stop_line)
                # If we haven't crossed the stop line and the light is not green/orange => slow/stop
                if dist_to_stop > 0 and not is_direction_green(self.direction):
                    if dist_to_stop < 50:
                        self.speed = max(self.speed - 0.4, 0)
                    else:
                        self.speed = min(self.speed + 0.2, self.max_speed)
                else:
                    # either already past line or we have green/orange
                    self.speed = min(self.speed + 0.2, self.max_speed)
            else:
                # no stop line => do normal
                self.speed = min(self.speed + 0.2, self.max_speed)
        else:
            # This lane ignores red
            self.speed = min(self.speed + 0.2, self.max_speed)

        # 2) Keep safe distance from vehicle ahead in the same lane
        safe_threshold = (
            motorcycle_safe_threshold
            if self.vehicle_type == "bike"
            else car_safe_threshold
        )
        closest_dist = float("inf")
        closest_speed = None

        for other in lane_vehicles:
            if other is self:
                continue
            d = distance_in_travel_dir(
                (self.x, self.y), (other.x, other.y), self.direction
            )
            if 0 < d < closest_dist:
                closest_dist = d
                closest_speed = other.speed

        if closest_dist < safe_threshold:
            if closest_speed is not None:
                self.speed = min(self.speed, closest_speed - 0.5)
            if self.speed < 0:
                self.speed = 0

        # 3) Check for left-turn yield
        self.yield_for_left_turn(all_vehicles)

        # 4) Check turn instructions
        self.check_turn_instructions()

        # 5) Move
        self.x, self.y = move_coords(self.x, self.y, self.speed, self.direction)

        # 6) If off-screen, remove & increment counters
        if (
            self.x < -50
            or self.x > screen_width + 50
            or self.y < -50
            or self.y > screen_height + 50
        ):
            if not self.has_been_counted:
                total_vehicles_passed += 1
                self.has_been_counted = True

                if self.lane_def["travel_dir"] == "S":
                    if self.lane_def["name"] in dedicated_lanes:
                        dedicated_passed_south += 1
                    else:
                        shared_passed_south += 1

            return True
        return False

    def distance_to_stop_line(self, stop_line):
        half_len = (
            (self.height / 2) if self.direction in ("N", "S") else (self.width / 2)
        )

        if self.direction == "S":
            return stop_line - (self.y + half_len)
        elif self.direction == "N":
            return self.y - half_len - stop_line
        elif self.direction == "E":
            return stop_line - (self.x + half_len)
        elif self.direction == "W":
            return self.x - half_len - stop_line
        return 9999

    def check_turn_instructions(self):
        if self.turn_index >= len(self.turn_instructions):
            return

        instr = self.turn_instructions[self.turn_index]
        tx, ty = instr["trigger_point"]
        dist = math.hypot(self.x - tx, self.y - ty)
        if dist < 15:
            action = instr["action"]
            if action == "turn_left":
                self.turn_left(instr["new_direction"])
            elif action == "turn_right":
                self.turn_right(instr["new_direction"])
            elif action == "move_up":
                self.move_up(instr["new_direction"])
            elif action == "branch":
                self.branch(instr["new_direction"])
            elif action == "branch_east":
                self.branch_east(instr["new_direction"])
            elif action == "move_west_to_east":
                self.move_west_to_east(instr["new_direction"])
            elif action == "move_east":
                self.move_east(instr["new_direction"])
            elif action == "turn_straight_east":
                self.turn_straight_east(instr["new_direction"])

            self.turn_index += 1

    def move_east(self, new_dir):
        """
        Move the vehicle east to (700, 600).
        """
        if self.x < 700:
            self.x += self.speed  # Move east
        else:
            pass

    def turn_straight_east(self, new_dir):
        """
        Move the vehicle straight east to (720, 530).
        """
        if self.y > 530:
            self.y -= self.speed
        else:
            self.direction = new_dir
            self.angle = angle_for_dir(new_dir)

    def move_up(self, new_dir):
        """
        Move the vehicle up to (680, 550) before turning left.
        """
        if self.y > 550:
            self.y -= self.speed
        else:
            # Once the vehicle reaches (680, 550), turn left
            self.turn_left(new_dir)

    def branch(self, new_dir):
        instr = self.turn_instructions[self.turn_index]
        tx, ty = instr["trigger_point"]
        self.x, self.y = tx, ty
        if self.vehicle_type == "bike":
            self.x, self.y = 510, 480
        elif self.vehicle_type == "car":
            self.x, self.y = 575, 480
        self.direction = new_dir
        self.angle = angle_for_dir(new_dir)

    def move_west_to_east(self, new_dir):
        instr = self.turn_instructions[self.turn_index]
        self.x, self.y = instr["trigger_point"]
        self.x, self.y = 680, 540
        self.direction = new_dir
        self.angle = angle_for_dir(new_dir)

    def branch_east(self, new_dir):
        instr = self.turn_instructions[self.turn_index]
        tx, ty = instr["trigger_point"]
        self.x, self.y = tx, ty

        if self.vehicle_type == "bike":
            self.x, self.y = 538, 590
        elif self.vehicle_type == "car":
            self.x, self.y = 600, 590

        # Rotate to goo north
        self.direction = new_dir
        self.angle = angle_for_dir(new_dir)

    def turn_left(self, new_dir):
        instr = self.turn_instructions[self.turn_index]
        tx, ty = instr["trigger_point"]
        self.x, self.y = tx, ty
        if self.vehicle_type == "bike" and self.x == 440 and self.y == 520:
            self.x, self.y = 480, 520
        self.direction = new_dir
        self.angle = angle_for_dir(new_dir)

    def turn_right(self, new_dir):
        instr = self.turn_instructions[self.turn_index]
        tx, ty = instr["trigger_point"]
        self.x, self.y = tx, ty
        self.direction = new_dir
        self.angle = angle_for_dir(new_dir)

    def draw(self, surface):
        vehicle_surf = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        if self.vehicle_type == "bike":
            pygame.draw.ellipse(vehicle_surf, YELLOW, (0, 0, self.width, self.height))
        else:
            pygame.draw.rect(vehicle_surf, WHITE, (0, 0, self.width, self.height))
        rotated_surf = pygame.transform.rotate(vehicle_surf, -self.angle)
        rect = rotated_surf.get_rect(center=(self.x, self.y))
        surface.blit(rotated_surf, rect)


clock = pygame.time.Clock()
running = True
all_vehicles = []

while running:
    dt = clock.tick(60)
    current_time = pygame.time.get_ticks()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        for ev_id, lane_name, vtype in timers:
            if event.type == ev_id:
                lane_def = None
                for ld in lanes_data:
                    if ld["name"] == lane_name:
                        lane_def = ld
                        break
                if not lane_def:
                    continue

                lane_list = lane_vehicles_map[lane_name]
                if len(lane_list) < lane_def.get(
                    "max_vehicles", 5
                ):  # if none specified assume to be 5
                    chosen_path = random.choice(lane_def["possible_paths"])
                    # Create a new vehicle with that path
                    newv = Vehicle(lane_def, vtype, chosen_path)
                    lane_list.append(newv)
                    all_vehicles.append(newv)

    # 2) Update traffic-light cycle
    elapsed_light = current_time - light_state_start
    if elapsed_light > light_durations[light_state]:
        # Move to the next state
        if light_state == "green":
            light_state = "orange"
        elif light_state == "orange":
            light_state = "allred"
        elif light_state == "allred":
            # Was allred => move to next direction's green
            direction_index = (direction_index + 1) % len(direction_order)
            if direction_order[direction_index] == "W":
                light_state = "green_west"
            elif direction_order[direction_index] == "E":
                light_state = "green_east"  # Transition to green_east for east lane
            else:
                light_state = "green"
        elif light_state == "green_west":
            light_state = "orange_west"
        elif light_state == "orange_west":
            light_state = "allred"
        elif light_state == "green_east":
            light_state = "orange_east"  # Transition to orange_east for east lane
        elif light_state == "orange_east":
            light_state = "allred"
        light_state_start = current_time

    # 3) Update traffic lights
    for direction, ddata in directions_data.items():
        color = get_light_color_for_direction(direction)
        for coord in ddata["traffic_lights"]:
            dash_colors[coord] = color

    screen.blit(background_image, (0, 0))

    dash_length = 20
    dash_thickness = 5
    for direction, ddata in directions_data.items():
        for lx, ly in ddata["traffic_lights"]:
            color = dash_colors.get((lx, ly), RED)
            if direction in ("N", "S"):  # horizontal dash draw
                pygame.draw.line(
                    screen,
                    color,
                    (lx - dash_length // 2, ly),
                    (lx + dash_length // 2, ly),
                    dash_thickness,
                )
            else:  # E, W => draw a vertical dash
                pygame.draw.line(
                    screen,
                    color,
                    (lx, ly - dash_length // 2),
                    (lx, ly + dash_length // 2),
                    dash_thickness,
                )

    # Show which direction is active
    font = pygame.font.SysFont(None, 24)
    # active_dir = direction_order[direction_index]
    # info_txt = f"Active: {active_dir} [{light_state.upper()}]"
    # info_surf = font.render(info_txt, True, (255, 255, 255))
    # screen.blit(info_surf, (20, 20))

    # 6) Update & draw vehicles
    to_remove = []
    for v in all_vehicles:
        lane_name = v.lane_def["name"]
        lane_list = lane_vehicles_map[lane_name]
        remove_it = v.move_and_collide(lane_list, all_vehicles)
        v.draw(screen)
        if remove_it:
            to_remove.append(v)

    # Remove off-screen vehicles
    for remv in to_remove:
        all_vehicles.remove(remv)
        lane_vehicles_map[remv.lane_def["name"]].remove(remv)

    # 7) Show total passed
    txt = font.render(
        f"Total Vehicles Passed: {total_vehicles_passed}", True, (255, 255, 255)
    )
    screen.blit(txt, (100, 100))

    text_n = font.render("N", True, (255, 255, 255))
    screen.blit(text_n, (370, 100))

    text_n = font.render("W", True, (255, 255, 255))
    screen.blit(text_n, (100, 700))

    text_n = font.render("S", True, (255, 255, 255))
    screen.blit(text_n, (820, 730))

    text_n = font.render("E", True, (255, 255, 255))
    screen.blit(text_n, (1110, 390))

    # # Show dedicated vs shared lanes rate (for vehicles that came from North -> South)
    # dedicated_txt = font.render(f"DEDICATED LANES RATE: {dedicated_passed_south}", True, (255,255,255))
    # screen.blit(dedicated_txt, (20, 80))

    # shared_txt = font.render(f"SHARED LANES RATE: {shared_passed_south}", True, (255,255,255))
    # screen.blit(shared_txt, (20, 110))

    pygame.display.flip()

pygame.quit()
sys.exit()

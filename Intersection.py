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

# Background image (replace with your intersection image if desired)
background_image = pygame.image.load("dedicated_laneIMG.png")
background_image = pygame.transform.scale(background_image, (screen_width, screen_height))

# Global counters
total_vehicles_passed = 0

# Additional counters for lanes that start from the North (travel_dir="S")
# We'll define which lanes are "dedicated" vs. "shared."
dedicated_passed_south = 0
shared_passed_south = 0

# Decide which lane names are considered "dedicated" if traveling south
dedicated_lanes = {"North-Car-Outer", "North-Bike-Middle"}
# The rest that travel south are considered "shared."

motorcycle_safe_threshold = 50
car_safe_threshold = 180
max_vehicles_per_lane = 15  # Just an example

#############################################################################
# TRAFFIC LIGHT DATA
#############################################################################
directions_data = {
    # Top approach traveling downward
    "S": {
        "traffic_lights": [(760, 420), (680, 420)],  # purely visual
        "stop_line_y": 415
    },
    # Right approach traveling left
    "W": {
        "traffic_lights": [(880, 590)],
        "stop_line_x": 875
    },
    # Bottom approach traveling upward
    "N": {
        "traffic_lights": [(600, 690)],
        "stop_line_y": 695
    },
    # Left approach traveling right
    "E": {
        "traffic_lights": [(400, 600)],
        "stop_line_x": 405
    }
}

# Initialize the dash_colors (for drawing the traffic lights).
dash_colors = {}
for direction, ddata in directions_data.items():
    for coord in ddata["traffic_lights"]:
        dash_colors[coord] = RED

#############################################################################
# TRAFFIC LIGHT CYCLE
#############################################################################
direction_order = ["N", "W", "S", "E"]  # cycle order
direction_index = 0  # starts with "S"

light_state = "green"
light_state_start = pygame.time.get_ticks()

light_durations = {
    "green": 13000,   # 7 seconds
    "orange": 2000,  # 2 seconds
    "allred": 1000,  # 1 seconds of all-red
    "green_west": 6000,  # 6 seconds for green (West)
    "orange_west": 2000 
}

def get_light_color_for_direction(dir_name):
    """Return the color for the given direction depending on the current state."""
    if light_state == "allred":
        return RED
    active_direction = direction_order[direction_index]
    if dir_name == active_direction:
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
            return light_state in ["green_west", "orange_west"]
        else:
            return light_state in ["green", "orange"]
    else:
        return False

#############################################################################
# LANE DEFINITIONS
#############################################################################
# We add a new key: "possible_paths". Each is a list of possible sets of
# turn_instructions. We pick one randomly at spawn time.
#
# For example, to go straight, we'd have an empty list [].
# For a left turn, we'd have something like:
# [ { "trigger_point": (X, Y), "action": "turn_left", "new_direction": "E" } ]
# For a right turn, we similarly define a "turn_right" action.
# (You can adjust trigger points as needed.)
#
# If you want a lane to remain only left-turn or only straight, give it just one item in possible_paths.
#############################################################################

lanes_data = [
    # -------------------------------------------------------
    # NORTH ROAD (travel_dir = "S"): Vehicles traveling downward
    # -------------------------------------------------------
    {
        "name": "North-Bike-Middle", 
        "spawn": (800, 0),
        "vehicle_types": ["bike"],
        "travel_dir": "S",
        "stop_for_red": False,
        # For demonstration, let's say they can either go straight or turn left
        "possible_paths": [
            # [],  # Straight (no turns)
            [{
                "trigger_point": (800, 510),
                "action": "turn_left",   # S->E
                "new_direction": "E"
            }]
        ]
    },
    {
        "name": "North-Car-Outer",
        "spawn": (850, 0),
        "vehicle_types": ["car"],
        "travel_dir": "S",
        "stop_for_red": False,
        # For demonstration, let's show left, right, or straight
        # NOTE: You must adjust trigger points for the right turn if your map supports it.
        "possible_paths": [
            # [],  # Straight
            [{
                "trigger_point": (845, 470),
                "action": "turn_left",  # S->E
                "new_direction": "E"
            }]
            # [{
            #     "trigger_point": (845, 530),
            #     "action": "turn_right",  # S->W  (just as an example)
            #     "new_direction": "W"
            # }]
        ]
    },
    {
        "name": "North-Lane-3",
        "spawn": (755, 0),
        "vehicle_types": ["bike"],
        "travel_dir": "S",
        "stop_for_red": True,
        # Maybe only straight or left
        "possible_paths": [
            [],  # Straight
            # [{
            #     "trigger_point": (760, 520),
            #     "action": "turn_left",
            #     "new_direction": "E"
            # }]
        ]
    },
    {
        "name": "North-Lane-4",
        "spawn": (680, 0),
        "vehicle_types": ["car"],
        "travel_dir": "S",
        "stop_for_red": True,
        # Maybe they can only go straight. (Adjust if you like.)
        "possible_paths": [
            [],
            # [{
            #     "trigger_point": (680, 610),
            #     "action": "turn_right",  # S->E
            #     "new_direction": "W"
            # }]
        ]
    },

    # -------------------------------------------------------
    # SOUTH ROAD (travel_dir = "N")
    # -------------------------------------------------------
    {
        "name": "South-Branching-Lane",
        "spawn": (520, 790),
        "vehicle_types": ["car", "bike"],
        "travel_dir": "N",
        "stop_for_red": False,
        "possible_paths": [
            [{
                "trigger_point": (520, 520),
                "action": "branch",  # Custom action for branching
                "new_direction": "N"  # Continue North initially
            }


            ]  # e.g., no turns, or add your own
        ]
    },
    {
        "name": "South-Lane-StopForRed",
        "spawn": (600, 790),
        "vehicle_types": ["car", "bike"],
        "travel_dir": "N",
        "stop_for_red": True,
        "possible_paths": [
            [{
                "trigger_point": (600, 540),
                "action": "turn_right",  # N->E
                "new_direction": "E"
            }]
        ]
    },

        # -------------------------------------------------------
    # EAST LANE (travel_dir = "W")
    # -------------------------------------------------------
    {
        "name": "East-NoStop",
        "spawn": (1280, 650),
        "vehicle_types": ["car", "bike"],
        "travel_dir": "W",
        "stop_for_red": False,
        "possible_paths": [
            [{
                "trigger_point": (770, 650),
                "action": "turn_left",  # W->S
                "new_direction": "S"
            }],
           
        ]
    },
    {
        "name": "East-StopThenBranch",
        "spawn": (1280, 590),
        "vehicle_types": ["car", "bike"],
        "travel_dir": "W",
        "stop_for_red": True,
        "possible_paths": [
            [{
                "trigger_point": (620,590),
                "action": "branch_east",
                "new_direction": "N"
            }],
            # []  # straight
        ]
    },

    # -------------------------------------------------------
    # WEST LANE (travel_dir = "E")
    # -------------------------------------------------------
    {
    "name": "West-LeftTurn",
    "spawn": (0, 520),
    "vehicle_types": ["car", "bike"],
    "travel_dir": "E",
    "stop_for_red": False,  # Vehicles won't stop for red traffic light
    "possible_paths": [
        [{
            "trigger_point": (440, 520),
            "action": "turn_left",  # Turn left to move north
            "new_direction": "N"
        }]
    ]
    },
    {
        "name": "West-StopThenMultiTurn",
        "spawn": (0, 620),
        "vehicle_types": ["car", "bike"],
        "travel_dir": "E",
        "stop_for_red": True,
        "possible_paths": [
            [
                {
                    "trigger_point": (680, 620),
                    "action": "turn_right",  # E->S
                    "new_direction": "S"
                }
            ],
            # [
            #     {
            #         "trigger_point": (680, 620),
            #         "action": "move_up",  # Move up to (680, 550)
            #         "new_direction": "E"
            #     },
            #     {
            #         "trigger_point": (680, 530),
            #         "action": "turn_left",  # E->N
            #         "new_direction": "N"
            #     }
            # ],
        
        ]
    }
]

#############################################################################
# PER-LANE TIMERS & DATA STRUCTURES
#############################################################################
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
        spawn_interval = 1200 if vtype == "bike" else 1500
        pygame.time.set_timer(event_id, spawn_interval)
        timers.append((event_id, lane_name, vtype))

#############################################################################
# HELPER FUNCTIONS
#############################################################################
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
    Returns how far `pos2` is in front of `pos1` along travel `direction`.
    If the result is negative, pos2 is behind pos1.
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

#############################################################################
# VEHICLE CLASS
#############################################################################
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

        # Visual properties
        if vehicle_type == "bike":
            self.width = 10
            self.height = 25
            self.max_speed = 3.0
        else:
            self.width = 20
            self.height = 40
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

        # Add special logic for south directional lane (520, 790)
    # if self.lane_def["name"] == "South-Branching-Lane":
    #     # Initialize the variables before using them
    #     east_light_color = get_light_color_for_direction("E")
    #     west_light_color = get_light_color_for_direction("W")
        
    #     east_has_red = (east_light_color == RED)
    #     west_has_green = (west_light_color == GREEN)
        
        # # If either condition is true, stop the vehicle
        # if not east_has_red or west_has_green:
        #     self.speed = 0
        #     return False  # Don't remove the vehicle
        # Ensure vehicles from (520,790) stop at (520,640) if west lane is green
        

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
        safe_threshold = motorcycle_safe_threshold if self.vehicle_type == "bike" else car_safe_threshold
        closest_dist = float('inf')
        closest_speed = None

        for other in lane_vehicles:
            if other is self:
                continue
            d = distance_in_travel_dir((self.x, self.y), (other.x, other.y), self.direction)
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
        if (self.x < -50 or self.x > screen_width + 50 or
            self.y < -50 or self.y > screen_height + 50):

            if not self.has_been_counted:
                total_vehicles_passed += 1
                self.has_been_counted = True

                # Also check if it originally traveled S (meaning it spawned from top/north)
                # and increment either dedicated or shared
                if self.lane_def["travel_dir"] == "S":
                    if self.lane_def["name"] in dedicated_lanes:
                        dedicated_passed_south += 1
                    else:
                        shared_passed_south += 1

            return True  # signal removal
        return False

    def distance_to_stop_line(self, stop_line):
        """
        Returns how far we are from the stop line along our travel direction.
        Positive => haven't reached the line yet, negative => we've passed it.
        """
        half_len = (self.height / 2) if self.direction in ("N","S") else (self.width / 2)

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
            # You can add "branch" or other actions here if needed.
            self.turn_index += 1

    def move_up(self, new_dir):
        """
        Move the vehicle up to (680, 550) before turning left.
        """
        if self.y > 550:
            self.y -= self.speed  # Move up
        else:
            # Once the vehicle reaches (680, 550), turn left
            self.turn_left(new_dir)

    def branch(self, new_dir):
        instr = self.turn_instructions[self.turn_index]
        tx, ty = instr["trigger_point"]
        self.x, self.y = tx, ty
        if self.vehicle_type == "bike":
            self.x, self.y = 515, 480
        elif self.vehicle_type == "car":
            self.x, self.y = 575, 480
        self.direction = new_dir
        self.angle = angle_for_dir(new_dir)

    def branch_east(self, new_dir):
        instr = self.turn_instructions[self.turn_index]
        tx, ty = instr["trigger_point"]
        self.x, self.y = tx, ty  # Move to the branching point (600, 590)
        
        # Branch based on vehicle type
        if self.vehicle_type == "bike":
            self.x, self.y = 530, 590  # Move to bike-only lane
        elif self.vehicle_type == "car":
            self.x, self.y = 600, 590  # Move to car-only lane
        
        # Rotate and move north
        self.direction = new_dir
        self.angle = angle_for_dir(new_dir)

    def turn_left(self, new_dir):
        instr = self.turn_instructions[self.turn_index]
        tx, ty = instr["trigger_point"]
        self.x, self.y = tx, ty
        if self.vehicle_type == "bike" and self.x == 440 and self.y == 520:
            self.x, self.y = 490, 520
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

#############################################################################
# MAIN LOOP
#############################################################################
clock = pygame.time.Clock()
running = True
all_vehicles = []

while running:
    dt = clock.tick(60)
    current_time = pygame.time.get_ticks()

    # 1) Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Check spawn events
        for (ev_id, lane_name, vtype) in timers:
            if event.type == ev_id:
                # Find the lane definition
                lane_def = None
                for ld in lanes_data:
                    if ld["name"] == lane_name:
                        lane_def = ld
                        break
                if not lane_def:
                    continue

                lane_list = lane_vehicles_map[lane_name]
                if len(lane_list) < max_vehicles_per_lane:
                    # Randomly choose one of the possible paths for this lane
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
            # Was allred => move to next direction’s green
            direction_index = (direction_index + 1) % len(direction_order)
            if direction_order[direction_index] == "W":
                light_state = "green_west"
            else:
                light_state = "green"
        elif light_state == "green_west":
            light_state = "orange_west"
        elif light_state == "orange_west":
            light_state = "allred"
        light_state_start = current_time

    # 3) Update dash_colors (purely for drawing the lights)
    for direction, ddata in directions_data.items():
        color = get_light_color_for_direction(direction)
        for coord in ddata["traffic_lights"]:
            dash_colors[coord] = color

    # 4) Draw the background
    screen.blit(background_image, (0, 0))

    # 5) Draw the traffic lights (the little colored dashes)
    dash_length = 20
    dash_thickness = 5
    for direction, ddata in directions_data.items():
        for (lx, ly) in ddata["traffic_lights"]:
            color = dash_colors.get((lx, ly), RED)
            if direction in ("N", "S"):  # draw a horizontal dash
                pygame.draw.line(screen, color,
                                 (lx - dash_length//2, ly),
                                 (lx + dash_length//2, ly),
                                 dash_thickness)
            else:  # E, W => draw a vertical dash
                pygame.draw.line(screen, color,
                                 (lx, ly - dash_length//2),
                                 (lx, ly + dash_length//2),
                                 dash_thickness)

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
    txt = font.render(f"Total Vehicles Passed: {total_vehicles_passed}", True, (255,255,255))
    screen.blit(txt, (20, 50))

    # Show dedicated vs shared lanes rate (for vehicles that came from North -> South)
    dedicated_txt = font.render(f"DEDICATED LANES RATE: {dedicated_passed_south}", True, (255,255,255))
    screen.blit(dedicated_txt, (20, 80))

    shared_txt = font.render(f"SHARED LANES RATE: {shared_passed_south}", True, (255,255,255))
    screen.blit(shared_txt, (20, 110))

    # 8) Flip screen
    pygame.display.flip()

pygame.quit()
sys.exit()

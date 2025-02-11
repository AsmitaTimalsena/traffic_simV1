
   


##NoRTH LANE ROAD
 # Four positions from where vehicles are generated:
 # (760,0),(800,0), 
# (680,0),(850,0),
# (520,790),(650,790),
### 1. from NORTH road there are four coordinates from where vehicles move:
#for motorcycle: 
'''
    These are the middle lanes, from where bikes move. For bike moving from coordinate (800,0) only, 
    
    1. if they reach to point (800, 530) they will have to take left turn, i.e, for this lane vehicles bikes wont stop for red traffic light 
    and continuously move to east road.   
    '''
    

    #for car:
'''
    These are the outer lanes, from where cars move. For cars moving from coordinate (850,0) only, 
    2. if they reach to point (845, 470 ) they will have to take left turn, i.e, for this lane vehicles cars wont stop for red traffic light 
    and continuously move to east road.   
    '''

    ##SOUTH LANE ROAD
    #VEHICLES generate from here:
(520,790),(600,790),
'''
    1. Both bikes and cars have to be generated from the coordinates: (520,790), (600,790) respectively.
    2. For the vehilces moving from coordinate: (520,790) only,  for this lane vehicles wont stop for red traffic light of south road. 
    If the vehicle reaches to coordinate:(520,520),the condition check must be done: 

    if vehicle_type==bike, move to travel along lane:(530,480),
    else if vehicle_type==car, move to travel along lane:(600,480),

    3. For the vehilces moving from coordinate: (600,790) only,  for this lane vehicles will stop for red traffic light of south road.
    When the traffic light is green and vehicles move up to position:(600,540), they will turn to East and continue moving forward. 
    There wont be any case of vehicle type here since travel mode is share->share.
    '''
   ##


   ##EAST LANE ROAD
   #vehicles both car or bike will be generated at this two position:
(1280,590), (1280,650),
'''
1.For the vehicles moving from coordinate: (1280,590) only,  for this lane vehicles wont stop for red traffic light of east road.
They will rather take left turn continuously to move to south road by rotating when they reach coordinate:(750,660).
2. For the vehicles moving from coordinate: (1280,650) only,  for this lane vehicles will stop for red traffic light of east road.
When light is green they move upto:(600,590) condition applies since it is shared->dedicated scenario:
a. if vehicle_type==bike, move to travel along lane:(530,590), rotate and move upto north direction with lane separated for bikes only.
b. if vehicle_type==car, from (600,590), rotate  and move upto north direction with lane separated for cars only.
   '''
   

   ##WEST LANE ROAD
#The vehicles both car or bike  will be generated from these coordinates at west road. West Road is one way:
(0,520),(0,620),
'''
1. For the vehicles moving from coordinate: (0,520) only,  for this lane vehicles wont stop for red traffic light of west road.
They will rather take left turn continuously to move to north road by rotating when they reach coordinate:(440,520).
 a. if vehicle_type==bike, once they reach (440,520), move upto position:(490,520), rotate and move upto north direction with lane separated for bikes only.
b. if vehicle_type==car, once they reach (440,520) simply  rotate and move upto north direction with lane separated for bikes only.

2. For the vehicles moving from coordinate: (0,620) only,  for this lane vehicles will stop for red traffic light of west road.
When the light is green, the vehicles move straight to:(680,620) and then :
i. rotate to move to south road. 
ii. OR it will move up  to short distance till:(680,550), and then rotate to move to east road.
'''

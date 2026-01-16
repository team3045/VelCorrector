import math
import pandas as pd
import os

global position, velocity, angle, targetPosition, distance, speed, vertangle, targetAngle, angleToTarget, height

#position = (0,0)  Robot Position
#velocity = (0,0)  Robot velocity in feet per second
#angle = 0         Robot Angle (relative to scoring table side)
#speed = 0         Robot firing speed

#vertangle = 0     Vertical angle to fire at
#targetPosition = (0,0) Position of the Hub
#targetAngle = 0   Angle to the target(relative to the scoring table side)

#angleToTarget = 0 Angle to the target(relative to the robot angle
#distance = 0      Distance to the target
#timeofFlight = 0  Time in seconds that the flight would take

global G
G = 32.174         #Gravity
height = 6         #Height of the target

def Dis_to_target(dis_position = (0,0), dis_target = (0,0)):
    distance = math.dist(dis_position, dis_target)

    return distance

def VertAngleCalc(s = 0.0, dis = 0.0, height = 6.0):
    try:

        temp = (s ** 2 - math.sqrt(s ** 4 - G * (G * dis ** 2 + 2 * height * s ** 2)))
        temp2 = math.degrees(math.atan(temp/(G*dis)))
        return temp2

    except:
        ValueError
        return 0

def HorizontalAngleCalc(pos = (0,0), targetposition = (0,0), dis = 0.0):
    angle = math.asin((targetposition[0]-pos[0])/dis)
    targetAngle = math.degrees(angle)
    return targetAngle

def HorizontalAngleToMove(selfAngle = 0.0, targetAngle = 0.0):
    angleToMove = targetAngle - selfAngle
    return angleToMove

def TimeofFlight(s = 0.0, angle = 0.0):
    time = distance/(math.cos(angle)*s)
    return time

def VelCorrection(velocity = (0,0), flightTime = 0.0, targetposition = (0,0)):
    Xdis = flightTime * velocity[0]
    Ydis = flightTime * velocity[1]
    CorrectedTarPosition = [targetposition[0] - Xdis, targetposition[1] - Ydis]
    return CorrectedTarPosition


while True:
    position = [0.0, 0.0]  #Robot Position
    velocity = [0.0,0.0]  #Robot velocity
    angle = 0         #Robot Angle (relative to scoring table side)
    speed = 0         #Robot firing speed

    vertangle = 0     #Vertical angle to fire at
    targetPosition = [0.0, 0.0]  #Position of the Hub
    targetAngle = 0   #Angle to the target(relative to the scoring table side)

    angleToTarget = 0 #Angle to the target(relative to the robot angle
    distance = 0      #Distance to the target

    position[0] = float(input("x value:"))
    position[1] = float(input("y value:"))
    targetPosition[0] = float(input("x value:"))
    targetPosition[1] = float(input("y value:"))
    velocity[0] = float(input("velocity x:"))
    velocity[1] = float(input("velocity y:"))
    speed = float(input("speed value:"))

    distance = Dis_to_target(position, targetPosition)
    vertangle = VertAngleCalc(speed, distance, height)
    targetAngle = HorizontalAngleCalc(position, targetPosition, distance)
    angleToTarget = HorizontalAngleToMove(angle, targetAngle)
    timeofFlight = TimeofFlight(speed, math.radians(vertangle))
    CorrectedTarget = VelCorrection(velocity, timeofFlight, targetPosition)
    CorrectedDistance = Dis_to_target(position, CorrectedTarget)
    CorrectedVertAngle = VertAngleCalc(speed, CorrectedDistance, height)
    CorrectedTargetAngle = HorizontalAngleCalc(position, CorrectedTarget, CorrectedDistance)
    CorrectedAngleToTarget = HorizontalAngleToMove(angle, CorrectedTargetAngle)
    CorrectedTimeOfFlight = TimeofFlight(speed, math.radians(CorrectedVertAngle))

    if vertangle == 0:
        print("Cannot hit the target with that speed")
    else:
        print("distance is " + str(distance))
        print("vertical angle is " + str(vertangle))
        print("target angle is " + str(targetAngle))
        print("angle to move is " + str(angleToTarget))
        print("time of flight is " + str(timeofFlight))
        print("----Corrections----")
        print("Corrected target position is " + str(CorrectedTarget))
        print("Corrected distance is " + str(CorrectedDistance))
        print("Corrected vertical angle is " + str(CorrectedVertAngle))
        print("Corrected target angle is " + str(CorrectedTargetAngle))
        print("Corrected angle to move is " + str(CorrectedAngleToTarget))
        print("Corrected time of flight is " + str(CorrectedTimeOfFlight))


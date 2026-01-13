import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px
import math


Hub_Height = 6
global G
G = 32.174
time_max = 10000



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
    try:
        top = float(((1/2)*G) + (math.sqrt((((-1/2)*G)**2) - 4*(s*math.sin(angle))*(Hub_Height))))
    except:
        ValueError
        top = float(((1/2)*G) + (math.sqrt(abs((((-1/2)*G)**2) - 4*(s*math.sin(angle))*(Hub_Height)))))
    try:
        time = top / (2*(s*math.sin(angle)))
    except:
        ValueError
        return 0

    return time

def VelCorrection(velocity = (0,0), flightTime = 0.0, targetposition = (0,0)):
    Xdis = flightTime * velocity[0]
    Ydis = flightTime * velocity[1]
    CorrectedTarPosition = [targetposition[0] - Xdis, targetposition[1] - Ydis]
    return CorrectedTarPosition




st.set_page_config(page_title="Velocity Correction", page_icon="🤖")
st.title("Velocity Correction")
st.set_page_config(layout="wide")
col1, col2, col3 = st.columns(3)

with (col1):
    s = st.number_input('Launch speed (feet/second)', value=25.0, step=1.0)
    pos1, pos2 = st.columns(2)
    Position = [0.0,0.0]
    TargetPosition = [0.0, 0.0]
    Velocity = [0.0,0.0]
    with pos1:
        Position[0] = st.number_input('Position x', value=0.0, min_value=0.0, step=0.1)
        Velocity[0] = st.number_input('Velocity x', value=0.0, min_value=0.0, step=0.1)
        TargetPosition[0] = st.number_input('Target Position x', value=1.0, min_value=0.0, step=0.1)
    with pos2:
        Position[1] = st.number_input('Position y', value=0.0, min_value=0.0, step=0.1)
        Velocity[1] = st.number_input('Velocity y', value=0.0, min_value=0.0, step=0.1)
        TargetPosition[1] = st.number_input('Target Position y', value=1.0, min_value=0.0, step=0.1)
    angle = st.number_input('Shooter angle(deg)', value=0.0, step=0.5, min_value=0.0)
    shooterheight = st.number_input('Shooter height (Inches)', value=1.0, min_value=0.0)
    Hub_Height = Hub_Height - (shooterheight/12)

distance = Dis_to_target(Position, TargetPosition)
vertangle = VertAngleCalc(s, distance, Hub_Height)
targetAngle = HorizontalAngleCalc(Position, TargetPosition, distance)
angleToTarget = HorizontalAngleToMove(angle, targetAngle)
timeofFlight = TimeofFlight(s, math.radians(vertangle))
CorrectedTarget = VelCorrection(Velocity, timeofFlight, TargetPosition)
CorrectedDistance = Dis_to_target(Position, CorrectedTarget)
CorrectedVertAngle = VertAngleCalc(s, CorrectedDistance, Hub_Height)
CorrectedTargetAngle = HorizontalAngleCalc(Position, CorrectedTarget, CorrectedDistance)
CorrectedAngleToTarget = HorizontalAngleToMove(angle, CorrectedTargetAngle)
CorrectedTimeOfFlight = TimeofFlight(s, math.radians(CorrectedVertAngle))

with col1:
    st.space("small")

    mark1, mark2 = st.columns(2)
    with mark1:

        st.markdown(f"**:blue[Distance is:]**", text_alignment="right")
        st.markdown(f"**:blue[Vertical Angle is:]**", text_alignment="right")
        st.markdown(f"**:blue[Target Angle is:]**", text_alignment="right")
        st.markdown(f"**:blue[Time of Flight is:]**", text_alignment="right")
    with mark2:
        st.markdown(f"**:red[{CorrectedDistance:.2f}]**")
        st.markdown(f"**:red[{CorrectedVertAngle:.2f}]**")
        st.markdown(f"**:red[{CorrectedTargetAngle:.2f}]**")
        st.markdown(f"**:red[{CorrectedTimeOfFlight:.2f}]**")


#with col2:





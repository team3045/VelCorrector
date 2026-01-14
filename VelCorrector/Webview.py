import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
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

        temp = (s ** 2 + math.sqrt(s ** 4 - G * (G * dis ** 2 + 2 * height * s ** 2)))
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
    """try:
        top = float(((1/2)*G) + (math.sqrt((((-1/2)*G)**2) - 4*(s*math.sin(angle))*(Hub_Height))))
    except:
        ValueError
        top = float(((1/2)*G) + (math.sqrt(abs((((-1/2)*G)**2) - 4*(s*math.sin(angle))*(Hub_Height)))))
    try:
        time = top / (2*(s*math.sin(angle)))
    except:
        ValueError
        return 0"""
    time = distance/(math.cos(angle)*s)
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
        Position[0] = st.number_input('Position x', value=-1.0, step=0.1)
        Velocity[0] = st.number_input('Velocity x', value=0.0, step=0.1)
        TargetPosition[0] = st.number_input('Target Position x', value=2.0, step=0.1)
    with pos2:
        Position[1] = st.number_input('Position y', value=0.0, step=0.1)
        Velocity[1] = st.number_input('Velocity y', value=0.0, step=0.1)
        TargetPosition[1] = st.number_input('Target Position y', value=0.0, step=0.1)
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

def trajectory():
    x = [0]
    xc = [0]
    y = [0]
    yc = [0]
    for each in range(int(timeofFlight*1000)+100):
        t = each/1000
        x.append(s*t*math.cos(math.radians(vertangle)))
        y.append(s*t*math.sin(math.radians(vertangle)) - (1/2) *G*t**2)
    for each in range(int(CorrectedTimeOfFlight*1000)+100):
        t = each/1000
        xc.append(s*t*math.cos(math.radians(CorrectedVertAngle)))
        yc.append(s*t*math.sin(math.radians(CorrectedVertAngle)) - (1/2) *G*t**2)
    return (x,y, xc, yc)

df = pd.DataFrame()
dfc = pd.DataFrame()
df['x'], df['y'], dfc['x'], dfc['y'] = trajectory()
df['type'] = 'Direct trajectory'
dfc['type'] = 'Corrected trajectory'
hub = pd.DataFrame()
hub['x'] = [distance - 1.75, distance +1.75]
hub['y'] = [Hub_Height, Hub_Height]
hub['type'] = 'Hub opening'



df = pd.concat([df,dfc])
df = pd.concat([df,hub])

temp = df.query(f"x > {CorrectedDistance - 1.75} and x < {CorrectedDistance} and y < {Hub_Height} and type != 'Hub opening' and type != 'Direct trajectory'")
print(temp)

fig = px.line(df, x=df["x"], y=df["y"], title="Vertical simulation", labels={'x':'Horizontal distance(feet)','y':'Vertical distance(feet)'}, color="type")
fig.add_scatter(x=[distance,CorrectedDistance], y=[Hub_Height,Hub_Height], name="Hub", mode="markers", marker=dict(color="red", opacity=0.5))
fig.add_shape(type="rect", x0=distance-1.75, x1=distance + 1.75, y0= 0, y1= Hub_Height, name="Hub box", fillcolor="red", opacity=0.5)



with col2:
    st.plotly_chart(fig)
    if vertangle == 0:
        st.markdown("**:red[If the lines do not cross the Hub adjust the variables]**")
    elif abs(distance) <= 1.75:
        st.markdown("**:red[You're somehow within the Hub rn, fix this.]**")
    elif not temp.empty:
        st.markdown("**:blue[The ball will not make it rn, please adjust so it doesn't hit the hub walls]**")


mapObjects =  pd.DataFrame()

mapObjects['x'] = [Position[0], TargetPosition[0], CorrectedTarget[0]]
mapObjects['y'] = [Position[1], TargetPosition[1], CorrectedTarget[1]]
mapObjects['type'] = ['Robot', 'Hub', 'Aim']

lines = pd.DataFrame()
lines['x'] = [Position[0], TargetPosition[0], Position[0], CorrectedTarget[0]]
lines['y'] = [Position[1], TargetPosition[1], Position[1], CorrectedTarget[1]]
lines['type'] = ['Direct shot', 'Direct shot', 'Corrected for Vel', 'Corrected for Vel']

map = px.scatter(mapObjects, x=mapObjects['x'], y=mapObjects['y'], color=mapObjects['type'])
map.add_shape(type="rect", x0=Position[0] - 1, x1=Position[0]+1, y0= Position[1] + 1, y1= Position[1]-1, name="Robot", fillcolor="red", opacity=0.75)
map.add_shape(type="rect", x0=TargetPosition[0] - 1.75, x1=TargetPosition[0] + 1.75, y0= TargetPosition[1] - 1.75, y1= TargetPosition[1] + 1.75, name="Hub box", fillcolor="red", opacity=0.5)
map.add_scatter(x=lines['x'], y=lines['y'], mode='lines', line_color="yellow", opacity=0.5, name="Aim")
map.update_layout(title_text="Vertical View", xaxis= dict(scaleanchor="y", scaleratio=1 ))




with col3:
    st.plotly_chart(map)





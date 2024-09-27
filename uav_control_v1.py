#!/usr/bin/env python
# Rescue coaxial hexacopter UAV dual tilt rotor demonstrator
# Demonstrate dual tilt rotor actions
# Calibrate rotor positions
import os
import sys, tty, termios
from dxl_uav_class import dxl_uav
import math
import time

fd = sys.stdin.fileno()
old_settings = termios.tcgetattr(fd)

#Keyboard input function
def getch():
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch

#Initialize 6 pitch and roll servo motor instances
DXL_roll=[]
DXL_pitch=[]
for i in range(6):
    DXL_roll.append( dxl_uav(i+1) )
    DXL_pitch.append( dxl_uav(i+11) )

#Set torque on. Assume mode is extended position mode
for i in range(6):
    DXL_roll[i].torqueOn()
    DXL_pitch[i].torqueOn()

#Control variables
mode=0
tiltX=0
tiltY=0
angleStep=1
positionStepX=0
positionStepY=0
scaleRoll=4096/360*40/12
scalePitch=4096/360*306/12
angle2rad=math.pi/180
radArm=[0*angle2rad, 180*angle2rad, 120*angle2rad, 300*angle2rad, 60*angle2rad, 240*angle2rad]
timeDelay=0.1
sweepAngle=30
sweepStep=5

#Read current status from servo motors and initialize to the present position offset
for i in range(6):
    DXL_roll[i].getCurrentPotision()
    DXL_pitch[i].getCurrentPotision()
    DXL_roll[i].POSITION_OFFSET=DXL_roll[i].PRESENT_POSITION
    DXL_pitch[i].POSITION_OFFSET=DXL_pitch[i].PRESENT_POSITION
    print("Status %d: %d/%d/%d %d/%d/%d" % (i+1, 
                                            DXL_roll[i].PRESENT_POSITION, 
                                            DXL_roll[i].GOAL_POSITION, 
                                            DXL_roll[i].POSITION_OFFSET, 
                                            DXL_pitch[i].PRESENT_POSITION, 
                                            DXL_pitch[i].GOAL_POSITION, 
                                            DXL_pitch[i].POSITION_OFFSET) )

#Print keyboard interface instructions
print("------------------------------------------")
print("0: all motors in same individual origin")
print("9: all motors as hexacopter")
print("q: sweep by individual origin")
print("w: sweep by hexacopter center")
print("-: move all motors to 0 position")
print("1-6: roll and pitch motor calibration")
print("m: save calibration")
print("j: left, l: right, i: forward, k: backward")
print("a: faster movement")
print("z: slower movement")
print("ESC to quit")
print("------------------------------------------")

#Start control loop
#Set modes by keyboard input and actuate motors based on the goal positions
while 1:
    charInput=getch()
    
    #Exit
    if charInput == chr(0x1b):
        break
    
    #All motors in same individual origin
    if charInput == "0":
        mode=20
    
    #All motors as hexacopter
    if charInput == "9":
        mode=29
    
    #Perform sweep by individual origin
    if charInput == "q":
        mode=27
    
    #Perform sweep by hexacopter center
    if charInput == "w":
        mode=28

    #Move all motors to reference position
    if charInput == "-": 
        for i in range(6):
            DXL_roll[i].setGoalPotision(0)
            DXL_pitch[i].setGoalPotision(0)
        tiltX=0
        tiltY=0
    
    #Increase angle step
    if charInput == "a":
        angleStep+=1   
    
    #Decrease angle step
    if charInput == "z":
        angleStep-=1
    
    #decrease X angle
    if charInput == "j":
        tiltX-=angleStep
    
    #Increase X angle
    if charInput == "l":
        tiltX+=angleStep
    
    #Increase Y angle
    if charInput == "i":
        tiltY+=angleStep
    
    #Decrease Y angle
    if charInput == "k":
        tiltY-=angleStep
    
    #Individual motor 1-6 control and calibration
    if charInput == "1":
        mode=1
        tiltX=0
        tiltY=0
    if charInput == "2":
        mode=2
        tiltX=0
        tiltY=0
    if charInput == "3":
        mode=3
        tiltX=0
        tiltY=0
    if charInput == "4":
        mode=4
        tiltX=0
        tiltY=0
    if charInput == "5":
        mode=5
        tiltX=0
        tiltY=0
    if charInput == "6":
        mode=6
        tiltX=0
        tiltY=0
    
    #Calibrate motor from current positions
    if charInput == "m":
        for i in range(6):
            DXL_roll[i].getCurrentPotision()
            DXL_pitch[i].getCurrentPotision()
            DXL_roll[i].POSITION_OFFSET=DXL_roll[i].PRESENT_POSITION
            DXL_pitch[i].POSITION_OFFSET=DXL_pitch[i].PRESENT_POSITION
    
    #Individual motor control
    if mode>0 and mode<7:
        positionStepX=int(tiltX*scaleRoll)
        positionStepY=int(tiltY*scalePitch)
        DXL_roll[mode-1].setGoalPotision(positionStepX)
        DXL_pitch[mode-1].setGoalPotision(positionStepY)
    
    #All motors in same individual origin
    if mode==20:
        positionStepX=int(tiltX*scaleRoll)
        positionStepY=int(tiltY*scalePitch)
        for i in range(6):
            DXL_roll[i].setGoalPotision(positionStepX)
            DXL_pitch[i].setGoalPotision(positionStepY)
    
    #All motors as hexacopter  
    if mode==29:
        for i in range(6):
            tRoll=int(scaleRoll*(-tiltX*math.sin(radArm[i])+tiltY*math.cos(radArm[i])))
            tPitch=int(scalePitch*(tiltX*math.cos(radArm[i])+tiltY*math.sin(radArm[i])))
            DXL_roll[i].setGoalPotision(tRoll)
            DXL_pitch[i].setGoalPotision(tPitch)    

    #Perform sweep by individual origin
    if mode==27:
        #set starting position
        tiltX=0
        tiltY=0
        positionStepX=int(tiltX*scaleRoll)
        positionStepY=int(tiltY*scalePitch)
        for i in range(6):
            DXL_roll[i].setGoalPotision(positionStepX)
            DXL_pitch[i].setGoalPotision(positionStepY)
        time.sleep(1)

        #X sweep to ready for 360 sweep
        for k in range(0,sweepAngle+sweepStep,sweepStep):
            tiltX=k
            positionStepX=int(tiltX*scaleRoll)
            for i in range(6):
                DXL_roll[i].setGoalPotision(positionStepX)
                DXL_pitch[i].setGoalPotision(positionStepY)
            time.sleep(timeDelay)
        
        #360 degree rotation sweep
        for k in range(0,360+sweepStep,sweepStep):
            tiltX=sweepAngle*math.cos(k*angle2rad)
            tiltY=sweepAngle*math.sin(k*angle2rad)
            positionStepX=int(tiltX*scaleRoll)
            positionStepY=int(tiltY*scalePitch)
            for i in range(6):
                DXL_roll[i].setGoalPotision(positionStepX)
                DXL_pitch[i].setGoalPotision(positionStepY)
            time.sleep(timeDelay)            
        
        #Return from x sweep to reference position
        for k in range(sweepAngle,-sweepStep,-sweepStep):
            tiltX=k
            positionStepX=int(tiltX*scaleRoll)
            for i in range(6):
                DXL_roll[i].setGoalPotision(positionStepX)
                DXL_pitch[i].setGoalPotision(positionStepY)
            time.sleep(timeDelay)
        
        #Reset to inital mode
        mode=0
    
    #Perform sweep by hexacopter center
    if mode==28:
        #set starting position
        tiltX=0
        tiltY=0
        positionStepX=int(tiltX*scaleRoll)
        positionStepY=int(tiltY*scalePitch)
        for i in range(6):
            DXL_roll[i].setGoalPotision(positionStepX)
            DXL_pitch[i].setGoalPotision(positionStepY)
        time.sleep(1)

        #X sweep to ready for 360 sweep
        for k in range(0,sweepAngle+sweepStep,sweepStep):
            tiltX=k
            for i in range(6):
                tRoll=int(scaleRoll*(-tiltX*math.sin(radArm[i])+tiltY*math.cos(radArm[i])))
                tPitch=int(scalePitch*(tiltX*math.cos(radArm[i])+tiltY*math.sin(radArm[i])))
                DXL_roll[i].setGoalPotision(tRoll)
                DXL_pitch[i].setGoalPotision(tPitch)  
            time.sleep(timeDelay)
        
        #360 degree rotation sweep
        for k in range(0,360+sweepStep,sweepStep):
            tiltX=sweepAngle*math.cos(k*angle2rad)
            tiltY=sweepAngle*math.sin(k*angle2rad)
            for i in range(6):
                tRoll=int(scaleRoll*(-tiltX*math.sin(radArm[i])+tiltY*math.cos(radArm[i])))
                tPitch=int(scalePitch*(tiltX*math.cos(radArm[i])+tiltY*math.sin(radArm[i])))
                DXL_roll[i].setGoalPotision(tRoll)
                DXL_pitch[i].setGoalPotision(tPitch)  
            time.sleep(timeDelay) 

        #Return from X sweep to reference position           
        for k in range(sweepAngle,-sweepStep,-sweepStep):
            tiltX=k
            for i in range(6):
                tRoll=int(scaleRoll*(-tiltX*math.sin(radArm[i])+tiltY*math.cos(radArm[i])))
                tPitch=int(scalePitch*(tiltX*math.cos(radArm[i])+tiltY*math.sin(radArm[i])))
                DXL_roll[i].setGoalPotision(tRoll)
                DXL_pitch[i].setGoalPotision(tPitch)  
            time.sleep(timeDelay)
        
        #Reset to initial mode
        mode=0

    #Report motor status
    for i in range(6):
        print("Status %d: %d %d" % (i+1, tiltX, tiltY) )

#Turn off motors and close
for i in range(6):
    DXL_roll[i].torqueOff()
    DXL_pitch[i].torqueOff()
    DXL_roll[i].closePort()
    DXL_pitch[i].closePort()
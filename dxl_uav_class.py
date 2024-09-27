#!/usr/bin/env python
import os, sys, tty, termios
from dynamixel_sdk import *   

#Dynamixel servo motor control class for UAV
#Adopted from Dynamixel example code
class dxl_uav:
    def __init__(self, ID):
        # Control table address
        # anything without "self." will not be used
        # just there for aesthetical purposes & as a reminder
        PROTOCOL_VERSION            = 2.0
        self.ADDR_TORQUE_ENABLE     = 64
        ADDR_LED_RED                = 65
        ADDR_OPERATING_MODE         = 11
        OP_VELOCITY_CTRL_MODE       = 1
        self.ADDR_GOAL_VELOCITY     = 104
        ADDR_VELOCITY_LIMIT         = 44
        VELOCITY_LIMIT              = 265
        self.ADDR_PRESENT_VELOCITY  = 128
        LEN_LED_RED                 = 1
        self.ADDR_GOAL_POSITION     = 116
        LEN_GOAL_POSITION           = 4
        self.ADDR_PRESENT_POSITION  = 132
        self.ADDR_OPERATING_MODE    = 4
        LEN_PRESENT_POSITION        = 4
        DXL_MINIMUM_POSITION_VALUE  = 0
        self.MAXIMUM_POSITION_VALUE = 4095
        self.BAUDRATE               = 57600
        self.DXL_ID                 = ID                 # Dynamixel#1 ID : 1
        self.orientation            = 1 #1 or -1
        self.PRESENT_POSITION       = 0
        self.POSITION_OFFSET        = 0
        self.GOAL_POSITION          = 0

        DEVICENAME                  = '/dev/ttyUSB0'
        self.TORQUE_ENABLE          = 1                 # Value for enabling the torque
        self.TORQUE_DISABLE         = 0                 # Value for disabling the torque
        #DXL_MOVING_STATUS_THRESHOLD = 20               # Dynamixel moving status threshold
        
        # Initialize PortHandler and PacketHandler
        self.portHandler = PortHandler(DEVICENAME)
        self.packetHandler = PacketHandler(PROTOCOL_VERSION)
        # Open port
        if self.portHandler.openPort():
            print(self.DXL_ID, ":Succeeded to open the port")
        else:
            print(self.DXL_ID, ":Failed to open the port.")
        # Set port baudrate
        if self.portHandler.setBaudRate(self.BAUDRATE):
            print(self.DXL_ID, ":Succeeded to change the baudrate to ", self.BAUDRATE)
        else:
            print(self.DXL_ID, ":Failed to change the baudrate.")

    #Engage motor
    def torqueOn(self):
        dxl_comm_result, dxl_error = self.packetHandler.write1ByteTxRx(self.portHandler, self.DXL_ID, self.ADDR_TORQUE_ENABLE, self.TORQUE_ENABLE)
        if dxl_comm_result != COMM_SUCCESS:
            print("torqueOn:%s" % self.packetHandler.getTxRxResult(dxl_comm_result))
        elif dxl_error != 0:
            print("torqueOn:%s" % self.packetHandler.getRxPacketError(dxl_error))

    #Disengage motor
    def torqueOff(self):
        # Enable Dynamixel Torque
        dxl_comm_result, dxl_error = self.packetHandler.write1ByteTxRx(self.portHandler, self.DXL_ID, self.ADDR_TORQUE_ENABLE, self.TORQUE_DISABLE)
        if dxl_comm_result != COMM_SUCCESS:
            print("torqueOff:%s" % self.packetHandler.getTxRxResult(dxl_comm_result))
        elif dxl_error != 0:
            print("torqueOff:%s" % self.packetHandler.getRxPacketError(dxl_error))

    #Close port
    def closePort(self):
        self.portHandler.closePort()

    #Collect current servo motor position
    def getCurrentPotision(self):
        self.PRESENT_POSITION, dxl_comm_result, dxl_error = self.packetHandler.read4ByteTxRx(self.portHandler, self.DXL_ID, self.ADDR_PRESENT_POSITION)
        if dxl_comm_result != COMM_SUCCESS:
            print(self.DXL_ID, ":getCurrentPotision:1:%s" % self.packetHandler.getTxRxResult(dxl_comm_result))
        elif dxl_error != 0:
            print(self.DXL_ID, ":getCurrentPotision:2:%s" % self.packetHandler.getRxPacketError(dxl_error))

    #Set target position
    def setGoalPotision(self, GOAL_POSITION_TARGET):
        self.GOAL_POSITION=GOAL_POSITION_TARGET
        dxl_comm_result, dxl_error = self.packetHandler.write4ByteTxRx(self.portHandler, self.DXL_ID, self.ADDR_GOAL_POSITION, self.GOAL_POSITION+self.POSITION_OFFSET)
        if dxl_comm_result != COMM_SUCCESS:
            print(self.DXL_ID, ":setGoalPotision:1:%s" % self.packetHandler.getTxRxResult(dxl_comm_result))
        elif dxl_error != 0:
            print(self.DXL_ID, ":setGoalPotision:2:%s" % self.packetHandler.getRxPacketError(dxl_error))

    #Set servo motor speed
    def setSpeed(self,speed,turn):
        if speed >=250:
            speed=250
        if speed <=-250:
            speed=-250
        if turn==0:
            self.speedMotor1=speed
        if turn<0 and turn >-300:
            self.speedMotor1=speed + turn * self.DXL1_left
        if turn>0 and turn <300:
            self.speedMotor1=speed + turn * self.DXL1_right
        if turn>=300:
            self.speedMotor1=speed * self.DXL1_leftright
        if turn<=-300:
            self.speedMotor1= -speed * self.DXL1_leftright
        if self.speedMotor1>250:
            self.speedMotor1=250
        if self.speedMotor1<-250:
            self.speedMotor1=-250

    #Update speed
    def updateSpeed(self):
        dxl_comm_result, dxl_error = self.packetHandler.write4ByteTxRx(self.portHandler, self.DXL_ID, self.ADDR_GOAL_VELOCITY, self.speedMotor1 * self.DXL1_orientation)
        if dxl_comm_result != COMM_SUCCESS:
            print("1 %s" % self.packetHandler.getTxRxResult(dxl_comm_result))
        elif dxl_error != 0:
            print("2 %s" % self.packetHandler.getRxPacketError(dxl_error))

    #Get current speed
    def getCurrentSpeed(self):
        self.speedNowMotor1, dxl_comm_result, dxl_error = self.packetHandler.read4ByteTxRx(self.portHandler, self.DXL_ID, self.ADDR_PRESENT_VELOCITY)
        # convert unsigned integer values to signed integer for readability
        if self.speedNowMotor1>1024: 
            self.speedNowMotor1-=2**32
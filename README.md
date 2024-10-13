# ISEF 2024 ETSD037 Rescue UAV Dual Tilt Rotor Control
## Python Codes
- `dxl_uav_class.py`: Class definition for Dynamixel servo motor control, migrated from Dynamixel example from Robotis
- `uav_control_v1.py`: In-arm pitch axis and roll control demonstration at a on-board JETSON Orin mission controller
## Operation
- It requires Dynamixel python library installed (https://emanual.robotis.com/docs/en/software/dynamixel/dynamixel_sdk/overview/).
- `python uav_control_v1.py`
- It printes an operation instrcution on screen.
```
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
```
## Example
![sample image](https://github.com/Cinderpe1t/ISEF_UAV_rescue_tilt_rotor/blob/main/Dual-axis%20tilt%20rotor%20test.png)

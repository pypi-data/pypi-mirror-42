'''
Created on 30.12.2018

@author: ED
'''

if __name__ == '__main__':
    pass

import PyTrinamic
from PyTrinamic.connections.serial_tmcl_interface import serial_tmcl_interface
from PyTrinamic.modules.TMCM_1640 import TMCM_1640

PyTrinamic.showInfo()
PyTrinamic.showAvailableComPorts()

myInterface = serial_tmcl_interface('COM9')
tmcm1640 = TMCM_1640(myInterface)

" motor configuration "
tmcm1640.setMotorPoles(8)
tmcm1640.setHallInvert(0)
tmcm1640.setMaxTorque(4000)

" show hall configuration "
tmcm1640.showHallConfiguration()

" motion settings "
tmcm1640.setAcceleration(2000)
tmcm1640.setRampEnabled(1)

# SAP 7, 0, 500     // target reached velocity
# SAP 10, 0, 5     // target reached distance

" show motion configuration "
tmcm1640.showMotionConfiguration()



# 
# //=== current PID values ===
# SAP 172, 0, 600   // P
# SAP 173, 0, 600   // I
# 
# //=== velocity PID values ===
# SAP 234, 0, 800 // P
# SAP 235, 0, 600 // I
# 
# //=== position PID values ===
# SAP 230, 0, 300    // P

# // === the test programm ===

# SAP 164, 0, 0             // deactivate left and right stop switch input
# 
# WAIT TICKS, 0, 100
# 
# SAP 159, 0, 6             // set commutation mode to FOC based on hall sensor signals
# 
# WAIT TICKS, 0, 100
# 
# SAP 1, 0, 0                 // set position counter to zero
# 
# MVP ABS, 0, 0
# WAIT TICKS, 0, 100

# // positioning test
# RepeatPositioningTest:
# 
#     MVP ABS, 0, 10000
#     CheckPosAReached:
#         GAP 1, 0
#         COMP 9990    // allow a small deviation 
#         JC LT, CheckPosAReached
# 
#     WAIT Ticks, 0, 300
# 
#     MVP ABS, 0, 0
#     CheckPosBReached:
#         GAP 1, 0
#         COMP 10      // allow a small deviation 
#         JC GT, CheckPosBReached
# 
#     WAIT Ticks, 0, 300
#         
#     JA RepeatPositioningTest

myInterface.close()
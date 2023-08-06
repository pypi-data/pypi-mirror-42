'''
Created on 25.02.2019

@author: ED
'''

class TMCM_1640(object):
    
    AP_TargetPosition               = 0
    AP_ActualPosition               = 1
    AP_TargetVelocity               = 2
    AP_ActualVelocity               = 3
    AP_MaxVelocity                  = 4
    AP_MaxTorque                    = 6
    AP_TargetReachedVelocity        = 7
    AP_MotorHaltedVelocity          = 9
    AP_TargetReachedDistance        = 10 
    AP_Acceleration                 = 11
    AP_RampVelocity                 = 13
    AP_ThermalWindingTimeConstant   = 25
    AP_IItlimit                     = 26
    AP_IItSum                       = 27
    AP_IItExceededCounter           = 28
    AP_ClearIItExceededFlag         = 29
    AP_ReinitBldcRegulation         = 31
    AP_EnableRamp                   = 146
    AP_ActualTorque                 = 150
    AP_SupplyVoltage                = 151
    AP_DriverTemperature            = 152
    AP_TargetTorque                 = 155
    AP_StatusFlags                  = 156
    AP_CommutationMode              = 159
    AP_ClearOnNull                  = 161
    AP_ClearOnce                    = 163
    AP_EncoderOffset                = 165
    AP_TorqueP                      = 172
    AP_TorqueI                      = 173
    AP_StartCurrent                 = 177
    AP_CurrentPIDError              = 200
    AP_CurrentPIDErrorSum           = 201
    AP_ActualHallAngle              = 210
    AP_ActualEncoderAngle           = 211
    AP_ActualControlledAngle        = 212
    AP_PositionPIDError             = 226
    AP_VelocityPIDError             = 228
    AP_VelocityPIDErrorSum          = 229
    AP_PositionP                    = 230
    AP_VelocityP                    = 234
    AP_VelocityI                    = 235
    AP_InitVelocity                 = 241
    AP_InitSineDelay                = 244
    AP_EncoderInitMode              = 249
    AP_EncoderSteps                 = 250
    AP_EncoderDirection             = 251
    AP_HallInterpolation            = 252
    AP_MotorPoles                   = 253
    AP_HallSensorInvert             = 254
    
    def __init__(self, connection):
        self.connection = connection
        self.motor = 0

    def maxVelocity(self):
        return self.connection.getAxisParameter(self.AP_MaxVelocity, self.motor).value
    
    def setMaxVelocity(self, maxVelocity):
        return self.connection.setAxisParameter(self.AP_MaxVelocity, maxVelocity)
    
    def maxTorque(self):
        return self.connection.getAxisParameter(self.AP_MaxTorque, self.motor).value
        
    def setMaxTorque(self, maxTorque):
        self.connection.setAxisParameter(self.AP_MaxTorque, self.motor, maxTorque)

    def acceleration(self):
        return self.connection.getAxisParameter(self.AP_Acceleration, self.motor).value

    def setAcceleration(self, acceleration):
        self.connection.setAxisParameter(self.AP_Acceleration, self.motor, acceleration)

    def rampEnabled(self):
        return self.connection.getAxisParameter(self.AP_EnableRamp, self.motor).value
    
    def setRampEnabled(self, enable):
        self.connection.setAxisParameter(self.AP_EnableRamp, self.motor, enable) 

    def motorPoles(self):
        return self.connection.getAxisParameter(self.AP_MotorPoles, self.motor).value
    
    def setMotorPoles(self, poles):
        self.connection.setAxisParameter(self.AP_MotorPoles, self.motor, poles)
        
    def hallInvert(self):
        return self.connection.getAxisParameter(self.AP_HallSensorInvert, self.motor).value
    
    def setHallInvert(self, invert):
        self.connection.setAxisParameter(self.AP_HallSensorInvert, self.motor, invert)

    def showHallConfiguration(self):
        print("Hall configuration:")
        print("\tMotor poles: " + str(self.motorPoles()))
        print("\tMax torque:  " + str(self.maxTorque()) + " mA")
        print("\tHall invert: " + str(self.hallInvert()))

    def showMotionConfiguration(self):
        print("Motion configuration:")
        print("\tMax velocity: " + str(self.maxVelocity()))
        print("\tAcceleration: " + str(self.acceleration()))
        print("\tRamp enabled: " + ("disabled" if (self.rampEnabled()==0) else "enabled"))
        
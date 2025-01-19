import pykos
import time
# KOS = pykos.KOS('Z-6.kscale.lan') 
client = pykos.KOS('10.33.11.192') 

sleep_int = 1

ACTUATOR_NAME_TO_ID = {
    "left_shoulder_yaw": 11,
    "left_shoulder_pitch": 12,
    "left_elbow_yaw": 13,
    "left_gripper": 14,
    "right_shoulder_yaw": 21,
    "right_shoulder_pitch": 22,
    "right_elbow_yaw": 23,
    "right_gripper": 24,
    "left_hip_yaw": 31,
    "left_hip_roll": 32,
    "left_hip_pitch": 33,
    "left_knee_pitch": 34,
    "left_ankle_pitch": 35,
    "right_hip_yaw": 41,
    "right_hip_roll": 42,
    "right_hip_pitch": 43,
    "right_knee_pitch": 44,
    "right_ankle_pitch": 45,
}

ACTUATOR_ID_TO_NAME = {v: k for k, v in ACTUATOR_NAME_TO_ID.items()}

# Zero the IMU with default parameters
response = client.imu.zero(duration=1.0)
if response.success:
    print("IMU zeroed successfully.")
else:
    print(f"Failed to zero IMU: {response.error}")

# Get basic IMU sensor values
imu_values = client.imu.get_imu_values()
print(f"Accelerometer X: {imu_values.accel_x}")
print(f"Gyroscope Z: {imu_values.gyro_z}")

# Configure actuator with ID 11
def configure_actuator(id):
    response = client.actuator.configure_actuator(
        actuator_id=id,
        kp=32,
        kd=32,
        ki=32,
        max_torque=100.0,
        torque_enabled=True,
        zero_position=True
    )
    if response.success:
        print(f"Actuator {id} configured successfully.")
    else:
        print(f"Failed to configure actuator {id}: {response.error}")

configure_actuator(11)
configure_actuator(12)
configure_actuator(13)
configure_actuator(21)
configure_actuator(22)
configure_actuator(23)
configure_actuator(14)
configure_actuator(24)
configure_actuator(31)
configure_actuator(32)
configure_actuator(33)
configure_actuator(34)
configure_actuator(35)
configure_actuator(41)
configure_actuator(42)
configure_actuator(43)
configure_actuator(44)
configure_actuator(45)

def activate(client, commands):
    response = client.actuator.command_actuators(commands)
# print(response)
    for result in response:
        if result.success:
            print(f"Actuator {result.actuator_id} commanded successfully.")
        else:
            print(f"Failed to command actuator {result.actuator_id}: {result.error}")

def activate_limbs(client, activate, out_commands, in_commands):
    activate(client, out_commands)
    time.sleep(sleep_int)
    activate(client, in_commands)
    time.sleep(sleep_int)

#
# START TESTS
#
SHOULDERS_OUT = [
    {"actuator_id": 11, "position": -30.0}, # left shoulder out
    {"actuator_id": 21, "position": 30.0}  # right shoulder out
]

SHOULDERS_IN = [
    {"actuator_id": 11, "position": 5.0},  # left shoulder in
    {"actuator_id": 21, "position": -5.0}   # right shoulder in
]

activate_limbs(client, activate, SHOULDERS_OUT, SHOULDERS_IN)

ARMS_BACK = [
    {"actuator_id": 12, "position": -30.0}, # left arm back 
    {"actuator_id": 22, "position": 30.0} # right arm back 

]

ARMS_FORWARD = [
    {"actuator_id": 12, "position": 5.0}, # left arm forward 
    {"actuator_id": 22, "position": -5.0} # right arm forward 

]

activate_limbs(client, activate, ARMS_BACK, ARMS_FORWARD)

ELBOW_BACK = [
    {"actuator_id": 13, "position": 30.0}, # left elbow back 
    {"actuator_id": 23, "position": -30.0} # right elbow back 
]

ELBOW_FORWARD = [
    {"actuator_id": 13, "position": -5.0}, # left elbow forward 
    {"actuator_id": 23, "position": 5.0} # right elbow forward 
]

activate_limbs(client, activate, ELBOW_BACK, ELBOW_FORWARD)

GRIPPERS_OPEN = [
    {"actuator_id": 14, "position": -30.0}, # left gripper open
    {"actuator_id": 24, "position": 30.0} # right gripper open
]

GRIPPERS_CLOSED = [
    {"actuator_id": 14, "position": 10.0}, # left gripper close
    {"actuator_id": 24, "position": -10.0} # right gripper close

]

activate_limbs(client, activate, GRIPPERS_OPEN, GRIPPERS_CLOSED)

HIPS_OUT = [
    {"actuator_id": 31, "position": -30.0}, # left hip out
    {"actuator_id": 41, "position": 30.0} # right hip out
]

HIPS_IN = [
    {"actuator_id": 31, "position": 5.0}, # left hip in
    {"actuator_id": 41, "position": -5.0} # left hip in
]

activate_limbs(client, activate, HIPS_OUT, HIPS_IN)

LEGS_OUT = [
    {"actuator_id": 32, "position": 30.0}, # left leg out  
    {"actuator_id": 42, "position": -30.0} # right leg out  

]

LEGS_IN = [
    {"actuator_id": 32, "position": -5.0}, # left leg back  
    {"actuator_id": 42, "position": 5.0} # right leg in  
]

activate_limbs(client, activate, LEGS_OUT, LEGS_IN)

THIGH_BACK = [
    {"actuator_id": 33, "position": 30.0}, # left thigh back
    {"actuator_id": 43, "position": -30.0} # right thigh back  
]

THIGH_FORWARD = [
    {"actuator_id": 33, "position": -5.0}, # left thigh forward 
    {"actuator_id": 43, "position": 5.0} # right thigh forward 
]

activate_limbs(client, activate, THIGH_BACK, THIGH_FORWARD)


SHIN_BACK = [
    {"actuator_id": 34, "position": 30.0}, # left shin back
    {"actuator_id": 44, "position": -30.0} # right shin back  
]

SHIN_FORWARD = [
    {"actuator_id": 34, "position": -5.0}, # left shin forward 
    {"actuator_id": 44, "position": 5.0} # right shin forward 
]

activate_limbs(client, activate, SHIN_BACK, SHIN_FORWARD)

FOOT_OUT = [
    {"actuator_id": 35, "position": -30.0}, # left foot out  
    {"actuator_id": 45, "position": 30.0} # right foot back 

]

FOOT_IN = [
    {"actuator_id": 35, "position": 5.0}, # left foot back 
    {"actuator_id": 45, "position": -5.0} # right foot forward 

]

activate_limbs(client, activate, FOOT_OUT, FOOT_IN)


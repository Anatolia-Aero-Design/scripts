import rospy
from sensor_msgs.msg import Imu, BatteryState
from nav_msgs.msg import Odometry
from std_msgs.msg import Float64
from message_filters import Subscriber, ApproximateTimeSynchronizer
from sensor_msgs.msg import NavSatFix
from geometry_msgs.msg import TwistStamped
from utils import quaternion_to_euler , calculate_speed

def callback(imu_msg, battery_msg, global_position_msg, rel_altitude_msg, position_msg, speed_sub):
    print("IHA_enlem : ",position_msg.latitude)
    print("IHA_boylam : ",position_msg.longitude)
    print("IHA_irtifa : ", rel_altitude_msg.data)
    print(f"IHA_yonelme : {imu_msg.orientation.x}\nIHA_dikilme : {imu_msg.orientation.y}\nIHA_yatis : {imu_msg.orientation.z}")
    yaw , pitch , roll  = quaternion_to_euler(imu_msg.orientation.x, imu_msg.orientation.y,imu_msg.orientation.z , imu_msg.orientation.w )
    print("IHA_hiz : ", calculate_speed(speed_sub.twist.linear.x , speed_sub.twist.linear.y , speed_sub.twist.linear.z))
    print("IHA_batarya: ", int(battery_msg.percentage * 100))
    print("IHA_otonom : 0")
    print(" ")
    
    



def synchronize_topics():
    rospy.init_node('sync_node', anonymous=True)

    imu_sub = Subscriber('/mavros/imu/data', Imu)
    battery_sub = Subscriber('/mavros/battery', BatteryState)
    global_position_sub = Subscriber('/mavros/global_position/local', Odometry)
    rel_altitude_sub = Subscriber('/mavros/global_position/rel_alt', Float64)
    position_sub = Subscriber('/mavros/global_position/global' , NavSatFix)
    speed_sub = Subscriber('/mavros/local_position/velocity_local', TwistStamped)

    # ApproximateTimeSynchronizer to synchronize messages based on timestamps
    sync = ApproximateTimeSynchronizer(
        [imu_sub, battery_sub, global_position_sub, rel_altitude_sub, position_sub, speed_sub],
        queue_size=10,
        slop=0.1, # Adjust this parameter based on your message timestamp tolerances
        allow_headerless=True
    )
    sync.registerCallback(callback)

    rospy.spin()

if __name__ == '__main__':
    synchronize_topics()

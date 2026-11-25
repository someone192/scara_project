from ik_node import ik

import rclpy
from rclpy.action import ActionClient
from rclpy.executors import ExternalShutdownException
from rclpy.node import Node

from control_msgs.action import FollowJointTrajectory
from trajectory_msgs.msg import JointTrajectoryPoint
from builtin_interfaces.msg import Duration

import logging
import threading
import traceback

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


L1 = 0.15
L2 = 0.15

# angles = ik(goal[0], goal[1], L1, L2)

class TrajectoryActionClient(Node):

    def __init__(self):
        super().__init__("trajectory_action_client")
        self._action_client = ActionClient(self, FollowJointTrajectory, "joint_trajectory_controller/follow_joint_trajectory")

    def send_goal(self, x, y):
        
        # goal: list[float] = [float(input("x_goal: ")), float(input("y_goal: "))]
        goal_msg = FollowJointTrajectory.Goal()
        goal_msg.trajectory.joint_names = ['joint1', 'joint2']

        point = JointTrajectoryPoint()

        point.positions = ik(x, y, L1, L2)

        point.time_from_start = Duration(sec=3, nanosec=0)

        goal_msg.trajectory.points.append(point)

        self._action_client.send_goal_async(goal_msg).add_done_callback(self.goal_response_callback)
        
        # self._action_client.wait_for_server()

        # self._send_goal_future = self._action_client.send_goal_async(goal_msg, feedback_callback = self.feedback_callback)

        # self._send_goal_future.add_done_callback(self.goal_response_callback)

    def goal_response_callback(self, future):

        goal_handle = future.result()

        if not goal_handle.accepted:
            self.get_logger().info("Goal rejected")
            return

        self.get_logger().info("Goal accepted")

        goal_handle.get_result_async().add_done_callback(self.get_result_callback)

        # self._get_result_future = goal_handle.get_result_async()
        # self._get_result_future.add_done_callback(self.get_result_callback)

    def get_result_callback(self, future):
        result = future.result().result
        if result.error_code == 0:
            self.get_logger().info('Result: SUCCESSFULL')
        # rclpy.shutdown()

    def feedback_callback(self, feedback_msg):
        feedback = feedback_msg.feedback

        self.get_logger().info('Recieved feedback: {0}'.format(feedback.actual))

def input_loop(node):
    print("Write x y in meters, or q to exit")
    while rclpy.ok():
        try:
            line = input('input >')
        except EOFError:
            break
        if not line:
            continue
        if line.lower() in ('q', 'quit', 'exit', 'stop'):
            logger.info('the input stopped by command')
            break

        try:
            x_str, y_str = line.split()
            x, y = float(x_str), float(y_str)
            node.send_goal(x, y)
        except ValueError:
            node.get_logger().warning("format: two numbers with a space between them")
        except Exception:
            node.get_logger().error('An unexpected error occured:\n'
                                     + traceback.format_exc())

    if rclpy.ok():
        rclpy.shutdown()



def main(args=None):
    try:
        with rclpy.init(args=args):

            action_client = TrajectoryActionClient()

            threading.Thread(target=input_loop, args=(action_client,), daemon=True).start()

            try:

            # action_client.send_goal()

                rclpy.spin(action_client)
            except (KeyboardInterrupt, ExternalShutdownException):
                pass
            finally:
                action_client.destroy_node()
                if rclpy.ok():
                    rclpy.shutdown()

    except (KeyboardInterrupt, ExternalShutdownException):
        pass

if __name__ == "__main__":
    main()
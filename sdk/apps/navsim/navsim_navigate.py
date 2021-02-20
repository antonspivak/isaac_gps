'''
Copyright (c) 2020, NVIDIA CORPORATION. All rights reserved.

NVIDIA CORPORATION and its licensors retain all intellectual property
and proprietary rights in and to this software, related documentation
and any modifications thereto. Any use, reproduction, disclosure or
distribution of this software and related documentation without an express
license agreement from NVIDIA CORPORATION is strictly prohibited.
'''
from isaac import Application
import argparse

import csv
from isaac import *
class PingPython(Codelet):
    def start(self):
        self.rx = self.isaac_proto_rx("Plan2Proto", "imu")
        self.rx1 = self.isaac_proto_rx("Odometry2Proto", "feedback")
        self.tx = self.isaac_proto_tx("Odometry2Proto", "odometry")
        self.tick_on_message(self.rx1)
        #with open('/home/ivan/Desktop/data.csv', 'w', newline='') as file:
        #    writer = csv.writer(file)
        #    writer.writerow(["real_x", "real_y", "odom_x", "odom_y", "gps_x", "gps_y"])

    def tick(self):
        plan_pos_x = False
        odom_x = False
        if self.rx.message:
            rx_message = self.rx.message
            received = rx_message.proto
            states = received.states[0]
            plan_pos_x = states.positionX
            plan_pos_y = states.positionY
            #print('plan pos x= ', plan_pos_x)
        if self.rx1.message:
            rx_message1 = self.rx1.message
            received1 = rx_message1.proto
            odom_x = received1.odomTRobot.translation.x #+ 0.5
            odom_y = received1.odomTRobot.translation.y
            #print("-----received-----")
            print(received1)
            #print('x = ', odom_x)
            #print('y = ', odom_y)
            print("----------")
            tx_message = self.tx.init()
            send_message = tx_message.proto
            send_message.odomTRobot
            send_message.odomTRobot.translation
            send_message.odomTRobot.translation.x = odom_x #- 2
            send_message.odomTRobot.translation.y = odom_y -1

            send_message.odomTRobot.rotation
            send_message.odomTRobot.rotation.q
            send_message.odomTRobot.rotation.q.x = received1.odomTRobot.rotation.q.x
            send_message.odomTRobot.rotation.q.y = received1.odomTRobot.rotation.q.y

            send_message.speed
            send_message.speed.x = received1.speed.x
            send_message.speed.y = received1.speed.y

            send_message.angularSpeed = received1.angularSpeed

            send_message.acceleration
            send_message.acceleration.x = received1.acceleration.x
            send_message.acceleration.y = received1.acceleration.y

            send_message.odometryFrame = received1.odometryFrame

            send_message.robotFrame = received1.robotFrame

            self.tx.publish()
            print('send_to', send_message)
        #import random
        #if (plan_pos_x and odom_x):
        #    with open('/home/ivan/Desktop/data.csv', 'a', newline='') as file:
        #        writer = csv.writer(file)
        #        writer.writerow(['{0:.5f}'.format(plan_pos_x), '{0:.5f}'.format(plan_pos_y), '{0:.5f}'.format(odom_x), '{0:.5f}'.format(odom_y), '{0:.5f}'.format(random.uniform(plan_pos_x-0.15, plan_pos_x+0.15)),'{0:.5f}'.format(random.uniform(plan_pos_y-0.15, plan_pos_y+0.15))])




if __name__ == '__main__':
    # Parse arguments
    parser = argparse.ArgumentParser(description="Navsim navigation app")
    parser.add_argument(
        "--map_json",
        help="The path to the map json to load",
        default="apps/assets/maps/virtual_small_warehouse.json")
    parser.add_argument(
        "--robot_json",
        help="The path to the robot json to load",
        default="packages/navsim/robots/carter.json")
    parser.add_argument(
        "--more",
        help="A comma separated list of additional json files to load")
    parser.add_argument(
        "--mission_robot_name",
        help="Accept missions from the remote mission server for the robot with the given name")
    parser.add_argument(
        "--mission_host",
        help="The ip address or hostname of the host to connect to and receive missions from",
        default="localhost")
    parser.add_argument(
        "--mission_port",
        help="The TCP port to connect to the mission server",
        type=int,
        default=9998)
    args = parser.parse_args()

    # Create and start the app
    more_jsons = args.map_json + "," + args.robot_json
    if args.more:
        more_jsons += "," + args.more
    app_path = "apps/navsim/navsim_navigate.app.json"
    app = Application(app_filename=app_path, more_jsons=more_jsons)

    if args.mission_robot_name:
        # Load the mission subgraph and set the config based on the input parameters
        app.load(
            "packages/behavior_tree/apps/missions.graph.json")
        app.nodes["tcp_client"].components["JsonTcpClient"].config["host"] = args.mission_host
        app.nodes["tcp_client"].components["JsonTcpClient"].config["port"] = args.mission_port
        app.nodes["mission_control"].components["NodeGroup"].config["node_names"] = \
            ["goals.goal_behavior"]
        app.nodes["robot_name"].components["JsonMockup"].config["json_mock"] = \
            {"text":args.mission_robot_name}
        app.nodes["goals.goal_behavior"].config["disable_automatic_start"] = True
        # Send the navigation output back through the json tcp client
        app.connect(app.nodes["navigation.subgraph"].components["interface"], "feedback",
            app.nodes["tcp_client"].components["JsonTcpClient"], "feedback")
    ###########################
    app.nodes["ping_node"].add(name='PingPython', ctype=PingPython)

    app.connect('navigation.imu_odometry.odometry/DifferentialBaseWheelImuOdometry', 'odometry',
               'ping_node/PingPython', 'feedback')
    #app.connect('simulation.scenario_manager/scenario_manager', 'robot',
    #            'ping_node/PingPython', 'feedback')
    #app.connect('simulation.interface/pose_injector', 'pose',
     #            'ping_node/PingPython', 'feedback')

    #app.connect('navigation.control.lqr/isaac.lqr.DifferentialBaseLqrPlanner', 'plan',
    #               'ping_node/PingPython', 'feedback')




    #app.connect('navigation.control.lqr/isaac.lqr.DifferentialBaseLqrPlanner', 'plan',
    #            'ping_node/PingPython', 'imu')





    #app.connect('simulation.interface/output', 'imu_raw',
    #            'ping_node/PingPython', 'imu')

    #app.connect('navigation.go_to.goal_monitor/GoalMonitor', 'feedback',
    #            'ping_node/PingPython', 'imu')

    app.connect('ping_node/PingPython', 'odometry',
                'navigation.control.trajectory_validation/TrajectoryValidation', 'odometry')

    app.connect('ping_node/PingPython', 'odometry',
                'navigation.control.lqr/isaac.lqr.DifferentialBaseLqrPlanner', 'odometry')

    app.run()

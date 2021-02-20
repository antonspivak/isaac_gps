from isaac import *
from navigation_system import NavigationSystem

class SendcorPython(Codelet):
    def start(self):
        self.navigation_system = NavigationSystem()
        self.tx = self.isaac_proto_tx("Vector2dProto", "odometry")
        self.tick_periodically(1.0)

    def tick(self):
        lat, lon = self.navigation_system.get_gps()
        print('original coordinates: ', lat, lon)
        tx_message = self.tx.init()
        tx_message.proto.x = lat
        tx_message.proto.y = lon
        self.tx.publish()

class PingPython(Codelet):
    def start(self):
        self.rx = self.isaac_proto_rx("Vector2dProto", "odometry")

        self.tick_on_message(self.rx)

    def tick(self):
        rx_message = self.rx.message
        received = rx_message.proto
        print("-----received-----")
        print('lat=', received.x)
        print('lon=', received.y)
        print("----------")
        print("")


def main():
    app = Application(app_filename="apps/tutorials/ping_python/ping_python.app.json")

    app.load_module("sight")
    app.nodes["ping_node"].add(name='PingPython', ctype=PingPython)
    app.nodes["sendcor_node"].add(name='SendcorPython', ctype=SendcorPython)
    #app.connect('sendcor_node/SendcorPython', 'odometry',
    #            'ping_node/PingPython', 'odometry')

    app.connect('sendcor_node/SendcorPython', 'odometry',
                'ping_node/PingPython', 'odometry')

    app.run()


if __name__ == '__main__':
    main()

from marvelmind import MarvelmindHedge
import csv
import sys
hedge = MarvelmindHedge(tty="/dev/ttyACM0", adr=None, debug=False)
hedge.start()

with open('/home/ivan/Desktop/coordinates.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["x", "y"])
    while True:
        try:
            hedge.dataEvent.wait(1)
            hedge.dataEvent.clear()

            if (hedge.positionUpdated):
                print('x: ', hedge.position()[1])
                print('y: ', hedge.position()[2])
                writer.writerow([hedge.position()[1], hedge.position()[2]])
        except KeyboardInterrupt:
            hedge.stop()
            sys.exit()

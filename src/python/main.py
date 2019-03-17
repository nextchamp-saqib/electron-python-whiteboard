import zerorpc

from newCalibration import Calibration
from detectIR import Start
from printSomething import printSomething

calibratedCoordinates = [0, 0]
cameraIP = [0, 0]


def calibrate():
    global cameraIP
    coordinates, last_frame = Calibration(cameraIP[0])
    calibratedCoordinates[0] = coordinates
    return str(coordinates)


def detect():
    global cameraIP
    Start(calibratedCoordinates[0], cameraIP[0])
    return "Done"


def setIPAddress(ipAddr):
    global cameraIP
    cameraIP[0] = str(ipAddr)
    return "Done"


class MainHandler(object):
    def startCalibrating(self):
        return calibrate()

    def printSomethingFunc(self):
        return printSomething()

    def listenForIR(self):
        return detect()

    def setIpAddress(self, ipAddr):
        return setIPAddress(ipAddr)


if __name__ == "__main__":
    addr = "tcp://127.0.0.1:1122"
    server = zerorpc.Server(MainHandler())
    server.bind(addr)
    print("start running on {}".format(addr))
    server.run()

# calibrate()

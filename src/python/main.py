import zerorpc

# from detectIR import Start
from newCalibration import Calibration
from perspective import correct
from printSomething import printSomething

coordinates = []


def calibrate():
    coordinates, last_frame = Calibration()
    # correct(coordinates) # save calibrated points on an image
    return "Done"


class MainHandler(object):
    def startCalibrating(self):
        return calibrate()

    def printSomethingFunc(self):
        return printSomething()


# if __name__ == "__main__":
#     addr = "tcp://127.0.0.1:1122"
#     server = zerorpc.Server(MainHandler())
#     server.bind(addr)
#     print("start running on {}".format(addr))
#     server.run()

calibrate()
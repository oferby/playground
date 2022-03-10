import pickle


f = open("demofile1.txt", "wb")
#
# # b = bytearray("Now the file has more content!")
#
# newFileBytes = [123, 3, 255, 0, 100]
# b = bytearray(newFileBytes)


class User:
    age = 0
    isAlive = True
    name = ''

    def __init__(self, name):
        self.name = name


u = User("Ofer")

pickle.dump(u, f)

f.close()

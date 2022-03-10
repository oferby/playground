import pickle


f = open("demofile1.txt", "rb")

class User:
    age = 0
    isAlive = True
    name = ''

    def __init__(self, name):
        self.name = name


u = pickle.load(f)

print(u.name)

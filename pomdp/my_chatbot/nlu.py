class RasaNLUInterpreter:
    def __init__(self, model_directory, ):
        from rasa_nlu.model import Interpreter
        self.interpreter = Interpreter.load(model_directory)

    def parse(self, text):
        return self.interpreter.parse(text)

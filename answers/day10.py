
class State:
    def run(self):
        assert 0, "NotImplementedError"
    def next(self, input):
        assert 0, "NotImplementedError"

class Enter(State):
    def run(self):
        pass
    def next(self, input):
        Encoder.c = input
        Encoder.prev_count = 1
        Encoder.prev = input
        Encoder.look_and_say = ""
        return Encoder.normal

class Normal(State):
    def run(self):
        pass
    def next(self, input):
        Encoder.c = input
        if Encoder.c == "":
            if Encoder.prev_count == 0:
                Encoder.look_and_say = Encoder.look_and_say + "1" + Encoder.prev
            else:
                Encoder.look_and_say = Encoder.look_and_say + f"{Encoder.prev_count}" + Encoder.prev
            return Encoder.end
        if Encoder.prev == Encoder.c:
            Encoder.prev_count +=1
        else:
            if Encoder.prev_count == 0:
                Encoder.look_and_say = Encoder.look_and_say + "1" + Encoder.prev
            else:
                Encoder.look_and_say = Encoder.look_and_say + f"{Encoder.prev_count}" + Encoder.prev
            Encoder.prev = Encoder.c
            Encoder.prev_count = 1
        return Encoder.normal

class End(State):
    def run(self):
        pass
    def next(self,input):
        raise RuntimeError("Input not supported for End state")

class Encoder:
    def __init__(self, initialState):
        Encoder.c = ""
        Encoder.prev = ""
        Encoder.prev_count = 0
        Encoder.look_and_say = ""
        self.currentState = initialState
        self.currentState.run()

    # Template method:
    def runAll(self, inputs):
        for i in inputs:
            self.currentState = self.currentState.next(i)
            self.currentState.run()
        self.currentState = self.currentState.next("")
        return Encoder.look_and_say

Encoder.enter = Enter()
Encoder.normal = Normal()
Encoder.end = End()

def run(input):
    data = input.read().strip()

    for i in range(50):
        encoder = Encoder(Encoder.enter)
        data = encoder.runAll(data)
        #print(data)
        print(f"step {i} len = {len(data)}")

import matplotlib.pyplot as plt
import numpy as np


class State:
    def run(self):
        assert 0, "NotImplementedError"

    def next(self, input):
        assert 0, "NotImplementedError"


class Fly(State):
    def run(self):
        pass

    def next(self, reindeer):
        reindeer.distance += reindeer._speed
        if reindeer.stamina > 1:
            reindeer.stamina -= 1
            reindeer.rest_level -= 1  # não é necessário, apenas para debug
            return Reindeer.flying
        else:
            reindeer.stamina = 0
            reindeer.rest_level = 1
            return Reindeer.resting

    def __repr__(self):
        return "Flying"


class Rest(State):
    def run(self):
        pass

    def next(self, reindeer):
        if reindeer.rest_level < reindeer._max_rest:
            reindeer.rest_level += 1
            return Reindeer.resting
        else:
            reindeer.rest_level = reindeer._max_rest
            reindeer.stamina = reindeer._max_stamina
            return Reindeer.flying

    def __repr__(self):
        return "Resting"


class Reindeer:
    flying = Fly()
    resting = Rest()

    def __init__(self, name, speed, stamina, rest_cycle):
        self.points = 0
        self.name = name
        self._speed = speed
        self.stamina = self._max_stamina = stamina
        self.rest_level = self._max_rest = rest_cycle
        self.distance = 0
        self.currentState = Fly()
        # self.currentState.run()

    def step(self):
        self.currentState = self.currentState.next(self)

    def __repr__(self):
        return f"{self.name}:{self.currentState} Star:{self.points} Travelled:{self.distance} Stamina:{self.stamina} RestLevel:{self.rest_level}"


"""
Dancer can fly 27 km/s for 5 seconds, but then must rest for 132 seconds.
Cupid can fly 22 km/s for 2 seconds, but then must rest for 41 seconds.
Rudolph can fly 11 km/s for 5 seconds, but then must rest for 48 seconds.
Donner can fly 28 km/s for 5 seconds, but then must rest for 134 seconds.
Dasher can fly 4 km/s for 16 seconds, but then must rest for 55 seconds.
Blitzen can fly 14 km/s for 3 seconds, but then must rest for 38 seconds.
Prancer can fly 3 km/s for 21 seconds, but then must rest for 40 seconds.
Comet can fly 18 km/s for 6 seconds, but then must rest for 103 seconds.
Vixen can fly 18 km/s for 5 seconds, but then must rest for 84 seconds.
"""


def run(input):
    _ = input.read()

    dancer = Reindeer("Dancer", 27, 5, 132)
    cupid = Reindeer("Cupid", 22, 2, 41)
    rudolph = Reindeer("Rudolph", 11, 5, 48)
    donner = Reindeer("Donner", 28, 5, 134)
    dasher = Reindeer("Dasher", 4, 16, 55)
    blitzen = Reindeer("Blitzen", 14, 3, 38)
    prancer = Reindeer("Prancer", 3, 21, 40)
    comet = Reindeer("Comet", 18, 6, 103)
    vixen = Reindeer("Vixen", 18, 5, 84)

    racers = [dancer, cupid, rudolph, donner, dasher, blitzen, prancer, comet, vixen]
    for _ in range(2503):
        for racer in racers:
            racer.step()
        # Give points to leaders
        leader_distance = max(r.distance for r in racers)
        current_leaders = filter(lambda r: r.distance == leader_distance, racers)
        for leader in current_leaders:
            leader.points += 1

    for r in racers:
        print(r)

    max_distance = max(r.distance for r in racers)
    print("Max travelled :", max_distance)
    max_points = max(r.points for r in racers)
    print("Max points :", max_points)

    """
    plt.rcdefaults()
    fig, ax = plt.subplots()

    y_pos = np.arange(len(racers))
    performance = np.array([r.distance for r in racers])

    ax.barh(y_pos, performance, align="center")
    ax.set_yticks(y_pos)
    ax.set_yticklabels(racers)
    ax.invert_yaxis()  # labels read top-to-bottom
    ax.set_xlabel("Distance")
    ax.set_title("How fast do you want to go today?")

    plt.show()
    # Comet can fly 14 km/s for 10 seconds, but then must rest for 127 seconds.
    # Dancer can fly 16 km/s for 11 seconds, but then must rest for 162 seconds.
    comet = Reindeer("Comet", 14, 10, 127)
    dancer = Reindeer("Dancer", 16, 11, 162)
    racers = [comet, dancer]
    for i in range(1, 1001):
        for racer in racers:
            racer.step()
        if i in (1, 10, 11, 12, 138, 139, 174, 175, 1000):
            print(f"Clock: {i}")
            for r in racers:
                print(r)
    """


# python -m ipdb script.py

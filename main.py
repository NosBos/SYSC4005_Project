# This is a sample Python script.
from Framework import Simulation
from Product import Product
from Component import Component
from Entities import Inspector, Buffer, WorkStation
import random
from inputModeling.generate_distributions import *

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


class ManufacturingSim(Simulation):
    def __init__(self, seed1):
        super(ManufacturingSim, self).__init__()
        max_amount = 300
        random_values = generate_random_values(max_amount * 5, seed)


        self.buffer1 = Buffer(self, "C1 WKS1 Buffer", Component.C1, 1)
        self.buffer2 = Buffer(self, "C1 WKS2 Buffer", Component.C1, 2)
        self.buffer3 = Buffer(self, "C2 WKS2 Buffer", Component.C2, 3)
        self.buffer4 = Buffer(self, "C1 WKS3 Buffer", Component.C1, 4)
        self.buffer5 = Buffer(self, "C3 WKS3 Buffer", Component.C3, 5)

        self.inspector1 = Inspector(self, "INSP1", [Component.C1], [self.buffer1, self.buffer2, self.buffer4], random_values[0:max_amount])
        self.inspector2 = Inspector(self, "INSP2", [Component.C2, Component.C3], [self.buffer3, self.buffer5], random_values[max_amount:max_amount * 2])

        self.workstation1 = WorkStation(self, "W1", Product.P1, [self.buffer1], random_values[max_amount * 2 :max_amount * 3])
        self.workstation2 = WorkStation(self, "W2", Product.P2, [self.buffer2, self.buffer3], random_values[max_amount * 3 :max_amount * 4])
        self.workstation3 = WorkStation(self, "W3", Product.P3, [self.buffer4, self.buffer5], random_values[max_amount * 4 :max_amount * 5])

        self.buffer1.add_work_station(self.workstation1)
        self.buffer2.add_work_station(self.workstation2)
        self.buffer3.add_work_station(self.workstation2)
        self.buffer4.add_work_station(self.workstation3)
        self.buffer5.add_work_station(self.workstation3)

        self.buffer1.add_inspector(self.inspector1)
        self.buffer2.add_inspector(self.inspector1)
        self.buffer3.add_inspector(self.inspector2)
        self.buffer4.add_inspector(self.inspector1)
        self.buffer5.add_inspector(self.inspector2)

        entity_list = [self.inspector1, self.inspector2, self.buffer1, self.buffer2, self.buffer3, self.buffer4, self.buffer5, self.workstation1, self.workstation2, self.workstation3]
        runtime = 200*Simulation.SECONDS
        self.run(entity_list, runtime)

    def _end(self, clock) -> None:
        #  probably worth outputting statistics of each into a file. Deal with all that within each entities end
        pass


if __name__ == "__main__":
    try:
        seed = int(input("Seed:"))
    except ValueError:
        print("That is not a whole number")
    random.seed(seed)
    sim = ManufacturingSim(seed)

import abc
import queue
from dataclasses import dataclass, field
from typing import Any
from abc import ABC, abstractmethod
import matplotlib.pyplot as plt


@dataclass(order=True)
class Event:
    time: float  # priority of event
    recipient: Any = field(compare=False)  # who shall receive the event
    item: Any = field(compare=False)  # the event information

    def __repr__(self):
        return f"{self.time} : {str(self.item)} "


class Result:
    def __init__(self):
        self.products_produced = 0
        self.p1_produced = 0
        self.p2_produced = 0
        self.p3_produced = 0
        self.inspector1_blocked_time = 0
        self.inspector2_blocked_time = 0
        self.buffer1_average_size = 0
        self.buffer2_average_size = 0
        self.buffer3_average_size = 0
        self.buffer4_average_size = 0
        self.buffer5_average_size = 0
        self.wk1_busy = 0
        self.wk2_busy = 0
        self.wk3_busy = 0
        self.products_produced = 0
        pass

    def __repr__(self):
        return f"{self.products_produced},{self.p1_produced},{self.p2_produced},{self.p3_produced},{self.inspector1_blocked_time},{self.inspector2_blocked_time}," \
               f"{self.buffer1_average_size},{self.buffer2_average_size},{self.buffer3_average_size},{self.buffer4_average_size},{self.buffer5_average_size}," \
               f"{self.wk1_busy},{self.wk2_busy},{self.wk3_busy},{self.products_produced}"

class Simulation(ABC):
    """
    Simulation base class. It handles everything to do with the future event list.
    User must define starting and ending simulation behaviour
    """
    SECONDS = 1
    MINUTES = 60
    HOURS = 3600
    SIMULATION_END = "SIMULATION END"

    def __init__(self, result):
        self.result = result
        self.clock = 0
        self.__future_event_list = queue.PriorityQueue()
        self.entity_list = []
        pass

    def run(self, entity_list, runtime=-1) -> None:
        """
        Runs the simulation from start() to end()
        :return: None
        """
        self.entity_list = entity_list
        self.__print_sim_table_header()
        self.__run(runtime=runtime)
        self._end(self.clock)
        pass

    def __run(self, runtime: float) -> None:
        # add ending event for timed simulations
        if runtime > 0:
            self.add_event(Event(runtime, self, Simulation.SIMULATION_END))
            pass

        previous_event = 0

        inspector1_previous_blocked_state = False
        inspector1_blocked_time = 0
        inspector2_previous_blocked_state = False
        inspector2_blocked_time = 0

        buffer1_time = [0,0,0]
        buffer1_occupancy = []
        buffer2_time = [0,0,0]
        buffer2_occupancy = []
        buffer3_time = [0,0,0]
        buffer3_occupancy = []
        buffer4_time = [0,0,0]
        buffer4_occupancy = []
        buffer5_time = [0,0,0]
        buffer5_occupancy = []

        # pop events and execute until there's none left or end event reached
        evt = ''

        while len(self.__future_event_list.queue):
            self.__print_sim_table_row()
            evt = self.__future_event_list.get()
            # I dont see where we can get the average buffer occupancy so Im going to get it here

            for entity in self.entity_list:
                if entity.name() == "INSP1":
                    isBlocked = entity.get_state()
                    if inspector1_previous_blocked_state:
                        inspector1_blocked_time += evt.time - self.clock
                    inspector1_previous_blocked_state = isBlocked
                elif entity.name() == "INSP2":
                    isBlocked = entity.get_state()
                    if inspector2_previous_blocked_state:
                        inspector2_blocked_time += evt.time - self.clock
                    inspector2_previous_blocked_state = isBlocked

                elif entity.name() == "C1 WKS1 Buffer":
                    buffer1_time[entity.get_state()] += evt.time - self.clock
                    buffer1_occupancy.append([evt.time, entity.get_state()])
                elif entity.name() == "C1 WKS2 Buffer":
                    buffer2_time[entity.get_state()] += evt.time - self.clock
                    buffer2_occupancy.append([evt.time, entity.get_state()])
                elif entity.name() == "C2 WKS2 Buffer":
                    buffer3_time[entity.get_state()] += evt.time - self.clock
                    buffer3_occupancy.append([evt.time, entity.get_state()])
                elif entity.name() == "C1 WKS3 Buffer":
                    buffer4_time[entity.get_state()] += evt.time - self.clock
                    buffer4_occupancy.append([evt.time, entity.get_state()])
                elif entity.name() == "C3 WKS3 Buffer":
                    buffer5_time[entity.get_state()] += evt.time - self.clock
                    buffer5_occupancy.append([evt.time, entity.get_state()])




            if evt.item == Simulation.SIMULATION_END:
                print("Inspector 1 Blocked Time: " + str(inspector1_blocked_time))
                print("Inspector 2 Blocked Time: " + str(inspector2_blocked_time))
                self.result.inspector1_blocked_time = inspector1_blocked_time
                self.result.inspector2_blocked_time = inspector2_blocked_time

                def get_average_buffer(buffer):
                    n = 0
                    value = 0
                    for index, val in enumerate(buffer):
                        n += val
                        value += val * index

                    return value / n


                print("Buffer 1 Occupancy Times: " + str(buffer1_time))
                print("Buffer 1 average: " + str(get_average_buffer(buffer1_time)))
                print("Buffer 2 Occupancy Times: " + str(buffer2_time))
                print("Buffer 2 average: " + str(get_average_buffer(buffer2_time)))
                print("Buffer 3 Occupancy Times: " + str(buffer3_time))
                print("Buffer 3 average: " + str(get_average_buffer(buffer3_time)))
                print("Buffer 4 Occupancy Times: " + str(buffer4_time))
                print("Buffer 4 average: " + str(get_average_buffer(buffer4_time)))
                print("Buffer 5 Occupancy Times: " + str(buffer5_time))
                print("Buffer 5 average: " + str(get_average_buffer(buffer5_time)))
                self.result.buffer1_average_size = get_average_buffer(buffer1_time)
                self.result.buffer2_average_size = get_average_buffer(buffer2_time)
                self.result.buffer3_average_size = get_average_buffer(buffer3_time)
                self.result.buffer4_average_size = get_average_buffer(buffer4_time)
                self.result.buffer5_average_size = get_average_buffer(buffer5_time)

                products_done = 0
                for entity in self.entity_list:
                    products_done += entity.products_done()
                    if entity.name() == "W1":
                        W1_busy_time = entity.time_busy
                        self.result.p1_produced +=entity.products_done()
                        pass
                    elif entity.name() == "W2":
                        W2_busy_time = entity.time_busy
                        self.result.p2_produced += entity.products_done()
                        pass
                    elif entity.name() == "W3":
                        W3_busy_time = entity.time_busy
                        self.result.p3_produced += entity.products_done()
                        pass
                print("Total number of products produced: " + str(products_done))
                print("WorkStation 1 busy time: " + str(W1_busy_time))
                print("WorkStation 2 busy time: " + str(W2_busy_time))
                print("WorkStation 3 busy time: " + str(W3_busy_time))
                self.result.products_produced = products_done
                self.result.wk1_busy = W1_busy_time
                self.result.wk2_busy = W2_busy_time
                self.result.wk3_busy = W3_busy_time

                def graph_buffer_occupancy(buffer_num):
                    if buffer_num == 1:
                        plt.plot([x[0] for x in buffer1_occupancy], [x[1] for x in buffer1_occupancy])
                        plt.title("Buffer C1 W1")
                        plt.xlabel("Time (minutes)")
                        plt.ylabel("Buffer occupancy")
                        plt.ylim([-0.05, 2.05])
                        plt.show()
                    elif buffer_num == 2:
                        plt.plot([x[0] for x in buffer2_occupancy], [x[1] for x in buffer2_occupancy])
                        plt.title("Buffer C1 W2")
                        plt.xlabel("Time (minutes)")
                        plt.ylabel("Buffer occupancy")
                        plt.ylim([-0.05, 2.05])
                        plt.show()
                    elif buffer_num == 3:
                        plt.plot([x[0] for x in buffer3_occupancy], [x[1] for x in buffer3_occupancy])
                        plt.title("Buffer C2 W2")
                        plt.xlabel("Time (minutes)")
                        plt.ylabel("Buffer occupancy")
                        plt.ylim([-0.05, 2.05])
                        plt.show()
                    elif buffer_num == 4:
                        plt.plot([x[0] for x in buffer4_occupancy], [x[1] for x in buffer4_occupancy])
                        plt.title("Buffer C1 W3")
                        plt.xlabel("Time (minutes)")
                        plt.ylabel("Buffer occupancy")
                        plt.ylim([-0.05, 2.05])
                        plt.show()
                    elif buffer_num == 5:
                        plt.plot([x[0] for x in buffer5_occupancy], [x[1] for x in buffer5_occupancy])
                        plt.title("Buffer C3 W3")
                        plt.xlabel("Time (minutes)")
                        plt.ylabel("Buffer occupancy")
                        plt.ylim([-0.05, 2.05])
                        plt.show()
                #for i in range(1, 6):
                #    graph_buffer_occupancy(i)

                break

            self.clock = evt.time
            evt.recipient.handle_event(evt)
            previous_event = evt
            pass
        pass

    def __print_sim_table_header(self):
        print('clock', end=',')
        for entity in self.entity_list:
            entity.start()
            print(entity.name(), end=',')
            pass
        print('FEL', end=',')
        print()
        pass

    def __print_sim_table_row(self):
        print(self.clock, end=',')
        for e in self.entity_list:
            e.print_state()
            pass
        print(f'"{str(self.__future_event_list.queue)}"')
        pass

    def __end(self) -> None:
        """
        Called when the simulation is done. Used to output all statistics
        :return: None
        """
        for entity in self.entity_list:
            entity.end(self.clock)
        pass

    def add_event(self, event: Event) -> None:
        """
        Adds an event with relative timing to the FEL
        :param event: the event
        :return: None
        """
        event.time += self.clock
        self.__future_event_list.put(event)
        pass

    pass


class Entity(ABC):
    """
    All active entities must inherit the Entity class.

    """

    def __init__(self, simulation: Simulation, name):
        self.__sim = simulation
        self.__name = name

    @abstractmethod
    def start(self) -> None:
        """
        Called right before the simulation starts. Used to add all the starting events to the FEL
        :return: None
        """
        pass

    @abstractmethod
    def handle_event(self, event: Event) -> None:
        """
        Called when an event occurs and the entity is the recipient
        :param event: the event
        :return: None
        """
        pass

    @abstractmethod
    def end(self, clock) -> None:
        """
        Called when the simulation ends
        :return: None
        """
        pass

    def _add_event(self, event: Event) -> None:
        """
        Adds an event to the FEL and uses relative time (like 5 seconds from now)
        :param event: the event to add
        :return: None
        """
        self.__sim.add_event(event)
        pass

    @abc.abstractmethod
    def print_state(self):
        pass

    def name(self) -> str:
        return self.__name

    pass

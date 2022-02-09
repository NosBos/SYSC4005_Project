import abc
import queue
from dataclasses import dataclass, field
from typing import Any
from abc import ABC, abstractmethod


@dataclass(order=True)
class Event:
    time: float  # priority of event
    recipient: Any = field(compare=False)  # who shall receive the event
    item: Any = field(compare=False)  # the event information

    def __repr__(self):
        return f"{self.time} : {str(self.item)} "


class Simulation(ABC):
    """
    Simulation base class. It handles everything to do with the future event list.
    User must define starting and ending simulation behaviour
    """
    SECONDS = 1
    MINUTES = 60
    HOURS = 3600
    SIMULATION_END = "SIMULATION END"

    def __init__(self):
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

        # pop events and execute until there's none left or end event reached
        evt = ''
        while len(self.__future_event_list.queue):
            self.__print_sim_table_row()
            evt = self.__future_event_list.get()
            if evt.item == Simulation.SIMULATION_END:
                break
            self.clock = evt.time
            evt.recipient.handle_event(evt)
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

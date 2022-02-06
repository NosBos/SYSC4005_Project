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
    pass


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
        pass

    def run(self) -> None:
        """
        Runs the simulation from start() to end()
        :return: None
        """
        end_time = self._start()
        self.__run(runtime=end_time)
        self._end(self.clock)
        pass

    @abc.abstractmethod
    def _start(self) -> float:
        """
        Used to put all the entities into a started state and add initial events to FEL
        :return: the runtime of the simulation
        """
        pass

    def __run(self, runtime: float) -> None:
        # add ending event for timed simulations
        if runtime > 0:
            self.add_event(Event(runtime, self, Simulation.SIMULATION_END))
            pass

        # pop events and execute until there's none left or end event reached
        while len(self.__future_event_list.queue):
            evt = self.__future_event_list.get()
            if evt.item == Simulation.SIMULATION_END:
                break
            self.clock = evt.time
            evt.recipient.handle_event(evt)
            pass
        pass

    @abc.abstractmethod
    def _end(self, clock) -> None:
        """
        Called when the simulation is done. Used to output all statistics
        :return: None
        """
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

    def __init__(self, simulation: Simulation):
        self.__sim = simulation

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

    pass

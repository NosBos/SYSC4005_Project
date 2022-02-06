from typing import List
import random
from Framework import Entity, Event, Simulation
from Component import Component
from Buffer import Buffer


class Inspector (Entity):

    def __init__(self, simulation: Simulation, component_type_list: List[Component], buffer_list: List[Buffer]):
        # We can remove component type list and derive it from the buffer list
        super(Inspector, self).__init__(simulation)
        self.type = component_type_list
        self.buffer_list = buffer_list
        self.blocked = False
        self.blocked_component = None
        self.time_blocked = 0
        self.total_time_blocked = 0

    def start(self) -> None:
        component_to_generate = random.choice(self.type)
        time = random.randint(1, 10)
        # Add starting event to Future Event List
        self._add_event(Event(time, self, component_to_generate))

    def handle_event(self, event: Event) -> None:
        # Get the component type from the event
        component_type = event.item

        # Get list of buffers that handle components of processed component type
        valid_buffers = [buffer for buffer in self.buffer_list if
                         buffer.componentType == component_type
                         and
                         len(buffer.queue) < 2]

        # Sort list by both buffer size and priority
        valid_buffers.sort(key=lambda x: (len(x.queue), x.priority), reverse=True)

        if len(valid_buffers) == 0:
            # Block the inspector
            self.blocked = True
            self.blocked_component = component_type

        else:
            self.create_component()
            buffer = valid_buffers[0]
            work_station = buffer.work_station

            if work_station.idle and work_station.has_required_components():
                work_station.idle = False
                work_station.create_product()

    def end(self, clock) -> None:
        pass

    def create_component(self) -> None:
        component_to_generate = random.choice(self.type)
        time = random.randint(1, 10)
        # Adds event to Future Event List
        self._add_event(Event(time, self, component_to_generate))

    # def process_component_done_event(self, component_type: Component):
    #     """
    #         Returns the sum of two decimal numbers in binary digits.
    #
    #                 Parameters:
    #                         component_type (Component): The component type that was created
    #
    #     """
    #     # Get list of buffers that handle components of processed component type
    #     valid_buffers = [buffer for buffer in self.buffer_list if
    #                      buffer.componentType == component_type
    #                      and
    #                      len(buffer.queue) < 2]
    #
    #     # Sort list by both buffer size and priority
    #     valid_buffers.sort(key=lambda x: (len(x.queue), x.priority), reverse=True)
    #
    #     if len(valid_buffers) == 0:
    #         # Block the inspector
    #         self.blocked = True
    #         self.blocked_component = component_type
    #
    #     else:
    #         self.create_component()
    #         buffer = valid_buffers[0]
    #         work_station = buffer.work_station
    #
    #         if work_station.idle and work_station.has_required_components():
    #             work_station.idle = False
    #             work_station.create_product()

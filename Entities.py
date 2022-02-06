from Framework import Entity, Event, Simulation
from typing import List
import random
from Component import Component
from Product import Product

"""

"""

class Inspector (Entity):

    def __init__(self, simulation: Simulation, component_type_list: List[Component], buffer_list):
        # We can remove component type list and derive it from the buffer list
        super(Inspector, self).__init__(simulation)
        self.sim = simulation
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
        valid_buffers.sort(key=lambda x: (len(x.queue), x.priority))

        if len(valid_buffers) == 0:
            # Block the inspector
            self.blocked = True
            self.blocked_component = component_type
            print(f"Inspector {self.type} is blocked \n")

        else:
            self.create_component()
            buffer = valid_buffers[0]
            buffer.add_component(component_type)
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

"""


"""
class WorkStation (Entity):

    def __init__(self, simulation: Simulation, product_type: Product, buffer_list):
        super(WorkStation, self).__init__(simulation)
        self.product_type = product_type
        self.buffer_list = buffer_list
        self.idle = True
        self.time_idle = 0
        self.products_produced = 0

    def start(self) -> None:
        pass

    def handle_event(self, event: Event) -> None:
        self.products_produced += 1
        if not self.has_required_components():
            self.idle = True
            print(f"Workstation {self.product_type} is idle")
        else:
            self.create_product()
            print(f"Workstation {self.product_type} is working")
            # Check if any inspectors need to be taken out of blocked state
            for buffer in self.buffer_list:
                inspector = buffer.inspector

                # Check if inspector is blocked AND it is blocked with component type that was used
                if inspector.blocked and inspector.blocked_component == buffer.componentType:
                    inspector.blocked = False
                    buffer.add_component(inspector.blocked_component)
                    inspector.blocked_component = None
                    inspector.create_component()

    def end(self, clock) -> None:
        pass

    def has_required_components(self) -> bool:
        return len(self.buffer_list) == len([buffer for buffer in self.buffer_list if len(buffer.queue) > 0])


    def create_product(self) -> None:
        time = random.randint(1, 10)
        for buffer in self.buffer_list:
            buffer.pop_component()
        # Adds product done event to Future Event List
        self._add_event(Event(time, self, self.product_type))


class Buffer (Entity):

    def start(self) -> None:
        pass

    def handle_event(self, event: Event) -> None:
        pass

    def end(self, clock) -> None:
        pass

    def __init__(self, simulation: Simulation, component_type: Component, priority: int):
        super(Buffer, self).__init__(simulation)
        self.componentType = component_type
        self.priority = priority
        self.queue = []
        self.work_station = None
        self.inspector = None

    def add_work_station(self, work_station: WorkStation) -> None:
        self.work_station = work_station

    def add_inspector(self, inspector: Inspector) -> None:
        self.inspector = inspector

    def add_component(self, component: Component) -> None:
        self.queue.append(component)
        self.print_state()

    def pop_component(self) -> Component:
        return self.queue.pop(0)
        self.print_state()

    def print_state(self):
        print(f"I am buffer {self.componentType} {self.priority} : {self.queue}")
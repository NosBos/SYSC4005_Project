from Framework import Entity, Event, Simulation
from typing import List
import random
from Component import Component
from Product import Product
from inputModeling.generate_distributions import *

"""

"""


class Inspector(Entity):

    def __init__(self, simulation: Simulation, name: str, component_type_list: List[Component], buffer_list, random_values):
        # We can remove component type list and derive it from the buffer list
        super(Inspector, self).__init__(simulation, name)
        self.type = component_type_list
        self.buffer_list = buffer_list
        self.blocked = False
        self.blocked_component = None
        self.time_blocked = 0
        self.time_blocked_start = 0
        self.random_values = random_values
        self.random_values_increment = 0

    def start(self) -> None:
        component_to_generate = random.choice(self.type)

        time = self.get_random_component_time(component_to_generate)

        # time = random.randint(1, self.rand)
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
            self.time_blocked_start = event.time

        else:
            self.create_component()
            buffer = valid_buffers[0]
            buffer.add_component(component_type)
            work_station = buffer.work_station

            if work_station.idle and work_station.has_required_components():
                work_station.idle = False
                work_station.create_product(event.time)

    def end(self, clock) -> None:
        pass

    def create_component(self) -> None:
        component_to_generate = random.choice(self.type)
        time = self.get_random_component_time(component_to_generate)
        # Adds event to Future Event List
        self._add_event(Event(time, self, component_to_generate))
        pass

    def get_random_component_time(self, component) -> float:
        if component == Component.C1:
            time = generate_value_inspector_1(self.random_values[self.random_values_increment])
        elif component == Component.C2:
            time = generate_value_inspector_2(self.random_values[self.random_values_increment])
        elif component == Component.C3:
            time = generate_value_inspector_3(self.random_values[self.random_values_increment])

        self.random_values_increment += 1

        return time


    def print_state(self):
        print(f'{"BLOCKED" if self.blocked else "CREATE"}', end=',')
        pass

    def get_state(self):
        return self.blocked

    def products_done(self):
        return 0


"""


"""


class WorkStation(Entity):

    def __init__(self, simulation: Simulation, name: str, product_type: Product, buffer_list, random_values):
        super(WorkStation, self).__init__(simulation, name)
        self.product_type = product_type
        self.buffer_list = buffer_list
        self.idle = True
        self.time_idle = 0
        self.time_busy = 0
        self.time_busy_start = 0
        self.products_produced = 0
        self.random_values = random_values
        self.random_values_increment = 0

    def start(self) -> None:
        pass

    def handle_event(self, event: Event) -> None:
        self.products_produced += 1
        self.time_busy += event.time - self.time_busy_start
        if not self.has_required_components():
            self.idle = True
        else:
            self.create_product(event.time)

    def end(self, clock) -> None:
        pass

    def has_required_components(self) -> bool:
        return len(self.buffer_list) == len([buffer for buffer in self.buffer_list if len(buffer.queue) > 0])

    def create_product(self, starting_time) -> None:
        self.time_busy_start = starting_time
        time = self.get_random_processing_time()
        for buffer in self.buffer_list:
            buffer.pop_component()
        # Adds product done event to Future Event List
        self._add_event(Event(time, self, self.product_type))


        # Check if any inspectors need to be taken out of blocked state
        for buffer in self.buffer_list:
            inspector = buffer.inspector

            # Check if inspector is blocked AND it is blocked with component type that was used
            if inspector.blocked and inspector.blocked_component == buffer.componentType:
                inspector.blocked = False
                inspector.time_blocked += starting_time - inspector.time_blocked_start
                print(inspector.time_blocked)
                buffer.add_component(inspector.blocked_component)
                inspector.blocked_component = None
                inspector.create_component()

    def get_random_processing_time(self):
        if self.product_type == Product.P1:
            time = generate_value_work_station_1(self.random_values[self.random_values_increment])
        elif self.product_type == Product.P2:
            time = generate_value_work_station_2(self.random_values[self.random_values_increment])
        elif self.product_type == Product.P3:
            time = generate_value_work_station_3(self.random_values[self.random_values_increment])

        self.random_values_increment += 1

        return time

    def print_state(self):
        print(f'{"IDLE" if self.idle else "CREATE"}', end=',')
        pass

    def get_state(self):
        return None

    def products_done(self):
        return self.products_produced



class Buffer(Entity):

    def start(self) -> None:
        pass

    def handle_event(self, event: Event) -> None:
        pass

    def end(self, clock) -> None:
        pass

    def __init__(self, simulation: Simulation, name, component_type: Component, priority: int):
        super(Buffer, self).__init__(simulation, name)
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

    def pop_component(self) -> Component:
        return self.queue.pop(0)

    def print_state(self):
        print(f'{len(self.queue)}', end=',')
        pass

    def get_state(self):
        return len(self.queue)

    def products_done(self):
        return 0

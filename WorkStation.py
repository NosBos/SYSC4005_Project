from typing import List
import random
from Framework import Entity, Event, Simulation
from Product import Product
from Buffer import Buffer


class WorkStation (Entity):

    def __init__(self, simulation: Simulation, product_type: Product, buffer_list: List[Buffer]):
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
        else:
            self.create_product()

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

    # def process_product_done_event(self):
    #     self.products_produced += 1
    #     if not self.has_required_components():
    #         self.idle = True
    #     else:
    #         self.create_product()
    #
    #         # Check if any inspectors need to be taken out of blocked state
    #         for buffer in self.buffer_list:
    #             inspector = buffer.inspector
    #
    #             # Check if inspector is blocked AND it is blocked with component type that was used
    #             if inspector.blocked and inspector.blocked_component == buffer.componentType:
    #                 inspector.blocked = False
    #                 buffer.add_component(inspector.blocked_component)
    #                 inspector.blocked_component = None
    #                 inspector.generate_component()





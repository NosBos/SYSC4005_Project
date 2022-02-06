from typing import List
from Product import Product
from Buffer import Buffer


class WorkStation:

    def __init__(self, product_type: Product, buffer_list: List[Buffer]):
        self.product_type = product_type
        self.buffer_list = buffer_list
        self.idle = True
        self.time_idle = 0
        self.products_produced = 0

    def has_required_components(self):
        """
            Check if the list of buffers has the same length as the list of buffers that are not empty

                    Returns:
                            boolean (bool): Boolean value with true if all required components are available,
                            false otherwise
        """
        return len(self.buffer_list) == len([buffer for buffer in self.buffer_list if len(buffer.queue) > 0])


    def create_product(self):
        for buffer in self.buffer_list:
            buffer.pop_component()
        """ CREATE PRODUCT DONE EVENT IN FEL """

    def process_product_done_event(self):
        self.products_produced += 1
        if not self.has_required_components():
            self.idle = True
        else:
            self.create_product()

            # Check if any inspectors need to be taken out of blocked state
            inspectors = []
            for buffer in self.buffer_list:
                inspector = buffer.inspector

                # Check if inspector is blocked AND it is blocked with component type that was used
                if inspector.blocked and inspector.blocked_component == buffer.componentType:
                    inspector.blocked = False
                    buffer.add_component(inspector.blocked)
                    inspector.blocked_component = None

                    inspector.generate_component()





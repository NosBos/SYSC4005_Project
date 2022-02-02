# This is a sample Python script.
from Buffer import Buffer
from Component import Component
from Product import Product
from Inspector import Inspector
from WorkStation import WorkStation
# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    buffer1 = Buffer(Component.C1, 1)
    buffer2 = Buffer(Component.C1, 2)
    buffer3 = Buffer(Component.C2, 3)
    buffer4 = Buffer(Component.C1, 4)
    buffer5 = Buffer(Component.C3, 5)

    inspector1 = Inspector([Component.C1], [buffer1, buffer2, buffer4])
    inspector2 = Inspector([Component.C2, Component.C3], [buffer3, buffer5])

    workstation1 = WorkStation(Product.P1, [buffer1])
    workstation2 = WorkStation(Product.P2, [buffer2, buffer3])
    workstation3 = WorkStation(Product.P3, [buffer4, buffer5])

    buffer1.add_work_station(workstation1)
    buffer2.add_work_station(workstation2)
    buffer3.add_work_station(workstation2)
    buffer4.add_work_station(workstation3)
    buffer5.add_work_station(workstation3)

    buffer1.add_inspector(inspector1)
    buffer2.add_inspector(inspector1)
    buffer3.add_inspector(inspector2)
    buffer4.add_inspector(inspector1)
    buffer5.add_inspector(inspector2)


    print_hi('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/

from module_lab2_task2 import *

a = NetworkElectricNZ()

a.read_network(directory=r".\nz_network")
a.plot_network(save='SAVE.png')

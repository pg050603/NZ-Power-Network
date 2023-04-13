import pytest
from module_lab2_task2 import *


def test_add_node():
    """ Test for creation of a node for add_node"""
    test_network = Network()
    name = 'A'

    assert (test_network.add_node(name) is not None)


def test_add_arc():
    """ Test for creation of an arc in add_arc"""
    test_network = Network()
    name = 'A'
    node_from = test_network.add_node(name)
    name = 'C'
    node_to = test_network.add_node(name)
    weight = 2
    test_network.add_arc(node_from, node_to, weight)
    assert (test_network.add_arc(test_network.arcs) == "arc:(node:A)-- 2 -->(node:C)")


def test_read_network():
    """ Test for read_network"""
    test_network = Network()
    test_network.read_network('network.txt')

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import os
from glob import glob

class Node(object):
    """
    Object representing network node.

    Attributes:
    -----------
    name : str, int
        unique identifier for the node.
    value : float, int, bool, str, list, etc...
        information associated with the node.
    arcs_in : list
        Arc objects that end at this node.
    arcs_out : list
        Arc objects that begin at this node.
    """

    def __init__(self, name=None, value=None, arcs_in=None, arcs_out=None):

        self.name = name
        self.value = value
        if arcs_in is None:
            self.arcs_in = []
        else:
            self.arcs = arcs_in
        if arcs_out is None:
            self.arcs_out = []
        else:
            self.arcs_out = arcs_out

    def __repr__(self):
        return f"node:{self.name}"


class Arc(object):
    """
    Object representing network arc.

    Attributes:
    -----------
    weight : int, float
        information associated with the arc.
    to_node : Node         object (defined above) at which arc ends.
    from_node : Node         object at which arc begins.
    """

    def __init__(self, weight=None, from_node=None, to_node=None):
        self.weight = weight
        self.from_node = from_node
        self.to_node = to_node

    def __repr__(self):
        return f"arc:({self.from_node.name})--{self.weight}-->({self.to_node.name})"


class Network(object):
    """
    Basic Implementation of a network of nodes and arcs.

    Attributes
    ----------
    nodes : list
        A list of all Node (defined above) objects in the network.
    arcs : list
        A list of all Arc (defined above) objects in the network.
    """

    def __init__(self, nodes=None, arcs=None):
        self.value = None
        self.node_from = None
        self.node_to = None
        self.weight = None
        self.name = None
        if nodes is None:
            self.nodes = []
        if arcs is None:
            self.arcs = []

    def __repr__(self):
        node_names = '\n'.join(node.__repr__() for node in self.nodes)
        arc_info = '\n'.join(arc.__repr__() for arc in self.arcs)
        return f'{node_names}\n{arc_info}'

    def get_node(self, name):
        """
        Return network node with name.

        Parameters:
        -----------
        name : str
            Name of node to return.

        Returns:
        --------
        node : Node or None
            Node object (defined above) with corresponding name, or None if not found.
        """
        # loop through list of nodes until node found
        for node in self.nodes:
            if node.name == name:
                return node

        # if node not found, return None
        return None

    # **these methods are incomplete, you must complete them as part of the lab task**
    def add_node(self, name, value=None):
        """
        Adds a new node object belonging to class Node to the network

        Args:
            name:  str representing node name
            value: value associated with the node
        """

        matcher = self.get_node(name)
        if matcher != None:
            return matcher # if the node is already found DONT create a new one, return existing node
        node_current = Node(name, value) # Initialise current node
        #Node:A
        #Inside Network class
        self.nodes.append(node_current) # In the current network in the nodes, add node_current
        return node_current

    def add_arc(self, node_from, node_to, weight):
        """
        Adds a new arc object, belonging to class Arc, to the network

        Args:
            node_from:  node object, representing arc source
            node_to: node object representing arc destination
            weight: flat representing arc value
        """
        arc_current = Arc(weight, node_from, node_to)  # Initialises arc
        self.arcs.append(arc_current)  # Appends arcs to arc list within network

    def read_network(self, filename):
        with open(filename, 'r') as fp:  # Open specified file
            names = []  # Initialise counters & storage array
            arcs = []

            for line in fp:
                names.append(line.split(',')[0])  # Get name of node
                arcs.append(line.rstrip().split(',')[1:])  # Get list of nodes_to of node

            for i in range(len(names)):
                name = names[i]
                node_from = self.add_node(name)  # Add network node with stored file name as node_from
                node_arcs = arcs[i]  # Get all nodes_to arcs for current node

                for arc_string in node_arcs:
                    arc_string = arc_string.split(";")  # Separate into individual arcs
                    for node_to_name, weight in arc_string:
                        node_to = self.add_node(node_to_name)  # Create new node for node_to
                        weight = int(weight)
                        self.add_arc(node_from, node_to, weight)  # Using node objects & weight

class NetworkElectricNZ(Network):
    """
    Inherited from the Network class. Used to represent the NZ electricity network.

    METHODS
    -------
    read_network
        Overloads the inherited read_network method to work on different format of network data.
    plot_network
        Produces a map of the NZ Electricity network once constructed with read_network.
    """

    def read_network(self, directory):
        """
        Reads network information from a directory

        PARAMETERS
        ----------
        directory : str
            Path to directory containing the network data (structure outlined below).

        NOTES
        -----
        Assume that directory parameter contains one folder for connections between nodes.
        All other folder define the nodes of the network.
        Each node folder contains a file called station_data.txt, which includes the x and y position of node.
        In the connections' folder, there is a file for each connection.
        The name of the file indicates that two nodes are connected (from-to).
        The contents of the file record the capacity of that connection over the last 35 years.
        The connection (arc) weight should be the mean capacity.
        """
        # Find connections subdirectory
        con_subdir = directory + os.sep + 'connections'

        # Loop through each node folder first
        # (Go through connections folder second, so we do not need to check for duplicates when adding new nodes)
        for subdir in glob(directory + os.sep + '*'):
            # Do not go through connections subdirectory
            if subdir != con_subdir:

                # Open the station_data.txt file as read-only
                with open(subdir + os.sep + 'station_data.txt', 'r') as fp:
                    # Get first line
                    ln = fp.readline()
                    # Initialise data array: data[0] will be code, data[1] will be x value, data[2] will be y value
                    data = []

                    # While loop to read data
                    while ln != '':
                        ln = ln.strip()
                        value = ln.split(' ')[1]
                        data.append(value)
                        ln = fp.readline()

                # Add nodes with appropriate name (code) and x and y values, converting these to floats
                self.add_node(data[0], [float(data[1]), float(data[2])])

        # Loop through each file in connections subdirectory
        for con_file in glob(con_subdir + os.sep + '*'):
            # Find the from-to nodes from the filename
            filename = os.path.splitext(con_file)[0]
            filename = filename.split(os.sep)[-1]
            [from_node_name, to_node_name] = filename.split('-')

            # Find the arc weight from the mean capacity of the connections
            [_, capacity] = np.genfromtxt(con_file, skip_header=1, delimiter=",").T
            arc_weight = np.mean(capacity)

            # Get source node object from source node name string
            from_node = self.get_node(from_node_name)

            # Get destination node object from destination node name string
            to_node = self.get_node(to_node_name)

            # link nodes together with appropriate arc weight
            self.add_arc(from_node, to_node, arc_weight)

    def plot_network(self, save=None):
        """
        Plot the network and optionally save to file SAVE
        """
        # create figure axes
        fig = plt.figure()
        fig.set_size_inches([10, 10])
        ax = plt.axes()

        # NZ coastline as background
        img = mpimg.imread('bg.png')
        ax.imshow(img, zorder=1)

        # a filthy hack to get coordinates in the right spot...
        for node in self.nodes:
            try:
                node._modified
            except AttributeError:
                x, y = node.value
                y = int((y + 10) * 1.06)
                x -= int(50 * y / 800.)
                node.value = [x, y]
                node._modified = True

        try:
            md = {'a': os.environ['COMPUTERNAME']}
        except KeyError:
            try:
                import socket
                md = {'a': socket.gethostname()}
            except:
                md = None
                pass

        # draw connections as lines
        weights = [arc.weight for arc in self.arcs]
        # scale for plotting connections
        wmin = np.min(weights)
        wmax = np.max(weights)
        lmin, lmax = [0.5, 10.0]

        # plot connections
        for arc in self.arcs:
            # compute line length, scales with connection size
            lw = (arc.weight - wmin) / (wmax - wmin) * (lmax - lmin) + lmin
            x1, y1 = arc.from_node.value
            x2, y2 = arc.to_node.value
            ax.plot([x1, x2], [y1, y2], '-', lw=lw, color=[0.6, 0.6, 0.6])

        # draw nodes as text boxes with station names
        # bounding box properties
        props = dict(boxstyle='round', facecolor='white', alpha=1.0)
        for node in self.nodes:
            # extract coordinates
            x, y = node.value
            ax.text(x, y, node.name, ha='center', va='center', zorder=2, bbox=props)

        # remove ticks
        ax.set_xticks([])
        ax.set_yticks([])

        # display options
        if save:

            # save to file
            plt.savefig(save, dpi=300, facecolor='w', edgecolor='w', orientation='portrait',
                        format=None, transparent=False, bbox_inches=None, pad_inches=0.1, metadata=md)
            plt.close()
        else:
            # open figure window in screen
            plt.show()

import random
import numpy as np
import networkx as nx

class GraphLayout:
    def __init__(self, dependencies):
        G = nx.DiGraph()
        for point in dependencies:
            for dep in point['directDependencies']:
                G.add_edge(dep, point['id'])

        self.graph = G
        self.positions = None
        self.props = list()
        self.prop_positions = {}  # Store special points outside self.positions
        self.special_nodes = []  # Track special nodes
    
    def getGraph(self):
        return self.graph 
    
    def getPositions(self):
        return self.positions
        
    def forceDirectedLayout(self, iterations=4000, attraction_strength=0.08, repulsion_strength=400, damping=0.9):
        pos = {node: np.array([random.uniform(-1, 1), random.uniform(-1, 1)]) for node in self.graph.nodes()}
    
        for _ in range(iterations):
            forces = {node: np.array([0.0, 0.0]) for node in self.graph.nodes()}
            
            # Apply forces between nodes in the graph
            for node in self.graph.nodes():
                for other_node in self.graph.nodes():
                    if node != other_node:
                        delta = pos[node] - pos[other_node]
                        distance = np.linalg.norm(delta)
                        if distance == 0:
                            distance = 0.1
                        # Apply stronger repulsion for special nodes
                        if node in self.special_nodes or other_node in self.special_nodes:
                            repulsion_force = 100 / (distance ** 2)  # Special repulsion strength
                        else:
                            repulsion_force = repulsion_strength / (distance ** 2)
                        forces[node] += delta / distance * repulsion_force
            
            # Apply attraction forces for edges in the graph
            for edge in self.graph.edges():
                node_a, node_b = edge
                delta = pos[node_a] - pos[node_b]
                distance = np.linalg.norm(delta)
                attraction_force = attraction_strength * distance
                forces[node_a] -= delta / distance * attraction_force
                forces[node_b] += delta / distance * attraction_force

            # Update positions with damping
            for node in self.graph.nodes():
                pos[node] += forces[node]
                pos[node] *= damping
    
        self.positions = pos
    
    def addSpecialPoints(self, num_points=0):
        """
        Add special points that will be stored in prop_positions.
        These points will be added to the graph, but not connected to any other node.
        They will have stronger repulsion when calculating layout.
        """
        for i in range(num_points):
            # Generate a random ID and position for the special point
            special_point_id = f"special_{i}"
            self.graph.add_node(special_point_id)  # Add special node to the graph
            self.prop_positions[special_point_id] = np.array([random.uniform(-2, 2), random.uniform(-2, 2)])
            self.special_nodes.append(special_point_id)  # Keep track of special nodes
    
    def getSpecialPositions(self):
        """
        Return the positions of the special points in the same format as self.positions.
        """
        return self.prop_positions

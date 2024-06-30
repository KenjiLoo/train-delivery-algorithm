class Delivery:
    def __init__(self, nodes, edges, packages, trains):
        self.trains = trains
        self.nodes = nodes
        self.edges = edges
        self.packages = packages
        self.graph = self.get_map(edges, nodes)
        self.loaded_packages = []
        self.delivered_packages = []
        self.time = 0

    ##################################################################################################

    def scheduler(self):
        packages = self.packages
        trains = self.trains
        edges = self.edges
        nodes = self.nodes
        routes = self.get_map(edges, nodes)

        # iterate packages
        for package in packages:
            # reset for new package
            self.loaded_packages = []

            # find best train
            train = self.find_best_train(package, trains)
            if train:
                while (train['StartingNode'] != package['StartingNode']):
                    # move train to pickup package
                    journey = self.shortest_path(self.graph, train['StartingNode'], package['StartingNode'])

                    for i in range(len(journey) - 1):
                        train = self.move_train(train, journey[i], journey[i+1])

                # add package to train
                train = self.pickup_package(train, package)

                while (train['StartingNode'] != package['DestinationNode']):
                    # move train to deliver package
                    journey = self.shortest_path(self.graph, train['StartingNode'], package['DestinationNode'])

                    for i in range(len(journey) - 1):
                        # on last move to destination
                        if (journey[i + 1] == package['DestinationNode']):
                            self.loaded_packages.remove(package['PackageName'])
                            self.delivered_packages.append(package['PackageName'])

                        train = self.move_train(train, journey[i], journey[i + 1])

                # remove package from train
                train = self.dropoff_package(train, package)

            ending_statement = f"Takes {self.time} minutes in total."
            print('----------------------------------')
            print(ending_statement)
        return

    ##################################################################################################
    # CALCULATION METHODS

    def find_edge(self, start, end):
        for edge in self.edges:
            if (edge['Node1'] == start and edge['Node2'] == end) or (edge['Node1'] == end and edge['Node2'] == start):
                return edge

        return None

    def get_map(self, edges, nodes):
        graph = {}

        for edge in edges:
            node1 = edge['Node1']
            node2 = edge['Node2']
            time = edge['JourneyTimeInMinutes']

            if node1 not in graph:
                graph[node1] = {}

            if node2 not in graph:
                graph[node2] = {}

            # append neighbours for respective nodes
            if node2 not in graph[node1] or graph[node1][node2] != time:
                graph[node1][node2] = time

            if node1 not in graph[node2]:
                graph[node2][node1] = time

        return graph

    def find_best_train(self, package, trains):
        # if train is in the same station as the package
        for train in trains:
            if train['StartingNode'] == package['StartingNode']:
                if train['CapacityInKg'] > package['WeightInKg']:
                    return train

        edges = self.edges

        # if train is not in the same station as the package
        for train in trains:
            bestEdge = None

            # look for nearest train available
            for edge in edges:
                if train['StartingNode'] in [edge['Node1'], edge['Node2']]:
                    if bestEdge is None or (package['StartingNode'] in [edge['Node1'], edge['Node2']] and bestEdge['JourneyTimeInMinutes'] > edge['JourneyTimeInMinutes']):
                        bestEdge = edge

            # return best train if a valid edge is found
            if bestEdge and train['StartingNode'] in [bestEdge['Node1'], bestEdge['Node2']]:
                return train

        return None

    def shortest_path(self, graph, start, end):
        shortest_distance = {}
        predecessor = {}
        unseenNodes = graph.copy()
        infinity = float('inf')
        path = []

        for node in unseenNodes:
            shortest_distance[node] = infinity

        shortest_distance[start] = 0

        while unseenNodes:
            minNode = None
            for node in unseenNodes:
                if minNode is None:
                    minNode = node
                elif shortest_distance[node] < shortest_distance[minNode]:
                    minNode = node

            for childNode, weight in graph[minNode].items():
                if weight + shortest_distance[minNode] < shortest_distance[childNode]:
                    shortest_distance[childNode] = weight + shortest_distance[minNode]
                    predecessor[childNode] = minNode

            unseenNodes.pop(minNode)

        currentNode = end

        while currentNode != start:
            try:
                path.insert(0, currentNode)
                currentNode = predecessor[currentNode]
            except KeyError:
                print('Path not reachable')
                break

        path.insert(0, start)

        if shortest_distance[end] != infinity:
            return path

    ##################################################################################################
    # ACTION METHODS

    def move_train(self, train, start, end):
        # find edge
        path = self.find_edge(start, end)

        # record state
        self.record_state(train, path, end, self.loaded_packages, self.delivered_packages)

        # update train state
        train['StartingNode'] = end
        self.time += path['JourneyTimeInMinutes']

        return train

    def pickup_package(self, train, package):
        # add package to train
        train['CapacityInKg'] -= package['WeightInKg']
        train['StartingNode'] = package['StartingNode']
        self.loaded_packages.append(package['PackageName'])

        return train

    def dropoff_package(self, train, package):
        # remove package from train
        train['CapacityInKg'] += package['WeightInKg']
        train['StartingNode'] = package['StartingNode']

        return train

    def record_state(self, train, edge, destination, package = None, delivery = None):
        moves = {}
        moves['w'] = self.time
        moves['t'] = train['TrainName']
        moves['N1'] = train['StartingNode']
        moves['P1'] = package
        moves['N2'] = destination
        moves['P2'] = delivery

        journey = f"Move {train['TrainName']} to {destination} via {edge['Name']}, takes {str(edge['JourneyTimeInMinutes'])} minutes."
        moves = f"W={moves['w']}, T={moves['t']}, N1={moves['N1']}, P1={moves['P1']}, N2={moves['N2']}, P2={moves['P2']}"

        print('----------------------------------')
        print(journey)
        print(moves)

        return moves

######################################################################################################
# GET USER INPUT

# uncomment to hardcode inpit
# nodes = [
#     {'NodeName': 'A'},
#     {'NodeName': 'B'},
#     {'NodeName': 'C'}
# ]
#
# edges = [
#     {'Name': 'E1', 'Node1': 'A', 'Node2': 'B', 'JourneyTimeInMinutes': 30},
#     {'Name': 'E2', 'Node1': 'B', 'Node2': 'C', 'JourneyTimeInMinutes': 10}
# ]
#
# packages = [
#     {'PackageName': 'K1', 'WeightInKg': 5, 'StartingNode': 'A', 'DestinationNode': 'C'}
# ]
#
# trains = [
#     {'TrainName': 'Q1', 'CapacityInKg': 6, 'StartingNode': 'B'}
# ]

def input_nodes():
    nodes = []
    num_nodes = int(input("Enter the number of nodes: "))
    index = 1

    for _ in range(num_nodes):
        node_name = input(f"Enter the name of node {index}: ")
        nodes.append({'NodeName': node_name})
        index += 1
    return nodes

def input_edges():
    edges = []
    num_edges = int(input("Enter the number of edges: "))
    index = 1

    for _ in range(num_edges):
        edge_name = input(f"Enter the name of edge {index}: ")
        node1 = input("Enter the name of the first node: ")
        node2 = input("Enter the name of the second node: ")
        journey_time = int(input("Enter the journey time in minutes: "))
        edges.append({'Name': edge_name, 'Node1': node1, 'Node2': node2, 'JourneyTimeInMinutes': journey_time})
        index += 1
    return edges

def input_packages():
    packages = []
    num_packages = int(input("Enter the number of packages: "))
    index = 1
    for _ in range(num_packages):
        package_name = input(f"Enter the name of package {index}: ")
        weight = int(input("Enter the weight of the package in kg: "))
        starting_node = input("Enter the starting node: ")
        destination_node = input("Enter the destination node: ")
        packages.append({'PackageName': package_name, 'WeightInKg': weight, 'StartingNode': starting_node, 'DestinationNode': destination_node})
        index += 1
    return packages

def input_trains():
    trains = []
    num_trains = int(input("Enter the number of trains: "))
    index = 1
    for _ in range(num_trains):
        train_name = input(f"Enter the name of the train {index}: ")
        capacity = int(input("Enter the capacity of the train in kg: "))
        starting_node = input("Enter the starting node: ")
        trains.append({'TrainName': train_name, 'CapacityInKg': capacity, 'StartingNode': starting_node})
        index += 1
    return trains

# Input data from user
nodes = input_nodes()
edges = input_edges()
packages = input_packages()
trains = input_trains()

# Initialize and run the scheduler
delivery = Delivery(nodes, edges, packages, trains)
delivery.scheduler()
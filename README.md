# Delivery Scheduler Documentation

## Overview

This script is designed to schedule and optimize the delivery of packages using a fleet of trains on a given network of nodes and edges. The main functionality is encapsulated in the `Delivery` class, which includes methods for scheduling deliveries, calculating routes, and handling train movements.

**this code supports data input via console, or you may uncomment the input section to hardcode data

## Class and Methods Documentation

### `Delivery`

The `Delivery` class handles the core functionality of the delivery scheduling algorithm. It includes methods to initialize the class with the required data, schedule deliveries, and perform various calculations and actions necessary for the delivery process.

#### `__init__(self, nodes, edges, packages, trains)`

- **Parameters:**
  - `nodes`: List of nodes in the network.
  - `edges`: List of edges connecting the nodes.
  - `packages`: List of packages to be delivered.
  - `trains`: List of trains available for deliveries.
- **Description:** Initializes the `Delivery` class with nodes, edges, packages, and trains. Also sets up the graph representation of the network and initializes tracking lists for loaded and delivered packages.

#### `scheduler(self)`

- **Description:** Manages the overall delivery process. Iterates over each package, finds the best available train, moves the train to pick up the package, delivers the package, and prints the total time taken for all deliveries.

#### `find_edge(self, start, end)`

- **Parameters:**
  - `start`: Starting node of the edge.
  - `end`: Ending node of the edge.
- **Returns:** The edge connecting the `start` and `end` nodes.
- **Description:** Finds and returns the edge connecting the given nodes.

#### `get_map(self, edges, nodes)`

- **Parameters:**
  - `edges`: List of edges.
  - `nodes`: List of nodes.
- **Returns:** Graph representation of the network.
- **Description:** Constructs and returns a graph representation of the network using the given edges and nodes.

#### `find_best_train(self, package, trains)`

- **Parameters:**
  - `package`: The package to be delivered.
  - `trains`: List of available trains.
- **Returns:** The best train available for the delivery.
- **Description:** Finds and returns the best train available for delivering the given package based on proximity and capacity.

#### `shortest_path(self, graph, start, end)`

- **Parameters:**
  - `graph`: Graph representation of the network.
  - `start`: Starting node.
  - `end`: Ending node.
- **Returns:** The shortest path between the `start` and `end` nodes.
- **Description:** Calculates and returns the shortest path between the given nodes using Dijkstra's algorithm.

#### `move_train(self, train, start, end)`

- **Parameters:**
  - `train`: The train to be moved.
  - `start`: Starting node.
  - `end`: Ending node.
- **Returns:** The updated train after moving.
- **Description:** Moves the train from the `start` node to the `end` node and updates the total delivery time.

#### `pickup_package(self, train, package)`

- **Parameters:**
  - `train`: The train picking up the package.
  - `package`: The package to be picked up.
- **Returns:** The updated train after picking up the package.
- **Description:** Adds the package to the train's cargo and updates the train's capacity.

#### `dropoff_package(self, train, package)`

- **Parameters:**
  - `train`: The train dropping off the package.
  - `package`: The package to be dropped off.
- **Returns:** The updated train after dropping off the package.
- **Description:** Removes the package from the train's cargo and updates the train's capacity.

#### `record_state(self, train, edge, destination, package=None, delivery=None)`

- **Parameters:**
  - `train`: The train involved in the action.
  - `edge`: The edge used for the movement.
  - `destination`: The destination node.
  - `package`: The package being moved (if any).
  - `delivery`: The package being delivered (if any).
- **Description:** Records and prints the state of the delivery process at each step.

## Flow of the Algorithm

1. **Initialization:** The `Delivery` class is initialized with nodes, edges, packages, and trains.
2. **Scheduling:** The `scheduler` method iterates over each package to be delivered.
3. **Finding Best Train:** For each package, the `find_best_train` method identifies the best train available based on proximity and capacity.
4. **Moving Train to Pickup:** If the train is not at the package's starting node, the `shortest_path` method calculates the shortest route to the starting node, and the train is moved using the `move_train` method.
5. **Picking Up Package:** The `pickup_package` method adds the package to the train.
6. **Moving Train to Deliver:** The `shortest_path` method calculates the shortest route to the destination node using the Djikstra Algorithm, and the train is moved using the `move_train` method. The package is removed from the train once it reaches the destination.
7. **Dropping Off Package:** The `dropoff_package` method updates the train's capacity after dropping off the package.
8. **Recording State:** Each step of the process is recorded and printed using the `record_state` method.
9. **Completion:** The total time taken for all deliveries is printed at the end of the scheduling process.

## Refactoring Plan

In the future, the calculation methods (`find_edge`, `get_map`, `find_best_train`, `shortest_path`) and action methods (`move_train`, `pickup_package`, `dropoff_package`, `record_state`) will be refactored into a separate class to improve code organization and maintainability. For convenience, these methods are currently included in a single class to allow users to easily copy and run the code, especially on online Python compilers.

class Agent(object):
    def SearchSolution(self, state):
        return []
        
class AgentSnake(Agent):    
    def SearchSolution(self, state):
        FoodX = state.FoodPosition.X
        FoodY = state.FoodPosition.Y

        HeadX = state.snake.HeadPosition.X #L
        HeadY = state.snake.HeadPosition.Y #T
        
        DR = FoodY - HeadY
        DC = FoodX - HeadX
        
        plan = []
        
        F = -1
        if(DR == 0 and state.snake.HeadDirection.X*DC < 0):
            plan.append(0)
            F = 6
            
        if(state.snake.HeadDirection.Y*DR < 0):
            plan.append(3)
            if(DC == 0):
                F = 9
            else:
                DC = DC - 1
        Di = 6
        if(DR < 0):
            Di = 0
            DR = -DR
        for i in range(0,int(DR)):
            plan.append(Di)
        Di = 3
        if(DC < 0):
            Di = 9
            DC = -DC
        for i in range(0,int(DC)):
            plan.append(Di)
        if(F > 0):
            plan.append(F)
            F = -1
            
        return plan
    
    def showAgent():
        print("A Snake Solver By MB")
        
# You code of agent goes here
# You must create three agents one using A*, second using greedy best first search and third using an uninformed algo of your choice to make a plan

class AStarAgent(Agent):  #By Afnan Hussain 21L-5693

    def __init__(self):
        self.name = "AStar"

    def heuristic(self, current, goal):
        """
        Manhattan distance heuristic.
        """
        return abs(current[0] - goal[0]) + abs(current[1] - goal[1])

    def get_neighbors(self, node, maze):
        """
        Returns valid neighbors of the current node in the maze.
        """
        neighbors = []
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]  # Right, Left, Down, Up
        for dr, dc in directions:
            r, c = node[0] + dr, node[1] + dc
            if 0 < r < len(maze)-1 and 0 < c < len(maze[0])-1 and maze[r][c] != -1:
                neighbors.append((r, c))
        return neighbors

    def enqueue(self, queue, item, priority):
        """
        Enqueue item with given priority.
        """
        index = 0
        while index < len(queue) and priority >= queue[index][0]:
            index += 1
        queue.insert(index, (priority, item))

    def dequeue(self, queue):
        """
        Dequeue and return the item with the lowest priority.
        """
        if not queue:
            raise IndexError("Trying to dequeue from an empty queue.")
        return queue.pop(0)[1]

    def SearchSolution(self, state):
        start = (state.snake.HeadPosition.Y, state.snake.HeadPosition.X)
        goal = (state.FoodPosition.Y, state.FoodPosition.X)
        open_set = []  # Priority queue (sorted by cost + heuristic)
        self.enqueue(open_set, start, 0)
        came_from = {}
        cost_so_far = {start: 0}

        while open_set:
            current_node = self.dequeue(open_set)

            if current_node == goal:
                break

            for next_node in self.get_neighbors(current_node, state.maze.MAP):
                new_cost = cost_so_far[current_node] + 1
                if next_node not in cost_so_far or new_cost < cost_so_far[next_node]:
                    cost_so_far[next_node] = new_cost
                    priority = new_cost + self.heuristic(next_node, goal)
                    self.enqueue(open_set, next_node, priority)
                    came_from[next_node] = current_node

        # Reconstruct path
        path = []
        current = goal
        while current != start:
            path.append(current)
            current = came_from[current]
        path.append(start)
        path.reverse()

        # Convert path to directions
        directions = []
        for i in range(1, len(path)):
            diff_r = path[i][0] - path[i - 1][0]
            diff_c = path[i][1] - path[i - 1][1]
            if diff_r == 1:
                directions.append(6)  # Down
            elif diff_r == -1:
                directions.append(0)  # Up
            elif diff_c == 1:
                directions.append(3)  # Right
            elif diff_c == -1:
                directions.append(9)  # Left

        return directions

class GreedyBestFirstAgent(Agent): #By Alaiba Nawaz 21L-5650

    def __init__(self):
        self.name = "Greedy"


    def heuristic(self, current, goal):
        """
        Manhattan distance heuristic.
        """
        return abs(current[0] - goal[0]) + abs(current[1] - goal[1])

    def get_neighbors(self, node, maze):
        """
        Returns valid neighbors of the current node in the maze.
        """
        neighbors = []
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]  # Right, Left, Down, Up
        for dr, dc in directions:
            r, c = node[0] + dr, node[1] + dc
            if 0 < r < len(maze)-1 and 0 < c < len(maze[0])-1 and maze[r][c] != -1:
                neighbors.append((r, c))
        return neighbors

    def enqueue(self, queue, item, priority):
        """
        Enqueue item with given priority.
        """
        index = 0
        while index < len(queue) and priority >= queue[index][0]:
            index += 1
        queue.insert(index, (priority, item))

    def dequeue(self, queue):
        """
        Dequeue and return the item with the highest priority.
        """
        if not queue:
            raise IndexError("Trying to dequeue from an empty queue.")
        return queue.pop()[1]

    def SearchSolution(self, state):
        start = (state.snake.HeadPosition.Y, state.snake.HeadPosition.X)
        goal = (state.FoodPosition.Y, state.FoodPosition.X)
        open_set = []  # Priority queue (sorted by heuristic value only)
        self.enqueue(open_set, start, self.heuristic(start, goal))
        came_from = {}

        while open_set:
            current_node = self.dequeue(open_set)

            if current_node == goal:
                break

            for next_node in self.get_neighbors(current_node, state.maze.MAP):
                if next_node not in came_from:
                    self.enqueue(open_set, next_node, self.heuristic(next_node, goal))
                    came_from[next_node] = current_node

        # Reconstruct path
        path = []
        current = goal
        while current != start:
            path.append(current)
            current = came_from[current]
        path.append(start)
        path.reverse()

        # Convert path to directions
        directions = []
        for i in range(1, len(path)):
            diff_r = path[i][0] - path[i - 1][0]
            diff_c = path[i][1] - path[i - 1][1]
            if diff_r == 1:
                directions.append(6)  # Down
            elif diff_r == -1:
                directions.append(0)  # Up
            elif diff_c == 1:
                directions.append(3)  # Right
            elif diff_c == -1:
                directions.append(9)  # Left

        return directions
    
class BreadthFirstAgent(Agent): #By Afnan Hussain 21L-5693 and Alaiba Nawaz 21L-5650
    def __init__(self):
        self.name = "BFS"


    def get_neighbors(self, node, maze):
        """
        Returns valid neighbors of the current node in the maze.
        """
        neighbors = []
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]  # Right, Left, Down, Up
        for dr, dc in directions:
            r, c = node[0] + dr, node[1] + dc
            if 0 < r < len(maze)-1 and 0 < c < len(maze[0])-1 and maze[r][c] != -1:
                neighbors.append((r, c))
        return neighbors

    def SearchSolution(self, state):
        start = (state.snake.HeadPosition.Y, state.snake.HeadPosition.X)
        goal = (state.FoodPosition.Y, state.FoodPosition.X)
        queue = [(start, [start])]  # Queue for BFS traversal
        visited = set()

        while queue:
            current_node, path = queue.pop(0)

            if current_node == goal:
                return self.convert_path_to_directions(path)

            visited.add(current_node)

            for next_node in self.get_neighbors(current_node, state.maze.MAP):
                if next_node not in visited:
                    queue.append((next_node, path + [next_node]))
                    visited.add(next_node)

        # If no path found
        return []

    def convert_path_to_directions(self, path):
        directions = []
        for i in range(1, len(path)):
            diff_r = path[i][0] - path[i - 1][0]
            diff_c = path[i][1] - path[i - 1][1]
            if diff_r == 1:
                directions.append(6)  # Down
            elif diff_r == -1:
                directions.append(0)  # Up
            elif diff_c == 1:
                directions.append(3)  # Right
            elif diff_c == -1:
                directions.append(9)  # Left
        return directions

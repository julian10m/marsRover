class MarsRover():
    def __init__(self, x, y):
        self.x =  x
        self.y = y
        
    def set_x(self, x):
        self.x = x
    
    def set_y(self, y):
        self.y = y

    def to_string(self):
        return ':'.join([str(self.x), str(self.y)])

    def get_next_coord(self, current_coord, delta, side_length):
        next_coord = current_coord + delta
        if next_coord < 0:
            return side_length - 1
        elif next_coord == side_length:
            return 0
        return next_coord

    def get_next_x_coord(self, delta, side_length):
        return self.get_next_coord(self.x, delta, side_length)

    def get_next_y_coord(self, delta, side_length):
        return self.get_next_coord(self.y, delta, side_length)        

    def coords_output(self, direction):
        return ':'.join([self.to_string(), direction])

    def obstacle_output(self, direction):
        return f'O:{self.coords_output(direction)}'

class MarsRoverAPI():
    right_direction_update = {
                'N': 'E',
                'E': 'S',
                'S': 'W',
                'W': 'N',}

    left_direction_update = {
                'E': 'N',
                'S': 'E',
                'W': 'S',
                'N': 'W',}

    def __init__(self, position, direction, grid):
        self.position = position
        self.direction = direction
        self.grid = grid

    def update_position(self):
        if self.direction == 'N' or self.direction == 'S':
            if self.direction == 'N':
                new_y = self.position.get_next_y_coord(1, len(self.grid[0]))
            else:
                new_y = self.position.get_next_y_coord(-1, len(self.grid[0]))
            if self.grid[self.position.x][new_y] == 'O':
                return self.position.obstacle_output(self.direction)
            self.position.set_y(new_y)
        else:
            if self.direction == 'E':
                new_x = self.position.get_next_x_coord(1, len(self.grid))
            else: # direction = 'W'
                new_x = self.position.get_next_x_coord(-1, len(self.grid))
            if self.grid[new_x][self.position.y] == 'O':
                return self.position.obstacle_output(self.direction)
            self.position.set_x(new_x)
        return None

    def _execute(self, command):
        if command == 'R':
            self.direction = self.right_direction_update[self.direction]
            return None
        elif command == 'L':
            self.direction = self.left_direction_update[self.direction]
            return None
        else: # assuming that the input was validated before, we have command = 'M'
            return self.update_position()

    def execute(self, commands):
        for c in commands:
            output = self._execute(c)
            if output is not None:
                return output
        return self.position.coords_output(self.direction)

    # def update_y_coord(self, delta):
    #     new_y_coord = self.position[1] + delta
    #     if new_y_coord < 0:

    # def increase_y_coord(self):
    #     self.update_y_coord(1)

    # def decrease_y_coord(self):
    #     self.update_y_coord(-1)       

class MarsRover():
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

    def get_next_coord(self, current_position, delta, side_length):
        current_position += delta
        if current_position < 0:
            return side_length - 1
        elif current_position == side_length:
            return 0
        return current_position

    def get_next_x_coord(self, delta):
        return self.get_next_coord(self.position[0], delta, len(self.grid[0]))

    def get_next_y_coord(self, delta):
        return self.get_next_coord(self.position[1], delta, len(self.grid))        

    def coords_output(self, *args):
        return ':'.join([':'.join(map(str, args)), self.direction])

    def obstacle_output(self, x, y):
        return f'O:{self.coords_output(self.position[0], self.position[1])}'

    def update_position(self):
        if self.direction == 'N' or self.direction == 'S':
            if self.direction == 'N':
                new_y = self.get_next_y_coord(1)
            else:
                new_y = self.get_next_y_coord(-1)
            if self.grid[self.position[0]][new_y] == 'O':
                return self.obstacle_output(self.position[1], new_y)
            self.position = (self.position[0], new_y)
        else:
            if self.direction == 'E':
                new_x = self.get_next_x_coord(1)
            else: # direction = 'W'
                new_x = self.get_next_x_coord(-1)
            if self.grid[new_x][self.position[1]] == 'O':
                return self.obstacle_output(new_x, self.position[1])
            self.position = (new_x, self.position[1])
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
        return self.coords_output(self.position[0], self.position[1])

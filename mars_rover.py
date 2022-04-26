
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

    def __init__(self, x, y, direction):
        self.x =  x
        self.y = y
        self.direction = direction
        
    def set_x(self, x):
        self.x = x
    
    def set_y(self, y):
        self.y = y

    def rotate_left(self):
        self.direction = self.left_direction_update[self.direction]

    def rotate_right(self):
        self.direction = self.right_direction_update[self.direction]

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

    def update_position(self, grid):
        if self.direction == 'N' or self.direction == 'S':
            if self.direction == 'N':
                new_y = self.get_next_y_coord(1, len(grid[0]))
            else:
                new_y = self.get_next_y_coord(-1, len(grid[0]))
            if grid[self.x][new_y] == 'O':
                return True
            self.set_y(new_y)
        else:
            if self.direction == 'E':
                new_x = self.get_next_x_coord(1, len(grid))
            else: # direction = 'W'
                new_x = self.get_next_x_coord(-1, len(grid))
            if grid[new_x][self.y] == 'O':
                return True
            self.set_x(new_x)
        return None


class MarsRoverAPI():

    def __init__(self, mars_rover, grid):
        self.mars_rover = mars_rover
        self.grid = grid

    def coords_string(self):
        return ':'.join([str(self.mars_rover.x), str(self.mars_rover.y)])

    def coords_output(self):
        return ':'.join([self.coords_string(), self.mars_rover.direction])

    def obstacle_output(self):
        return f'O:{self.coords_output()}'


    def _execute(self, command):
        if command == 'R':
            self.mars_rover.rotate_right()
        elif command == 'L':
            self.mars_rover.rotate_left()
        else: # assuming that the input was validated before, we have command = 'M'
            if self.mars_rover.update_position(self.grid) is True:
                return self.obstacle_output()

    def execute(self, commands):
        for c in commands:
            output = self._execute(c)
            if output is not None:
                return output
        return self.coords_output()

from abc import ABCMeta, abstractmethod


class MarsRoverState(metaclass=ABCMeta):
    @abstractmethod
    def rotate_left():
        '''Defines what each command does.'''

    @abstractmethod
    def rotate_right():
        '''Defines what each command does.'''
    
    @abstractmethod
    def move():
        '''Defines what each command does.'''

    def get_next_coord(self, current_coord, delta, side_length):
        next_coord = current_coord + delta
        if next_coord < 0:
            return side_length - 1
        elif next_coord == side_length:
            return 0
        return next_coord

    def get_next_x_coord(self, mars_rover, delta, side_length):
        return self.get_next_coord(mars_rover.x, delta, side_length)

    def get_next_y_coord(self, mars_rover, delta, side_length):
        return self.get_next_coord(mars_rover.y, delta, side_length)

    def is_facing_obstacle(self, grid, x, y):
        return grid[x][y] == 'O'


class FacingNorth(MarsRoverState):
    direction = 'N'

    def rotate_left(self, mars_rover):
        mars_rover.set_state(FacingWest())

    def rotate_right(self, mars_rover):
        mars_rover.set_state(FacingEast())

    def move(self, mars_rover, grid):
        new_y = self.get_next_y_coord(mars_rover, 1, len(grid))
        if self.is_facing_obstacle(grid, mars_rover.x, new_y):
            return True
        mars_rover.set_y(new_y)


class FacingEast(MarsRoverState):
    direction = 'E'

    def rotate_left(self, mars_rover):
        mars_rover.set_state(FacingNorth())

    def rotate_right(self, mars_rover):
        mars_rover.set_state(FacingSouth())

    def move(self, mars_rover, grid):
        new_x = self.get_next_x_coord(mars_rover, 1, len(grid[0]))
        if self.is_facing_obstacle(grid, new_x, mars_rover.y):
            return True
        mars_rover.set_x(new_x)


class FacingSouth(MarsRoverState):
    direction = 'S'

    def rotate_left(self, mars_rover):
        mars_rover.set_state(FacingEast())

    def rotate_right(self, mars_rover):
        mars_rover.set_state(FacingWest())

    def move(self, mars_rover, grid):
        new_y = self.get_next_y_coord(mars_rover, -1, len(grid))
        if self.is_facing_obstacle(grid, mars_rover.x, new_y):
            return True
        mars_rover.set_y(new_y)


class FacingWest(MarsRoverState):
    direction = 'W'

    def rotate_left(self, mars_rover):
        mars_rover.set_state(FacingSouth())

    def rotate_right(mars_rover):
        mars_rover.set_state(FacingNorth())

    def move(self, mars_rover, grid):
        new_x = self.get_next_x_coord(mars_rover, -1, len(grid[0]))
        if self.is_facing_obstacle(grid, new_x, mars_rover.y):
            return True
        mars_rover.set_x(new_x)

class MarsRover():
    def __init__(self, x, y, direction):
        self.x = x
        self.y = y
        self.state = None
        self.set_state_for_direction(direction)

    def set_state_for_direction(self, direction):
        if direction == 'N':
            self.set_state(FacingNorth())
        elif direction == 'E':
            self.set_state(FacingEast())
        elif direction == 'S':
            self.set_state(FacingSouth())
        else:
            self.set_state(FacingWest())

    def set_state(self, state):
        self.state = state

    def set_x(self, x):
        self.x = x

    def set_y(self, y):
        self.y = y

    def set_direction(self, direction):
        self.direction = direction

    def rotate_left(self):
        self.state.rotate_left(self)

    def rotate_right(self):
        self.state.rotate_right(self)

    def move(self, grid):
        return self.state.move(self, grid)


class ICommand(metaclass=ABCMeta):
    def __init__(self, mars_rover):
        self._mars_rover = mars_rover

    @abstractmethod
    def execute():
        '''Defines what each command does.'''


class RotateLeft(ICommand):
    def execute(self):
        self._mars_rover.rotate_left()


class RotateRight(ICommand):
    def execute(self):
        self._mars_rover.rotate_right()


class Move(ICommand):
    def __init__(self, mars_rover, grid):
        super().__init__(mars_rover)
        self._grid = grid

    def execute(self):
        return self._mars_rover.move(self._grid)


class MarsRoverAPI():
    def __init__(self, mars_rover, grid):
        self.mars_rover = mars_rover
        self.grid = grid
        self.commands = self.register_commands()

    def register_commands(self):
        return {'L': RotateLeft(self.mars_rover),
                'R': RotateRight(self.mars_rover),
                'M': Move(self.mars_rover, self.grid), }

    def coords_string(self):
        return ':'.join([str(self.mars_rover.x), str(self.mars_rover.y)])

    def coords_output(self):
        return ':'.join([self.coords_string(), self.mars_rover.state.direction])

    def obstacle_output(self):
        return f'O:{self.coords_output()}'

    def execute(self, commands):
        for c in commands:
            output = self.commands[c].execute()
            if output is True:
                return self.obstacle_output()
        return self.coords_output()

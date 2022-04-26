import unittest
from mars_rover import *

class TestMarsRoverBasicMoves(unittest.TestCase):
    def setUp(self):
        self.grid = [['' for i in range(10)] for i in range(10)]

    def testMoveNorth(self):
        mars_rover = MarsRover((2, 7), 'W', self.grid)
        self.assertEqual(mars_rover.execute('M'), '1:7:W')
    
    def testMoveSouth(self):
        mars_rover = MarsRover((2, 7), 'S', self.grid)
        self.assertEqual(mars_rover.execute('M'), '2:6:S')

    def testMoveEast(self):
        mars_rover = MarsRover((2, 7), 'E', self.grid)
        self.assertEqual(mars_rover.execute('M'), '3:7:E')

    def testMoveWest(self):
        mars_rover = MarsRover((2, 7), 'W', self.grid)
        self.assertEqual(mars_rover.execute('M'), '1:7:W')

    def testRotate(self):
        mars_rover = MarsRover((0, 0), 'E', self.grid)
        self.assertEqual(mars_rover.execute('L'), '0:0:N')
        self.assertEqual(mars_rover.execute('R'), '0:0:E')

class TestMarsRoverPaths(unittest.TestCase):
    def setUp(self):
        self.grid = [['' for i in range(10)] for i in range(10)]

    def testBorderWrapping(self):
        mars_rover = MarsRover((0, 0), 'S', self.grid)
        self.assertEqual(mars_rover.execute('M'), '0:9:S')
        
    def testPathWithoutObstacles(self):
        mars_rover = MarsRover((0, 0), 'N', self.grid)
        self.assertEqual(mars_rover.execute('MMRMMLM'), '2:3:N')

    def testWrappingPathWithoutObstacles(self):
        mars_rover = MarsRover((0, 0), 'N', self.grid)
        self.assertEqual(mars_rover.execute('MMMMMMMMMM'), '0:0:N')
    
    def testPathWithObstacle(self):
        self.grid[0][3] = 'O'
        mars_rover = MarsRover((0, 0), 'N', self.grid)
        self.assertEqual(mars_rover.execute('MMMM'), 'O:0:2:N')

if __name__ == '__main__':
    unittest.main()
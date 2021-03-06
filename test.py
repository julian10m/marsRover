import unittest
from mars_rover import *

class TestMarsRoverBasicMoves(unittest.TestCase):
    def setUp(self):
        self.grid = [['' for i in range(10)] for i in range(10)]

    def testMoveNorth(self):
        mars_rover_api = MarsRoverAPI(MarsRover(2, 7, 'W'), self.grid)
        self.assertEqual(mars_rover_api.execute('M'), '1:7:W')

    def testMoveSouth(self):
        mars_rover_api = MarsRoverAPI(MarsRover(2, 7, 'S'), self.grid)
        self.assertEqual(mars_rover_api.execute('M'), '2:6:S')

    def testMoveEast(self):
        mars_rover_api = MarsRoverAPI(MarsRover(2, 7, 'E'), self.grid)
        self.assertEqual(mars_rover_api.execute('M'), '3:7:E')

    def testMoveWest(self):
        mars_rover_api = MarsRoverAPI(MarsRover(2, 7, 'W'), self.grid)
        self.assertEqual(mars_rover_api.execute('M'), '1:7:W')

    def testMoveIncresingStepSize(self):
        mars_rover_api = MarsRoverAPI(MarsRover(2, 7, 'W'), self.grid)
        MarsRover.step_size = 2
        self.assertEqual(mars_rover_api.execute('M'), '0:7:W')
        MarsRover.step_size = len(self.grid[0])
        self.assertEqual(mars_rover_api.execute('M'), '0:7:W')
        MarsRover.step_size = 2 * len(self.grid[0])
        self.assertEqual(mars_rover_api.execute('M'), '0:7:W')
        MarsRover.step_size = 2 * len(self.grid[0]) + 1
        self.assertEqual(mars_rover_api.execute('M'), '9:7:W')

class TestMarsRoverBasicRotations(unittest.TestCase):
    def testRotateFromNorth(self):
        mars_rover_api = MarsRoverAPI(MarsRover(0, 0, 'N'), [])
        self.assertEqual(mars_rover_api.execute('L'), '0:0:W')
        self.assertEqual(mars_rover_api.execute('R'), '0:0:N')
        self.assertEqual(mars_rover_api.execute('R'), '0:0:E')    

    def testRotateFromEast(self):
        mars_rover_api = MarsRoverAPI(MarsRover(0, 0, 'E'), [])
        self.assertEqual(mars_rover_api.execute('L'), '0:0:N')
        self.assertEqual(mars_rover_api.execute('R'), '0:0:E')
        self.assertEqual(mars_rover_api.execute('R'), '0:0:S')

    def testRotateFromSouth(self):
        mars_rover_api = MarsRoverAPI(MarsRover(0, 0, 'S'), [])
        self.assertEqual(mars_rover_api.execute('L'), '0:0:E')
        self.assertEqual(mars_rover_api.execute('R'), '0:0:S')
        self.assertEqual(mars_rover_api.execute('R'), '0:0:W')

    def testRotateFromWest(self):
        mars_rover_api = MarsRoverAPI(MarsRover(0, 0, 'W'), [])
        self.assertEqual(mars_rover_api.execute('L'), '0:0:S')
        self.assertEqual(mars_rover_api.execute('R'), '0:0:W')
        self.assertEqual(mars_rover_api.execute('R'), '0:0:N')

class TestMarsRoverPaths(unittest.TestCase):
    def setUp(self):
        self.grid = [['' for i in range(10)] for i in range(10)]
        MarsRover.step_size = 1

    def testBorderWrapping(self):
        mars_rover_api = MarsRoverAPI(MarsRover(0, 0, 'S'), self.grid)
        self.assertEqual(mars_rover_api.execute('M'), '0:9:S')
        self.assertEqual(mars_rover_api.execute('RRM'), '0:0:N')
        
    def testBorderWrapping(self):
        mars_rover_api = MarsRoverAPI(MarsRover(0, 0, 'W'), self.grid)
        self.assertEqual(mars_rover_api.execute('M'), '9:0:W')
        self.assertEqual(mars_rover_api.execute('LLM'), '0:0:E')

    def testPathWithoutObstacles(self):
        mars_rover_api = MarsRoverAPI(MarsRover(0, 0, 'N'), self.grid)
        self.assertEqual(mars_rover_api.execute('MMRMMLM'), '2:3:N')

    def testWrappingPathWithoutObstacles(self):
        mars_rover_api = MarsRoverAPI(MarsRover(0, 0, 'N'), self.grid)
        self.assertEqual(mars_rover_api.execute('MMMMMMMMMM'), '0:0:N')
    
    def testPathWithObstacle(self):
        self.grid[0][3] = 'O'
        mars_rover_api = MarsRoverAPI(MarsRover(0, 0, 'N'), self.grid)
        self.assertEqual(mars_rover_api.execute('MMMM'), 'O:0:2:N')

if __name__ == '__main__':
    unittest.main()
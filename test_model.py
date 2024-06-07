import copy
import unittest
from model import Cell, Board

class TestModel(unittest.TestCase):

    def test_row_completion_4x3(self) -> None:
        cells = [Cell(0, 0, 0),
                Cell(1, 0, 0), Cell(1, 1, 0), Cell(1, 2, 0),
                Cell(2, 0, 0), Cell(2, 1, 0), Cell(2, 2, 0),
                Cell(3, 0, 0), Cell(3, 1, 0), Cell(3, 2, 0)]
        board = Board(4, 3, copy.deepcopy(cells))
        self.assertEqual(board.get_layout(), [[True, False, False], 
                                              [True, True, True], 
                                              [True, True, True], 
                                              [True, True, True]])
        self.assertEqual(board.get_completed_rows(), [1, 2, 3])

        board.remove_rows([1, 2, 3])
        self.assertEqual(board.get_layout(), [[False, False, False],
                                              [False, False, False],
                                              [False, False, False], 
                                              [True, False, False]])
        
        board = Board(4, 3, copy.deepcopy(cells))
        board.remove_rows([1])
        self.assertEqual(board.get_layout(), [[False, False, False],
                                              [True, False, False],
                                              [True, True, True], 
                                              [True, True, True]])
        
        board.remove_rows([3])
        self.assertEqual(board.get_layout(), [[False, False, False],
                                              [False, False, False],
                                              [True, False, False],
                                              [True, True, True]])
        
        board.remove_rows([3])
        self.assertEqual(board.get_layout(), [[False, False, False],
                                              [False, False, False],
                                              [False, False, False],
                                              [True, False, False]])
        
        board.remove_rows([3])
        self.assertEqual(board.get_layout(), [[False, False, False],
                                              [False, False, False],
                                              [False, False, False],
                                              [False, False, False]])
        
        board.remove_rows([0, 1, 2, 3])
        self.assertEqual(board.get_layout(), [[False, False, False],
                                              [False, False, False],
                                              [False, False, False],
                                              [False, False, False]])

    def test_row_completion_4x4(self):
        cells = [Cell(0, 0, 0),
                Cell(1, 0, 0), Cell(1, 1, 0), Cell(1, 2, 0), Cell(1, 3, 0),
                Cell(2, 1, 0), Cell(2, 2, 0),
                Cell(3, 3, 0), Cell(3, 2, 0), Cell(3, 1, 0), Cell(3, 0, 0)]
        board = Board(4, 4, cells)
        self.assertEqual(board.get_layout(), [[True, False, False, False], 
                                              [True, True, True, True], 
                                              [False, True, True, False], 
                                              [True, True, True, True]])
        self.assertEqual(board.get_completed_rows(), [1, 3])

        board.remove_rows([1, 3])
        self.assertEqual(board.get_layout(), [[False, False, False, False],
                                              [False, False, False, False],
                                              [True, False, False, False], 
                                              [False, True, True, False]])
        
        board.remove_rows([3])
        self.assertEqual(board.get_layout(), [[False, False, False, False],
                                              [False, False, False, False],
                                              [False, False, False, False],
                                              [True, False, False, False]])

if __name__ == '__main__':
    unittest.main()

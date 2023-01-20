import unittest
from column_game_mechanics import ColumnState, Input

## The game can begin with an empty field of the correct size.
## The game can begin with the contents of the field specified, with jewels in some of the cells.
## When there are "holes" in the contents of the field specified at the beginning, the jewels "fall" immediately to fill the empty spaces below them.
## It is possible to quit the program with the Q command. (I did this one fairly early; you might want to do the same.)
## A faller can be created in a column and appear with only the bottommost of its three jewels visible.
## Fallers can be moved to the left and to the right at any point until they have frozen.
## Fallers cannot be moved to the left or right if they are blocked by jewels that are previously frozen.
## Fallers can be rotated at any point until they have frozen.
## Fallers land when they can't be moved down any further.
## Fallers freeze at the next "tick" of time after they have landed.
## The freezing of a faller can be postponed by moving it to a column with empty space underneath it after landing.
## The game ends when a faller freezes but cannot be displayed entirely in the field because it didn't move down far enough.
## Matching can be performed horizontally (i.e., three jewels of the same color horizontally would be considered to match).
## Matching can be performed vertically.
## Matching can be performed diagonally.
## Matched sequences longer than three jewels are handled.
## More than one matching sequence at the same time can be handled.
# The ending of a game can be postponed if a faller freezes without fitting in the field, but which matches enough jewels that everything then fits.
## When there are three or more jewels in a row in the contents of the field specified at the beginning, matching is triggered.
## When there are "holes" in the contents of the field specified at the beginning and jewels fill the spaces immediately, matching is triggered if three or more jewels in a row are present.

class ColumnGameTest(unittest.TestCase):
    def setUp(self):
        self._columnstate = ColumnState()

    # def test_input_empty(self):
    #     initial_info = Input.get_initial()
    #     self.assertEqual(type(initial_info[0]), int)
    #     self.assertEqual(type(initial_info[1]), int)

    def _basic_setup(self):
        self._columnstate.empty_setup(10, 4)

    def _basic_given_setup(self):
        self._columnstate.empty_setup(4, 4)
        given_board_info = ['Y X ', 'S V ', 'TXYS', 'X XY']
        given_board = Input.get_setup_content(4, 4, given_board_info)
        self._columnstate.load_initial_content(given_board)

    def test_game_begins_with_empty_field_with_size(self):
        self._columnstate.empty_setup(4, 7)
        self.assertEqual(len(self._columnstate.get_board()[0]), 4)
        self.assertEqual(len(self._columnstate.get_board()), 7)

    def test_game_begins_with_content(self):
        self._basic_given_setup()
        self.assertEqual(self._columnstate.get_board(), [['Y', 'S', 'T', 'X'], [' ', ' ', 'X', ' '], ['X', 'V', 'Y', 'X'], [' ', ' ', 'S', 'Y']])

    def test_jewels_fall_into_place(self):
        self._basic_given_setup()
        self._columnstate.adjust_fall()
        self.assertEqual(self._columnstate.get_board(), [['Y', 'S', 'T', 'X'], [' ', ' ', ' ', 'X'], ['X', 'V', 'Y', 'X'], [' ', ' ', 'S', 'Y']])

    # def test_q_for_quit(self):
    #     running = True
    #     while running:
    #         command = Input.get_command()
    #         if command[0] == 'Q':
    #             running = False
    #     self.assertEqual(running, False)

    def test_initialize_faller(self):
        self._basic_setup()
        self._columnstate.initialize_faller(3, ('X', 'Y', 'Z'))
        self.assertEqual(self._columnstate.get_board(), [[' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], ['Z', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']])

    def test_faller_can_fall(self):
        self._basic_setup()
        self._columnstate.initialize_faller(3, ('X', 'Y', 'Z'))
        self._columnstate.faller_fall()
        self.assertEqual(self._columnstate.get_board(), [[' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], ['Y', 'Z', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']])

    def test_left_right_faller_move(self):
        self._basic_setup()
        self._columnstate.initialize_faller(3, ('X', 'Y', 'Z'))
        self._columnstate.faller_move_left()
        self._columnstate.faller_move_left()
        self._columnstate.faller_move_right()
        self._columnstate.faller_fall()
        self.assertEqual(self._columnstate.get_board(), [[' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], ['Y', 'Z', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']])
        # print()
        # self._columnstate.print_board()

    def test_left_right_faller_move_blocked(self):
        self._basic_given_setup()
        self._columnstate.initialize_faller(3, ('X', 'Y', 'Z'))
        self._columnstate.faller_move_left()
        self._columnstate.faller_fall()
        self.assertEqual(self._columnstate.get_board(), [['Y', 'S', 'T', 'X'], [' ', ' ', 'X', ' '], ['X', 'V', 'Y', 'X'], ['Y', 'Z', 'S', 'Y']])

    def test_faller_rotation(self):
        self._basic_setup()
        self._columnstate.initialize_faller(3, ('X', 'Y', 'Z'))
        self._columnstate.faller_fall()
        self._columnstate.faller_fall()
        self._columnstate.faller_rotate()
        self.assertEqual(self._columnstate.get_board(), [[' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], ['Z', 'X', 'Y', ' ', ' ', ' ', ' ', ' ', ' ', ' ']])

    def test_faller_fall_blocked(self):
        self._basic_setup()
        self._columnstate.initialize_faller(3, ('X', 'Y', 'Z'))
        for i in range(9):
            # print()
            # self._columnstate.print_board()
            self._columnstate.faller_fall()
        self.assertEqual(self._columnstate.get_board(), [[' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], [' ', ' ', ' ', ' ', ' ', ' ', ' ', 'X', 'Y', 'Z']])

if __name__ == '__main__':
    unittest.main()

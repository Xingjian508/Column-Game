from column_game_mechanics import ColumnState, Faller
import pygame
import random

## The field will always consist of 13 rows and 6 columns, and will always start out empty.
## The seven colors of jewels were represented as uppercase letters previously. Instead, choose seven colors — you can choose any colors you'd like, though they should be different enough that you can easily tell the difference between them at a glance. (You might want your game mechanics to still refer to them using uppercase letters, and that's fine; but when you display them, what differentiates the jewels should be their colors.)
## There needs to be some kind of visual cue when fallers land. Additionally, if you support matching, you would ideally want a visual cue when jewels match before they disappear, as well. You have your choice about these visual cues — you can use colors or other visual effects.
## Rather than the user adding fallers manually, they appear randomly. Whenever there isn't a faller in the field, a new one appears in a randomly-chosen column and consisting of random colors. (When choosing a column randomly, never choose a column that is already filled with frozen jewels, unless all columns are already filled with jewels.)
## Rather than the user pressing the Enter key to simulate the passage of time, you'll instead "tick" the game mechanics once per second automatically.
## Rather than the user typing commands like R, <, and > in the Python shell to rotate and move the faller, the user instead should move them by pressing keys on the keyboard; every keypress rotates or moves the faller once. So that we'll know how to grade your project, we'll all use the same keys: left arrow and right arrow should move the faller to the left and right, respectively, while the spacebar should rotate the faller.

# To-Do, as of Nov 27:
## - Finish up the run() function below, which uses "redraw()" to display the board.
## - Finish up the user interface and input interactions with the buttons.
# - Do a diagram of the entire thing to get more organized. Think how to modify programs this way.


class ColumnInterface:
    def handle_command(command: list, columnstate: ColumnState) -> bool:
        if command == '':
            pass
        elif command == 'return':
            # FALL or FREEZE.
            game_status = columnstate.faller_fall()
            if game_status == False:
                return False
        elif command[0] == 'Q':
            # GAME QUITS HERE.
            return 'EXIT'
        elif command[0] == 'R':
            # ROTATE.
            columnstate.faller_rotate()
        elif command[0] == '<':
            # MOVE LEFT.
            columnstate.faller_move_left()
        elif command[0] == '>':
            # MOVE RIGHT.
            columnstate.faller_move_right()
        elif command[0] == 'F':
            # NEW FALLER.
            columnstate.initialize_faller(command[1]-1, (command[2], command[3], command[4]))
            pass
        else:
            raise Exception("Initial input is wrong.")
        return True

    def determine_if_landed(columnstate: ColumnState) -> bool:
        landed = False
        if columnstate.get_landed():
            landed = True
        if columnstate.get_faller().get_col() == None and columnstate.get_faller().get_lowest_pos() == None:
            if columnstate.get_backup_faller().get_col() != None and columnstate.get_backup_faller().get_lowest_pos() != None:
                landed = True
        return landed

    def fill_grid(surface, x: int, y: int) -> None:
        for i in range(6):
            pygame.draw.line(surface, pygame.Color(240,255,255), (i*(x/6), 0), (i*(x/6), y))
        for j in range(13):
            pygame.draw.line(surface, pygame.Color(240,255,255), (0, j*(y/13)), (x, j*(y/13)))

    def draw_board(surface, columnstate, landed):
        board = columnstate.get_board()
        col = columnstate.get_faller().get_col()
        lowest_pos = columnstate.get_faller().get_lowest_pos()
        ColumnInterface.display_board(surface, columnstate.get_board(), columnstate.get_faller().get_col(), columnstate.get_faller().get_lowest_pos(), landed)

    def get_color(letter):
        new_letter = letter
        if letter[0] == '*':
            if letter[1] == '*':
                new_letter = letter[2]
            else:
                new_letter = letter[1]
        if new_letter == 'S':
            return pygame.Color('aqua')
        if new_letter == 'T':
            return pygame.Color('azure4')
        if new_letter == 'U':
            return pygame.Color('bisque1')
        if new_letter == 'V':
            return pygame.Color('darkblue')
        if new_letter == 'W':
            return pygame.Color('cadetblue3')
        if new_letter == 'Y':
            return pygame.Color('chartreuse4')
        if new_letter == 'Z':
            return pygame.Color('darkorchid4')

    def display_board(surface, board: list, col: int, lowest_pos: int, landed: bool):
        for j in range(len(board[0])):
            for i in range(len(board)):
                if board[i][j] == ' ':
                    pass
                elif landed and col != None and ((i, j) == (col, lowest_pos) or (i, j) == (col, lowest_pos-1) or (i, j) == (col, lowest_pos-2)):
                    # Landed.
                    ColumnInterface.draw_single_color_landed(surface, i, j, ColumnInterface.get_color(board[i][j]))
                elif col != None and ((i, j) == (col, lowest_pos) or (i, j) == (col, lowest_pos-1) or (i, j) == (col, lowest_pos-2)):
                    ColumnInterface.draw_faller_color(surface, i, j, ColumnInterface.get_color(board[i][j]))
                elif board[i][j][0] == '*':
                    ColumnInterface.draw_single_color_matching(surface, i, j, ColumnInterface.get_color(board[i][j][-1]))
                else:
                    ColumnInterface.draw_single_color(surface, i, j, ColumnInterface.get_color(board[i][j]))

    def draw_single_color(surface, col, index, color):
        x, y = surface.get_size()
        pygame.draw.rect(surface, color, pygame.Rect(col*(x/6)+1, index*(y/13)+1, (x/6)-1, (y/13)-1))

    def draw_single_color_landed(surface, col, index, color):
        x, y = surface.get_size()
        pygame.draw.rect(surface, color, pygame.Rect(col*(x/6)+(x/36), index*(y/13)+(y/78), (x/6)-(x/36)-1, (y/13)-(y/78-1)))

    def draw_single_color_matching(surface, col, index, color):
        x, y = surface.get_size()
        ColumnInterface.draw_single_color(surface, col, index, pygame.Color('darkred'))
        ColumnInterface.draw_faller_color(surface, col, index, color)

    def draw_faller_color(surface, col, index, color):
        x, y = surface.get_size()
        pygame.draw.rect(surface, color, pygame.Rect(col*(x/6)+(x/36), index*(y/13)+(y/78), (x/6)-(2*x/36), (y/13)-(2*y/78)))

    def display_text(surface, x, y):
        green = (0, 255, 0)
        blue = (0, 0, 128)
        pygame.display.set_caption('Show Text')
        font = pygame.font.Font('freesansbold.ttf', 10)
        text1 = font.render('Press "f" to initialize, or initialize fallers when needed.', True, green, blue)
        text2 = font.render('Press "left/right arrows" to go left and right, "space" to rotate.', True, green, blue)
        rectangle = text1.get_rect()
        rectangle.center = (x/2, y/5)
        surface.blit(text1, rectangle)
        rectangle.center = (x/2, y/5+10)
        surface.blit(text2, rectangle)

    def redraw(surface, columnstate, landed):
        # 1. Draws the grid.
        x, y = surface.get_size()
        surface.fill((0,0,0))
        ColumnInterface.fill_grid(surface, x, y)
        # 2. Draws the board.
        ColumnInterface.draw_board(surface, columnstate, landed)
        ColumnInterface.display_text(surface, x, y)

    def resize_surface(size: tuple[int, int]) -> None:
        pygame.display.set_mode(size, pygame.RESIZABLE)

    def handle_key(key):
        # Left.
        if str(key) == '1073741904':
            return ['<']
        # Right.
        elif str(key) == '1073741903':
            return ['>']
        # Rotate.
        elif str(key) == '32':
            return 'R'
        elif str(key) == '102':
            output_list = ['F']
            choices = ['S', 'T', 'U', 'V', 'W', 'Y', 'Z']
            cols = [1, 2, 3, 4, 5, 6]
            output_list.append(random.choices(cols)[0])
            output_list.append(random.choice(choices))
            output_list.append(random.choice(choices))
            output_list.append(random.choice(choices))
            return output_list

    def run():
        pygame.init()

        columnstate = ColumnState()
        columnstate.empty_setup(13, 6)

        surface = pygame.display.set_mode((450, 975), pygame.RESIZABLE)
        surface.fill(pygame.Color(0, 0, 0))

        running = True
        changed = False
        landed = False
        clock = pygame.time.Clock()



        next_time_102 = False
        while running:
            clock.tick(2)

            # 1. Getting commands.
            command = 'return'
            if next_time_102:
                command = ColumnInterface.handle_key('102')
                next_time_102 = False
            if landed and (changed == False) and (next_time_102 == False):
                next_time_102 = True
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.VIDEORESIZE:
                    ColumnInterface.resize_surface(event.size)
                elif event.type == pygame.KEYDOWN:
                    command = ColumnInterface.handle_key(event.key)

            # 2. Game logic.
            if changed:
                columnstate.check_and_erase_matchings()
                columnstate.adjust_fall()
            if columnstate.get_faller().get_col() == None or columnstate.get_faller().get_lowest_pos() == None:
                changed = columnstate.check_and_mark_matchings()
                if changed:
                    command = 'return'
            landed = columnstate.get_landed()

            # 3. Displaying the board.
            ColumnInterface.redraw(surface, columnstate, landed)
            pygame.display.flip()

            # 4. Handling commands.
            game_status = ColumnInterface.handle_command(command, columnstate)
            if game_status == 'EXIT':
                break
            if game_status == False:
                # Game quits here.
                running = False

        pygame.quit()

if __name__ == '__main__':
    ColumnInterface.run()

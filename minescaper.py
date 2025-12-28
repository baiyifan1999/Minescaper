# stage 1
def create_mine_board(grid_size, mine_positions):
    """
    Fill blank grids with valid positions and expel the corner positions.
    Then calculate positions of mines, substitute these positions with -1
    """
    # set up a grid filled with 0.
    grid = [[0 for i in range(grid_size)] for i in range(grid_size)]
    
    # work out valid positions.
    valid_positions = [pos for pos in mine_positions
    if pos != (0, 0) and pos != (grid_size - 1, grid_size - 1)]

    # substitute 0 of mine positions with -1.
    for x, y in valid_positions:
        grid[x][y] = -1

    # for mine positions plus 1 to all adjacent non-mine positions. 
    for x, y in valid_positions:
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue
                nx, ny = x + dx, y + dy
                if 0 <= nx < grid_size and 0 <= ny < grid_size:
                    if grid[nx][ny] != -1:
                        grid[nx][ny] += 1

    return grid

# stage 2
def process_input(mine_board, current_pos, move_str):
    """
    Make a movement of mines by calculating positions 
    of rows and columns in four directions.
    Mark the positions after movement and make sure they are in valid range. 
    """
    x, y = current_pos
    dx = x
    dy = y
    
    # rewrite move_str into lower letters，
    # reserve letters in 'wasdf', reserve the first three letters.
    move = [char for char in move_str.lower() if char in 'wasdf'][:3]

    # reserve the firsttwo letters of direction.
    direction = [char for char in move if char in 'wasd'][:2]

    # if there's no valid movement, return the initial position.
    if list(move) == []:
        return x, y, False

    # make a movement.
    for i in move:
        if i == 'w':
            dx = x - 1
        elif i == 'a':
            dy = y - 1
        elif i == 's':
            dx = x + 1
        elif i == 'd':
            dy = y + 1

    # estimate valid flag.
    board_range = len(mine_board)
    valid_flag = (
        len(direction) > 0 
        and len(move) == len(direction) + 1 
        and move[-1] == 'f' 
        and 0 <= dx < board_range 
        and 0 <= dy < board_range 
        and (dx, dy) not in [(0, 0), (board_range - 1, board_range -1)]
        )

    if valid_flag:
        return dx, dy, True
    
    # make a movement and estimate if it is in valid range.
    else:
        if 0 <= dx < board_range and 0 <= dy < board_range:
            return dx, dy, False
        else:
            return x, y, False
    
# stage 3
def reveal_zeros(mine_board, visited, current_pos):
    """
    Calculate whether the adjacent grids of visited grids are safe
    by checking their adjacent mine count,
    add these grids into safe cells to expand safe zone.
    """
    visited_update = set()
    to_visit = [current_pos]

    # when there's still positions in to_visit, keep cycling
    while to_visit:
        x, y = to_visit.pop()
    
        # skip chosen grids
        if (x, y) in visited_update or (x, y) in visited:
            continue

        # add new grids into visited_update
        visited_update.add((x, y))

        # expand the adjacent grids of whose value is 0
        if mine_board[x][y] == 0:
            for dx in [-1, 0, 1]:
                for dy in [-1, 0, 1]:
                    if dx == 0 and dy == 0:
                        continue

                    # generate positions and make sure they are valid
                    # add valid positions to to_visit
                    nx, ny = x + dx, y + dy
                    if (
                        0 <= nx < len(mine_board) 
                        and 0 <= ny < len(mine_board[0])
                        ):
                        if (
                            mine_board[nx][ny] != -1 and (nx, ny) 
                            not in visited 
                            and (nx, ny) not in visited_update
                            ):
                            to_visit.append((nx, ny))

    return visited_update | visited
        
# stage 4
def create_game_board(
    mine_board, visited, current_pos, flagged, show_all=False
    ):
    """
    Show the board status:
    If the game is win or lose, 
    show the positions of mines, current location, 
    adjacent mine count, the exit, flag,
    and other information by calculating these positions and
    fill them into the board.
    """
    row = len(mine_board)
    col = len(mine_board[0])
    
    # copy the board
    # fill all the values with ' . '
    # fill the lower rightcorner with ' E '
    game_board = [[' . ' for i in range(col)] for i in range(row)]
    game_board[row - 1][col - 1] = ' E '
    
    # when there is no mine:
    # substitute visited grid with value
    for x, y in visited:
        if (x, y) != current_pos:
            val = mine_board[x][y]
            game_board[x][y] = f' {val} '

    # mark current positions
    x, y = current_pos
    val = mine_board[x][y]
    if val == -1:
        game_board[x][y] = '[*]'
    elif (x, y) == (row - 1, col - 1):
        game_board[x][y] = '[E]'
    else:
        game_board[x][y] = f'[{val}]'

    # mark the flags
    for x, y in flagged:
        if (x, y) != current_pos and (x, y) not in visited:
            game_board[x][y] = ' F '

    # when there is a mine:
    # show the board of values and mines
    if show_all:
        for i in range(row):
            for j in range(col):
                if (i, j) == current_pos:
                    continue
                elif mine_board[i][j] == -1:
                    game_board[i][j] = ' * '
                elif (i, j) == (row - 1, col -1):
                    game_board[i][j] = ' E '
                else:
                    game_board[i][j] = f' {mine_board[i][j]} '

    return game_board
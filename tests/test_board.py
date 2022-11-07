from battleship.board import Board
from battleship.ship import Ship


def test_board():
    ships = [
        Ship(start=(3, 1), end=(3, 5)),  # length = 5
        Ship(start=(9, 7), end=(9, 10)),  # length = 4
        Ship(start=(1, 9), end=(3, 9)),  # length = 3
        Ship(start=(5, 2), end=(6, 2)),  # length = 2
        Ship(start=(8, 3), end=(8, 3)),  # length = 1
    ]

    board = Board(ships=ships)
    print(board.ships)
    is_ship_hit, has_ship_sunk = board.is_attacked_at((3, 4))
    print(is_ship_hit, has_ship_sunk)
    assert is_ship_hit == True
    assert has_ship_sunk == False

def test_are_ships_within_bounds():

    # These ships are out of the map
    try:
        ships = [
            Ship(start=(3, 1), end=(3, 5)),  # length = 5
            Ship(start=(9, 7), end=(9, 10)),  # length = 4
            Ship(start=(1, 9), end=(3, 9)),  # length = 3
            Ship(start=(5, 2), end=(6, 2)),  # length = 2
            Ship(start=(11, 3), end=(11, 3)),  # length = 1 OUT OF THE MAP
        ]
        board = Board(ships=ships)

        output = board.are_ships_within_bounds()
        condition = False
    except ValueError:
        condition = True
        pass

    assert condition

    # These ships are not out of the map
    ships = [
        Ship(start=(3, 1), end=(3, 5)),  # length = 5
        Ship(start=(9, 7), end=(9, 10)),  # length = 4
        Ship(start=(1, 9), end=(3, 9)),  # length = 3
        Ship(start=(5, 2), end=(6, 2)),  # length = 2
        Ship(start=(8, 3), end=(8, 3)),  # length = 1
    ]
    board = Board(ships=ships)
    output = board.are_ships_within_bounds()
    assert output == True


def test_are_ships_too_close():

    # Not too close
    ships = [
        Ship(start=(3, 1), end=(3, 5)),  # length = 5
        Ship(start=(9, 7), end=(9, 10)),  # length = 4
        Ship(start=(1, 9), end=(3, 9)),  # length = 3
        Ship(start=(5, 5), end=(6, 5)),  # length = 2
        Ship(start=(8, 3), end=(8, 3)),  # length = 1
    ]
    board = Board(ships=ships)
    output = board.are_ships_too_close()
    assert not output

    # Too close
    try:
        ships = [
            Ship(start=(3, 1), end=(3, 5)),  # length = 5
            Ship(start=(9, 7), end=(9, 10)),  # length = 4
            Ship(start=(1, 9), end=(3, 9)),  # length = 3
            Ship(start=(6, 3), end=(7, 3)),  # length = 2 This ship
            Ship(start=(8, 3), end=(8, 3)),  # length = 1 And this ship are too close
        ]
        board = Board(ships=ships)
        output = board.are_ships_too_close()
        assert not output
        condition = False
    except KeyError:
        condition = True
    assert condition


def test_have_all_ships_sunk():
    ships = [
        Ship(start=(3, 1), end=(3, 5)),  # length = 5
        Ship(start=(9, 7), end=(9, 10)),  # length = 4
        Ship(start=(1, 9), end=(3, 9)),  # length = 3
        Ship(start=(5, 5), end=(6, 5)),  # length = 2
        Ship(start=(8, 3), end=(8, 3)),  # length = 1
    ]
    board = Board(ships=ships)
    output = board.have_all_ships_sunk()
    assert not output


if __name__ == "__main__":
    test_are_ships_within_bounds()
    test_are_ships_too_close()
    test_are_ships_too_close()
    test_board()

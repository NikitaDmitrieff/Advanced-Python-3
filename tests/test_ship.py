from battleship.ship import Ship

def test_horizontal():
    start = (4, 5)
    end = (2, 5)
    ship = Ship(start=start, end=end)
    output = ship.is_horizontal()
    print(output)
    assert output == True

def test_vertical():
    start = (4, 3)
    end = (4, 5)
    ship = Ship(start=start, end=end)
    output = ship.is_vertical()
    print(output)
    assert output == True

def test_get_cells():

    # Tests for the horizontal case
    start = (4, 5)
    end = (2, 5)
    ship = Ship(start=start, end=end)
    output = ship.get_cells()
    # print("This is for the horizontal case", output)
    assert output == set([start, (3, 5), end])

    # Tests for the one-square ship case
    start = (4, 5)
    end = (4, 5)
    ship = Ship(start=start, end=end)
    output = ship.get_cells()
    # print("This is for the vertical case", output)
    assert output == set([start])

    # Tests for the one-square ship case
    start = (4, 3)
    end = (4, 5)
    ship = Ship(start=start, end=end)
    output = ship.get_cells()
    # print("This is for the one-square case", output)
    assert output == set([start, (4, 4), end])


def test_length():

    # For a ship of length 3
    start = (4, 5)
    end = (2, 5)
    ship = Ship(start=start, end=end)
    output = ship.length()
    print(output)
    assert output == 3

    # For a ship of length 1
    start = (4, 5)
    end = (4, 5)
    ship = Ship(start=start, end=end)
    output = ship.length()
    print("This is for the ship of length 1 case", output)
    assert output == 1


def test_is_occupying_cell():

    # The ship occupies the cell
    start = (4, 5)
    end = (2, 5)
    ship = Ship(start=start, end=end)
    cell = (3, 5)
    output = ship.is_occupying_cell(cell)
    print(output)
    assert output == True

    # The ship does not
    start = (4, 5)
    end = (2, 5)
    ship = Ship(start=start, end=end)
    cell = (7, 5)
    output = ship.is_occupying_cell(cell)
    print(output)
    assert output == False


def test_receive_damage():

    # Ship receives damage
    start = (4, 5)
    end = (2, 5)
    ship = Ship(start=start, end=end)
    cell = (3, 5)
    output = ship.receive_damage(cell)
    print(output)
    assert output
    assert ship.damaged_cells == {cell}

    # The ship does not
    start = (4, 5)
    end = (2, 5)
    ship = Ship(start=start, end=end)
    cell = (7, 5)
    output = ship.receive_damage(cell)
    print(output)
    assert output == False
    assert ship.damaged_cells == set()

def test_count_damaged_cells():
    # Ship receives 1 damage
    start = (4, 5)
    end = (2, 5)
    ship = Ship(start=start, end=end)
    cell = (3, 5)
    ship.receive_damage(cell)
    output = ship.count_damaged_cells()
    print(output)
    assert output == 1

    # Ship receives 2 damages
    start = (4, 5)
    end = (2, 5)
    ship = Ship(start=start, end=end)
    cell1 = (3, 5)
    ship.receive_damage(cell1)
    cell2 = (4, 5)
    ship.receive_damage(cell2)
    output = ship.count_damaged_cells()
    assert output == 2

    # The ship does not
    start = (4, 5)
    end = (2, 5)
    ship = Ship(start=start, end=end)
    cell = (7, 5)
    ship.receive_damage(cell)
    output = ship.count_damaged_cells()
    print(output)
    assert output == 0


def test_has_sunk():

    # A ship was hit but has not sunk
    start = (4, 5)
    end = (2, 5)
    ship = Ship(start=start, end=end)
    cell = (3, 5)
    ship.receive_damage(cell)
    output = ship.has_sunk()
    print(output)
    assert output == False

    # A ship has sunk
    start = (4, 5)
    end = (2, 5)
    ship = Ship(start=start, end=end)
    cell1 = (3, 5)
    ship.receive_damage(cell1)
    cell2 = (4, 5)
    ship.receive_damage(cell2)
    cell3 = (2, 5)
    ship.receive_damage(cell3)
    output = ship.has_sunk()
    assert output == True

    # A ship was not even hit
    start = (4, 5)
    end = (2, 5)
    ship = Ship(start=start, end=end)
    output = ship.has_sunk()
    assert output == False


def test_is_near_ship():
    # This is the ship
    start = (4, 5)
    end = (2, 5)
    other_ship = Ship(start=start, end=end)

    # Ship is near
    start = (2, 6)
    end = (4, 6)
    ship_near = Ship(start=start, end=end)
    output = ship_near.is_near_ship(other_ship)
    print(output)
    assert output == True

    # Ship is not near
    start = (6, 7)
    end = (8, 7)
    ship_far = Ship(start=start, end=end)
    output = ship_far.is_near_ship(other_ship)
    print(output)
    assert output == False


if __name__ == "__main__":
    test_horizontal()
    test_vertical()
    test_get_cells()
    test_length()
    test_is_occupying_cell()
    test_receive_damage()
    test_count_damaged_cells()
    test_has_sunk()
    test_is_near_ship()
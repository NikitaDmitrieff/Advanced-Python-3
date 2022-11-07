import random

from battleship.convert import CellConverter


class Ship:
    """ Represent a ship that is placed on the board.
    """

    def __init__(self, start, end, should_validate=True, board_width=float("inf"), board_height=float("inf")):
        """ Creates a ship given its start and end coordinates on the board. 
        
        The order of the cells do not matter.

        Args:
            start (tuple[int, int]): tuple of 2 positive integers representing
                the starting cell coordinates of the Ship on the board
            end (tuple[int, int]): tuple of 2 positive integers representing
                the ending cell coordinates of the Ship on the board
            should_validate (bool): should the constructor check whether the 
                given coordinates result in a horizontal or vertical ship? 
                Defaults to True.

        Raises:
            ValueError: if should_validate==True and 
                if the ship is neither horizontal nor vertical
        """
        # Start and end (x, y) cell coordinates of the ship
        self.x_start, self.y_start = start
        self.x_end, self.y_end = end

        # make x_start on left and x_end on right
        self.x_start, self.x_end = min(self.x_start, self.x_end), max(self.x_start, self.x_end)

        # make y_start on top and y_end on bottom
        self.y_start, self.y_end = min(self.y_start, self.y_end), max(self.y_start, self.y_end)

        if should_validate:
            if not self.is_horizontal() and not self.is_vertical():
                raise ValueError("The given coordinates are invalid. "
                                 "The ship needs to be either horizontal or vertical.")

        # Set of all (x,y) cell coordinates that the ship occupies
        self.cells = self.get_cells()

        # Set of (x,y) cell coordinates of the ship that have been damaged
        self.damaged_cells = set()

        # Set the board size it is evolving in
        self.board_width = board_width
        self.board_height = board_height

    def __len__(self):
        return self.length()

    def __repr__(self):
        return (f"Ship(start=({self.x_start},{self.y_start}), "
                f"end=({self.x_end},{self.y_end}))")

    def is_vertical(self):
        """ Check whether the ship is vertical.
        
        Returns:
            bool : True if the ship is vertical. False otherwise.
        """

        return self.x_start == self.x_end

    def is_horizontal(self):
        """ Check whether the ship is horizontal.
        
        Returns:
            bool : True if the ship is horizontal. False otherwise.
        """

        return self.y_start == self.y_end

    def get_cells(self):
        """ Get the set of all cell coordinates that the ship occupies.
        
        For example, if the start cell is (3, 3) and end cell is (5, 3),
        then the method should return {(3, 3), (4, 3), (5, 3)}.
        
        This method is used in __init__() to initialise self.cells
        
        Returns:
            set[tuple] : Set of (x ,y) coordinates of all cells a ship occupies
        """

        cells = []
        if self.is_vertical() and self.is_horizontal():
            return {(self.x_start, self.y_start)}
        elif self.is_horizontal():
            for x_coordinate in range(self.x_end - self.x_start + 1):
                cells.append(tuple([self.x_start + x_coordinate, self.y_start]))
        elif self.is_vertical():
            for y_coordinate in range(self.y_end - self.y_start + 1):
                cells.append(tuple([self.x_start, self.y_start + y_coordinate]))
        else:
            raise ValueError("Ship is neither horizontal nor vertical")

        return set(cells)

    def length(self):
        """ Get length of ship (the number of cells the ship occupies).
        
        Returns:
            int : The number of cells the ship occupies
        """
        # TODO: Complete this method
        return len(self.cells)

    def is_occupying_cell(self, cell):
        """ Check whether the ship is occupying a given cell

        Args:
            cell (tuple[int, int]): tuple of 2 positive integers representing
                the (x, y) cell coordinates to check

        Returns:
            bool : return True if the given cell is one of the cells occupied 
                by the ship. Otherwise, return False
        """
        # TODO: Complete this method
        return cell in self.cells

    def receive_damage(self, cell):
        """ Receive attack at given cell. 
        
        If ship occupies the cell, add the cell coordinates to the set of 
        damaged cells. Then return True. 
        
        Otherwise return False.

        Args:
            cell (tuple[int, int]): tuple of 2 positive integers representing
                the cell coordinates that is damaged

        Returns:
            bool : return True if the ship is occupying cell (ship is hit). 
                Return False otherwise.
        """
        ship_was_hit = False
        if self.is_occupying_cell(cell):
            ship_was_hit = True
            self.damaged_cells.add(cell)

        return ship_was_hit

    def count_damaged_cells(self):
        """ Count the number of cells that have been damaged.
        
        Returns:
            int : the number of cells that are damaged.
        """

        return len(self.damaged_cells)

    def has_sunk(self):
        """ Check whether the ship has sunk.
        
        Returns:
            bool : return True if the ship is damaged at all its positions. 
                Otherwise, return False
        """

        has_sunk_condition = False

        if self.damaged_cells == self.cells:
            has_sunk_condition = True

        return has_sunk_condition

    def is_near_ship(self, other_ship):
        """ Check whether a ship is near another ship instance.
        
        Hint: Use the method is_near_cell(...) to complete this method.

        Args:
            other_ship (Ship): another Ship instance against which to compare

        Returns:
            bool : returns True if and only if the coordinate of other_ship is 
                near to this ship. Returns False otherwise.
        """

        for cell_of_other_ship in other_ship.cells:
            if self.is_near_cell(cell_of_other_ship):
                return True

        return False

    def is_near_cell(self, cell):
        """ Check whether the ship is near an (x,y) cell coordinate.

        In the example below:
        - There is a ship of length 3 represented by the letter S.
        - The positions 1, 2, 3 and 4 are near the ship
        - The positions 5 and 6 are NOT near the ship

        --------------------------
        |   |   |   |   | 3 |   |
        -------------------------
        |   | S | S | S | 4 | 5 |
        -------------------------
        | 1 |   | 2 |   |   |   |
        -------------------------
        |   |   | 6 |   |   |   |
        -------------------------

        Args:
            cell (tuple[int, int]): tuple of 2 positive integers representing
                the (x, y) cell coordinates to compare

        Returns:
            bool : returns True if and only if the (x, y) coordinate is at most
                one cell from any part of the ship OR is at the corner of the 
                ship. Returns False otherwise.
        """

        for cell_of_ship in self.cells:
            neighbours = self.get_neighbours(cell_of_ship)
            if cell in neighbours:
                return True

        return False

    def get_neighbours(self, cell):
        """ Gets all 8 neighbours of a certain cell.

        Args:
            cell (tuple[int, int]): tuple of 2 positive integers representing
                the (x, y) cell coordinates that we wish to get the neighbours of

        Returns:
            neighbours (tuple[(x1, y1), ..., (xN, yN)]): tuple of the coordinates of
                all the neighbouring cells of cell
        """

        top, bottom, left, right, top_left, top_right, bottom_left, bottom_right = [None] * 8

        neighbours = ()

        if cell[0] <= self.board_width:
            right = (cell[0] + 1, cell[1])
            neighbours += (right,)
        if cell[0] >= 2:
            left = (cell[0] - 1, cell[1])
            neighbours += (left,)
        if cell[1] <= self.board_height:
            bottom = (cell[0], cell[1] + 1)
            neighbours += (bottom,)
        if cell[1] >= 2:
            top = (cell[0], cell[1] - 1)
            neighbours += (top,)
        if top is not None and right is not None:
            top_right = (cell[0] + 1, cell[1] - 1)
            neighbours += (top_right,)
        if top is not None and left is not None:
            top_left = (cell[0] - 1, cell[1] - 1)
            neighbours += (top_left,)
        if bottom is not None and right is not None:
            bottom_right = (cell[0] + 1, cell[1] + 1)
            neighbours += (bottom_right,)
        if bottom is not None and right is not None:
            bottom_left = (cell[0] - 1, cell[1] + 1)
            neighbours += (bottom_left,)

        return neighbours


class ShipFactory:
    """ Class to create new ships in specific configurations."""

    def __init__(self, board_size=(10, 10), ships_per_length=None):
        """ Initialises the ShipFactory class with necessary information.
        
        Args: 
            board_size (tuple[int,int]): the (width, height) of the board in 
                terms of number of cells. Defaults to (10, 10)
            ships_per_length (dict): A dict with the length of ship as keys and
                the count as values. Defaults to 1 ship each for lengths 1-5.
        """
        self.board_size = board_size

        if ships_per_length is None:
            # Default: lengths 1 to 5, one ship each
            self.ships_per_length = {1: 1, 2: 1, 3: 1, 4: 1, 5: 1}
        else:
            self.ships_per_length = ships_per_length

    @classmethod
    def create_ship_from_str(cls, start, end, board_size=(10, 10)):
        """ A class method for creating a ship from string based coordinates.
        
        Example usage: ship = ShipFactory.create_ship_from_str("A3", "C3")
        
        Args:
            start (str): starting coordinate of the ship (example: 'A3')
            end (str): ending coordinate of the ship (example: 'C3')
            board_size (tuple[int,int]): the (width, height) of the board in 
                terms of number of cells. Defaults to (10, 10)

        Returns:
            Ship : a Ship instance created from start to end string coordinates
        """
        converter = CellConverter(board_size)
        return Ship(start=converter.from_str(start),
                    end=converter.from_str(end))

    def generate_ships(self):
        """ Generate a list of ships in the appropriate configuration.
        
        The number and length of ships generated must obey the specifications 
        given in self.ships_per_length.
        
        The ships must also not overlap with each other, and must also not be 
        too close to one another (as defined earlier in Ship::is_near_ship())
        
        The coordinates should also be valid given self.board_size
        
        Returns:
            list[Ships] : A list of Ship instances, adhering to the rules above
        """

        ships = []
        ship_to_test = None

        for ship_length, number_of_ships in self.ships_per_length.items():

            for ship_nb in range(number_of_ships):

                # Prevents an infinite loop from happening when an impossible configuration of
                # ships is generated which would not give a single valid space for the last
                # ship to be generated
                number_of_iterations = 0
                max_iterations = 10 ** 3

                # Generate a new ship with length ship_length and valid coordinates
                while not(self.check_coordinates(ships, ship_to_test)):

                    start, end = self.generate_random_coordinates(ship_length)
                    ship_to_test = Ship(start, end, board_width=self.board_size[0], board_height=self.board_size[1])
                    number_of_iterations += 1

                    # Function is stuck in infinite loop, resets the ships by calling
                    # the generate_ships() method again
                    if number_of_iterations > max_iterations:
                        ships = self.generate_ships()
                        return ships

                ships.append(ship_to_test)

        return ships

    def check_coordinates(self, ships, ship_to_test):
        """ Checks if the given coordinates check all the requirements

        Args:
            ships (list[Ship1, ... , ShipN]): list of Ships
            ship_to_test (Ship): ship we want to test the coordinates for

        Returns:
            bool: True if the coordinates of ship_to_test are valid, False otherwise
        """

        if ship_to_test is None:
            return False

        if not self.is_ship_in_bound(ship_to_test):
            return False

        # Check that the ship is not overlapping with any other ship
        # Check that the ship is not near any other ship
        if len(ships) > 0:

            for ship in ships:

                if self.are_overlapping(ship, ship_to_test):
                    return False

                if ship.is_near_ship(ship_to_test):
                    return False
        else:
            pass

        return True

    def is_ship_in_bound(self, ship):
        """ Checks that the ship is in bound

        Args:
            ship (Ship): ship we want to test the coordinates for

        Returns:
            bool: True if the coordinates of ship_to_test are within the board, False otherwise
        """

        condition = True

        if not (1 <= ship.x_start <= self.board_size[0] and
                1 <= ship.x_end <= self.board_size[0] and
                1 <= ship.y_start <= self.board_size[1] and
                1 <= ship.y_end <= self.board_size[1]):
            condition = False

        return condition

    def are_overlapping(self, ship, other_ship):
        """ Checks if two ships are overlapping

        Args:
            ship (Ship): first ship we want to test the coordinates for
            other_ship (Ship): second ship we want to test the coordinates

        Returns:
            bool: True if the two ships occupy the same cell(s), False otherwise
        """

        for cell_of_ship in ship.cells:
            if cell_of_ship in other_ship.cells:
                return True

        return False

    def generate_random_coordinates(self, dimension):
        """ Generates random coordinates

        Args:
            dimension (int): length of the ship we want random coordinates for

        Returns:
            start (tuple[int, int]): tuple of 2 positive integers representing
                the starting cell coordinates of the Ship on the board
            end (tuple[int, int]): tuple of 2 positive integers representing
                the ending cell coordinates of the Ship on the board
        """

        # Choose between vertical (1) and horizontal (0)
        condition_vertical = random.randint(0, 1)

        if condition_vertical:  # X is fixed, Y is changing

            x_start = random.randint(1, self.board_size[0])
            x_end = x_start

            y_start = random.randint(1, self.board_size[1] - dimension + 1)
            y_end = y_start + dimension - 1

            start = (x_start, y_start)
            end = (x_end, y_end)

        else:  # Y is fixed, X is changing

            x_start = random.randint(1, self.board_size[0] - dimension + 1)
            x_end = x_start + dimension - 1

            y_start = random.randint(1, self.board_size[1])
            y_end = y_start

            start = (x_start, y_start)
            end = (x_end, y_end)

        return start, end


if __name__ == '__main__':
    # SANDBOX for you to play and test your methods

    ship = Ship(start=(3, 3), end=(5, 3))
    print(ship.get_cells())
    print(ship.length())
    print("Horizontal test:", ship.is_horizontal())
    print("Vertical test:", ship.is_vertical())
    print(ship.is_near_cell((5, 3)))

    print(ship.receive_damage((4, 3)))
    print(ship.receive_damage((10, 3)))
    print(ship.damaged_cells)

    ship2 = Ship(start=(4, 1), end=(4, 5))
    print(ship.is_near_ship(ship2))

    # For Task 3
    ships = ShipFactory().generate_ships()
    print("These are my ships", ships)

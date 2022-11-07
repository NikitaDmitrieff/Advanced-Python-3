import random

from battleship.board import Board
from battleship.convert import CellConverter
from battleship.ship import Ship


class Player:
    """ Class representing the player
    """
    count = 0  # for keeping track of number of players

    def __init__(self, board=None, name=None):
        """ Initialises a new player with its board.

        Args:
            board (Board): The player's board. If not provided, then a board
                will be generated automatically
            name (str): Player's name
        """

        if board is None:
            self.board = Board()
        else:
            self.board = board

        Player.count += 1
        if name is None:
            self.name = f"Player {self.count}"
        else:
            self.name = name

    def __str__(self):
        return self.name

    def select_target(self):
        """ Select target coordinates to attack.
        
        Abstract method that should be implemented by any subclasses of Player.
        
        Returns:
            tuple[int, int] : (x, y) cell coordinates at which to launch the 
                next attack
        """
        raise NotImplementedError

    def receive_result(self, is_ship_hit, has_ship_sunk):
        """ Receive results of latest attack.
        
        Player receives notification on the outcome of the latest attack by the 
        player, on whether the opponent's ship is hit, and whether it has been 
        sunk. 
        
        This method does not do anything by default, but can be overridden by a 
        subclass to do something useful, for example to record a successful or 
        failed attack.
        
        Returns:
            None
        """
        return None

    def has_lost(self):
        """ Check whether player has lost the game.
        
        Returns:
            bool: True if and only if all the ships of the player have sunk.
        """
        return self.board.have_all_ships_sunk()


class ManualPlayer(Player):
    """ A player playing manually via the terminal
    """

    def __init__(self, board, name=None):
        """ Initialise the player with a board and other attributes.
        
        Args:
            board (Board): The player's board. If not provided, then a board
                will be generated automatically
            name (str): Player's name
        """
        super().__init__(board=board, name=name)
        self.converter = CellConverter((board.width, board.height))

    def select_target(self):
        """ Read coordinates from user prompt.
               
        Returns:
            tuple[int, int] : (x, y) cell coordinates at which to launch the 
                next attack
        """
        print(f"It is now {self}'s turn.")

        while True:
            try:
                coord_str = input('coordinates target = ')
                x, y = self.converter.from_str(coord_str)
                return x, y
            except ValueError as error:
                print(error)


class RandomPlayer(Player):
    """ A Player that plays at random positions.

    However, it does not play at the positions:
    - that it has previously attacked
    """

    def __init__(self, name=None):
        """ Initialise the player with an automatic board and other attributes.
        
        Args:
            name (str): Player's name
        """
        # Initialise with a board with ships automatically arranged.
        super().__init__(board=Board(), name=name)
        self.tracker = set()

    def select_target(self):
        """ Generate a random cell that has previously not been attacked.
        
        Also adds cell to the player's tracker.
        
        Returns:
            tuple[int, int] : (x, y) cell coordinates at which to launch the 
                next attack
        """
        target_cell = self.generate_random_target()
        self.tracker.add(target_cell)
        return target_cell

    def generate_random_target(self):
        """ Generate a random cell that has previously not been attacked.
               
        Returns:
            tuple[int, int] : (x, y) cell coordinates at which to launch the 
                next attack
        """
        has_been_attacked = True
        random_cell = None

        while has_been_attacked:
            random_cell = self.get_random_coordinates()
            has_been_attacked = random_cell in self.tracker

        return random_cell

    def get_random_coordinates(self):
        """ Generate random coordinates.
               
        Returns:
            tuple[int, int] : (x, y) cell coordinates at which to launch the 
                next attack
        """
        x = random.randint(1, self.board.width)
        y = random.randint(1, self.board.height)
        return (x, y)


class AutomaticPlayer(Player):
    """ Player playing automatically using a strategy."""

    def __init__(self, name=None):
        """ Initialise the player with an automatic board and other attributes.
        
        Args:
            name (str): Player's name
        """
        # Initialise with a board with ships automatically arranged.
        super().__init__(board=Board(), name=name)
        self.tracker = set()
        self.sunken_ships = []
        self.successful_hits = []
        self.last_target = None

    def select_target(self):
        """ Select target coordinates to attack.
        
        Returns:
            tuple[int, int] : (x, y) cell coordinates at which to launch the 
                next attack
        """

        target_cell = self.generate_random_target()
        self.tracker.add(target_cell)
        return target_cell

    def generate_random_target(self):
        """ Generate a random cell that has previously not been attacked.

        Returns:
            tuple[int, int] : (x, y) cell coordinates at which to launch the
                next attack
        """

        # Initialize the conditions to enter the while loop at least once
        random_cell = None
        has_been_attacked = True

        sunken_ships = self.are_there_sunken_ships()
        is_close_to_ship = True

        is_there_a_hunt, list_of_hits = self.is_there_a_hunt()
        is_a_hunting_cell = False

        within_bounds = False

        # Stays in the loop until the cell chosen:
        #   - Is not close to a sunken ship
        #   - Is within bounds
        #   - Has not been attacked already
        #   - Is a 'hunting cell' in the case of a 'hunt' (hit ship that has not been downed yet)
        while has_been_attacked or is_close_to_ship or not is_a_hunting_cell or not within_bounds:

            random_cell = self.get_random_coordinates()

            # If there has been a successful attack that has not yet resulted in the sinking of
            # an opponent's ship, then the priority is to sink that ship. This is called a "hunt"
            if is_there_a_hunt:

                # In this case, a possible cell is already given by the function.
                # It replaces the random_cell generated previously
                is_a_hunting_cell, random_cell = self.hunting_cell(random_cell, list_of_hits)

            else:
                is_a_hunting_cell = True

            # The attack should be on a cell that has not yet been attacked and is within bounds
            has_been_attacked = random_cell in self.tracker
            within_bounds = self.is_it_within_bounds(random_cell)

            # If there are sunken ships, the attack should not be launched on a nearby cell
            if sunken_ships:
                is_close_to_ship = self.is_close_to_ship(random_cell)
            else:
                is_close_to_ship = False

        self.last_target = random_cell

        return random_cell

    def are_there_sunken_ships(self):
        """ Checks if there are sunken ships already

        Returns:
            bool: True if there are sunken ships, False otherwise
        """
        return len(self.sunken_ships) > 0

    def hunting_cell(self, cell, list_of_hits):  # TO modify
        """ Given that there were successful hits that were not part of any
                sunken ships, this function checks that the target selected (cell)
                is, at least, a neighbour of that successful hit. If there are multiple
                successful hits already, it gets an even better target thanks to the
                get_better_target() method.

        Args:
            cell (tuple[int, int]) : (x, y) cell coordinates which we are planning on
                launching the next attack
            list_of_hits (list[(int, int), ... , (int, int)] : list of the cells that
                were successful hits yet not part of any sunken ship

        Returns:
            bool: True if the cell is a neighbour of a hit cell, otherwise False
            tuple[int, int]: cell coordinates of the new target if there were more hints
            (see doc string of the next function), otherwise returns the cell coordinates
            it was given (cell)
        """

        if len(list_of_hits) > 1:
            new_target = self.get_better_target(list_of_hits)
            print(new_target)
            return True, new_target
        else:
            neighbours = self.get_neighbours(list_of_hits[0], cell_hunt=True)
            if cell in neighbours:
                return True, cell
            else:
                return False, cell

    def get_better_target(self, list_of_hits):
        """ Given that there are multiple successful hits that were not part
                of any sunken ship, it means the orientation of the soon-to-be
                sunken ship can be deduced and hence a better target can be obtained

        Args:
            list_of_hits (list[(int, int), ... , (int, int)] : list of the cells that
                were successful hits yet not part of any sunken ship

        Returns:
            tuple[(int, int)]: new target to attack
        """

        cell = list_of_hits[0]

        # Find the start and end of the 'hit' parts of the ship
        start, end = self.find_start_and_end(cell)

        if start[0] == end[0]: # Ship is vertical
            possible_cells = ((start[0], start[1] - 1), (end[0], end[1] + 1))
        else: # Ship is horizontal
            possible_cells = ((start[0] - 1, start[1]), (end[0] + 1, end[1]))

        # Choose between one cell before the start cell or one cell after the end cell
        new_target = random.choice(possible_cells)

        return new_target

    def is_there_a_hunt(self):
        """ Checks if there are hit cells that are not part of any sunken ship
            This would mean there is a "hunt": a ship has been uncovered

        Returns:
            bool: True if there is a hunt, False otherwise
            list[(int, int), ... , (int, int)]: list of coordinates of the cells that
                were successful hits yet not part of any sunken ship
        """

        list_of_hits = self.successful_hits.copy()

        # Remove from the list_of_hits all the hits that belong to sunken ships
        if len(self.sunken_ships) > 0:
            for ship in self.sunken_ships:
                for cell in ship.cells:
                    index = list_of_hits.index(cell)
                    list_of_hits.pop(index)

        return len(list_of_hits) > 0, list_of_hits

    def is_close_to_ship(self, cell):
        """ Checks if the given cell is near a sunken ship

        Args:
            cell (tuple[(int, int)]): coordinates of a cell to check if it is
                near a sunken ship

        Returns:
            bool: True if the given cell is near a ship, False otherwise
        """

        for ship in self.sunken_ships:
            if ship.is_near_cell(cell):
                return True
            else:
                pass

        return False

    def get_random_coordinates(self):
        """ Generate random coordinates.

        Returns:
            tuple[int, int] : (x, y) cell coordinates at which to launch the
                next attack
        """
        x = random.randint(1, self.board.width)
        y = random.randint(1, self.board.height)
        return (x, y)

    def receive_result(self, is_ship_hit, has_ship_sunk):
        """ Receive the results of each turn:
                - Has a ship been hit ?
                - Has a ship sunken ?
            Updates two attributes:
                - self.successful_hits
                - self.sunken_ships
        """
        if is_ship_hit:
            self.successful_hits.append(self.last_target)

        if is_ship_hit and has_ship_sunk:
            start, end = self.find_start_and_end(self.last_target)
            ship = Ship(start, end, should_validate=True)
            self.sunken_ships.append(ship)

    def find_start_and_end(self, cell):
        """ Given a cell, finds the start and end coordinates of the
                whole ship, or at least the part already uncovered
                thanks to successful hits

        Args:
            cell (tuple[(int, int)]): coordinates of a cell to find the start
                and end coordinates of the ship for

        Returns:
            start (tuple[int, int]): tuple of 2 positive integers representing
                the starting cell coordinates of the Ship on the board
            end (tuple[int, int]): tuple of 2 positive integers representing
                the ending cell coordinates of the Ship on the board
        """

        start, end = None, None

        cells = self.get_all_cells(cell, except_cell=cell)
        cells += (cell,)

        if len(cells) == 1:
            return cell, cell

        max_x = 0
        min_x = self.board.width + 1
        max_y = 0
        min_y = self.board.height + 1

        if self.is_this_ship_vertical(cells):
            for cell in cells:
                if min_y > cell[1]:
                    min_y = cell[1]
                    start = cell
                if max_y < cell[1]:
                    max_y = cell[1]
                    end = cell
        else:
            for cell in cells:
                if min_x > cell[0]:
                    min_x = cell[0]
                    start = cell
                if max_x < cell[0]:
                    max_x = cell[0]
                    end = cell

        return start, end

    def is_this_ship_vertical(self, cells):
        """ Checks if this ship is vertical

        Args:
            cells (tuple[(int, int), ... , (int, int)]): tuple of tuples of the coordinates
                of a ship we want to check the orientation for

        Returns:
            bool: True if the ship is vertical, False otherwise
        """
        return cells[0][0] == cells[1][0]

    def get_all_cells(self, cell, except_cell=None):
        """ Recursive function which gathers the nearby hit cells for a given cell

        Args:
            cell (tuple[(int, int)]): coordinates of a cell to find the nearby successful
                hit cells for
            except_cell (tuple[(int, int)]): coordinates of a cell to omit in the search
                for nearby successful hit cells

        Returns:
            tuple[(int, int), ... , (int, int)]: tuple of the nearby successful hit cells
        """

        all_hit_cells_nearby = ()
        neighbours = self.get_neighbours(cell)

        for neighbour in neighbours:
            if neighbour in self.successful_hits and neighbour != except_cell:
                all_hit_cells_nearby += (neighbour,)

                new_neighbours = self.get_all_cells(neighbour, except_cell=cell)
                if new_neighbours is not None:
                    for new_neighbour in new_neighbours:
                        all_hit_cells_nearby += (new_neighbour,)

        return all_hit_cells_nearby

    def get_neighbours(self, cell, cell_hunt=False):
        """
        Args:
            cell (tuple[(int, int)]): coordinates of a cell to gather all
                the neighbours for
            cell_hunt (bool): True if we are searching neighbours in the
                context of hunt, False otherwise

        Returns:
            tuple[(int, int), ... , (int, int)]: tuple of the neighbouring cells
        """

        top, bottom, left, right, top_left, top_right, bottom_left, bottom_right = [None] * 8

        neighbours = ()

        if cell[0] <= self.board.width - 1:
            right = (cell[0] + 1, cell[1])
            neighbours += (right,)
        if cell[0] >= 2:
            left = (cell[0] - 1, cell[1])
            neighbours += (left,)
        if cell[1] <= self.board.height - 1:
            bottom = (cell[0], cell[1] + 1)
            neighbours += (bottom,)
        if cell[1] >= 2:
            top = (cell[0], cell[1] - 1)
            neighbours += (top,)

        if not cell_hunt:
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

    def is_it_within_bounds(self, cell):
        """ Checks if a cell is within bound

        Args:
            cell (tuple[(int, int)]): coordinates of a cell to check if it
                is in bound for

        Returns:
            bool: True if the cell is in bound, False otherwise
        """
        return (1 <= cell[0] <= self.board.width and
                1 <= cell[1] <= self.board.height)

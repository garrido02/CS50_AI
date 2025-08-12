import sys

from crossword import *


class CrosswordCreator():

    def __init__(self, crossword):
        """
        Create new CSP crossword generate.
        """
        self.crossword = crossword
        self.domains = {
            var: self.crossword.words.copy()
            for var in self.crossword.variables
        }

    def letter_grid(self, assignment):
        """
        Return 2D array representing a given assignment.
        """
        letters = [
            [None for _ in range(self.crossword.width)]
            for _ in range(self.crossword.height)
        ]
        for variable, word in assignment.items():
            direction = variable.direction
            for k in range(len(word)):
                i = variable.i + (k if direction == Variable.DOWN else 0)
                j = variable.j + (k if direction == Variable.ACROSS else 0)
                letters[i][j] = word[k]
        return letters

    def print(self, assignment):
        """
        Print crossword assignment to the terminal.
        """
        letters = self.letter_grid(assignment)
        for i in range(self.crossword.height):
            for j in range(self.crossword.width):
                if self.crossword.structure[i][j]:
                    print(letters[i][j] or " ", end="")
                else:
                    print("█", end="")
            print()

    def save(self, assignment, filename):
        """
        Save crossword assignment to an image file.
        """
        from PIL import Image, ImageDraw, ImageFont
        cell_size = 100
        cell_border = 2
        interior_size = cell_size - 2 * cell_border
        letters = self.letter_grid(assignment)

        # Create a blank canvas
        img = Image.new(
            "RGBA",
            (self.crossword.width * cell_size,
             self.crossword.height * cell_size),
            "black"
        )
        font = ImageFont.truetype("assets/fonts/OpenSans-Regular.ttf", 80)
        draw = ImageDraw.Draw(img)

        for i in range(self.crossword.height):
            for j in range(self.crossword.width):

                rect = [
                    (j * cell_size + cell_border,
                     i * cell_size + cell_border),
                    ((j + 1) * cell_size - cell_border,
                     (i + 1) * cell_size - cell_border)
                ]
                if self.crossword.structure[i][j]:
                    draw.rectangle(rect, fill="white")
                    if letters[i][j]:
                        _, _, w, h = draw.textbbox((0, 0), letters[i][j], font=font)
                        draw.text(
                            (rect[0][0] + ((interior_size - w) / 2),
                             rect[0][1] + ((interior_size - h) / 2) - 10),
                            letters[i][j], fill="black", font=font
                        )

        img.save(filename)

    def solve(self):
        """
        Enforce node and arc consistency, and then solve the CSP.
        """
        self.enforce_node_consistency()
        self.ac3()
        return self.backtrack(dict())

    def enforce_node_consistency(self):
        """
        Update `self.domains` such that each variable is node-consistent.
        (Remove any values that are inconsistent with a variable's unary
         constraints; in this case, the length of the word.)
        """

        # Iterate each variable in domains (each blank space)
        for var in self.domains:
            # Iterate the values in that var's set. We make a copy to avoid problems while looping
            for word in self.domains[var].copy():
                # If the length of the word is not the same as the variable, then remove
                if len(word) != var.length:
                    self.domains[var].remove(word)


    def revise(self, x, y):
        """
        Make variable `x` arc consistent with variable `y`.
        This means we want to check where x and y overlap if there is any word in x that can be overlapped by a word
        in y, at the indexes x and y overlap.
        To do so, remove values from `self.domains[x]` for which there is no
        possible corresponding value for `y` in `self.domains[y]`.

        Return True if a revision was made to the domain of `x`; return
        False if no revision was made.
        """

        # Check overlaps
        overlaps = self.crossword.overlaps[x, y]

        # Start a flag for the return value
        revised = False

        # If there are no overlaps then no are changes needed
        if overlaps is None:
            return False
        else:
            # Loop for every word in x
            for wordX in self.domains[x].copy():
                found = False
                # Loop every word in y
                for wordY in self.domains[y]:
                    # If we find the words that overlap at the exact indexes, break early thus pruning the rest
                    if wordX[overlaps[0]] == wordY[overlaps[1]]:
                        found = True
                        break
                # If the word in X cannot be matched to any word in Y at the indexes found, remove it
                if not found:
                    self.domains[x].remove(wordX)
                    revised = True
            return revised


    def ac3(self, arcs=None):
        """
        Update `self.domains` such that each variable is arc consistent.
        If `arcs` is None, begin with initial list of all arcs in the problem.
        Otherwise, use `arcs` as the initial list of arcs to make consistent.

        Return True if arc consistency is enforced and no domains are empty;
        return False if one or more domains end up empty.
        """

        # Check if arcs is None, if so we need to gather all arcs - Initial state
        queue = []
        if arcs is None:
            # Iterate each variable
            for var in self.domains:
                # Get its neighbors which is a set of all the variables it is connected
                for neighbor in self.crossword.neighbors(var):
                    queue.append((var, neighbor))
        else:
            queue = arcs

        # Loop while the queue is not empty
        while queue:
            # Remove the first element from the queue
            (x, y) = queue.pop(0)

            # If there were revisions to x, then we need to re-add all arcs connected to x, i.e, (z,x) with z != y
            if self.revise(x, y):
                # If x has no words then return false, it's not possible to solve
                if not self.domains[x]:
                    return False

                # Add the arcs (z,x). z is a direct neighbor of x
                for z in self.crossword.neighbors(x):
                    if z != y:
                        queue.append((z, x))
        return True


    def assignment_complete(self, assignment):
        """
        Return True if `assignment` is complete (i.e., assigns a value to each
        crossword variable); return False otherwise.
        """

        # We want to check if all the variables in self.domains are present in the assigment
        for var in self.domains:
            # If at least one is not then it's not yet completed
            if var not in assignment:
                return False
        return True


    def consistent(self, assignment):
        """
        Return True if `assignment` is consistent (i.e., words fit in crossword
        puzzle without conflicting characters); return False otherwise.
        """
        # Check if every value of each variable is different
        words = set()
        for var in assignment:
            # If the word assigned is not in the set then is unique
            if assignment[var] not in words:
                # Check if the length of the word is the correct length
                if len(assignment[var]) != var.length:
                    return False
                # Checking conflicts starts with getting the neighbors
                for neighbor in self.crossword.neighbors(var):
                    # Only bother if the neighbor is on the assignment
                    if neighbor in assignment:
                        # Get the overlap indexed
                        (i,j) = self.crossword.overlaps[var, neighbor]
                        if (i,j) is not None:
                            # If the letters on the indexes of the words are not the same then conflict exists
                            if assignment[var][i] != assignment[neighbor][j]:
                                return False
                words.add(assignment[var])
            # If the word is repeated then consistency fails
            else:
                return False
        return True


    def order_domain_values(self, var, assignment):
        """
        Return a list of values in the domain of `var`, in order by
        the number of values they rule out for neighboring variables.
        The first value in the list, for example, should be the one
        that rules out the fewest values among the neighbors of `var`.
        """

        # Start an empty list to return
        rulesOut = []

        # Get every neighbor
        neighbors = self.crossword.neighbors(var)

        # Loop every word in var
        for wordVar in self.domains[var]:
            count = 0
            # Loop each neighbor
            for neighbor in neighbors:
                # Only bother if it's not yet assigned
                if neighbor not in assignment:
                    # Get overlap indexes
                    (i,j) = self.crossword.overlaps[var, neighbor]
                    # If there is overlap, check for conflicts
                    if (i,j) is not None:
                        # Loop neighbor words
                        for wordNeighbor in self.domains[neighbor]:
                            # If the indexes at the words are not the same letter then we have conflict -> Rules out
                            if wordVar[i] != wordNeighbor[j]:
                                count += 1
            # Save how many neighbors values would have to be ruled out if we chose a certain word for var
            rulesOut.append((wordVar, count))

        # Sort the list by asc count value
        rulesOut.sort(key=lambda x: x[1])

        # Return only the list of words
        return [word for (word, count) in rulesOut]


    def select_unassigned_variable(self, assignment):
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest
        degree. If there is a tie, any of the tied variables are acceptable
        return values.
        """

        # List of (variable, nrValues) - variable is a variable and nrValues is the number of words still available to choose
        variables = []

        # Loop every variable available
        for var in self.domains:
            # Filter those not yet assigned
            if var not in assignment:
                variables.append((var, len(self.domains[var])))

        # Sort for the nrValues - In case of a tie, choose whoever has most neighbors first
        variables.sort(key=lambda x: (x[1], -len(self.crossword.neighbors(x[0]))))

        # Return the first variable
        return variables[0][0]


    def backtrack(self, assignment):
        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.

        `assignment` is a mapping from variables (keys) to words (values).

        If no assignment is possible, return None.
        """

        # If the assignment is complete, return it
        if self.assignment_complete(assignment):
            return assignment

        # Select an unassigned variable
        var = self.select_unassigned_variable(assignment)

        # Order values by the least ruled out - i.e, value that offers most choices
        values = self.order_domain_values(var, assignment)

        # Try to complete the assignment for each value
        for value in values:
            assigmentCopy = assignment.copy()
            assigmentCopy[var] = value
            # Now we need to get the neighbors of var and use it as arcs for ac3. (neighbor, var)
            arcs = []
            for neighbor in self.crossword.neighbors(var):
                arcs.append((neighbor, var))
            # Check if it's arc consistent and the assigment is consistent with the rules
            if self.ac3(arcs) and self.consistent(assigmentCopy):
                # If so recursive call with the new assigment and if we find a solution then return it
                result = self.backtrack(assigmentCopy)
                if result is not None:
                    return result

        # No solution was found
        return None


def main():

    # Check usage
    if len(sys.argv) not in [3, 4]:
        sys.exit("Usage: python generate.py structure words [output]")

    # Parse command-line arguments
    structure = sys.argv[1]
    words = sys.argv[2]
    output = sys.argv[3] if len(sys.argv) == 4 else None

    # Generate crossword
    crossword = Crossword(structure, words)
    creator = CrosswordCreator(crossword)
    assignment = creator.solve()

    # Print result
    if assignment is None:
        print("No solution.")
    else:
        creator.print(assignment)
        if output:
            creator.save(assignment, output)


if __name__ == "__main__":
    main()

### Project 1 - Knowledge:

<br></br>

### 1a - Knights

Through the use of logical rules I wrote an AI capable of deducing the conclusion of certain problems and puzzles.
If we consider logical propositions such as P, Q, R and S we can assume the following rules to be true:

1. A logical proposition can either be true or false
2. Conjuction: P & Q. It means we have both P and Q evaluated as true
3. Disjunction: P or Q. It means we have at least one of them evaluated as true
4. Double Negative: ~~Q. It is the same as having a double false, i.e, true
5. The implication rule: P => Q.  It means that Q is always true, depite the value of P. A simplification of the implication rule can be (~P or Q)

Using the rules described above the AI was capable of deducing various solutions to logical problems.


<br></br>

### 1a - MineSweeper

Minesweeper is a puzzle game that consists of a grid of cells, where some of the cells contain hidden “mines.” Clicking on a cell that contains a mine detonates the mine, and causes the user to lose the game. Clicking on a “safe” cell (i.e., a cell that does not contain a mine) reveals a number that indicates how many neighboring cells – where a neighbor is a cell that is one square to the left, right, up, down, or diagonal from the given cell – contain a mine.

<img width="598" height="420" alt="imagem" src="https://github.com/user-attachments/assets/dc43596a-bd94-43cc-80ed-580c10a392a7" />

In this 3x3 Minesweeper game, for example, the three 1 values indicate that each of those cells has one neighboring cell that is a mine. The four 0 values indicate that each of those cells has no neighboring mine.

<img width="510" height="510" alt="imagem" src="https://github.com/user-attachments/assets/57047e11-c5d1-4014-a671-16d6b3bbe358" />

Given this information, a logical player could conclude that there must be a mine in the lower-right cell and that there is no mine in the upper-left cell, for only in that case would the numerical labels on each of the other cells be accurate.

The goal of the game is to flag (i.e., identify) each of the mines. In many implementations of the game, including the one in this project, the player can flag a mine by right-clicking on a cell (or two-finger clicking, depending on the computer).

My goal in this project will be to build an AI that can play Minesweeper. Knowing that knowledge-based agents make decisions by considering their knowledge base, and making inferences based on that knowledge.

One way we could represent an AI’s knowledge about a Minesweeper game is by making each cell a propositional variable that is true if the cell contains a mine, and false otherwise.

What information does the AI have access to? Well, the AI would know every time a safe cell is clicked on and would get to see the number for that cell. Consider the following Minesweeper board, where the middle cell has been revealed, and the other cells have been labeled with an identifying letter for the sake of discussion.

<img width="507" height="509" alt="imagem" src="https://github.com/user-attachments/assets/de49a0bb-8db3-4458-a462-8181ac16fb3b" />

What information do we have now? It appears we now know that one of the eight neighboring cells is a mine. Therefore, we could write a logical expression like the below to indicate that one of the neighboring cells is a mine.

{A, B, C, D, E, F, G, H} = 1

Every logical sentence in this representation has two parts: a set of cells on the board that are involved in the sentence, and a number count, representing the count of how many of those cells are mines. The above logical sentence says that out of cells A, B, C, D, E, F, G, and H, exactly 1 of them is a mine.

Why is this a useful representation? In part, it lends itself well to certain types of inference. Consider the game below.

<img width="507" height="503" alt="imagem" src="https://github.com/user-attachments/assets/a24496d6-eb3f-46ae-9cd9-278449883a38" />

Using the knowledge from the lower-left number, we could construct the sentence {D, E, G} = 0 to mean that out of cells D, E, and G, exactly 0 of them are mines. Intuitively, we can infer from that sentence that all of the cells must be safe. By extension, any time we have a sentence whose count is 0, we know that all of that sentence’s cells must be safe.

Similarly, consider the game below.

<img width="492" height="500" alt="imagem" src="https://github.com/user-attachments/assets/f7d1f94e-934c-4382-a6cf-7d2445d496d7" />

Our AI would construct the sentence {E, F, H} = 3. Intuitively, we can infer that all of E, F, and H are mines. More generally, any time the number of cells is equal to the count, we know that all of that sentence’s cells must be mines.

In general, we’ll only want our sentences to be about cells that are not yet known to be either safe or mines. This means that, once we know whether a cell is a mine or not, we can update our sentences to simplify them and potentially draw new conclusions.

For example, if our AI knew the sentence {A, B, C} = 2, we don’t yet have enough information to conclude anything. But if we were told that C were safe, we could remove C from the sentence altogether, leaving us with the sentence {A, B} = 2 (which, incidentally, does let us draw some new conclusions.)

Likewise, if our AI knew the sentence {A, B, C} = 2, and we were told that C is a mine, we could remove C from the sentence and decrease the value of count (since C was a mine that contributed to that count), giving us the sentence {A, B} = 1. This is logical: if two out of A, B, and C are mines, and we know that C is a mine, then it must be the case that out of A and B, exactly one of them is a mine.

If we’re being even more clever, there’s one final type of inference we can do.

<img width="503" height="498" alt="imagem" src="https://github.com/user-attachments/assets/0597ce91-789b-4ad0-8b58-7cef100f25d0" />

Consider just the two sentences our AI would know based on the top middle cell and the bottom middle cell. From the top middle cell, we have {A, B, C} = 1. From the bottom middle cell, we have {A, B, C, D, E} = 2. Logically, we could then infer a new piece of knowledge, that {D, E} = 1. After all, if two of A, B, C, D, and E are mines, and only one of A, B, and C are mines, then it stands to reason that exactly one of D and E must be the other mine.

More generally, any time we have two sentences set1 = count1 and set2 = count2 where set1 is a subset of set2, then we can construct the new sentence set2 - set1 = count2 - count1. Consider the example above to ensure you understand why that’s true. 

This technique is called resolution and a more theoretical explanation is that when we have two clauses, for instance {A, B, C} and {~C} (not C) we can infer {A, B}. In our game, when we have a bigger clause and a subclause of that such as {A, B, C, D, E} and {A, B, C} what we are saying is that we can assume we have {~A, ~B, ~C} so that the resolution of both clauses will give us {D, E}.

Using this method of representing knowledge, we can write an AI agent that can gather knowledge about the Minesweeper board, and hopefully select cells it knows to be safe!



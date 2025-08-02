### Project 0 - Search:

<br></br>

### 0a - Degrees
  According to the Six Degrees of Kevin Bacon game, anyone in the Hollywood film industry can be connected to Kevin Bacon within six steps, where each step consists of finding a film that two actors both starred in.
  
  In this problem, we’re interested in finding the shortest path between any two actors by choosing a sequence of movies that connects them. For example, the shortest path between Jennifer Lawrence and Tom Hanks is 2: Jennifer Lawrence is connected to Kevin Bacon by both starring in “X-Men: First Class,” and Kevin Bacon is connected to Tom Hanks by both starring in “Apollo 13.”
  
  We can frame this as a search problem: our states are people. Our actions are movies, which take us from one actor to another (it’s true that a movie could take us to multiple different actors, but that’s okay for this problem). Our initial state and goal state are defined by the two people we’re trying to connect. By using breadth-first search, we can find the shortest path from one actor to another. 


<img width="548" height="660" alt="degrees" src="https://github.com/user-attachments/assets/84067d23-eeb0-4ec6-9b6c-66580496e218" />

<br></br>
<br></br>

### 0b - Tic Tac Toe
  The classic game where the player face an opposing AI. The AI was coded using the minimax algorithm and with alpha-beta pruning to account for efficiency.

  <br></br>
  
  #### The minimax approach can be framed in the following scenario:
  Let's propose that we have two players. One named maximizing and the other named minimizing. Both players have a competition going on between them where the goal of the competition is, of course, to have a winner. But there is a catch: The score is shared between them.
    
  The objective of the maximizing player is to increase the shared score as high as he can and, as you guessed it, the objective of the minimizing player is to decrease the score as much as he can.
    
  To better understand the logic behind minimax let's consider a concrete competition where this approach can be used and easily understood.
  
  <br></br>

  #### The dessert competition:
  Each player takes turns, without any preference with regards to whoever starts first. 
      
  The first player to play will have at his disposal 3 tables. Each table with 3 desserts placed on them, ie, 9 choices of desserts. This player will then have to choose 1 dessert from each table and bring them to the second player, ie, 3 choices to the second player.
      
  Considering the minimizing player starts first, we know that the goal of this player is to decreased the shared score as much as he can. Let's consider that each dessert is evaluated on a scale of 0 to 10. We then know for certain that this player will choose from each table the dessert that is closer to 0 on the scale.

  After the minimizing player chooses 1 dessert from each of the 3 tables, the maximizing player will then choose 1 dessert from the 3 desserts presented by the minimizing player. Only this time, the maximizing player will choose the dessert closer to 10 on the scale.

  We can see that having a winner is not an easy or direct task, mostly because each player is not really trying to win. They are, however, trying to decrease the chances of the other player winning.

  This logic is the fundamental premise behind minimax: "Which choices do I have that allow me to have a bigger impact on my opponent's chances to win the game".

  The beauty is that with a computer we can simulate different scenarios, allowing for a big degree of complexity.

  Back to Tic Tac Toe.
  As we know understand minimax, the analogy to the classic game is very obvious. The minimizing player is looking into the future, seeing all possible playable scenarios where he can turn the tide in his favour. While the maximizing player is doing the opposite. A constant game of tug-o' war.

  However, on a 3x3 grid such as the one in tic tac toe, on a fresh new game the AI will have to compute 9 factorial (9x8x...x1) possible combinations of plays, ie, 362 880 different possibilities before the first turn is over.  

  Here is when efficiency becomes key and for that we will introduce an optimization algorithm named alpha-beta pruning.

  <br></br>
  
  #### Alpha-Beta Pruning:
  The objective of this algorithm is to skip all the playable scenarios that we know will never happen.

  How can we know for sure a scenario won't play out? Because, we know that the basic premise of one player is to maximize and the other to minimize the score.

  The image below demonstrates this idea visually:

  <img width="1600" height="898" alt="0b" src="https://github.com/user-attachments/assets/04c21627-6b2d-4ad0-b92e-c8a35a524bc4" />

  Consider that the maximizing player is represented by the green triangles (alpha) and the minimizing player by the red ones (beta).

  We are looking at a very simplified version of a choice tree but we can make the analogy to a bigger one.

  Starting from the left, red will have to choose the lowest of 9, 6 and 5. Of course, it will choose 5. There is no optimization possible here. So now green will have the possibility to choose at least a 5 from the 3 options he will have available (after red finishes choosing).

  On the middle, red will find 1. This is the lowest score red as ever found. So we know now that on this middle branch we will only choose something that is lesser than 1. However, we know that the green player already has a 5 guaranteed (the result from the left branch). There is not a single scenario where green chooses a 1 over a 5. We can then optimize by not even looking at the 4 and the 3, essencially skipping them.

  Red moves to the right side and finds a 7. This would be very good for green since the best he can do at the moment is a 5, so red will keep searching. He finds a 2, well just like before, if red keeps searching, he will only choose a new value if it finds a value lesser than 2. But since green already has a 5 guaranteed we know he will never choose a 2 over a 5. And we skip looking for the 8.

  We can then see a pattern. When the lowest value found by the red player (beta) is lesser or equal (<=) than the highest value available at the moment for the green player (alpha), we know the green player will never choose this newer option when presented to him. Therefore, we can skip checking all other possible scenarios that result from this playable case.

  On this small example, we saved computing time by skipping over the triangles with the numbers 4, 3 and 8. So on a 9 choice problem we skipped 3 of them. Imagine on a 200 choice problem, or the tic tac toe situation 362 880 possible choices.


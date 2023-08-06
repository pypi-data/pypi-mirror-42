# SZGO


```

import szgo.engine

>>> from szgo.board.board import Board
>>> b = Board([])

   A B C D E F G H J K L M N O P Q R S T
19 . . . . . . . . . . . . . . . . . . . 19 
18 . . . . . . . . . . . . . . . . . . . 18 
17 . . . . . . . . . . . . . . . . . . . 17 
16 . . . * . . . . . * . . . . . * . . . 16 
15 . . . . . . . . . . . . . . . . . . . 15 
14 . . . . . . . . . . . . . . . . . . . 14 
13 . . . . . . . . . . . . . . . . . . . 13 
12 . . . . . . . . . . . . . . . . . . . 12 
11 . . . . . . . . . . . . . . . . . . . 11 
10 . . . * . . . . . * . . . . . * . . . 10 
 9 . . . . . . . . . . . . . . . . . . . 9 
 8 . . . . . . . . . . . . . . . . . . . 8 
 7 . . . . . . . . . . . . . . . . . . . 7 
 6 . . . . . . . . . . . . . . . . . . . 6 
 5 . . . . . . . . . . . . . . . . . . . 5 
 4 . . . * . . . . . * . . . . . * . . . 4 
 3 . . . . . . . . . . . . . . . . . . . 3 
 2 . . . . . . . . . . . . . . . . . . . 2 
 1 . . . . . . . . . . . . . . . . . . . 1 
   A B C D E F G H J K L M N O P Q R S T
 -----------------------------------------
  Move: 0 
  B captured: 0
  W captured: 0

  go(B)? auto

   A B C D E F G H J K L M N O P Q R S T
19 O . O O O O . O X X O O O . O O O O O 19 
18 O O . O O O O O X X X X O O O O O O O 18 
17 O O O O . O O O X X . X X O . O O . O 17 
16 O O O * O O O X X X X X O O O O O O O 16 
15 O O O O O . O X X X X X O O . O . O O 15 
14 O O O O . O O O X . X . X X O O O O . 14 
13 O X O O O X O X X X . X X X X O . O O 13 
12 X X X X X X O X X X X . X . X O O . O 12 
11 X X O X X X O X X . X X X X X X O O O 11 
10 O X O O O X X . X X . X . X X X X X X 10 
 9 O O O . O O X X X . X X X X O X X . X 9 
 8 O O O O X O X X . X . X X X O X X X X 8 
 7 . O . O X X X X X X X X X X O O X X X 7 
 6 O O O X X X X . X X X . X X O X X X . 6 
 5 X O O X . X X X X . X X O O O O X X X 5 
 4 X X X X X X O O X X X O O O O X X X . 4 
 3 X . X . X X O X X X O O O X X X X X X 3 
 2 . X X X X O O O O O O . O X . X X . X 2 
 1 X X . X O O O . O O O O X X X X . X X 1 
   A B C D E F G H J K L M N O P Q R S T
 -----------------------------------------
  Move: 421 PASS

  B captured: 62
  W captured: 41
  pass cnt: 2

  ----------
  Game Over!
  ----------
  B: 169 + 27 = 196
  W: 145 + 20 = 165

  BLACK WON 31

  go(W)? output

Please check file: output.sgf
```

# szgo

# chess_rl
Chess environment. Agent-agent, agent-human, human-human can play


Chess game environment for ML agent. 'S' (upper case 'S') for blacks, 's' (lower case 's') for whites.
For Agent-Agent game:

      -Create two agents with p1 = Agent('S'), p2 = Agent('s')
      
      -Create chess environment with chs = chess()
      
      -Start the game by start_game(p1, p2, chs)


For Agent-Human game:

      -Create two agents with p1 = Human('S'), p2 = Agent('s')  or  p1 = Human('s'), p2 = Agent('S')
      
      -Create chess environment with chs = chess()
      
      -Start the game by start_game(p1, p2, chs)


For Human-Human game:

      -Create two agents with p1 = Human('S'), p2 = Human('s')
      
      -Create chess environment with chs = chess()
      
      -Start the game by start_game(p1, p2, chs)

Board represented by 8x8 array. Topleft corner -> board[0][0], third line forth column -> board[2][3]
If you are playing, give the coordinates in the form of:

i,j,k,l 

where i j k and l are integers. This means that 'I wanna move the stone in i,j coordinates to k,l coordinates.'


Things that are missing:

      - Rook move
      
      - En passant
      
      - Reading from already played matches data
      

Note: There is no intelligence in agents yet. This is just an environment, agents takes actions randomly.

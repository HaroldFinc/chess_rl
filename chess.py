from __future__ import print_function, division
import math as m
from builtins import range, input
import time

# Note: you may need to update your version of future
# sudo pip install -U future
import numpy as np
import time

class chess:
    def __init__(self):
        self.board = np.chararray((8, 8), unicode = True);
        self.board[:] = '.';
        self.whites = 'pkafvs'
        self.blacks = 'PKAFVS'
        self.white_stones = [];
        self.black_stones = [];
        self.removed_blacks = [];
        self.removed_whites = [];
        self.restart_game();

    def restart_game(self):
        for i in range(8):
            self.white_stones.append(stone(self.whites[0],1,i));
            self.black_stones.append(stone(self.blacks[0],6,i));
            self.board[1, i] = self.whites[0];
            self.board[6, i] = self.blacks[0];
        for i in range(5):
            self.white_stones.append(stone(self.whites[i + 1], 0, i));
            self.black_stones.append(stone(self.blacks[i + 1], 7, i));
            self.board[0, i] = self.whites[i + 1];
            self.board[7, i] = self.blacks[i + 1];
            if i<3:
                self.white_stones.append(stone(self.whites[i + 1], 0, 7 - i));
                self.black_stones.append(stone(self.blacks[i + 1], 7, 7 - i));
                self.board[0, 7 - i] = self.whites[i + 1];
                self.board[7, 7 - i] = self.blacks[i + 1];

    def move(self,x1,y1,x2,y2,sym):
        if (sym in self.whites):
            stn = next((st for st in self.white_stones if (st.coords == [x1,y1])),None);
            if (stn == None):
                print("",end="For None: ");print((x1, y1, x2, y2),end='');print(self.board[x1,y1]);
                print("-----------HATA-------");
                print(self.print_board());
                print("-----------------------");
            idx = self.white_stones.index(stn);
            stn.first_move = False;
            if(self.board[x2,y2] in self.blacks):
                rem = next((stn for stn in self.black_stones if (stn.coords == [x2,y2])), None);
                self.removed_blacks.append(rem);
                self.black_stones.remove(rem);
            self.white_stones[idx].coords = [x2,y2];
        else:
            stn = next((st for st in self.black_stones if (st.coords == [x1, y1])),None);
            if (stn == None):
                print("",end="For None: ");print((x1, y1, x2, y2),end='');print(self.board[x1,y1]);
                print("-----------HATA-------");
                print(self.board);
                print("-----------------------");
            idx = self.black_stones.index(stn);
            stn.first_move = False;
            if(self.board[x2,y2] in self.whites):
                rem = next((stn for stn in self.white_stones if (stn.coords == [x2,y2])), None);
                self.removed_whites.append(rem);
                self.white_stones.remove(rem);
            self.black_stones[idx].coords = [x2,y2];
        self.board[x1, y1] = '.';
        self.board[x2, y2] = stn.sym;

    def check(self,checking_side):
        if (checking_side == 's'):
            sah = next((s for s in self.black_stones if (s.sym == 'S')),None);
            for stn in self.white_stones:
                for psbl in stn.find_possible_moves(self.board):
                    if ((psbl[2] == sah.coords[0]) & (psbl[3] == sah.coords[1])):
                        return True
        else:
            sah = next((s for s in self.white_stones if (s.sym == 's')),None);
            for stn in self.black_stones:
                for psbl in stn.find_possible_moves(self.board):
                    if ((psbl[2] == sah.coords[0]) & (psbl[3] == sah.coords[1])):
                        return True
        return False

    def checkmate_moves(self, checking_side):
        check_moves = []
        temp_stones1 = (self.black_stones).copy()
        temp_stones2 = (self.removed_blacks).copy()
        temp_stones3 = (self.white_stones).copy()
        temp_stones4 = (self.removed_whites).copy()
        temp_board = (self.board).copy()
        print(self.board)
        if checking_side == 's':
            for stn in self.black_stones:
                psbl = stn.find_possible_moves(self.board)
                for act in psbl:
                    self.move(act[0],act[1],act[2],act[3],'S')
                    if self.check(checking_side) == False:
                        check_moves.append(act)
                    self.move(act[2], act[3], act[0], act[1], 'S')
                    self.white_stones = temp_stones3.copy()
                    self.removed_whites = temp_stones4.copy()
                    self.board = temp_board.copy()
        else:
            for stn in self.white_stones:
                psbl = stn.find_possible_moves(self.board)
                for act in psbl:
                    self.move(act[0], act[1], act[2], act[3], 's')
                    if self.check(checking_side) == False:
                        check_moves.append(act)
                    self.move(act[2], act[3], act[0], act[1], 's')
                    self.black_stones = temp_stones1.copy()
                    self.removed_blacks = temp_stones2.copy()
                    self.board = temp_board.copy()

        return check_moves

    def valid_acts(self,psbl,side):
        acts = []
        temp_board = self.board.copy()
        is_black = (side == 'S')
        temp_stones1 = self.white_stones.copy()
        temp_stones2 = self.removed_whites.copy()
        temp_stones3 = self.black_stones.copy()
        temp_stones4 = self.removed_blacks.copy()
        if is_black:
            checking_side = 's'
        else:
            checking_side = 'S'

        for act in psbl:
            self.move(act[0], act[1], act[2], act[3], side)
            if self.check(checking_side) == False:
                acts.append(act)
            self.move(act[2], act[3], act[0], act[1], side)
            self.white_stones = temp_stones1.copy()
            self.removed_whites = temp_stones2.copy()
            self.black_stones = temp_stones3.copy()
            self.removed_blacks = temp_stones4.copy()
            self.board = temp_board.copy()

        print("# of valid acts: " + str(len(acts)))
        return acts

    def draw_board(self):
        board = self.board.copy()
        for i in range(8):
            for j in range(8):
                #   	 	 	 	♙
                if self.board[i,j] == 's':
                    board[i,j] = '♚';
                elif self.board[i,j] == 'S':
                    board[i,j] = '♔';
                elif self.board[i,j] == 'v':
                    board[i,j] = '♛';
                elif self.board[i,j] == 'V':
                    board[i,j] = '♕';
                elif self.board[i,j] == 'k':
                    board[i,j] = '♜';
                elif self.board[i,j] == 'K':
                    board[i,j] = '♖';
                elif self.board[i,j] == 'a':
                    board[i,j] = '♞';
                elif self.board[i,j] == 'A':
                    board[i,j] = '♘';
                elif self.board[i,j] == 'f':
                    board[i,j] = '♝';
                elif self.board[i,j] == 'F':
                    board[i,j] = '♗';
                elif self.board[i,j] == 'p':
                    board[i,j] = '♟';
                elif self.board[i,j] == 'P':
                    board[i,j] = '♙';
        print("------------")
        print('\n'.join([''.join(['{:12}'.format(item) for item in row])
                         for row in board]))
        print("------------")

    def algebraic_chess(self,file_path):
        with open(file_path) as fp:
            line = fp.readline()

            cnt = 1
            while line:
                print("Line {}: {}".format(cnt, line.strip()))
                line = fp.readline()
                cnt += 1

class Agent:
    def __init__(self,sym):
        self.sym = sym;
        self.possible_actions = []

    def take_action(self):
        acts = self.possible_actions;
        idx = np.random.choice(len(acts));print(len(acts));
        action = self.possible_actions[idx];
        self.clear_list()
        return action;

    def append_to_list(self,list):
        temp = self.possible_actions ;
        self.possible_actions = temp + list;

    def clear_list(self):
        self.possible_actions = [];

class Human:
    def __init__(self,sym):
        self.sym = sym;
        self.possible_actions = []

    def take_action(self):
        while True:
            # break if we make a legal move
            move = input("Enter coordinates i,j , k,l for your next move (i,j,k,l = 0,2,0,4)(i,j -> k,l): ")
            try:
                i, j, k, l = move.split(',')
            except ValueError:
                continue

            i = int(i)
            j = int(j)
            k = int(k)
            l = int(l)
            action = (i,j,k,l);
            if action in self.possible_actions:
                return action;
            else:
                print("Please enter a legal action.");
                return self.take_action();

    def append_to_list(self, list):
        temp = self.possible_actions;
        self.possible_actions = temp + list;

class stone:
    def __init__(self,sym,x,y):
        self.first_move = True;
        self.blacks = 'PKFAVS';
        self.whites = 'pkfavs';
        self.sym = sym;
        self.possible_moves = [];
        self.coords = [];
        self.coords.append(x);
        self.coords.append(y);

    def find_possible_moves(self,board):
        if self.sym == 'p':
            self.possible_moves_p( board);
        elif self.sym == 'P':
            self.possible_moves_P( board);
        elif (self.sym == 'a'):
            self.possible_moves_at(board,self.whites);
        elif (self.sym == 'A'):
            self.possible_moves_at(board,self.blacks);
        elif (self.sym == 'f'):
            self.possible_moves_fil(board,self.whites);
        elif (self.sym == 'F'):
            self.possible_moves_fil(board,self.blacks);
        elif (self.sym == 'v'):
            self.possible_moves_vezir(board,self.whites);
        elif (self.sym == 'V'):
            self.possible_moves_vezir(board,self.blacks);
        elif (self.sym == 's'):
            self.possible_moves_şah(board,self.whites);
        elif (self.sym == 'S'):
            self.possible_moves_şah(board,self.blacks);
        possible = self.possible_moves.copy();
        self.possible_moves = [];
        return possible;

    def clear_moves(self):
        self.possible_moves = [];

    def possible_moves_p(self,board):
        # Forward movement
        a = self.coords[0];
        b = self.coords[1];
        if a == 7:
            self.change_piyon(board);
            print("selamm")
            return
        if ((board[ a+ 1, b] == '.')):
            self.possible_moves.append((a,b,a + 1, b));
            if (self.first_move):
                if(board[a + 2, b] == '.'):
                    self.possible_moves.append((a,b,a + 2, b));
        # Eating a stone movement
        if(b != 0):# check left side
            if (( self.blacks.find(board[a + 1,b - 1]) != -1) ):
                self.possible_moves.append((a,b,a + 1, b - 1));
        if ((b != 7) ):# check right side
            if(self.blacks.find(board[a + 1, b + 1]) != -1):
                self.possible_moves.append((a,b,a + 1, b + 1));
        if a == 7:
            self.change_piyon(board);
            print("selamm")
            return

    def possible_moves_P(self,board):
        a = self.coords[0];
        b = self.coords[1];
        if a == 0:
            self.change_piyon(board);
            print("selamm")
            return
        if (board[a - 1, b] == '.'):# Forward movement
            self.possible_moves.append((a,b,a - 1, b));
            if (self.first_move):
                if(board[a - 2, b] == '.'):
                    self.possible_moves.append((a,b,a - 2, b));
        #cross movement
        if (b != 0):#left side
            if(self.whites.find(board[a - 1, b - 1]) != -1):
                self.possible_moves.append((a,b,a - 1, b - 1));
        if (b != 7):#right side
            if(self.whites.find(board[a - 1, b + 1]) != -1):
                self.possible_moves.append((a,b,a - 1, b + 1));
        if a == 0:
            self.change_piyon(board);
            print("selamm")
            return

    def possible_moves_at(self,board,syms):
        a = self.coords[0];
        b = self.coords[1];
        if(((a+2)<8) &  ((b+1)<8)):
            if(syms.find(board[a+2,b+1]) == -1):
                self.possible_moves.append((a,b,a+2,b+1));
        if (((a - 2) > -1) & ((b + 1) < 8)):
            if (syms.find(board[a - 2, b + 1]) == -1):
                self.possible_moves.append((a,b,a - 2, b + 1));
        if (((a + 2) < 8) & ((b - 1) > -1)):
            if (syms.find(board[a + 2, b - 1]) == -1):
                self.possible_moves.append((a,b,a + 2, b - 1));
        if (((a - 2) > -1) & ((b - 1) > -1)):
            if (syms.find(board[a - 2, b - 1]) == -1):
                self.possible_moves.append((a,b,a - 2, b - 1));
        #  #####
        if (((a + 1) < 8) & ((b + 2) < 8)):
            if (syms.find(board[a + 1, b + 2]) == -1):
                self.possible_moves.append((a,b,a + 1, b + 2));
        if (((a - 1) > -1) & ((b + 2) < 8)):
            if (syms.find(board[a - 1, b + 2]) == -1):
                self.possible_moves.append((a,b,a - 1, b + 2));
        if (((a + 1) < 8) & ((b - 2) > -1)):
            if (syms.find(board[a + 1, b - 2]) == -1):
                self.possible_moves.append((a,b,a + 1, b - 2));
        if (((a - 1) > -1) & ((b - 2) > -1)):
            if (syms.find(board[a - 1, b - 2]) == -1):
                self.possible_moves.append((a,b,a - 1, b - 2));
        #  #####

    def possible_moves_fil(self,board,syms):
        a = self.coords[0];
        b = self.coords[1];
        i=1;
        while(((a+i) != 8) & ((b+i) != 8)):
            sym = board[a+i, b+i];
            if (syms.find(sym) == -1):
                self.possible_moves.append((a,b,a+i , b+i ));
            i = i + 1;
            if(sym != '.') :
                break;

        i=1;
        while (((a + i) != 8) & ((b - i) != -1)):
            sym = board[a + i, b - i];
            if (syms.find(sym) == -1):
                self.possible_moves.append((a,b,a+i, b-i));
            i = i + 1;
            if (sym != '.'):
                break;

        i=1;
        while (((a - i) != -1) & ((b + i) != 8)):
            sym = board[a - i, b + i];
            if (syms.find(sym) == -1):
                self.possible_moves.append((a,b,a-i, b+i));
            i = i + 1;
            if (sym != '.'):
                break;

        i=1;
        while (((a - i) != -1) & ((b - i) != -1)):
            sym = board[a - i, b - i];
            if (syms.find(board[a-i, b-i]) == -1):
                self.possible_moves.append((a,b,a-i, b-i));
            i = i + 1;
            if (sym != '.'):
                break;

    def possible_moves_kale(self,board,syms):
        a = self.coords[0];
        b = self.coords[1];
        i=1;
        while (((a + i) != 8)):
            sym = board[a+i, b ];
            if (syms.find(sym) == -1):
                self.possible_moves.append((a,b,a+i, b));
            i=i+1;
            if (sym != '.'):
                break;

        i=1;
        while (((a - i) != -1)):
            sym = board[a-i, b];
            if (syms.find(sym) == -1):
                self.possible_moves.append((a,b,a-i, b));
            i=i+1;
            if (sym != '.'):
                break;

        i=1;
        while (((b + i) != 8)):
            sym = board[a, b + i]
            if (syms.find(sym) == -1):
                self.possible_moves.append((a,b,a, b+i));
            i=i+1;
            if (sym != '.'):
                break;
        i=1;
        while (((b - i) != -1)):
            sym = board[a, b - i]
            if (syms.find(sym) == -1):
                self.possible_moves.append((a,b,a, b-i));
            i=i+1;
            if (sym != '.'):
                break;

    def possible_moves_vezir(self,board,syms):
        self.possible_moves_fil(board,syms);
        self.possible_moves_kale(board,syms);

    def possible_moves_şah(self,board,syms):
        a = self.coords[0];
        b = self.coords[1];
        if(((a+1) != 8) & ((b+1) !=8)):
            if (syms.find(board[a+1, b+1]) == -1):
                self.possible_moves.append((a,b,a+1, b+1));
            if (syms.find(board[a, b+1]) == -1):
                self.possible_moves.append((a,b,a, b+1));
            if (syms.find(board[a + 1, b]) == -1):
                self.possible_moves.append((a,b,a+1, b));
        if (((a + 1) != 8) & ((b - 1) != -1)):
            if (syms.find(board[a + 1, b - 1]) == -1):
                self.possible_moves.append((a,b,a + 1, b - 1));
            if (syms.find(board[a, b - 1]) == -1):
                self.possible_moves.append((a,b,a, b - 1));
            if (syms.find(board[a + 1, b]) == -1):
                self.possible_moves.append((a,b,a + 1, b));
        if (((a - 1) != -1) & ((b + 1) != 8)):
            if (syms.find(board[a - 1, b + 1]) == -1):
                self.possible_moves.append((a,b,a - 1, b + 1));
            if (syms.find(board[a, b + 1]) == -1):
                self.possible_moves.append((a,b,a, b + 1));
            if (syms.find(board[a - 1, b]) == -1):
                self.possible_moves.append((a,b,a - 1, b));
        if (((a - 1) != -1) & ((b - 1) != -1)):
            if (syms.find(board[a - 1, b - 1]) == -1):
                self.possible_moves.append((a,b,a - 1, b - 1));
            if (syms.find(board[a, b - 1]) == -1):
                self.possible_moves.append((a,b,a, b - 1));
            if (syms.find(board[a - 1, b]) == -1):
                self.possible_moves.append((a,b,a - 1, b));

    def change_piyon(self,board):
        if (self.coords[0] == 7):
            self.sym = 'v';
        elif (self.coords[0] == 0):
            self.sym = 'V';
        self.possible_moves = [];

def play_game(p1, p2,chs):
    start_time = time.time()
    psbl = []
    current_player = p1;
    if current_player.sym == 's':
        for stn in chs.white_stones:
            psbl = psbl + stn.find_possible_moves(chs.board);
    else:
        for stn in chs.black_stones:
            psbl = psbl + stn.find_possible_moves(chs.board);
    current_player.append_to_list(psbl);
    psbl = [];
    action = current_player.take_action();
    chs.move(action[0],action[1],action[2],action[3],current_player.sym);
    chs.draw_board()
    #time.sleep(0.33);
    i=0;
    while i!=500:
        if current_player == p1:
            current_player = p2
        else:
            current_player = p1

        if current_player.sym == 's':
            i=i+1;
            if chs.check('S') == False:
                for stn in chs.white_stones:
                    psbl = psbl + stn.find_possible_moves(chs.board)
                psbl = chs.valid_acts(psbl,current_player.sym)
                if len(psbl) == 0:
                    print("Game over! Winning side : Blacks!")
                    return

            else:
                print("Check !")
                psbl = chs.checkmate_moves('S')
                print("CHECK MATE MOVES:" + str(psbl))
                if len(psbl) == 0:
                    chs.draw_board()
                    print("Game over! Winning side : Blacks!")
                    return
        else:
            if chs.check('s') == False:
                for stn in chs.black_stones:
                    psbl = psbl + stn.find_possible_moves(chs.board)
                psbl = chs.valid_acts(psbl, current_player.sym)
                if len(psbl) == 0:
                    print("Game over! Winning side : Whites!")
                    return
            else:
                print("Check !")
                psbl = chs.checkmate_moves('s')
                print("CHECK MATE MOVES:" + str(psbl))
                if len(psbl) == 0:
                    chs.draw_board()
                    print("Game over! Winning side : Whites!")
                    return
        print("i: "+str(i))
        current_player.append_to_list(psbl);
        psbl = [];
        action = current_player.take_action();
        chs.move(action[0], action[1], action[2], action[3], current_player.sym);
        chs.draw_board()

        print(action);
        #time.sleep(0.33);
    print("Time: "+str(time.time()-start_time));



p1 = Agent('s');
p2 = Human('S');
#p2 = Agent('S');
chs = chess();
play_game(p1,p2,chs);
chs.draw_board();

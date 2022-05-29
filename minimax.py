from cmath import inf
from state import State
import evaluation
import copy
import time

DEPTH = 4
ALPHA = float(-inf)
BETA = float(inf)

class Game(object):

    __slots__ = ['current_state', 'player_turn' , 'state_before', 'phase']

    def __init__(self):
        self.current_state = None
        self.player_turn = None
        self.state_before = None
        self.phase = None

    def initialize_game(self):
        self.current_state = State()
        self.phase = 1
        self.state_before = copy.deepcopy(self.current_state)
        while True:
            user_input = input("Da li želite prvi da igrate?\n(Unesite 'da' ili 'ne'): ")
            if self.check_first_player_input(user_input) == True:
                if user_input.upper() == "DA":
                    self.player_turn = State.PLAYER
                else:
                    self.player_turn = State.AI
                break
            else:
                print("Unos nije dobar!")
                continue

    def check_first_player_input(self, txt):
        if txt.upper() == "DA" or txt.upper() == "NE":
            return True
        else:
            return False

    def change_player(self,player):
        if player == State.PLAYER:
            return State.AI
        else:
            return State.PLAYER


    #----------------------------------------------------------------------- MINIMAX funkcije -----------------------------------------------------------------------

    def max(self, depth, alpha, beta):
        max_eval = float(-inf)
        max_index = None
        result = False

        if self.phase != 1:
            result, winner = self.current_state.is_end()

        if depth == 0 or result == True:
            return evaluation.eval(self.current_state, self.state_before, self.phase), max_index

        for i in range(0,24):
            if self.current_state.get_value(i) == "X":
                self.state_before = copy.deepcopy(self.current_state)
                self.current_state.set_value(i, self.current_state.AI)
                # print(self.current_state) #OBRISATI KASNIJE


                if evaluation.closed_mill(self.current_state, self.state_before) == 1:
                    eval, index = self.min_remove(depth-1,alpha,beta)
                else:
                    eval, index = self.min(depth-1,alpha,beta)

                if eval > max_eval:
                    max_eval = eval
                    max_index = i

                alpha = max(alpha, eval)

                self.current_state.set_value(i, "X")

            if max_eval >= beta:
                return max_eval, max_index

        return max_eval, max_index


    def min(self, depth, alpha, beta):
        min_eval = float(+inf)
        min_index = None
        result = False

        if self.phase != 1:
            result, winner = self.current_state.is_end()

        if depth == 0 or result == True:
            return evaluation.eval(self.current_state, self.state_before, self.phase), min_index

        for i in range(0,24):
            if self.current_state.get_value(i) == "X":
                self.state_before = copy.deepcopy(self.current_state)
                self.current_state.set_value(i, self.current_state.PLAYER)
                # print(self.current_state)   #OBRISATI KASNIJE

                if evaluation.closed_mill(self.current_state, self.state_before) == -1:
                    eval, index = self.max_remove(depth-1,alpha,beta)
                else:
                    eval, index = self.max(depth-1,alpha,beta)

                if eval < min_eval:
                    min_eval = eval
                    min_index = i
                beta = min(beta, eval)

                self.current_state.set_value(i, "X")

            if min_eval <= alpha:
                return min_eval, min_index
                
        return min_eval, min_index

#---------------------------------------------------------------------------------------------------------------------------------------------------------------


#---------------------------------------------------- MINIMAX funckije koje se pozivaju u slucaju brisanja figure --------------------------------------------

    def max_remove(self, depth, alpha, beta):
        max_eval = float(-inf)
        max_index = None
        result = False
        # enemy = self.change_player(self.player_turn)
        free_figures = evaluation.are_there_non_mill_figures(self.current_state,self.current_state.PLAYER)  #Bool vrednost koja pokazuje da li ima figura koje nisu u mici

        if self.phase != 1:
            result, winner = self.current_state.is_end()

        if depth == 0 or result == True:
            return evaluation.eval(self.current_state, self.state_before, self.phase), max_index

        for i in range(0,24):
            if self.current_state.get_value(i) == self.current_state.PLAYER:
                
                if free_figures and evaluation.is_mill(self.current_state,self.current_state.PLAYER,i): #Ako je figura u mici i ima slobodnih figura preskacemo
                    continue

                self.state_before = copy.deepcopy(self.current_state)
                self.current_state.set_value(i, "X")
                self.current_state.black_figures -= 1
                # print(self.current_state)   #OBRISATI KASNIJE

                eval, index = self.min(depth-1,alpha,beta)

                if eval > max_eval:
                    max_eval = eval
                    max_index = i
                alpha = max(alpha, eval)

                self.current_state.set_value(i, self.current_state.PLAYER)
                self.current_state.black_figures += 1

            if max_eval >= beta:
                return max_eval, max_index
        return max_eval, max_index


    def min_remove(self, depth, alpha, beta):
        min_eval = float(+inf)
        min_index = None
        result = False
        # enemy = self.change_player(self.player_turn)
        free_figures = evaluation.are_there_non_mill_figures(self.current_state,self.current_state.AI)  #Bool vrednost koja pokazuje da li ima figura koje nisu u mici

        if self.phase != 1:
            result, winner = self.current_state.is_end()

        if depth == 0 or result == True:
            return evaluation.eval(self.current_state, self.state_before, self.phase), min_index

        for i in range(0,24):
            if self.current_state.get_value(i) == self.current_state.AI:
                
                if free_figures and evaluation.is_mill(self.current_state,self.current_state.AI,i): #Ako je figura u mici i ima slobodnih figura preskacemo
                    continue

                self.state_before = copy.deepcopy(self.current_state)
                self.current_state.set_value(i, "X")
                self.current_state.white_figures -= 1
                # print(self.current_state)   #OBRISATI KASNIJE

                eval, index= self.max(depth-1,alpha,beta)

                if eval < min_eval:
                    min_eval = eval
                    min_index = i
                beta = min(beta, eval)

                self.current_state.set_value(i, self.current_state.AI)
                self.current_state.white_figures += 1

            if min_eval <= alpha:
                return min_eval, min_index
                
        return min_eval, min_index

#---------------------------------------------------------------------------------------------------------------------------------------------------------------

    def phase_one_player(self):
        print(self.current_state)
        while True:
            user_input = input("Unesite polje na koje želite da postavite figuru: ")
            if self.current_state.is_move_valid(user_input):
                self.current_state.set_value(user_input, State.PLAYER)
                break
            else:
                print("Unos nije dobar!")
                continue
        print(self.current_state)
        if evaluation.closed_mill(self.current_state, self.state_before) == -1:
            while True:
                user_input = input("Unesite polje sa kojeg želite da skinete figuru: ")
                try:
                    user_input = int(user_input)
                    if self.current_state.get_value(user_input) == State.AI:
                        free_figures = evaluation.are_there_non_mill_figures(self.current_state,self.current_state.AI)
                        if free_figures and evaluation.is_mill(self.current_state,self.current_state.AI,user_input):
                            print("Ne možete pojesti ovu figuru!")
                            continue
                        self.remove_figure(user_input)
                        break
                    else:
                        print("Na ovoj poziciji se ne nalazi neprijateljska figura!")
                        continue

                except:
                    print("Unos nije dobar!")
                    continue
            print(self.current_state)

    def phase_one_ai(self):
        self.state_before = copy.deepcopy(self.current_state)

        start_time = time.time()
        eval, index = self.max(DEPTH, ALPHA, BETA)
        print("--- %s seconds ---" % (time.time() - start_time))

       
        self.current_state.set_value(index, self.current_state.AI)

        if evaluation.is_mill(self.current_state, self.current_state.AI, index):
            print(self.current_state)
            eval2, index2 = self.max_remove(DEPTH - 1, ALPHA, BETA)
            self.remove_figure(index2)       
        print(self.current_state)

            
    def remove_figure(self,index):
        if self.current_state.get_value(index) == State.AI:
            self.current_state.white_figures -= 1
        else:
            self.current_state.black_figures -= 1
        self.state_before = copy.deepcopy(self.current_state)
        self.current_state.set_value(index,"X")   

    def play(self):
        self.initialize_game()

        #FAZA 1
        for i in range(0,9):
            self.phase_one_player()
            self.phase_one_ai()

        #FAZA 2
        # while True:
        #     result, winner = self.current_state.is_end()

        #     if result == True:
        #         print("*"*30 + "\n\n" "Pobednik je: " + winner + "!\n\n" + "*"*30)



if __name__ == "__main__":
    game = Game()
    game.play()
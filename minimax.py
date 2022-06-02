from cmath import inf
from state import State
import evaluation
import copy
import time

DEPTH = 4
DEPTH2 = 5
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
        print("\n"*2 + "*"*30 + " MICE " + "*"*30 + "\n")
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


    #----------------------------------------------------------------------- MINIMAX funkcije za fazu 1 -----------------------------------------------------------------------

    def max(self, depth, alpha, beta):
        max_eval = float(-inf)
        max_index = None

        if depth == 0:
            return evaluation.eval(self.current_state, self.state_before, self.phase), max_index

        for i in range(0,24):
            if self.current_state.get_value(i) == "X":
                self.state_before = copy.deepcopy(self.current_state)
                self.current_state.set_value(i, self.current_state.AI)
                self.current_state.placed_figures[State.AI] += 1


                if evaluation.closed_mill(self.current_state, self.state_before) == 1:
                    eval, index = self.max_remove(depth-1,alpha,beta)
                else:
                    if self.current_state.placed_figures[State.PLAYER] == 9:    #Ako su postavljene sve figure prelazi na fazu 2
                        self.phase = 2
                        eval, index, neighbour = self.min2(depth-1,alpha,beta)
                    else:
                        eval, index = self.min(depth-1,alpha,beta)

                if eval > max_eval:
                    max_eval = eval
                    max_index = i

                alpha = max(alpha, eval)

                #Vracam sve vrednosti nazad
                self.current_state.set_value(i, "X")
                self.current_state.placed_figures[State.AI] -= 1
                self.phase = 1 

            if max_eval >= beta:
                return max_eval, max_index

        return max_eval, max_index


    def min(self, depth, alpha, beta):
        min_eval = float(+inf)
        min_index = None
        result = False

        if depth == 0 or result == True:
            return evaluation.eval(self.current_state, self.state_before, self.phase), min_index

        for i in range(0,24):
            if self.current_state.get_value(i) == "X":
                self.state_before = copy.deepcopy(self.current_state)
                self.current_state.set_value(i, self.current_state.PLAYER)
                self.current_state.placed_figures[State.PLAYER] += 1

                if evaluation.closed_mill(self.current_state, self.state_before) == -1:
                    eval, index = self.min_remove(depth-1,alpha,beta)
                else:
                    if self.current_state.placed_figures[State.AI] == 9:    #Ako su postavljene sve figure prelazi na fazu 2
                        self.phase = 2
                        eval, index, neighbour = self.max2(depth-1,alpha,beta)
                    else:
                        eval, index = self.max(depth-1,alpha,beta)

                if eval < min_eval:
                    min_eval = eval
                    min_index = i
                beta = min(beta, eval)

                #Vracam sve vrednosti nazad
                self.current_state.set_value(i, "X")
                self.current_state.placed_figures[State.PLAYER] -= 1
                self.phase = 1 

            if min_eval <= alpha:
                return min_eval, min_index
                
        return min_eval, min_index

#**************************************************************************************************************************************************************************



#----------------------------------------------------------------------- MINIMAX funkcije za fazu 2 -----------------------------------------------------------------------

    def max2(self, depth, alpha, beta):
        max_eval = float(-inf)
        max_index = None    #polje na kojem se nalazi figura
        max_neighbour = None    #Polje na koje se pomera figura
        result = False

        result, winner = self.current_state.is_end()    #posto je faza 2 racunam kraj

        if depth == 0 or result == True:
            return evaluation.eval(self.current_state, self.state_before, self.phase), max_index, max_neighbour

        for i in range(0,24):
            if self.current_state.get_value(i) == State.AI:
                for neighbour in State.NEIGHBOURS[i]:
                    if self.current_state.get_value(neighbour) == "X":
                        self.state_before = copy.deepcopy(self.current_state)
                        self.current_state.set_value(neighbour, State.AI)
                        self.current_state.set_value(i,"X")

                        if evaluation.closed_mill(self.current_state, self.state_before) == 1:
                            eval, index = self.max_remove(depth-1,alpha,beta)
                        else:
                            eval, index, ret2 = self.min2(depth-1,alpha,beta)

                        if eval > max_eval:
                            max_eval = eval
                            max_index = i
                            max_neighbour = neighbour

                        alpha = max(alpha, eval)

                        #Vracam sve vrednosti nazad
                        self.current_state.set_value(i, State.AI)
                        self.current_state.set_value(neighbour, "X")

                    if max_eval >= beta:
                        return max_eval, max_index, max_neighbour

        return max_eval, max_index, max_neighbour


    def min2(self, depth, alpha, beta): #RADI DOBRO
        min_eval = float(+inf)
        min_index = None    #polje na kojem se nalazi figura
        min_neighbour = None    #Polje na koje se pomera figura
        result = False

        result, winner = self.current_state.is_end()    #posto je faza 2 racunam kraj

        if depth == 0 or result == True:
            return evaluation.eval(self.current_state, self.state_before, self.phase), min_index, min_neighbour

        for i in range(0,24):
            if self.current_state.get_value(i) == State.PLAYER:
                for neighbour in State.NEIGHBOURS[i]:
                    if self.current_state.get_value(neighbour) == "X":
                        self.state_before = copy.deepcopy(self.current_state)
                        self.current_state.set_value(neighbour, State.PLAYER)
                        self.current_state.set_value(i,"X")

                        if evaluation.closed_mill(self.current_state, self.state_before) == -1:
                            eval, index = self.min_remove(depth-1,alpha,beta)
                        else:
                            eval, index, ret2 = self.max2(depth-1,alpha,beta)

                        if eval < min_eval:
                            min_eval = eval
                            min_index = i
                            min_neighbour = neighbour
                        beta = min(beta, eval)

                        #Vracam sve vrednosti nazad
                        self.current_state.set_value(i, State.PLAYER)
                        self.current_state.set_value(neighbour, "X")

                    if min_eval <= alpha:
                        return min_eval, min_index, min_neighbour
                
        return min_eval, min_index, min_neighbour

#***************************************************************************************************************************************************************************




#------------------------------------------------------------ MINIMAX funckije koje se pozivaju u slucaju brisanja figure --------------------------------------------------

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

                if self.phase == 2:
                    eval, index, neighbour = self.min2(depth-1,alpha,beta)
                else:
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

                if self.phase == 2:
                    eval, index, neighbour = self.max2(depth-1,alpha,beta)
                else:
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

#*************************************************************************************************************************************************************************



#------------------------------------------------------------------------ funkcije za poteze u PRVOJ fazi ----------------------------------------------------------------

    def phase_one_player(self):
        print(self.current_state)
        while True:
            user_input = input("Unesite polje na koje želite da postavite figuru (Unesite 'X' za prekid igre): ")
            if user_input.upper() == "X":
                return "X"
            if self.current_state.is_move_valid(user_input):
                self.state_before = copy.deepcopy(self.current_state)
                self.current_state.set_value(user_input, State.PLAYER)
                self.current_state.placed_figures[State.PLAYER] += 1
                print(self.current_state)
                break
            else:
                print("Unos nije dobar!")
                continue
        if evaluation.closed_mill(self.current_state, self.state_before) == -1:
            while True:
                user_input2 = input("Unesite polje sa kojeg želite da skinete figuru (Unesite 'X' za prekid igre): ")
                if user_input2.upper() == "X":
                    return "X"
                try:
                    user_input2 = int(user_input2)
                    if self.current_state.get_value(user_input2) == State.AI:
                        free_figures = evaluation.are_there_non_mill_figures(self.current_state,self.current_state.AI)
                        if free_figures and evaluation.is_mill(self.current_state,self.current_state.AI,user_input2):
                            print("Ne možete pojesti ovu figuru!")
                            continue
                        self.remove_figure(user_input2)
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

        eval, index = self.max(DEPTH, ALPHA, BETA)

        self.current_state.set_value(index, State.AI)
        print("Postavljena je figura na poziciju '{}'".format(index))
        self.current_state.placed_figures[State.AI] += 1

        if evaluation.is_mill(self.current_state, State.AI, index):
            print(self.current_state)

            eval2, index2 = self.max_remove(DEPTH , ALPHA, BETA)

            self.remove_figure(index2)
            print("Skinuta je figura na poziciji", index2)
        # print(self.current_state)

#*************************************************************************************************************************************************************************




#------------------------------------------------------------------------ funkcije za poteze u DRUGOJ fazi ----------------------------------------------------------------

    def phase_two_player(self):
        print(self.current_state)
        while True:
            user_input1 = input("Unesite broj polja na kojem se nalazi figura koju želite da pomerite (Unesite 'X' za prekid igre): ")
            if user_input1.upper() == "X":
                return "X"
            try:
                user_input1 = int(user_input1)
                if self.current_state.get_value(user_input1) == State.PLAYER:
                    potential_possible_moves = State.NEIGHBOURS[user_input1]
                    possible_moves = []
                    for i in potential_possible_moves:
                        if self.current_state.get_value(i) == "X":
                            possible_moves.append(i)
                else:
                    print("Na ovom polju se ne nalazi vaša figura!")
                    continue
                if len(possible_moves) == 0:
                    print("Ova figura je blokirana!")
                    continue
                break
            except:
                print("Unos nije dobar!")
        while True:
            user_input2 = input("Unesite polje na koje želite da pomerite figuru (moguća polja su {}) (Unesite 'X' za prekid igre): ".format(possible_moves))
            if user_input2.upper() == "X":
                return "X"
            try:
                user_input2 = int(user_input2)
                if user_input2 in possible_moves:
                    self.state_before = copy.deepcopy(self.current_state)
                    self.current_state.set_value(user_input1, "X")
                    self.current_state.set_value(user_input2, State.PLAYER)
                    print(self.current_state)
                    break
                else:
                    print("Morate izabrati neki od ponuđenih polja!")
                    continue
            except:
                print("Nije dobar unos!")
                continue
        if evaluation.closed_mill(self.current_state, self.state_before) == -1:
            while True:
                user_input3 = input("Unesite polje sa kojeg želite da skinete figuru (Unesite 'X' za prekid igre): ")
                if user_input3.upper() == "X":
                    return "X"
                try:
                    user_input3 = int(user_input3)
                    if self.current_state.get_value(user_input3) == State.AI:
                        free_figures = evaluation.are_there_non_mill_figures(self.current_state,self.current_state.AI)
                        if free_figures and evaluation.is_mill(self.current_state,self.current_state.AI,user_input3):
                            print("Ne možete pojesti ovu figuru!")
                            continue
                        self.remove_figure(user_input3)
                        break
                    else:
                        print("Na ovoj poziciji se ne nalazi neprijateljska figura!")
                        continue
                except:
                    print("Unos nije dobar!")
                    continue
            print(self.current_state)

    def phase_two_ai(self):
        self.state_before = copy.deepcopy(self.current_state)

        eval, index, neighbour = self.max2(DEPTH2, ALPHA, BETA)

        self.current_state.set_value(neighbour, State.AI)
        self.current_state.set_value(index, "X")
        print("Pomerena je figura sa pozicije '{}' na poziciju '{}'".format(index,neighbour))
       
        if evaluation.is_mill(self.current_state, State.AI, neighbour):
            print(self.current_state)

            eval2, index2 = self.max_remove(DEPTH2, ALPHA, BETA)

            self.remove_figure(index2)  
            print("Skinuta je figura na poziciji", index2)     
        # print(self.current_state)

#*************************************************************************************************************************************************************************



    def remove_figure(self,index):
        if self.current_state.get_value(index) == State.AI:
            self.current_state.white_figures -= 1
        else:
            self.current_state.black_figures -= 1
        self.state_before = copy.deepcopy(self.current_state)
        self.current_state.set_value(index,"X")   

    def check_winner(self):
        result, winner = self.current_state.is_end()
        if result == True:
            print("*"*30 + "\n\n" "Pobednik je: " + winner + "!\n\n" + "*"*30 + "\n")
            return True

    def play(self):
        self.initialize_game()

        #FAZA 1
        print("\n" + "*"*30 + " FAZA 1 " + "*"*30 + "\n")
        for i in range(0,9):
            if self.player_turn == State.PLAYER:
                if self.phase_one_player() == "X":
                    break

                start_time = time.time()
                self.phase_one_ai()
                print("--- %s seconds ---" % (time.time() - start_time))

            elif self.player_turn == State.AI:
                start_time = time.time()
                self.phase_one_ai()
                print("--- %s seconds ---" % (time.time() - start_time))

                if self.phase_one_player() == "X":
                    break
            

        #FAZA 2
        self.phase = 2
        print("\n" + "*"*30 + " FAZA 2 " + "*"*30 + "\n")
        while True:
            if self.check_winner():
                break

            if self.player_turn == State.PLAYER:
                if self.phase_two_player() == "X":
                    break
                if self.check_winner():
                    break

                start_time = time.time()
                self.phase_two_ai()
                print("--- %s seconds ---" % (time.time() - start_time))

            elif self.player_turn == State.AI:

                start_time = time.time()
                self.phase_two_ai()
                print("--- %s seconds ---" % (time.time() - start_time))

                if self.check_winner():
                    break
                if self.phase_two_player()  == "X":
                    break
        print("*"*20 + " KRAJ IGRE " + "*"*20)

            



if __name__ == "__main__":
    game = Game()
    game.play()

    #TO DO
    # uraditi fazu 2 i preurediti minmax algoritam da zna sta da radi pred kraj faze 1
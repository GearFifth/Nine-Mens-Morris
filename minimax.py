from cmath import inf
from state import State
import evaluation
import copy

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

    def max(self, depth, alpha, beta):
        max_eval = float(-inf)
        result = False

        if self.phase != 1:
            result, winner = self.current_state.is_end()

        if depth == 0 or result == True:
            return evaluation.eval(self.current_state)

        for i in range(0,24):
            if self.current_state.get_value(i) == "X":
                self.state_before = copy.deepcopy(self.current_state)
                self.current_state.set_value(i, self.player_turn)

                if evaluation.closed_mill(self.current_state, self.state_before, self.player_turn):
                    eval = self.min_remove(depth-1,alpha,beta)
                else:
                    eval = self.min(depth-1,alpha,beta)

                max_eval = max(max_eval,eval)
                alpha = max(alpha, eval)

                self.current_state.set_value(i, "X")

            if max_eval >= beta:
                return max_eval

        self = self.change_player(self.player_turn)
        return max_eval

    def max_remove(self, depth, alpha, beta):

    def min(self, depth, alpha, beta):
        min_eval = float(+inf)
        result = False

        if self.phase != 1:
            result, winner = self.current_state.is_end()

        if depth == 0 or result == True:
            return evaluation.eval(self.current_state)

        for i in range(0,24):
            if self.current_state.get_value(i) == "X":
                self.state_before = copy.deepcopy(self.current_state)
                self.current_state.set_value(i, self.player_turn)

                if evaluation.closed_mill(self.current_state, self.state_before, self.player_turn):
                    eval = self.max_remove(depth-1,alpha,beta)
                else:
                    eval = self.max(depth-1,alpha,beta)

                min_eval = min(min_eval,eval)
                beta = min(beta, eval)

                self.current_state.set_value(i, "X")

            if min_eval <= alpha:
                return min_eval

        self = self.change_player(self.player_turn)
        return min_eval


    # def minimax(self, state, depth, alpha, beta, max_player):

    #     eval = self.current_state.eval()    #TO DO: Namestiti eval funkciju u state-u

    #     result, winner = self.current_state.is_end()
    #     if depth == 0 or result == True:
    #         return eval

    #     #Ako je na potezu max korisnik
    #     if max_player:
    #         max_eval = float(-inf)

            #--------------------------------------------------------------------------------------------------

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
        if evaluation.closed_mill(self.current_state, self.state_before, "PLAYER"):
            while True:
                user_input = input("Unesite polje sa kojeg želite da skinete figuru: ")
                try:
                    user_input = int(user_input)
                    if self.current_state.get_value(user_input) == State.AI:
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
        self.max()


            
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
        while True:
            result, winner = self.current_state.is_end()

            if result == True:
                print("*"*30 + "\n\n" "Pobednik je: " + winner + "!\n\n" + "*"*30)



if __name__ == "__main__":
    game = Game()
    game.play()
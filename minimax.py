from cmath import inf
from state import State

class Game(object):

    __slots__ = ['current_state', 'player_turn']

    def __init__(self):
        self.current_state = None
        self.player_turn = None

    def initialize_game(self):
        self.current_state = State()
        while True:
            is_first = input("Da li želite prvi da igrate?\n(Unesite 'da' ili 'ne'): ")
            if self.check_first_player_input(is_first) == True:
                if is_first.upper() == "DA":
                    self.player_turn = "PLAYER"
                else:
                    self.player_turn = "AI"
                break
            else:
                print("Unos nije dobar!")
                continue

    def check_first_player_input(self, txt):
        if txt.upper() == "DA" or txt.upper() == "NE":
            return True
        else:
            return False


    def minimax(self, depth, alpha, beta, max_player):

        eval = self.current_state.eval()    #TO DO: Namestiti eval funkciju u state-u

        result, winner = self.current_state.is_end()
        if depth == 0 or result == True:
            return eval, winner

        #Ako je na potezu max korisnik
        if max_player:
            max_eval = float(-inf)

            #--------------------------------------------------------------------------------------------------

    def play(self):
        self.initialize_game(self)

if __name__ == "__main__":
    game = Game()
# from state import State
#Heuristika
# 1 - Closed Morris: 1 if a morris was closed in the last move by the player
#     (and an opponent’s piece should be grabbed in this move),
#     -1 if a morris was closed by the opponent in the last move, 0 otherwise
# 2 - Number of Morrises: Difference between the number of yours and yours opponent’s morrises
# 3 - Number of blocked opponent pieces: Difference between the number of yours opponent’s and yours blocked pieces (pieces which don’t have an empty adjacent point)
# 4 - Number of pieces: Difference between the number of yours and yours opponent’s pieces
# 5 - Number of 2 piece configurations: Difference between the number of yours and yours opponent’s 2 piece configurations 
#     (A 2-piece configuration is one to which adding one more piece would close a morris)
# 6 - Number of 3-piece configurations: Difference between the number of yours and yours opponent’s 3 piece configurations
#     (A 3-piece configuration is one to which a piece can be added in which one of two ways to close a morris)
# 7 - Double morris: Difference between number of yours and yours opponent’s double morrises 
#     (A double morris is one in which two morrises share a common piece)
# 8 - Winning configuration: 1 if the state is winning for the player, -1 if losing, 0 otherwise


def change_player(state,player):
    if player == state.PLAYER:
        return state.AI
    else:
        return state.PLAYER

def are_there_non_mill_figures(state,player):
    for i in range(0,24):
        if not is_mill(state,player,i): #Cim naidje na jednu figuru koja nije u mici prekida pretragu
            return True
    return False


#HEURISTIKA 1
#Proverava da li je igrac napravio micu u odnosu na prosli potez
#Ako je igrac namestio micu vraca 1, ako je protivnik onda vraca -1, u suprotnom 0
def closed_mill(state, state_before):
    # enemy = change_player(state,player)
    
    mills_before = count_mills(state_before, state.AI)
    mills_now = count_mills(state, state.AI)

    enemy_mills_before = count_mills(state_before, state.PLAYER)
    enemy_mills_now = count_mills(state, state.PLAYER)

    if mills_now > mills_before:
        return 1
    elif enemy_mills_now > enemy_mills_before:
        return -1
    else:
        return 0


#Proverava da li je spojen mill na odredjenoj poziciji 
def is_mill(state,player,index):       
    mills = state.MILLS_BY_INDEX
    possible_mills = mills[index]

    for mill in possible_mills:
        count = 0
        for i in mill:
            if state.get_value(i) == player:
                count += 1
        if count == 3: #spojen mill
            # state.num_of_mills[player] += 1 #Ako je formiran mill povecavam broj millova
            return True         
    return False


#Broji koliko ima mica odredjeni igrac i vraca tu vrednost
def count_mills(state, player):
    mills = 0
    for mill in state.SINGLE_MILLS:
        count = 0
        for i in mill:
            if state.get_value(i) != "X":
                if state.get_value(i) == player:
                    count += 1    
        if count == 3:
            mills += 1       
    return mills



#HEURISTIKA 2
#Razlika u broju formiranih morissa
def mill_diff(state):
        return count_mills(state, state.AI) - count_mills(state, state.PLAYER)


#HEURISTIKA 3
#Broj blokiranih figura - vraca vrednost AI, PLAYER
def blocked_figures(state):
    blocked = {state.AI : 0, state.PLAYER: 0}
    for i in range(0,24):
        if state.get_value(i) != "X":
            flag = 1    #FLAG da li je blokirana figura (na pocetku stasvljam da jeste)
            checking_figure = state.get_value(i)

            for neighbour in state.NEIGHBOURS[i]:
                if state.get_value(neighbour) == "X":
                    flag = 0
                    break

            if flag == 1:
                blocked[checking_figure] += 1

    return blocked[state.AI], blocked[state.PLAYER]

def diff_blocked_figures(state):
    white_blocked, black_blocked = blocked_figures(state)
    return black_blocked - white_blocked 


#HEURISTIKA 4
#Razlika u broju figura na tabli
def figures_diff(state):
        return state.white_figures - state.black_figures


#HEURISTIKA 5
#Razlika broja konfiguracija od 2 figure
#(A 2-piece configuration is one to which adding one more piece would close a morris)
def num_of_2_piece_config(state,player):
    two_piece_config = 0
    for mill in state.SINGLE_MILLS:
        count_free = 0
        count_player = 0
        for i in mill:
            if state.get_value(i) == player:
                count_player += 1
            elif state.get_value(i) == "X":
                count_free += 1
        if count_player == 2 and count_free == 1:
            two_piece_config += 1
    return two_piece_config

def diff_two_piece_config(state):
    return num_of_2_piece_config(state,state.AI) - num_of_2_piece_config(state,state.PLAYER)


#HEURISTIKA 6
#Razlika broja konfiguracija od 3 figure
#(A 3-piece configuration is one to which a piece can be added in which one of two ways to close a morris)
def num_of_3_piece_config(state,player):
    three_piece_config = 0
    for mill in state.CONNECTORS:
        if mill[0] == mill[1] == mill[2] == player:
            if mill[3] == mill[4] == "X":
                three_piece_config += 1
    return three_piece_config

def diff_three_piece_config(state):
    return num_of_3_piece_config(state,state.AI) - num_of_3_piece_config(state,state.PLAYER)
    

#HEURISTIKA 7
#Razlika u broju duplih mica
def num_of_double_mills(state,player):
    double_mills = 0
    for mill in state.DOUBLE_MILLS:
        flag = 1
        for i in mill:
            if state.get_value(i) != player:
                flag = 0
        if flag:
            double_mills += 1
    return double_mills

def diff_double_mills(state):
    return num_of_double_mills(state,state.AI) - num_of_double_mills(state,state.PLAYER)


#HEURISTIKA 8
#Pobednicka konfiguracija (1 ako je pobeda, -1 poraz, u suprotnom 0)
def winning_configuration(state):
    result,winner = state.is_end()
    if result:
        if winner == state.AI:
            return 1
        else:
            return -1
    else:
        return 0

def eval(state, state_before, phase):

    if phase == 1:    #18 26 1 6 21 7
        evaluation = \
            18 * closed_mill(state, state_before) + \
            26 * mill_diff(state) + \
            1 * diff_blocked_figures(state) + \
            6 * figures_diff(state) + \
            21 * diff_two_piece_config(state) + \
            7 * diff_three_piece_config(state)
    return evaluation



if __name__ == "__main__":
    pass
    # state = State()
    # state.set_value(0, state.PLAYER)
    # state.set_value(1, state.AI)
    # state.set_value(3, state.AI)
    # state.set_value(2, state.PLAYER)
    # state.set_value(4, state.PLAYER)
    # state.set_value(7, state.PLAYER)
    # print(state)
    # ismill = is_mill(state,7)
    # print("Da li je mill:",ismill)
    # print("Broj formiranih millova:", state.num_of_mills)
    # print("Vrednost za razliku millova:", mill_difference(state))
    # print("Vrednost za blokirane figure", blocked_figures(state))

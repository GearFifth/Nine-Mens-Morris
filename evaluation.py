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
# 8 - Opened Morris: Difference between number of yours and yours opponent's opened morrises
#     (An open morris is one in which 1 piece is missing and it is at the node nearby)
# 9 - Winning configuration: 1 if the state is winning for the player, -1 if losing, 0 otherwise


def change_player(state,player):
    if player == state.PLAYER:
        return state.AI
    else:
        return state.PLAYER

def are_there_non_mill_figures(state,player):
    for i in range(0,24):
        if state.get_value(i) == player:
            if not is_mill(state,player,i): #Cim naidje na jednu figuru koja nije u mici prekida pretragu
                return True
        else: 
            continue
    return False


#HEURISTIKA 1
#Proverava da li je igrac napravio micu u odnosu na prosli potez
#Ako je igrac namestio micu vraca 1, ako je protivnik onda vraca -1, u suprotnom 0
def closed_mill(state, state_before):
    # enemy = change_player(state,player)
    
    mills_before = get_list_of_mills(state_before, state.AI)
    mills_now = get_list_of_mills(state, state.AI)

    enemy_mills_before = get_list_of_mills(state_before, state.PLAYER)
    enemy_mills_now = get_list_of_mills(state, state.PLAYER)

    for mill in mills_now:
        if mill not in mills_before:
            return 1

    for mill in enemy_mills_now:
        if mill not in enemy_mills_before:
            return -1

    return 0

    # if len(mills_now) > len(mills_before):
    #     return 1
    # elif len(enemy_mills_now) > len(enemy_mills_before):
    #     return -1
    # else:

    #     return 0

def get_list_of_mills(state,player):
    mills = []
    for mill in state.SINGLE_MILLS:
        count = 0
        for i in mill:
            if state.get_value(i) != "X":
                if state.get_value(i) == player:
                    count += 1    
        if count == 3:
            mills.append(mill)      
    return mills

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
# def num_of_double_mills(state,player):
#     double_mills = 0
#     for mill in state.DOUBLE_MILLS:
#         flag = 1
#         for i in mill:
#             if state.get_value(i) != player:
#                 flag = 0
#         if flag:
#             double_mills += 1
#     return double_mills

# def diff_double_mills(state):
#     return num_of_double_mills(state,state.AI) - num_of_double_mills(state,state.PLAYER)

def num_of_double_mills(state,player):
    print(state)
    double_mills = 0
    for mill in state.SINGLE_MILLS:
        flag = 1
        for i in mill:
            if state.get_value(i) != player:
                flag = 0
                break
        if flag:
            for i in mill:
                for neighbour in state.NEIGHBOURS[i]:
                    if state.get_value(neighbour) == "X":
                        state.set_value(neighbour, player)
                        state.set_value(i, "X")

                        if is_mill(state,player,neighbour):
                            double_mills += 1

                        #Vratim kako je bilo
                        state.set_value(i, player)
                        state.set_value(neighbour, "X")                
    return double_mills

def diff_double_mills(state):
    return num_of_double_mills(state,state.AI) - num_of_double_mills(state,state.PLAYER)


#HEURISTIKA 8
#Razlika u broju otvorenih mica
#(An open morris is one in which 1 piece is missing and it is at the node nearby)
def num_of_opened_mills(state,player):
    opened_mills = 0
    for mill in state.SINGLE_MILLS:
        player_figures = 0
        empty_node = 0
        empty_index = None
        for i in mill:
            if state.get_value(i) == player:
                player_figures += 1
            elif state.get_value(i) == "X":
                empty_node += 1
                empty_index = i
            else:
                continue
        if player_figures == 2 and empty_node == 1:
            for neighbour in state.NEIGHBOURS[empty_index]:
                if state.get_value(neighbour) == player:
                    opened_mills += 1
                    break
    return opened_mills


def opened_mills_diff(state):
    return num_of_opened_mills(state, state.AI) - num_of_opened_mills(state, state.PLAYER) 


#HEURISTIKA 9
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

    if phase == 1:    #18 26 1 6 12 7 
        evaluation = \
            18 * closed_mill(state, state_before) + \
            26 * mill_diff(state) + \
            1 * diff_blocked_figures(state) + \
            6 * figures_diff(state) + \
            12 * diff_two_piece_config(state) + \
            7 * diff_three_piece_config(state)
    elif phase == 2:    #14 43 10 8 7 42 1086 
        evaluation = \
            14 * closed_mill(state, state_before) + \
            43 * mill_diff(state) + \
            10 * diff_blocked_figures(state) + \
            8 * figures_diff(state) + \
            7 * opened_mills_diff(state) + \
            42 * diff_double_mills(state) + \
            1086 * winning_configuration(state)
            
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

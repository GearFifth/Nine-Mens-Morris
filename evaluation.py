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


# MILL_VAL = 50
# DOUBLE_MILL_VAL = 100
# MILL_DIFF_VAL = 20
# BLOCKED_DIFF_VAL = 20

#Broji koliko ima mica odredjeni igrac i vraca tu vrednost
def count_mills(state, player):
    count = 0
    mills = 0
    for mill in state.SINGLE_MILLS:
        for i in mill:
            if state.get_value(i) != "X":
                if state.get_value(i) == player:
                    count += 1    
        if count == 3:
            mills += 1       
    return mills



#Proverava da li je igrac napravio micu u odnosu na prosli potez
def closed_mill(state, state_before, player):
    mills_before = count_mills(state_before, player)
    mills_now = count_mills(state, player)
    if mills_now > mills_before:
        return True
    else:
        return False


#Proverava da li je spojen mill na odredjenoj poziciji 
def is_mill(state,index):       
    player = None
    figure = state.board[index]
    if figure == "X":
        return False
    elif figure == "⚪":
        player = "AI"
    elif figure == "⚫":
        player = "PLAYER"

    mills = state.MILLS_BY_INDEX
    possible_mills = mills[index]
    count = 0

    for mill in possible_mills:
        for node in mill:
            if state.board[node] == figure:
                count += 1
        if count == 3: #spojen mill
            state.num_of_mills[player] += 1 #Ako je formiran mill povecavam broj millova
            return True         

    return False

#Razlika u broju formiranih morissa
def mill_difference(state):
    diff =  state.num_of_mills["PLAYER"] - state.num_of_mills["AI"]
    return diff

#Broj blokiranih figura - vraca vrednost AI, PLAYER
def blocked_figures(state):
    blocked = {"AI" : 0, "PLAYER": 0}
    for i in range(0,24):
        if state.board[i] != "X":
            flag = 1    #FLAG da li je blokirana figura (na pocetku stasvljam da jeste)
            checking_figure = state.board[i]
            if checking_figure == "⚪":
                player = "AI"
            else:
                player = "PLAYER"

            for neighbour in state.NEIGHBOURS[i]:
                if player == "AI":
                    if state.board[neighbour] != "⚫":
                        flag = 0
                        break
                else:
                    if state.board[neighbour] != "⚪":
                        flag = 0
                        break

            if flag == 1:
                blocked[player] += 1

    return blocked["AI"], blocked["PLAYER"]

# def eval(State,index):
#     if State.phase == 1:
#         evaluation = is_mill(State,index) + 



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

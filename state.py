import time
import copy
import evaluation

class State(object):
    AI = "⚪"
    PLAYER = "⚫"

    NEIGHBOURS = {
        0: [1,3], 1: [0,2,9], 2: [1,4], 3: [0,5,11],
        4: [2,7,12], 5: [3,6], 6: [5,7,14], 7: [4,6],
        8: [9,11], 9: [1,8,10,17], 10: [9,12], 11: [3,8,13,19],
        12: [4,10,15,20], 13: [11,14], 14: [6,13,15,22], 15: [12,14],
        16: [17,19], 17: [9,16,18], 18: [17,20], 19: [11,16,21],
        20: [12,18,23], 21: [19,22], 22: [14,21,23], 23: [20,22]
    }

    MILLS_BY_INDEX = {
        0: [[0,1,2], [0,3,5]],
        1: [[0,1,2], [1,9,17]],
        2: [[0,1,2], [2,4,7]],
        3: [[0,3,5], [3,11,19]],
        4: [[2,4,7], [4,12,20]],
        5: [[0,3,5], [5,6,7]],
        6: [[5,6,7], [6,14,22]],
        7: [[2,4,7], [5,6,7]],
        9: [[1,9,17], [8,9,10]],
        10: [[8,9,10], [10,12,15]],
        11: [[3,11,19], [8,11,13]],
        12: [[4,12,20], [10,12,15]],
        13: [[8,11,13], [13,14,15]],
        14: [[6,14,22], [13,14,15]],
        15: [[13,14,15], [10,12,15]],
        16: [[16,17,18], [16,19,21]],
        17: [[1,9,17], [16,17,18]],
        18: [[16,17,18], [18,20,23]],
        19: [[3,11,19], [16,19,21]],
        20: [[4,12,20], [18,20,23]],
        21: [[16,19,21], [21,22,23]],
        22: [[6,14,22], [21,22,23]],
        23: [[21,22,23], [18,20,23]],
    }

    SINGLE_MILLS = (
        [0,1,2], [0,3,5], [5,6,7], [2,4,7],
        [8,9,10], [8,11,13], [13,14,15], [10,12,15],
        [16,19,21], [16,17,18], [21,22,23], [18,20,23],
        [1,9,17], [3,11,19], [6,14,22], [4,12,20]
    )

    DOUBLE_MILLS = (
        [1,2,4,0,7], [4,7,6,2,5], [6,5,3,7,0], [3,0,1,5,2],
        [9,10,12,8,15], [12,15,14,10,13], [14,13,11,15,8], [11,8,9,13,10],
        [17,18,20,16,23], [20,23,22,18,21], [22,21,19,23,16], [19,16,17,21,18],
        [0,1,2,9,17], [2,4,7,12,20], [7,6,5,14,22], [5,3,0,11,19],
        [8,9,10,1,17], [10,12,15,4,20], [15,14,13,22,6], [13,11,8,3,19],
        [16,17,18,1,9], [18,20,23,12,4], [23,22,21,14,6], [16,19,21,11,3]
        )

    CONNECTORS = (
        [1,2,4,0,7], [4,7,6,2,5], [6,5,3,7,0], [3,0,1,5,2],
        [9,10,12,8,15], [12,15,14,10,13], [14,13,11,15,8], [11,8,9,13,10],
        [17,18,20,16,23], [20,23,22,18,21], [22,21,19,23,16], [19,16,17,21,18],
        [0,1,9,17,2], [2,1,9,17,0], [2,4,12,20,7], [7,4,12,20,2],
        [7,6,14,22,5], [5,6,14,22,7], [5,3,11,19,0], [0,3,11,19,5],
        [8,9,1,17,10], [8,9,17,1,10], [10,9,1,17,8], [10,9,17,1,8],
        [10,12,20,4,15], [10,12,4,20,15], [15,12,20,4,10], [15,12,4,20,10],
        [15,14,22,6,13], [15,14,6,22,13], [13,14,22,6,15], [13,14,6,22,15],
        [13,11,19,3,8], [13,11,3,19,8], [8,11,19,3,13], [8,11,3,19,13],
        [16,17,9,1,18], [18,17,9,1], [18,20,12,4,23], [23,20,12,18,4],
        [23,22,14,6,21], [21,22,14,23,6], [21,19,11,3,16], [16,19,11,21,3],
    )

    num_of_mills = {"PLAYER": 0, "AI": 0}

    def __init__(self):
        self.board = []
        for i in range(0, 24):
            self.board.append('X')
        self.black_figures = 9      #PLAYER
        self.white_figures = 9      #AI

    def get_value(self, i):
        return self.board[int(i)]

    def set_value(self, i, value):
        self.board[int(i)] = value

    def is_move_valid(self, i):
        try:
            i = int(i)
        except:
            return False

        if i > 23 or i < 0:
            return False

        if self.board[i] != 'X':
            return False

        return True
    
    
    #Uslovi za kraj - nema mogucih poteza(sve figure blokirane)

    def is_end(self): #vraca format bool, pobednik
        # for i in range(0,24):
        #     if self.board[i] == "⚫":
        #         player += 1
        #     elif self.board[i] == "⚪":
        #         ai += 1
        white_blocked, black_blocked = evaluation.blocked_figures(self)
        if self.white_figures == 2 or self.white_figures == white_blocked:
            return True, "PLAYER"
        elif self.black_figures == 2 or self.black_figures == black_blocked:
            return True, "AI"
        else:
            return False, None      


    def print_node(self,arr,index):
        if index < 10:
            i = "0" + str(index)
        else:
            i = str(index)

        if arr[index] == "X":
            return "X[{}]".format(i)
        else:
            return " {}  ".format(arr[index])


    def __str__(self):
        ret = "\n"*3 + self.print_node(self.board,0) + "-"*22 + self.print_node(self.board,1) + "-"*22 + self.print_node(self.board,2) \
            + "\n" + "  |" + " "*26 + "|" + " "*26 + "|" \
            + "\n" + "  |" + " "*5 + self.print_node(self.board,8) + "-"*14 + self.print_node(self.board,9) + "-"*14 + self.print_node(self.board,10) + " "*5 + "|" \
            + "\n" + "  |" + " "*7 + "|" + " "*18 + "|" + " "*18 + "|" + " "*7 + "|" \
            + "\n" + "  |" + " "*7 + "|" + " "*18 + "|" + " "*18 + "|" + " "*7 + "|" \
            + "\n" + "  |" + " "*7 + "|" + " "*6 + self.print_node(self.board,16) + "-"*5 + self.print_node(self.board,17) + "-"*5 + self.print_node(self.board,18) + " "*6 + "|" + " "*7 + "|"  \
            + "\n" + "  |" + " "*7 + "|" + " "*8 + "|" + " "*19 + "|" + " "*8 + "|" + " "*7 + "|" \
            + "\n" + "  |" + " "*7 + "|" + " "*8 + "|" + " "*19 + "|" + " "*8 + "|" + " "*7 + "|" \
            + "\n" + self.print_node(self.board,3) + "-"*3 + self.print_node(self.board,11) + "-"*4 + self.print_node(self.board,19) + " "*15 + self.print_node(self.board,20) + "-"*4 + self.print_node(self.board,12) + "-"*3 + self.print_node(self.board,4) \
            + "\n" + "  |" + " "*7 + "|" + " "*8 + "|" + " "*19 + "|" + " "*8 + "|" + " "*7 + "|" \
            + "\n" + "  |" + " "*7 + "|" + " "*8 + "|" + " "*19 + "|" + " "*8 + "|" + " "*7 + "|" \
            + "\n" + "  |" + " "*7 + "|" + " "*6 + self.print_node(self.board,21) + "-"*5 + self.print_node(self.board,22) + "-"*5 + self.print_node(self.board,23) + " "*6 + "|" + " "*7 + "|"  \
            + "\n" + "  |" + " "*7 + "|" + " "*18 + "|" + " "*18 + "|" + " "*7 + "|" \
            + "\n" + "  |" + " "*7 + "|" + " "*18 + "|" + " "*18 + "|" + " "*7 + "|" \
            + "\n" + "  |" + " "*5 + self.print_node(self.board,13) + "-"*14 + self.print_node(self.board,14) + "-"*14 + self.print_node(self.board,15) + " "*5 + "|" \
            + "\n" + "  |" + " "*26 + "|" + " "*26 + "|" \
            + "\n" + self.print_node(self.board,5) + "-"*22 + self.print_node(self.board,6) + "-"*22 + self.print_node(self.board,7) + "\n"
        return ret

if __name__ == "__main__":
    state = State()
    # state.set_value(0,state.AI)
    # state.set_value(9,state.PLAYER)
    # state.set_value(8,state.PLAYER)
    # state.set_value(15,state.PLAYER)
    # state.set_value(10,state.PLAYER)
    # state.set_value(17,state.AI)
    # state.set_value(14,state.AI)
    # state.set_value(11,state.AI)
    # print(state.is_move_valid(25))
    print(state)   

    # start_time1 = time.time()
    # count = 0
    # for mill in state.CONNECTORS:
    #     for i in mill:
    #         if i == state.AI:
    #             count += 1
    # print("--- %s seconds ---" % (time.time() - start_time1))
    
    # start_time = time.time()
    # for i in range (0,100):
    #     new_state = copy.deepcopy(state)
    # print("--- %s seconds ---" % (time.time() - start_time))
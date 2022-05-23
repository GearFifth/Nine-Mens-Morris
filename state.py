class State(object):
    AI = "⚪"
    PLAYER = "⚫"
    FIELDS_AROUND = {
        0: [1,2], 1: [0,2,9], 2: [1,4], 3: [0,5,11],
        4: [2,7,12], 5: [3,6], 6: [5,7,14], 7: [4,6],
        8: [9,11], 9: [1,8,10,17], 10: [9,12], 11: [3,8,13,19],
        12: [4,10,15,20], 13: [11,14], 14: [6,13,15,22], 15: [12,14],
        16: [17,19], 17: [9,16,18], 18: [17,20], 19: [11,16,21],
        20: [12,18,23], 21: [19,22], 22: [14,21,23], 23: [20,22]
    }

    def __init__(self):
        self.board = []
        for i in range(0, 24):
            self.board.append('X')

    def get_value(self, i):
        return self.board[i]

    def set_value(self, i, value):
        self.board[i] = value

    def is_move_valid(self, i, value):
        value = value.upper()
        if i > 23 or i < 0:
            return False

        if value not in "12":
            return False

        if self.board[i] != 'X':
            return False

        return True
    
    def is_end(self): #vraca format bool, pobednik
        player = 0
        ai = 0
        for i in range(0,24):
            if self.board[i] == "⚫":
                player += 1
            elif self.board[i] == "⚪":
                ai += 1
        if ai == 2:
            return True, "PLAYER"
        elif player == 2:
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
            + "\n" + self.print_node(self.board,5) + "-"*22 + self.print_node(self.board,6) + "-"*22 + self.print_node(self.board,7) + "\n"*3

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
    # print(state.is_move_valid(25,"x"))
    print(state)
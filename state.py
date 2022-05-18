class State(object):

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
    
    def is_end(self): #Treba da dodam
        pass

    def print_node(self,arr,index):
        if index < 10:
            i = "0" + str(index)
        else:
            i = str(index)

        if arr[index] == "X":
            return "X[{}]".format(i)
        else:
            return "  {}  ".format(arr[index])


    def __str__(self):
        ret = "\n"*3 + self.print_node(self.board,0) + "-"*22 + self.print_node(self.board,1) + "-"*22 + self.print_node(self.board,2) \
            + "\n" + "  |" + " "*26 + "|" + " "*26 + "|" \
            + "\n" + "  |" + " "*5 + self.print_node(self.board,8) + "-"*14 + self.print_node(self.board,9) + "-"*14 + self.print_node(self.board,10) + " "*5 + "|" \
            + "\n" + "  |" + " "*7 + "|" + " "*18 + "|" + " "*18 + "|" + " "*7 + "|" \
            + "\n" + "  |" + " "*7 + "|" + " "*18 + "|" + " "*18 + "|" + " "*7 + "|" \
            + "\n" + "  |" + " "*7 + "|" + " "*6 + self.print_node(self.board,16) + "-"*5 + self.print_node(self.board,17) + "-"*5 + self.print_node(self.board,18) + " "*6 + "|" + " "*7 + "|"  \
            + "\n" + "  |" + " "*7 + "|" + " "*8 + "|" + " "*19 + "|" + " "*8 + "|" + " "*7 + "|" \
            + "\n" + "  |" + " "*7 + "|" + " "*8 + "|" + " "*19 + "|" + " "*8 + "|" + " "*7 + "|" \
            + "\n" + self.print_node(self.board,3) + "-"*3 + self.print_node(self.board,11) + "-"*4 + self.print_node(self.board,19) + " "*15 + self.print_node(self.board,20) + "-"*4 + self.print_node(self.board,21) + "-"*3 + self.print_node(self.board,22) \
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
    state.set_value(0,"P")
    state.set_value(9,"C")
    state.set_value(17,"P")
    # print(state.is_move_valid(25,"x"))
    print(state)
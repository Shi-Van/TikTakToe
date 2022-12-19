from random import randint

win_lines = (
    (0, 1, 2), (3, 4, 5), (6, 7, 8),  # horizontals
    (0, 3, 6), (1, 4, 7), (2, 5, 8),  # verticals
    (0, 4, 8), (2, 4, 6)  # diagonals
)


class TikTakToe:
    decode = {0: '.', 1: 'X', 2: 'O'}

    def __init__(self):
        self.board = [
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0]
        ]
        player1, player2, level = get_players()
        self.pl1 = player1
        self.pl2 = player2
        self.who = {player1.sign: player1, player2.sign: player2}
        self.moves_num = 0
        self.high_level = level

    def run(self):
        win = 0
        sign = None
        while not win:
            self.new_move()
            win, sign = self.win()
        if win == 1:
            self.show_board()
            print(self.who[sign].name, ' won!')
        else:
            self.show_board()
            print('Draw')

    def show_board(self):
        for line in self.board:
            print(" ".join(map(lambda x: self.decode[x], line)))

    def win(self):
        for line in win_lines:
            # first, second and third elements in line
            first, second, third = get_el_from_line(line, self)
            if first == second == third != 0:
                # 1 -- win
                return [1, first]
        if self.moves_num == 9:
            # 2 -- draw
            return [2, -1]
        # 0 -- nothing
        return [0, -1]

    def check_move(self, x, y):
        if x < 0 or x > 2 or y < 0 or y > 2:
            return 1  # Invalid input format
        if self.board[x][y] != 0:
            return 2  # The field is taken
        return 0  # OK

    def new_move(self):
        self.moves_num += 1
        cur_player = self.pl1 if self.moves_num % 2 else self.pl2
        x, y, sign = cur_player.get_move(self)
        self.board[x][y] = sign


class Player:
    def __init__(self, first, name):
        self.name = name
        if first:
            self.sign = 1
        else:
            self.sign = 2

    def get_move(self, board):
        board.show_board()
        print(f'{self.name}, make a move: ', end='')
        while True:
            try:
                x, y = map(int, input().split())
                check = board.check_move(x - 1, y - 1)
                if not check:
                    return [x - 1, y - 1, self.sign]
                elif check == 2:
                    print('The field is taken: ', end='')
                else:
                    print('Invalid input format: ', end='')
            except ValueError:
                print('Invalid input format: ', end='')


class SuperPlayer(Player):
    def __init__(self, first, mode):
        super().__init__(first, 'bot')
        if mode == 3:
            self.get_move = self.get_move_hard_mode
        elif mode == 2:
            self.get_move = self.get_move_medium_mode
        else:
            self.get_move = self.get_move_easy_mode

    def get_move_easy_mode(self, board):
        x, y = randint(0, 2), randint(0, 2)
        while board.check_move(x, y):
            x, y = randint(0, 2), randint(0, 2)
        return [x, y, self.sign]

    def get_move_medium_mode(self, board):
        next_move = (-1, -1)
        for i in range(3):
            for j in range(3):
                if self.next_move_win(board, i, j, self.sign):
                    next_move = (i, j)
        if next_move != (-1, -1):
            return [*next_move, self.sign]
        for i in range(3):
            for j in range(3):
                if self.next_move_win(board, i, j, 3 - self.sign):
                    next_move = (i, j)
        if next_move != (-1, -1):
            return [*next_move, self.sign]
        return self.get_move_easy_mode(board)

    def next_move_win(self, board, i, j, sign):
        ans = False
        if board.board[i][j] == 0:
            board.board[i][j] = sign
            if board.win()[0] == 1:
                board.board[i][j] = 0
                ans = True
            board.board[i][j] = 0
        return ans

    def get_move_hard_mode(self, board):
        if board.moves_num == 1:
            return [0, 0, self.sign]
        board.moves_num -= 1
        end, xy = self.move_to_win(True, board)
        board.moves_num += 1
        return [xy[0], xy[1], self.sign]

    def move_to_win(self, bot, board):
        win, sign = board.win()
        if win == 2:
            return 3, (-1, -1)
        elif win == 1:
            return 1 + int(self.sign == sign), (-1, -1)
        # end 2 - bot wins, 1 - bot loses, 3 - draw
        end = {1: 0, 2: 0, 3: 0}
        for i in range(3):
            for j in range(3):
                if board.board[i][j] == 0:
                    board.moves_num += 1
                    board.board[i][j] = (board.moves_num + 1) % 2 + 1
                    e, x = self.move_to_win(not bot, board)
                    end[e] = (i, j)
                    board.board[i][j] = 0
                    board.moves_num -= 1
        if bot:
            # happy end for bot
            if end[2] != 0:
                return 2, end[2]
            if end[3] != 0:
                return 3, end[3]
            return 1, end[1]
        else:
            # happy end for player
            if end[1] != 0:
                return 1, end[1]
            if end[3] != 0:
                return 3, end[3]
            return 2, end[2]


def get_players():
    name1 = input("Enter your name: ")

    print(f"OK, {name1}\nDo you want to play first or second?")
    order = input_num([1, 2])

    print("A game for one or two?")
    x = input_num([1, 2])

    first_player = Player(order % 2, name1)
    if x == 2:
        name2 = input("Second player, enter your name: ")
        second_player = Player(not order % 2, name2)
    else:
        print("Easy, medium or hard mode?")
        mode = input_num([1, 2, 3])

        second_player = SuperPlayer(not order % 2, mode)
    if order % 2:
        return first_player, second_player, True
    else:
        return second_player, first_player, True


def input_num(numbers):
    x = ''
    numbers = list(map(str, numbers))
    while x not in numbers:
        x = input(f"Enter {', '.join(numbers[:-1])} or {numbers[-1]}: ")
    x = int(x)
    return x


def get_el_from_line(line, b):
    first, second, third = line
    first = b.board[first % 3][first // 3]
    second = b.board[second % 3][second // 3]
    third = b.board[third % 3][third // 3]
    return first, second, third


if __name__ == '__main__':
    game = TikTakToe()
    game.run()

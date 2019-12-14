from typing import Callable, Optional
from bot import UserHandler
from tictactoe import Player, TicTacToe


class TicTacToeUserHandler(UserHandler):
    def __init__(self, send_message: Callable[[str], None]) -> None:
        super(TicTacToeUserHandler, self).__init__(send_message)
        self.game: Optional[TicTacToe] = None

    def handle_message(self, message: str) -> None:
        message = message.strip()
        if message == 'start':
            self.start_game()
            return
        if self.game is None:
            self.send_message('Game is not started')
            return
        row, col, player = message.split()
        self.make_turn(Player.X if player == 'X' else Player.O, row=int(row), col=int(col))

    def start_game(self) -> None:
        self.game = TicTacToe()
        self.send_field()

    def make_turn(self, player: Player, *, row: int, col: int) -> None:
        assert self.game is not None
        if not self.game.can_make_turn(player, row=row, col=col):
            self.send_message('Invalid turn')
            return
        self.game.make_turn(player, row=row, col=col)
        self.send_field()
        if self.game.is_finished():
            if self.game.winner() == Player.X:
                self.send_message('Game is finished, X wins')
            elif self.game.winner() == Player.O:
                self.send_message('Game is finished, O wins')
            elif not self.game.winner():
                self.send_message('Game is finished, draw')
            self.game = None

    def send_field(self) -> None:
        assert self.game
        field = ''
        for col in self.game.field:
            for row in col:
                if row is None:
                    field += '.'
                if row == Player.X:
                    field += 'X'
                if row == Player.O:
                    field += 'O'
            field += '\n'
        self.send_message(field.strip('\n'))

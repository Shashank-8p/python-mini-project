import pygame

SQUARE_WIDTH = 90


class Renderer:
    def __init__(self, input_handler, board, loader):
        self.board = board
        self.input_handler = input_handler
        self.loader = loader
        self.loader.load_pieces()
        self.loader.convert()

    def render_board(self, screen):

        for row in range(8):
            for col in range(8):

                x = col * SQUARE_WIDTH
                y = row * SQUARE_WIDTH

                if (row + col) % 2 == 0:
                    screen.blit(
                        self.loader.board_pieces["white"],
                        (x, y)
                    )
                else:
                    screen.blit(
                        self.loader.board_pieces["black"],
                        (x, y)
                    )

    def render_pieces(self, screen):

        for row in range(8):
            for col in range(8):

                square = self.board.convert_index_to_square(
                    col * SQUARE_WIDTH,
                    row * SQUARE_WIDTH
                )

                piece = self.board.get_piece_in_square(square)

                if piece is None:
                    continue

                x = col * SQUARE_WIDTH
                y = row * SQUARE_WIDTH

                piece_symbol = piece.symbol()

                # White pieces
                if piece_symbol == "P":
                    screen.blit(self.loader.white_pieces["pawn"], (x, y))

                elif piece_symbol == "R":
                    screen.blit(self.loader.white_pieces["rook"], (x, y))

                elif piece_symbol == "N":
                    screen.blit(self.loader.white_pieces["knight"], (x, y))

                elif piece_symbol == "B":
                    screen.blit(self.loader.white_pieces["bishop"], (x, y))

                elif piece_symbol == "Q":
                    screen.blit(self.loader.white_pieces["queen"], (x, y))

                elif piece_symbol == "K":
                    screen.blit(self.loader.white_pieces["king"], (x, y))

                # Black pieces
                elif piece_symbol == "p":
                    screen.blit(self.loader.black_pieces["pawn"], (x, y))

                elif piece_symbol == "r":
                    screen.blit(self.loader.black_pieces["rook"], (x, y))

                elif piece_symbol == "n":
                    screen.blit(self.loader.black_pieces["knight"], (x, y))

                elif piece_symbol == "b":
                    screen.blit(self.loader.black_pieces["bishop"], (x, y))

                elif piece_symbol == "q":
                    screen.blit(self.loader.black_pieces["queen"], (x, y))

                elif piece_symbol == "k":
                    screen.blit(self.loader.black_pieces["king"], (x, y))

    def highlight_square(self, screen):

        square = self.input_handler.selected

        if square is None:
            return

        row, col = self.board.square_to_index(square)

        highlight_surf = pygame.Surface(
            (SQUARE_WIDTH, SQUARE_WIDTH),
            pygame.SRCALPHA
        )

        highlight_surf.fill((255, 255, 0, 100))

        screen.blit(
            highlight_surf,
            (col * SQUARE_WIDTH, row * SQUARE_WIDTH)
        )

        # Highlight legal moves
        if self.input_handler.valid_moves:

            for move in self.input_handler.valid_moves:

                dest_row, dest_col = self.board.square_to_index(move)

                center_x = (
                    dest_col * SQUARE_WIDTH
                    + SQUARE_WIDTH // 2
                )

                center_y = (
                    dest_row * SQUARE_WIDTH
                    + SQUARE_WIDTH // 2
                )

                radius = SQUARE_WIDTH // 6

                circle_surf = pygame.Surface(
                    (radius * 2, radius * 2),
                    pygame.SRCALPHA
                )

                pygame.draw.circle(
                    circle_surf,
                    (0, 100, 255, 120),
                    (radius, radius),
                    radius
                )

                screen.blit(
                    circle_surf,
                    (center_x - radius, center_y - radius)
                )

    def display_winner(self, screen):

        game_board = self.board.board

        if game_board.is_checkmate():

            if game_board.turn:
                message = "BLACK WINS!"
            else:
                message = "WHITE WINS!"

        elif game_board.is_stalemate():
            message = "STALEMATE"

        elif game_board.is_insufficient_material():
            message = "DRAW"

        else:
            return

        overlay = pygame.Surface((720, 720))
        overlay.set_alpha(180)
        overlay.fill((0, 0, 0))
        screen.blit(overlay, (0, 0))

        font = pygame.font.SysFont(None, 80)

        text = font.render(
            message,
            True,
            (255, 255, 255)
        )

        text_rect = text.get_rect(
            center=(360, 360)
        )

        screen.blit(text, text_rect)

    def draw(self, screen):

        self.render_board(screen)

        self.highlight_square(screen)

        self.render_pieces(screen)

        self.display_winner(screen)

        pygame.display.flip()

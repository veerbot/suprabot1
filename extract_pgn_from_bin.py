# extract_pgn_from_bin.py

import chess
import chess.pgn
from chess.polyglot import open_reader

book_path = "engines/OPTIMUS2502.bin"
output_pgn = "engines/OPTIMUS2502.pgn"

seen_positions = set()
games_written = 0

with open(output_pgn, "w", encoding="utf-8") as pgn_file:
    with open_reader(book_path) as reader:
        for entry in reader:
            board = chess.Board()
            # Play book moves up to this key
            try:
                board.push(entry.move())
            except:
                continue

            fen = board.fen()
            if fen in seen_positions:
                continue
            seen_positions.add(fen)

            game = chess.pgn.Game()
            game.headers["Event"] = "Book Line from OPTIMUS2502.bin"
            game.setup(board)
            node = game.add_main_variation(entry.move())

            print(game, file=pgn_file, end="\n\n")
            games_written += 1

print(f"✅ Extracted {games_written} PGN lines to {output_pgn}")


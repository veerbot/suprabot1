# extract_pgn_from_bin.py
from six.moves import copyreg
from chess.polyglot import open_reader
import chess.pgn
import chess
import os

book_path = "engines/OPTIMUS2502.bin"
output_pgn = "engines/OPTIMUS2502.pgn"

reader = open_reader(book_path)
seen_positions = set()
games_written = 0

with open(output_pgn, "w", encoding="utf-8") as pgn_file:
    for entry in reader:
        board = entry.position()
        fen = board.fen()
        if fen in seen_positions:
            continue
        seen_positions.add(fen)

        move = entry.move()
        board.push(move)
        game = chess.pgn.Game()
        node = game
        node.board().set_fen(entry.position().fen())
        node = node.add_variation(move)
        game.headers["Event"] = "Extracted from OPTIMUS2502.bin"
        print(game, file=pgn_file, end="\n\n")
        games_written += 1

print(f"Extracted {games_written} positions to {output_pgn}")

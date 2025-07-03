# extract_pgn_from_bin.py

import chess
import chess.pgn
from chess.polyglot import open_reader
from collections import defaultdict

book_path = "engines/OPTIMUS2502.bin"
output_pgn = "engines/OPTIMUS2502.pgn"
MAX_DEPTH = 200  # Max moves per line

seen_fens = set()
games_written = 0

def build_lines(book_path, max_depth=20):
    lines = []

    def dfs(board, moves_so_far, depth):
        if depth >= max_depth:
            return
        with open_reader(book_path) as reader:
            entries = list(reader.find_all(board))
        if not entries:
            if moves_so_far:
                lines.append(moves_so_far[:])
            return
        for entry in entries:
            move = entry.move  # ✅ FIXED HERE: no parentheses
            board.push(move)
            dfs(board, moves_so_far + [move], depth + 1)
            board.pop()

    board = chess.Board()
    dfs(board, [], 0)
    return lines

def write_pgn(lines, output_file):
    global games_written
    with open(output_file, "w", encoding="utf-8") as f:
        for line in lines:
            board = chess.Board()
            game = chess.pgn.Game()
            game.headers["Event"] = "Extracted from OPTIMUS2502.bin"
            node = game

            for move in line:
                node = node.add_variation(move)
                board.push(move)

            fen = board.fen()
            if fen in seen_fens:
                continue
            seen_fens.add(fen)

            print(game, file=f, end="\n\n")
            games_written += 1

# === RUN ===
print("⏳ Extracting book lines...")
lines = build_lines(book_path, MAX_DEPTH)
write_pgn(lines, output_pgn)
print(f"✅ Extracted {games_written} PGN games to {output_pgn}")




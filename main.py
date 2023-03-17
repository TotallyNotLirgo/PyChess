from board import Board, convert_position, BoardError
from argparse import ArgumentParser
import logging

parser = ArgumentParser()
parser.add_argument('-d', '--debug', help="Enables debug output", required=False, action='store_true')
parser.add_argument('--clear', help="Enables clearing console", required=False, action='store_true')
args = parser.parse_args()

format = "%(asctime)s | %(levelname)s| %(filename)s:%(lineno)d | %(message)s"
if args.debug:
    logging.basicConfig(level=logging.DEBUG, format=format)
else:
    logging.basicConfig(level=logging.CRITICAL, format=format)

logger = logging.getLogger(__name__)

TURNS = ["White", "Black"]

def main():
    board = Board()
    # board.set_board("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR" )
    board.set_board("rnbqkbnr/ppppp2p/8/5pp1/4P3/3P4/PPP2PPP/RNBQKBNR")
    move = 0
    flag = False
    while True:
        if args.clear:
            board.print()
        else:
            print(board)

        if flag:
            print("Invalid move, try again")
            flag = False

        color = TURNS[move % 2]
        if board.is_checkmate(color):
            print(f"Checkmate, {TURNS[(move -1) % 2]} won")
            return
        print(f'{color} to move\n')
        try:
            move_list = input("Your move: ").split(" ")
        except KeyboardInterrupt:
            print("\nQuitting")
            break

        if len(move_list) != 2:
            flag = True
            continue

        move_from, move_to = move_list

        if len(move_from) != 2 or len(move_to) != 2:
            flag = True
            continue

        try:
            board.move(move_from, move_to, color)
        except BoardError as e:
            logger.error(e)
            flag = True
            continue

        logger.info(board.get_position())
        move += 1

if __name__ == '__main__':
    main()
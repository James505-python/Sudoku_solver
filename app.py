from flask import Flask, render_template, request

app = Flask(__name__)


def find_empty(board):
    for row in range(9):
        for col in range(9):
            if board[row][col] == 0:
                return row, col
    return None


def is_valid(board, number, row, col):
    # Sjekk raden
    for i in range(9):
        if board[row][i] == number:
            return False

    # Sjekk kolonnen
    for i in range(9):
        if board[i][col] == number:
            return False

    # Finn starten på 3x3-boksen
    box_row = (row // 3) * 3
    box_col = (col // 3) * 3

    # Sjekk 3x3-boksen
    for r in range(box_row, box_row + 3):
        for c in range(box_col, box_col + 3):
            if board[r][c] == number:
                return False

    return True


def solve(board):
    empty = find_empty(board)

    if empty is None:
        return True

    row, col = empty

    for number in range(1, 10):
        if is_valid(board, number, row, col):
            board[row][col] = number

            if solve(board):
                return True

            board[row][col] = 0

    return False


@app.route("/", methods=["GET", "POST"])
def home():

    board = [[0 for _ in range(9)] for _ in range(9)]
    message = ""

    if request.method == "POST":

        # Hent alle 81 rutene fra nettsiden
        for row in range(9):
            for col in range(9):

                value = request.form.get(f"cell-{row}-{col}", "")

                if value.isdigit():
                    number = int(value)

                    if 1 <= number <= 9:
                        board[row][col] = number

        # Prøv å løse Sudokuen
        if solve(board):
            message = "Sudokuen er løst!"
        else:
            message = "Denne Sudokuen kunne ikke løses."

    return render_template(
        "index.html",
        board=board,
        message=message
    )


if __name__ == "__main__":
    app.run(debug=True)
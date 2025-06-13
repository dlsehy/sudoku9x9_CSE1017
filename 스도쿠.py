# 스도쿠 팀 프로젝트 - 9x9 보드
########### 스도쿠 제작 함수 설명##########
# r은 행(row) 번호, c는 열(column) 번호
#
# r % base는 현재 행이 i=a블록 안에서 몇 번째 줄인지를 나타냄
#
# r // base는 현재 행이 전체 보드에서 몇 번째 블록에 속하는지를 나타냄
#
# base * (r % base)는 블록 안에서의 위치를 전체 보드 기준으로 정렬하는 데 사용됨
#
# + r // base는 블록의 전반적인 순서를 정함
#
# + c는 열의 변화에 따라 숫자를 순회하도록 해 줌
#
# % side는 전체 숫자 범위(1~9)로 순환하게 함

import random
import copy

# ==============================
# 보드 초기화 및 생성 관련 함수
# ==============================

def initialize_board_9x9():
    """기본 9x9 스도쿠 보드 생성 (3x3 블럭 기준 패턴)"""
    base = 3
    side = base * base

    def pattern(r, c):
        # 스도쿠의 기본 패턴 생성 함수
        return (base * (r % base) + r // base + c) % side

    return [[(pattern(r, c) + 1) for c in range(side)] for r in range(side)]


def shuffle_ribbons(board):
    """가로줄을 블럭 단위로 셔플"""
    top, middle, bottom = board[0:3], board[3:6], board[6:9]
    random.shuffle(top)
    random.shuffle(middle)
    random.shuffle(bottom)
    return top + middle + bottom


def transpose(board):
    """보드를 전치 (행 <-> 열 바꾸기)"""
    size = len(board)
    return [[board[j][i] for j in range(size)] for i in range(size)]


def create_solution_board_9x9():
    """정답 보드 생성"""
    board = initialize_board_9x9()
    board = shuffle_ribbons(board)
    board = transpose(board)
    board = shuffle_ribbons(board)
    board = transpose(board)
    return board


def make_holes(board, no_of_holes):
    """보드에 지정된 수만큼 구멍 만들기 (0으로 표시)"""
    while no_of_holes > 0:
        i, j = random.randint(0, 8), random.randint(0, 8)
        if board[i][j] != 0:
            board[i][j] = 0
            no_of_holes -= 1
    return board


# =====================
# 입출력 및 보조 함수
# =====================

def deep_copy_board(board):
    return copy.deepcopy(board)


def get_level():
    """사용자 난이도 선택"""
    print("Enter your level.")
    level = input("Beginner=1, Intermediate=2, Advanced=3 :\n")
    while level not in ("1", "2", "3"):
        level = input("Invalid. Choose 1, 2 or 3 :\n")
    return {"1": 6, "2": 8, "3": 10}[level]


def get_integer(message, min_val, max_val):
    """정수 입력 유효성 검사"""
    while True:
        val = input(message)
        if val.isdigit() and min_val <= int(val) <= max_val:
            return int(val)
        print("Invalid input. Try again.")


def show_board(board):
    """현재 보드 상태 출력"""
    print("    1 2 3 4 5 6 7 8 9 / in col")
    print("   -------------------")
    for idx, row in enumerate(board, start=1):
        print(f"{idx} |", end=' ')
        for num in row:
            print(num if num != 0 else ".", end=" ")
        print()
    print("/in row\n")


# =====================
# 유저 기록 관련 함수
# =====================

def load_members():
    """기록 불러오기"""
    members = {}
    try:
        with open("sudoku_members.csv", "r") as file:
            for line in file:
                name, passwd, tries, wins = line.strip().split(',')
                members[name] = (passwd, int(tries), int(wins))
    except FileNotFoundError:
        pass  # 파일이 없으면 빈 dict 반환
    return members


def store_members(members):
    """기록 저장하기"""
    with open("sudoku_members.csv", "w") as file:
        for name, (passwd, tries, wins) in members.items():
            file.write(f"{name},{passwd},{tries},{wins}\n")


# =====================
# 게임 로직
# =====================

def sudoku_mini():
    """한 명의 플레이어가 플레이하는 미니 스도쿠 게임"""
    solution_board = create_solution_board_9x9()
    puzzle_board = deep_copy_board(solution_board)
    no_of_holes = get_level()
    puzzle_board = make_holes(puzzle_board, no_of_holes)
    show_board(puzzle_board)

    try_points = no_of_holes + 3
    print("If you wanna leave, Press 0 (zero)")

    while no_of_holes > 0:
        i = get_integer("Row#(1~9) : ", 0, 9) - 1
        if i == -1:
            print("See you again")
            return 0
        j = get_integer("Column#(1~9) : ", 0, 9) - 1
        if j == -1:
            print("See you again")
            return 0

        if puzzle_board[i][j] != 0:
            print("Not empty! Try another cell.")
            continue

        n = get_integer("Number(1~9) : ", 0, 9)
        if n == solution_board[i][j]:
            puzzle_board[i][j] = n
            show_board(puzzle_board)
            no_of_holes -= 1
        else:
            print(f"{n} : Wrong number! Try again.")

        try_points -= 1
        if try_points == 0:
            print("You lose..")
            return -1

    print("Well done! Come again.")
    return 1


def login(members):
    """유저 로그인 / 신규 등록"""
    username = input("Enter your name (4 letters max): ").strip()
    while len(username) > 4:
        username = input("Name too long. Try again (max 4 letters): ")

    password = input("Enter your password: ")

    if username in members:
        if password == members[username][0]:
            tries, wins = members[username][1], members[username][2]
            print(f"You played {tries} games and won {wins}.")
            percent = (100 * wins / tries) if tries > 0 else 0
            print(f"Winning percentage: {percent:.1f}%")
            return username, tries, wins, members
        else:
            print("Incorrect password. Try again.")
            return login(members)
    else:
        members[username] = (password, 0, 0)
        return username, 0, 0, members


def show_top5(members):
    """Top5 랭킹 출력"""
    print("----")
    print("All-time Top 5 based on the number of wins.")
    top_members = sorted(members.items(), key=lambda x: x[1][2], reverse=True)[:5]
    for rank, (name, (pw, tries, wins)) in enumerate(top_members, start=1):
        print(f"Rank {rank}: {name} | Games: {tries} | Wins: {wins}")


# =====================
# 메인 게임 루프
# =====================

def play_sudoku_game():
    print("Welcome to Sudoku!")
    members = load_members()
    mode = get_integer("Solo-mode or Multi-mode (Press 1 or 2): ", 1, 2)

    if mode == 1:
        username, tries, wins, members = login(members)
        result = sudoku_mini()
        if result == 1:
            print("Congratulations! You won!")
            wins += 1
        elif result == -1:
            print("You lost the game.")
        tries += 1
        members[username] = (members[username][0], tries, wins)
        store_members(members)
        show_top5(members)

    else:
        print("Player 1's turn")
        player1_result = sudoku_mini()

        print("\nNow Player 2's turn")
        player2_result = sudoku_mini()

        if player1_result > player2_result:
            print("Player 1 wins!")
        elif player1_result < player2_result:
            print("Player 2 wins!")
        else:
            print("It's a draw. Well played!")


# 실행
if __name__ == "__main__":
    play_sudoku_game()

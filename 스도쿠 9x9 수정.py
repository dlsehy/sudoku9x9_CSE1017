# 스도쿠 팀 프로젝트 - 9 x 9 보드

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
# ========================
# 보드 초기화 및 생성 관련 함수
# ========================

# 기본 스도쿠 보드 제작
def initialize_board_9x9():
    """기본 9x9 스도쿠 보드 생성"""
    base = 3
    side = base * base

    def pattern(r, c):
        # 스도쿠의 기본 패턴 생성 함수
        return (base * (r % base) + r // base + c) % side

    board = [[(pattern(r, c) + 1) for c in range(side)] for r in range(side)]
    return board


# 보드 셔플
def shuffle_ribbons(board):
    """가로줄을 블럭 단위로 셔플"""
    top = board[0:3]
    middle = board[3:6]
    bottom = board[6:9]
    random.shuffle(top)
    random.shuffle(middle)
    random.shuffle(bottom)
    return top + middle + bottom


# 가로세로 전환
def transpose(board):
    """보드를 전치(행 <-> 열 바꾸기)"""
    size = len(board)
    transposed = []
    for _ in range(size):
        transposed.append([])
    for row in board:
        for j in range(size):
            transposed[j].append(row[j])
    return transposed


# 정답 보드
def create_solution_board_9x9():
    """정답 보드 생성"""
    board = initialize_board_9x9()
    board = shuffle_ribbons(board)
    board = transpose(board)
    board = shuffle_ribbons(board)
    board = transpose(board)
    return board


# 정답보드 구멍 생성
def make_holes(board, no_of_holes):
    """보드에 지정된 수만큼 구멍 만들기(0으로 표시)"""
    while no_of_holes > 0:
        i = random.randint(0, 8)
        j = random.randint(0, 8)
        if board[i][j] != 0:
            board[i][j] = 0
            no_of_holes -= 1
    return board

# ==========================
# 입출력 및 보조 함수
# ==========================

# 깊은 복사
def deep_copy_board(board):
    return copy.deepcopy(board)


# 난이도 입력 후 스도쿠 구멍의 갯수 리턴
def get_level():
    """사용자 난이도 선택"""
    print("Enter your level.")
    level = input("Beginner=1, Intermediate=2, Advanced=3 :\n")
    while level not in ("1", "2", "3"):
        level = input("Beginner=1, Intermediate=2, Advanced=3 :\n")
    if level == "1":
        return 6
    elif level == "2":
        return 8
    else:
        return 10

# 정수입력
def get_integer(message, min_num, max_num):
    """정수 입력 유효성 검사"""
    number = input(message)
    while not (number.isdigit() and min_num <= int(number) <= max_num):
        number = input(message + "(Invalid input, Try again)")
    return int(number)


# 보드 진행 상황
def show_board(board):
    """현재 보드 상태 출력"""
    print("    1 2 3 4 5 6 7 8 9 / in col")
    print("   -------------------")
    rowcount = 1
    for row in board:
        print(rowcount, end=' ')
        print("|", end=' ')
        rowcount += 1
        for entry in row:
            if entry == 0:
                print(".", end=" ")
            else:
                print(entry, end=" ")
        print()
    print("/in row\n")


# ========================
# 유저 기록 관련 함수
# ========================

# 기록불러오기 (파일 경로 수정 필요)
def load_members():
    """기록 불러오기"""
    file = open("sudoku9x9/sudoku_members.csv", "r")
    members = {}
    for line in file:
        name, passwd, tries, points = line.strip('\n').split(',')
        members[name] = (passwd, int(tries), int(points))
    file.close()
    return members


# 기록 저장하기
def store_members(members):
    file = open("sudoku9x9/sudoku_members.csv", "r")
    names = members.keys()
    for name in names:
        passwd, tries, points = members[name]
        line = name + ',' + passwd + ',' + str(tries) + ',' + \
               str(points) + '\n'
        file.write(line)
    file.close()


# ========================
# 게임 로직
# ========================


# 스도쿠 본게임
def sudoku_mini():
    """한 명의 플레이터가 플레이하는 미니 스도쿠 게임"""
    solution_board = create_solution_board_9x9()
    puzzle_board = deep_copy_board(solution_board)
    no_of_holes = get_level()
    puzzle_board = make_holes(puzzle_board, no_of_holes)
    show_board(puzzle_board)

    try_points = no_of_holes + 3  # 도전기회 : 구멍의 갯수 +3 (전부 소모할 경우 패배, -1 을 리턴)
    print("If you wanna leave, Press 0(zero)")

    while no_of_holes > 0:
        i = get_integer("Row#(1,2,3,4,5,6,7,8,9) : ", 0, 9) - 1
        if i == -1:
            print("See you again")
            return 0
        j = get_integer("Column#(1,2,3,4,5,6,7,8,9) : ", 0, 9) - 1
        if j == -1:
            print("See you again")
            return 0

        if puzzle_board[i][j] != 0:
            print("Not empty! Try another cell.")
            continue

        n = get_integer("Number(1,2,3,4,5,6,7,8,9) : ", 0, 9)
        if n == solution_board[i][j]:
            puzzle_board[i][j] = n
            show_board(puzzle_board)
            no_of_holes -= 1
        else:
            print(n, ": Wrong number! Try again.")

        try_points -= 1
        if try_points == 0:
            print("You lose..")
            return -1
    print("Well done! Come again.")
    return 1


def login(members):
    """유저 로그인 / 신규 등록"""
    username = input("Enter your name (4 letters max) : ")
    while len(username) > 4:
        username = input("Enter your name (4 letters max) : ")

    passwd = input("Enter your password : ")

    if username in members.keys():
        if passwd == members.get(username)[0]:
            tries = members.get(username)[1]
            wins = members.get(username)[2]
            print(f"You played {tries} games and won {wins} of them.")
            percent = (100 * wins / tries) if tries > 0 else 0
            print(f"Your all-time winning percentage is {percent}%")
            return username, tries, wins, members
        else:
            print("Incorrect password. Try again.")
            return login(members)
    else:
        members[username] = (passwd, 0, 0)
        return username, 0, 0, members


def show_top5(members):
    """Top 5 랭킹 출력"""
    print("----")
    rank_sorted = sorted(members.items(), key=lambda x: x[1][2], reverse=True)
    print("All-time Top 5 based on the number of wins.")
    rank = 1
    for member in rank_sorted[:5]:
        pw, tries, wins = member[1]
        name = member[0]
        print(f"ranked {rank}", end=' ')
        print(f"name : {name} tries : {tries} wins : {wins}")
        rank += 1


# 게임 실행 함수
def play_sudoku_game():
    print("Welcome to Sudoku!")

    # 회원 정보 불러오기
    members = load_members()

    # 로그인
    num_of_player = get_integer("Solo-mode or Multi-mode (Press 1 or 2) :\n", 1, 2)
    if num_of_player == 1:  # 솔로모드일 경우 게임을 기록하고 그 정보를 저장
        username, tries, wins, members = login(members)

        # 게임 실행
        result = sudoku_mini()

        # 결과 처리
        if result == 1:
            print("Congratulations! You won!")
            wins += 1
        elif result == 0:
            print("See you again")
            return None
        elif result == -1:
            print("You lost the game.")

        tries += 1
        # 업데이트 후 저장
        password = members[username][0]
        members[username] = (password, tries, wins)
        store_members(members)

        # 랭킹 보여주기
        show_top5(members)
    else:  # 둘 이상일 경우 게임의 승패를 가리고 종료
        print("Player 1's game")
        player1_result = sudoku_mini()
        if player1_result == 1:
            print("Congratulations! You cleared a stage!")
            print("Now, please wait about next player")

        elif player1_result == 0:  # 멀티모드에선 게임 중도 종료는 게임 기권
            print("You gave up the game.")
            return "..."

        elif player1_result == -1:
            print("You lost the game.")
            print("Now, please wait about next player.")

        print("Now player 2's game")

        player2_result = sudoku_mini()

        if player2_result == 0:
            print("You gave up the game.")
            return "..."

        if player1_result > player2_result:
            print("Player 1 wins ! ")

        elif player1_result < player2_result:
            print("Player 2 wins ! ")

        else:
            print("It's a draw")
            print("But Well done, both of you.")


play_sudoku_game()
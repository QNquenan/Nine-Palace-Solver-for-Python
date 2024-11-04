# -*- coding: utf-8 -*-
# @Time    : 2024/11/4 上午11:27
# @Author  : Quenan

import heapq

import numpy as np


class PuzzleState:
    def __init__(self, board, moves=0, previous=None):
        self.board = board
        self.empty_tile = self.find_empty_tile()
        self.moves = moves
        self.previous = previous
        self.priority = self.moves + self.heuristic()

    def find_empty_tile(self):
        return tuple(np.argwhere(self.board == 0)[0])

    def heuristic(self):
        """ 计算曼哈顿距离作为启发函数 """
        distance = 0
        for r in range(3):
            for c in range(3):
                if self.board[r, c] != 0:
                    target_r = (self.board[r, c] - 1) // 3
                    target_c = (self.board[r, c] - 1) % 3
                    distance += abs(r - target_r) + abs(c - target_c)
        return distance

    def get_neighbors(self):
        neighbors = []
        row, col = self.empty_tile
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            new_row, new_col = row + dr, col + dc
            if 0 <= new_row < 3 and 0 <= new_col < 3:
                new_board = self.board.copy()
                new_board[row, col], new_board[new_row, new_col] = new_board[new_row, new_col], new_board[row, col]
                neighbors.append(PuzzleState(new_board, self.moves + 1, self))
        return neighbors

    def is_goal(self):
        return np.array_equal(self.board, np.array([[1, 2, 3], [4, 5, 6], [7, 8, 0]]))

    def __lt__(self, other):
        return self.priority < other.priority


def a_star(initial_state):
    open_set = []
    heapq.heappush(open_set, initial_state)
    closed_set = set()

    while open_set:
        current_state = heapq.heappop(open_set)

        if current_state.is_goal():
            return current_state

        closed_set.add(tuple(current_state.board.flatten()))

        for neighbor in current_state.get_neighbors():
            if tuple(neighbor.board.flatten()) not in closed_set:
                heapq.heappush(open_set, neighbor)

    return None


def print_solution(solution):
    path = []
    while solution:
        path.append(solution.board)
        solution = solution.previous

    green = "\033[92m"  # 绿色
    reset = "\033[0m"  # 重置颜色

    for i, step in enumerate(reversed(path)):
        print(f"步骤 {i}:")
        for row in step.tolist():  # 转换为列表，逐行打印
            print(" ".join(f"{green}{num:2}{reset}" if num == 0 else f"{num:2}" for num in row))  # 固定宽度格式化
        print("-" * 15)


def get_initial_board():
    while True:
        user_input = input("九宫格的初始状态：")
        print()
        numbers = list(map(int, user_input.split()))
        if len(numbers) == 9 and all(0 <= num <= 8 for num in numbers):
            return np.array(numbers).reshape((3, 3))
        print("输入无效，请确保输入九个数字（0-8）并用空格分隔。")

def first_show():
    green = "\033[92m"  # 绿色
    reset = "\033[0m"   # 重置颜色

    print()
    print(f"{green}解密微软九宫格（理论上可以解密其他九宫格）")
    print("author：鹊楠")
    print("Github：https://github.com/QNquenan/Nine-Palace-Solver-for-Python")
    print()
    print("-" * 15)
    print("使用教程：")
    print("输入九宫格初始状态，用空格分隔的九个数字，0代表空白格 例如:0 5 7 1 4 3 6 8 2")
    print("然后根据解题步骤点击绿色的0一步一步操作即可")
    print(f"{'-' * 15}{reset}")
    print()



if __name__ == "__main__":
    first_show =  first_show()
    initial_board = get_initial_board()
    initial_state = PuzzleState(initial_board)
    solution = a_star(initial_state)

    print("-" * 15)
    if solution:
        print("找到解决方案：")
        print("-" * 15)
        print_solution(solution)
    else:
        print("没有找到解决方案。")

    input("按下 Enter 关闭窗口...")
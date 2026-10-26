"""Kiểm thử tự động logic của trò chơi Pacman."""

import pytest
from game.constants import UP, DOWN, LEFT, RIGHT, STOP, SCORE_PELLET, SCORE_STEP_PENALTY, SCORE_WIN_BONUS, SCORE_LOSE_PENALTY
from game.grid import MazeLayout
from game.engine import GameState


# Mê cung nhỏ phục vụ test chính xác các góc cạnh
# (0,0) (1,0) (2,0)
# (0,1) (1,1) (2,1)
# (0,2) (1,2) (2,2)
TINY_MAZE = [
    "###",
    "#P.",
    "###",
]

MINI_MAZE_WITH_GHOST = [
    "######",
    "#P.G.#",
    "######",
]


def test_initial_state():
    """Kiểm tra khởi tạo trạng thái từ bản đồ."""
    layout = MazeLayout(TINY_MAZE)
    state = GameState(layout)

    assert state.pacman_pos == (1, 1)
    assert (2, 1) in state.pellets
    assert len(state.pellets) == 1
    assert state.score == 0
    assert not state.is_game_over
    assert not state.is_won


def test_legal_actions_and_walls():
    """Kiểm tra Pacman không thể đi xuyên tường."""
    layout = MazeLayout(TINY_MAZE)
    state = GameState(layout)

    legal_actions = state.get_legal_actions()
    # Ở (1, 1): Trên là tường (1, 0), Dưới là tường (1, 2), Trái là tường (0, 1)
    # Duy nhất hướng PHẢI (RIGHT) là sang (2, 1) hợp lệ
    assert legal_actions == [RIGHT]

    # Cố tình đi lên trên (va vào tường)
    moved = state.step(UP)
    assert not moved
    assert state.pacman_pos == (1, 1)  # Vị trí không đổi
    assert state.score == 0            # Không bị trừ điểm phạt nếu không đi được


def test_valid_movement_and_score():
    """Kiểm tra di chuyển hợp lệ, ăn thức ăn và tính điểm."""
    layout = MazeLayout(TINY_MAZE)
    state = GameState(layout)

    # Bước sang phải vào ô (2, 1) chứa thức ăn
    moved = state.step(RIGHT)
    assert moved
    assert state.pacman_pos == (2, 1)
    assert (2, 1) not in state.pellets

    # Điểm = ăn 1 hạt (10) + trừ 1 bước (-1) + thưởng thắng (500 vì hết pellet)
    assert state.is_won
    assert state.is_game_over
    assert state.score == SCORE_PELLET + SCORE_STEP_PENALTY + SCORE_WIN_BONUS


def test_collision_ghost():
    """Kiểm tra va chạm với ma dẫn đến thua cuộc."""
    layout = MazeLayout(MINI_MAZE_WITH_GHOST)
    state = GameState(layout)

    assert state.pacman_pos == (1, 1)
    assert state.ghost_positions == [(3, 1)]

    # Bước sang ô (2, 1) ăn pellet
    state.step(RIGHT)
    assert state.pacman_pos == (2, 1)
    assert not state.is_game_over

    # Bước tiếp sang ô (3, 1) gặp ma
    state.step(RIGHT)
    assert state.pacman_pos == (3, 1)
    assert state.is_game_over
    assert not state.is_won
    assert state.score < 0  # Bị phạt điểm thua


def test_reset():
    """Kiểm tra hàm reset khôi phục đầy đủ trạng thái ban đầu."""
    layout = MazeLayout(TINY_MAZE)
    state = GameState(layout)

    state.step(RIGHT)
    assert state.is_game_over

    state.reset()
    assert state.pacman_pos == (1, 1)
    assert len(state.pellets) == 1
    assert state.score == 0
    assert not state.is_game_over
    assert not state.is_won


def test_clone():
    """Kiểm tra hàm clone tạo bản sao độc lập."""
    layout = MazeLayout(TINY_MAZE)
    state = GameState(layout)

    clone_state = state.clone()
    clone_state.step(RIGHT)

    # Clone đã thắng và mất pellet
    assert clone_state.is_game_over
    assert len(clone_state.pellets) == 0

    # Bản gốc vẫn giữ nguyên
    assert not state.is_game_over
    assert len(state.pellets) == 1
    assert state.pacman_pos == (1, 1)

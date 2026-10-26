"""Module quản lý luật chơi và trạng thái trò chơi (Game Engine)."""

from typing import List, Set, Tuple, Optional
from copy import deepcopy

from game.constants import (
    ALL_DIRECTIONS,
    STOP,
    SCORE_PELLET,
    SCORE_STEP_PENALTY,
    SCORE_WIN_BONUS,
    SCORE_LOSE_PENALTY,
)
from game.grid import MazeLayout, DEFAULT_MAZE


class GameState:
    """Đại diện cho trạng thái của bàn cờ tại một thời điểm."""

    def __init__(self, layout: MazeLayout):
        self.layout = layout
        self.width = layout.width
        self.height = layout.height
        self.walls: Set[Tuple[int, int]] = layout.walls

        # Lưu lại tập thức ăn và vị trí xuất phát để reset
        self._initial_pellets: Set[Tuple[int, int]] = set(layout.pellets)
        self._initial_pacman_pos: Tuple[int, int] = layout.pacman_start
        self._initial_ghost_starts: List[Tuple[int, int]] = list(layout.ghost_starts)

        # Trạng thái thay đổi trong khi chơi
        self.pacman_pos: Tuple[int, int] = self._initial_pacman_pos
        self.pacman_dir: Tuple[int, int] = STOP
        self.ghost_positions: List[Tuple[int, int]] = list(self._initial_ghost_starts)
        self.pellets: Set[Tuple[int, int]] = set(self._initial_pellets)

        self.score: int = 0
        self.is_game_over: bool = False
        self.is_won: bool = False
        self.steps_taken: int = 0

    def reset(self) -> None:
        """Khôi phục trạng thái trò chơi về lúc bắt đầu."""
        self.pacman_pos = self._initial_pacman_pos
        self.pacman_dir = STOP
        self.ghost_positions = list(self._initial_ghost_starts)
        self.pellets = set(self._initial_pellets)
        self.score = 0
        self.is_game_over = False
        self.is_won = False
        self.steps_taken = 0

    def get_legal_actions(self, pos: Optional[Tuple[int, int]] = None) -> List[Tuple[int, int]]:
        """Trả về danh sách các vector hướng di chuyển hợp lệ (không đâm vào tường)."""
        target_pos = pos if pos is not None else self.pacman_pos
        x, y = target_pos
        legal = []

        for dx, dy in ALL_DIRECTIONS:
            next_pos = (x + dx, y + dy)
            if not self.layout.is_wall(next_pos):
                legal.append((dx, dy))

        return legal

    def can_move(self, pos: Tuple[int, int], action: Tuple[int, int]) -> bool:
        """Kiểm tra một bước đi từ vị trí pos có hợp lệ không."""
        dx, dy = action
        next_pos = (pos[0] + dx, pos[1] + dy)
        return not self.layout.is_wall(next_pos)

    def check_ghost_collision(self) -> bool:
        """Kiểm tra Pacman có chạm vào con ma nào không."""
        for ghost_pos in self.ghost_positions:
            if self.pacman_pos == ghost_pos:
                return True
        return False

    def step(self, action: Tuple[int, int]) -> bool:
        """Thực hiện một bước đi của Pacman theo hướng action.

        Trả về True nếu bước đi thực sự làm thay đổi vị trí, False nếu đứng yên hoặc đâm tường.
        """
        if self.is_game_over:
            return False

        if action == STOP:
            return False

        # Kiểm tra di chuyển hợp lệ
        if not self.can_move(self.pacman_pos, action):
            return False

        # Di chuyển Pacman
        dx, dy = action
        self.pacman_pos = (self.pacman_pos[0] + dx, self.pacman_pos[1] + dy)
        self.pacman_dir = action
        self.steps_taken += 1
        self.score += SCORE_STEP_PENALTY

        # Ăn thức ăn nếu ô hiện tại có pellet
        if self.pacman_pos in self.pellets:
            self.pellets.remove(self.pacman_pos)
            self.score += SCORE_PELLET

        # Kiểm tra va chạm với ma
        if self.check_ghost_collision():
            self.is_game_over = True
            self.is_won = False
            self.score += SCORE_LOSE_PENALTY
            return True

        # Kiểm tra điều kiện chiến thắng (ăn sạch thức ăn)
        if len(self.pellets) == 0:
            self.is_game_over = True
            self.is_won = True
            self.score += SCORE_WIN_BONUS
            return True

        return True

    def clone(self) -> "GameState":
        """Tạo bản sao sâu (deep copy) của trạng thái hiện tại phục vụ thuật toán AI."""
        new_state = GameState.__new__(GameState)
        new_state.layout = self.layout
        new_state.width = self.width
        new_state.height = self.height
        new_state.walls = self.walls

        new_state._initial_pellets = self._initial_pellets
        new_state._initial_pacman_pos = self._initial_pacman_pos
        new_state._initial_ghost_starts = self._initial_ghost_starts

        new_state.pacman_pos = self.pacman_pos
        new_state.pacman_dir = self.pacman_dir
        new_state.ghost_positions = list(self.ghost_positions)
        new_state.pellets = set(self.pellets)

        new_state.score = self.score
        new_state.is_game_over = self.is_game_over
        new_state.is_won = self.is_won
        new_state.steps_taken = self.steps_taken
        return new_state

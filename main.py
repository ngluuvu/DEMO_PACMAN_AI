"""Điểm khởi chạy chính của trò chơi Pacman AI.

Người chơi có thể điều khiển Pacman bằng phím mũi tên hoặc WASD.
Nhấn [R] để khởi động lại ván chơi.
Nhấn [ESC] để thoát game.
"""

import sys
import pygame

from game.constants import UP, DOWN, LEFT, RIGHT, STOP
from game.grid import MazeLayout, DEFAULT_MAZE
from game.engine import GameState
from ui.renderer import GameRenderer


def main() -> None:
    # 1. Khởi tạo bản đồ và trạng thái trò chơi
    layout = MazeLayout(DEFAULT_MAZE)
    state = GameState(layout)

    # 2. Khởi tạo Renderer giao diện Pygame
    renderer = GameRenderer(state)
    clock = pygame.time.Clock()

    # Nhịp di chuyển của Pacman (số bước mỗi giây)
    PACMAN_SPEED_FPS = 8
    move_delay_ms = int(1000 / PACMAN_SPEED_FPS)
    last_move_time = pygame.time.get_ticks()

    # Hướng người chơi dự định đi (đệm phím - input buffering)
    next_direction = STOP

    running = True
    while running:
        current_time = pygame.time.get_ticks()

        # 3. Lắng nghe và xử lý sự kiện
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                    break

                elif event.key == pygame.K_r:
                    state.reset()
                    next_direction = STOP

                # Phím điều khiển người chơi
                elif event.key in (pygame.K_UP, pygame.K_w):
                    next_direction = UP
                elif event.key in (pygame.K_DOWN, pygame.K_s):
                    next_direction = DOWN
                elif event.key in (pygame.K_LEFT, pygame.K_a):
                    next_direction = LEFT
                elif event.key in (pygame.K_RIGHT, pygame.K_d):
                    next_direction = RIGHT

        # 4. Cập nhật bước đi theo nhịp thời gian
        if not state.is_game_over and current_time - last_move_time >= move_delay_ms:
            if next_direction != STOP:
                # Nếu hướng đệm đi được thì rẽ theo hướng đó
                if state.can_move(state.pacman_pos, next_direction):
                    state.step(next_direction)
                # Nếu không rẽ được thì tiếp tục đi thẳng theo hướng cũ (nếu hướng cũ vẫn đi được)
                elif state.pacman_dir != STOP and state.can_move(state.pacman_pos, state.pacman_dir):
                    state.step(state.pacman_dir)

            last_move_time = current_time

        # 5. Vẽ giao diện
        renderer.draw(mode_name="Người chơi (WASD / Mũi tên)")

        # Khóa FPS đồ họa ở mức 60 để hiển thị mượt mà
        clock.tick(60)

    pygame.quit()
    sys.exit(0)


if __name__ == "__main__":
    main()

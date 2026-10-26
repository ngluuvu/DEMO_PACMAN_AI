"""Module hiển thị đồ họa trò chơi Pacman bằng Pygame."""

import math
from typing import List, Tuple, Optional
import pygame

from game.constants import (
    TILE_SIZE,
    COLOR_BG,
    COLOR_WALL,
    COLOR_WALL_OUTLINE,
    COLOR_PELLET,
    COLOR_PACMAN,
    COLOR_PATH,
    COLOR_TEXT,
    COLOR_GHOSTS,
    UP,
    DOWN,
    LEFT,
    RIGHT,
)
from game.engine import GameState

HUD_HEIGHT = 70


class GameRenderer:
    """Đảm nhận toàn bộ việc vẽ các đối tượng game lên màn hình."""

    def __init__(self, state: GameState):
        self.state = state
        self.screen_width = state.width * TILE_SIZE
        self.screen_height = state.height * TILE_SIZE + HUD_HEIGHT

        pygame.init()
        pygame.font.init()
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Pacman AI - Nhập môn Trí tuệ Nhân tạo")

        # Fonts
        self.font = pygame.font.SysFont("Arial", 16, bold=True)
        self.big_font = pygame.font.SysFont("Arial", 28, bold=True)

    def draw(self, mode_name: str = "Người chơi (Phím mũi tên/WASD)", ai_path: Optional[List[Tuple[int, int]]] = None) -> None:
        """Vẽ toàn bộ khung cảnh: Mê cung, Thức ăn, Đường đi AI, Nhân vật và HUD."""
        self.screen.fill(COLOR_BG)

        self._draw_walls()
        self._draw_pellets()

        if ai_path:
            self._draw_ai_path(ai_path)

        self._draw_pacman()
        self._draw_ghosts()
        self._draw_hud(mode_name)

        if self.state.is_game_over:
            self._draw_game_over_banner()

        pygame.display.flip()

    def _draw_walls(self) -> None:
        """Vẽ các khối tường."""
        for x, y in self.state.walls:
            rect = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
            # Vẽ khối tường bên trong
            pygame.draw.rect(self.screen, COLOR_WALL, rect, border_radius=4)
            # Viền ngoài sắc nét
            pygame.draw.rect(self.screen, COLOR_WALL_OUTLINE, rect, width=1, border_radius=4)

    def _draw_pellets(self) -> None:
        """Vẽ các viên thức ăn."""
        radius = max(2, TILE_SIZE // 8)
        for x, y in self.state.pellets:
            cx = x * TILE_SIZE + TILE_SIZE // 2
            cy = y * TILE_SIZE + TILE_SIZE // 2
            pygame.draw.circle(self.screen, COLOR_PELLET, (cx, cy), radius)

    def _draw_ai_path(self, path: List[Tuple[int, int]]) -> None:
        """Vẽ đường đi dự kiến mà thuật toán AI đã tính toán."""
        if len(path) < 2:
            return

        pixel_points = []
        for x, y in path:
            cx = x * TILE_SIZE + TILE_SIZE // 2
            cy = y * TILE_SIZE + TILE_SIZE // 2
            pixel_points.append((cx, cy))
            # Vẽ chấm nhỏ trên các bước đi
            pygame.draw.circle(self.screen, COLOR_PATH, (cx, cy), 3)

        # Nối các điểm bằng đường line
        pygame.draw.lines(self.screen, COLOR_PATH, False, pixel_points, 2)

    def _draw_pacman(self) -> None:
        """Vẽ Pacman với miệng mở theo hướng di chuyển."""
        px, py = self.state.pacman_pos
        cx = px * TILE_SIZE + TILE_SIZE // 2
        cy = py * TILE_SIZE + TILE_SIZE // 2
        radius = TILE_SIZE // 2 - 2

        # Vẽ thân tròn vàng
        pygame.draw.circle(self.screen, COLOR_PACMAN, (cx, cy), radius)

        # Xác định góc miệng mở theo hướng
        direction = self.state.pacman_dir
        mouth_angle = 45  # độ mở 45 độ mỗi bên

        base_angle = 0  # RIGHT
        if direction == UP:
            base_angle = 90
        elif direction == LEFT:
            base_angle = 180
        elif direction == DOWN:
            base_angle = 270

        # Cắt miệng tam giác màu nền
        rad1 = math.radians(base_angle - mouth_angle)
        rad2 = math.radians(base_angle + mouth_angle)

        p1 = (cx + radius * math.cos(rad1), cy - radius * math.sin(rad1))
        p2 = (cx + radius * math.cos(rad2), cy - radius * math.sin(rad2))

        # Miệng vẽ bằng tam giác đè lên
        pygame.draw.polygon(self.screen, COLOR_BG, [(cx, cy), p1, p2])

    def _draw_ghosts(self) -> None:
        """Vẽ các con ma dạng vòm kèm đôi mắt."""
        radius = TILE_SIZE // 2 - 2

        for i, (gx, gy) in enumerate(self.state.ghost_positions):
            color = COLOR_GHOSTS[i % len(COLOR_GHOSTS)]
            cx = gx * TILE_SIZE + TILE_SIZE // 2
            cy = gy * TILE_SIZE + TILE_SIZE // 2

            # Đầu tròn nửa trên
            top_rect = pygame.Rect(gx * TILE_SIZE + 2, gy * TILE_SIZE + 2, TILE_SIZE - 4, TILE_SIZE - 4)
            pygame.draw.ellipse(self.screen, color, top_rect)

            # Đôi mắt màu trắng
            eye_offset_x = radius // 2
            eye_y = cy - radius // 4
            eye_radius = max(2, radius // 3)
            pupil_radius = max(1, eye_radius // 2)

            # Mắt trái, mắt phải
            for ex in [cx - eye_offset_x, cx + eye_offset_x]:
                pygame.draw.circle(self.screen, (255, 255, 255), (ex, eye_y), eye_radius)
                pygame.draw.circle(self.screen, (20, 20, 100), (ex, eye_y), pupil_radius)

    def _draw_hud(self, mode_name: str) -> None:
        """Vẽ thanh thông tin (HUD) phía dưới màn hình."""
        hud_top = self.state.height * TILE_SIZE
        hud_rect = pygame.Rect(0, hud_top, self.screen_width, HUD_HEIGHT)
        pygame.draw.rect(self.screen, (20, 20, 35), hud_rect)
        pygame.draw.line(self.screen, (60, 60, 90), (0, hud_top), (self.screen_width, hud_top), 2)

        # Dòng 1: Điểm và Thức ăn còn lại
        score_text = self.font.render(f"ĐIỂM: {self.state.score}", True, (255, 215, 0))
        pellet_text = self.font.render(f"THỨC ĂN: {len(self.state.pellets)}", True, COLOR_TEXT)
        self.screen.blit(score_text, (12, hud_top + 8))
        self.screen.blit(pellet_text, (self.screen_width - pellet_text.get_width() - 12, hud_top + 8))

        # Dòng 2: Chế độ chơi và hướng dẫn
        mode_text = self.font.render(f"Chế độ: {mode_name}", True, (100, 220, 255))
        help_text = self.font.render("[R] Khởi động lại   [M] Đổi chế độ   [ESC] Thoát", True, (160, 160, 170))
        self.screen.blit(mode_text, (12, hud_top + 34))
        self.screen.blit(help_text, (self.screen_width - help_text.get_width() - 12, hud_top + 34))

    def _draw_game_over_banner(self) -> None:
        """Hiển thị bảng thông báo Thắng/Thua mờ đè lên trung tâm."""
        overlay = pygame.Surface((self.screen_width, self.screen_height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))  # Màu đen trong suốt
        self.screen.blit(overlay, (0, 0))

        if self.state.is_won:
            msg = "CHIẾN THẮNG!"
            color = (46, 204, 113)
        else:
            msg = "BỊ MA BẮT - GAME OVER!"
            color = (231, 76, 60)

        title_surf = self.big_font.render(msg, True, color)
        sub_surf = self.font.render("Nhấn [R] để chơi lại màn mới", True, COLOR_TEXT)

        cx = self.screen_width // 2
        cy = (self.state.height * TILE_SIZE) // 2

        self.screen.blit(title_surf, (cx - title_surf.get_width() // 2, cy - 25))
        self.screen.blit(sub_surf, (cx - sub_surf.get_width() // 2, cy + 20))

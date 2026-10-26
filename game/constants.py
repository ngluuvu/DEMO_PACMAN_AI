"""Các hằng số cấu hình trong trò chơi Pacman.

Tất cả tọa độ được biểu diễn dưới dạng tuple (x, y):
- x: cột (chạy từ trái sang phải, từ 0 đến width - 1)
- y: hàng (chạy từ trên xuống dưới, từ 0 đến height - 1)
"""

# Hướng di chuyển (vector (dx, dy))
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)
STOP = (0, 0)

ALL_DIRECTIONS = [UP, DOWN, LEFT, RIGHT]

# Tên hướng thân thiện (dành cho log / debug)
DIRECTION_NAMES = {
    UP: "LÊN",
    DOWN: "XUỐNG",
    LEFT: "TRÁI",
    RIGHT: "PHẢI",
    STOP: "ĐỨNG YÊN",
}

# Kích thước hiển thị
TILE_SIZE = 28  # Kích thước mỗi ô vuông (pixel)

# Bảng màu chuẩn RGB
COLOR_BG = (10, 10, 20)           # Màu nền tối
COLOR_WALL = (33, 33, 222)        # Tường màu xanh dương cổ điển
COLOR_WALL_OUTLINE = (70, 70, 255)# Viền tường sáng
COLOR_PELLET = (255, 184, 151)    # Viên thức ăn màu kem hồng
COLOR_PACMAN = (255, 238, 0)      # Pacman màu vàng tươi
COLOR_PATH = (46, 204, 113)       # Đường đi dự kiến của AI (xanh lá)
COLOR_TEXT = (240, 240, 240)      # Chữ màu trắng ngà

# Màu sắc các con ma
COLOR_GHOSTS = [
    (231, 76, 60),   # Đỏ (Blinky)
    (241, 148, 180), # Hồng (Pinky)
    (52, 152, 219),  # Xanh dương nhạt (Inky)
    (230, 126, 34),  # Cam (Clyde)
]

# Cơ chế điểm số
SCORE_PELLET = 10         # Điểm nhận được khi ăn 1 hạt
SCORE_STEP_PENALTY = -1   # Trừ 1 điểm mỗi bước đi (để AI tối ưu số bước)
SCORE_WIN_BONUS = 500     # Thưởng lớn khi ăn sạch thức ăn
SCORE_LOSE_PENALTY = -500 # Phạt khi bị ma bắt

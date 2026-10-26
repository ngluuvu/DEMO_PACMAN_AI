"""Module quản lý sơ đồ mê cung (Grid & Layout)."""

from typing import Set, Tuple, List

# Bản đồ mê cung tiêu chuẩn 19 cột x 15 hàng
# Ký tự:
# '#' = Tường (Wall)
# '.' = Thức ăn (Pellet)
# 'P' = Vị trí xuất phát của Pacman
# 'G' = Vị trí xuất phát của Ma (Ghost)
# ' ' = Đường đi trống (không có thức ăn)
DEFAULT_MAZE = [
    "###################",
    "#........#........#",
    "#.##.###.#.###.##.#",
    "#.................#",
    "#.##.#.#####.#.##.#",
    "#....#...#...#....#",
    "####.### # ###.####",
    "   #.#  GGG  #.#   ",
    "####.# ##### #.####",
    "#........P........#",
    "#.##.###.#.###.##.#",
    "#..#.....#.....#..#",
    "##.#.#.#####.#.#.##",
    "#....#...#...#....#",
    "###################",
]


class MazeLayout:
    """Lưu trữ cấu trúc tĩnh của bản đồ trò chơi."""

    def __init__(self, layout_lines: List[str]):
        self.height = len(layout_lines)
        self.width = max(len(line) for line in layout_lines)

        self.walls: Set[Tuple[int, int]] = set()
        self.pellets: Set[Tuple[int, int]] = set()
        self.pacman_start: Tuple[int, int] = (1, 1)
        self.ghost_starts: List[Tuple[int, int]] = []

        self._parse(layout_lines)

    def _parse(self, lines: List[str]) -> None:
        """Phân tích các dòng ký tự để lấy tọa độ các thực thể."""
        for y, line in enumerate(lines):
            for x, char in enumerate(line):
                pos = (x, y)
                if char == "#":
                    self.walls.add(pos)
                elif char == ".":
                    self.pellets.add(pos)
                elif char == "P":
                    self.pacman_start = pos
                elif char == "G":
                    self.ghost_starts.append(pos)
                # Ký tự ' ' là khoảng trống hợp lệ, không chứa pellet

        # Nếu không có vị trí Pacman chỉ định, tìm ô trống đầu tiên
        if not hasattr(self, "pacman_start") or self.pacman_start in self.walls:
            for y in range(self.height):
                for x in range(self.width):
                    if (x, y) not in self.walls:
                        self.pacman_start = (x, y)
                        break
                else:
                    continue
                break

    def is_wall(self, pos: Tuple[int, int]) -> bool:
        """Kiểm tra một tọa độ (x, y) có phải là tường hoặc nằm ngoài biên hay không."""
        x, y = pos
        if x < 0 or x >= self.width or y < 0 or y >= self.height:
            return True
        return pos in self.walls

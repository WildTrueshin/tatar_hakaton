from __future__ import annotations
from dataclasses import dataclass, field
from typing import Callable, List, Optional, Tuple, Literal
import math

Vec2 = Tuple[float, float]


# ==========================
# Геометрия и утилиты
# ==========================

@dataclass
class Rect:
    x1: float
    y1: float
    x2: float
    y2: float

    @property
    def w(self) -> float:
        return self.x2 - self.x1

    @property
    def h(self) -> float:
        return self.y2 - self.y1

    def moved(self, dx: float, dy: float) -> "Rect":
        return Rect(self.x1 + dx, self.y1 + dy, self.x2 + dx, self.y2 + dy)

    def intersects(self, other: "Rect") -> bool:
        return not (self.x2 <= other.x1 or self.x1 >= other.x2 or
                    self.y2 <= other.y1 or self.y1 >= other.y2)

    def center(self) -> Vec2:
        return (self.x1 + self.w * 0.5, self.y1 + self.h * 0.5)


def distance_point_to_rect(px: float, py: float, r: Rect) -> float:
    dx = max(r.x1 - px, 0, px - r.x2)
    dy = max(r.y1 - py, 0, py - r.y2)
    return math.hypot(dx, dy)


# ==========================
# Текстовое окно
# ==========================

Mode = Literal["hidden", "hint", "dialog"]


@dataclass
class TextWindow:
    mode: Mode = "hidden"
    text: str = ""
    source_object_id: Optional[str] = None

    def show_hint(self, text: str, source_object_id: Optional[str]) -> None:
        self.mode = "hint"
        self.text = text
        self.source_object_id = source_object_id

    def show_dialog(self, text: str, source_object_id: Optional[str]) -> None:
        self.mode = "dialog"
        self.text = text
        self.source_object_id = source_object_id

    def hide(self) -> None:
        self.mode = "hidden"
        self.text = ""
        self.source_object_id = None


# ==========================
# Игровые объекты
# ==========================

SceneFactory = Callable[[], "Scene"]


@dataclass
class GameObject:
    """
    Базовый объект сцены.
    - rect: границы объекта (левый-верхний и правый-нижний).
    - solid: непроходимый?
    - interactable: можно ли взаимодействовать?
    - next_scene_factory: фабрика следующей сцены (при взаимодействии).
    - texture_path: ПУТЬ к изображению (PNG и т.п.), хранится как строка.
    - z: порядок отрисовки (чем больше, тем позже рисуется поверх).
    """
    id: str
    rect: Rect
    solid: bool = False
    interactable: bool = False
    next_scene_factory: Optional[SceneFactory] = None
    name: Optional[str] = None

    texture_path: Optional[str] = None
    l: int = 0

    z: int = 0
    # Если True — текстуру масштабировать под rect при отрисовке.
    scale_texture_to_rect: bool = True

    def on_interact(self, scene: "Scene") -> Optional["Scene"]:
        if self.next_scene_factory:
            return self.next_scene_factory()
        return None


@dataclass
class NPC(GameObject):
    dialog_lines: List[str] = field(default_factory=list)
    _dialog_index: int = 0
    repeatable: bool = False
    persist_progress: bool = True

    def has_dialog(self) -> bool:
        return len(self.dialog_lines) > 0

    def is_dialog_finished(self) -> bool:
        return self._dialog_index >= len(self.dialog_lines)

    def reset_dialog(self) -> None:
        self._dialog_index = 0

    def next_dialog_line(self) -> Optional[str]:
        if self._dialog_index < len(self.dialog_lines):
            line = self.dialog_lines[self._dialog_index]
            self._dialog_index += 1
            return line
        return None

    def on_dialog_finished(self) -> None:
        if not self.repeatable:
            self.interactable = False

    def on_interact(self, scene: "Scene") -> Optional["Scene"]:
        if self.is_dialog_finished() and self.next_scene_factory:
            return self.next_scene_factory()
        return None


@dataclass
class StaticObject(GameObject):
    pass


# ==========================
# Сцена
# ==========================

@dataclass
class Scene:
    id: str
    objects: List[GameObject]
    player_pos: Vec2
    player_size: Vec2 = (16, 16)
    text_window: TextWindow = field(default_factory=TextWindow)
    interact_distance: float = 24.0
    texture_path_to_player: str = "sprites/bahtiyar"
    l: int = 0
    c: int = 0
    player_speed: int = 5
    # Путь к текстуре игрока:
    player_texture_path: Optional[str] = None
    # Масштабировать ли текстуру игрока под размер хитбокса:
    scale_player_texture_to_rect: bool = True
    # Порядок отрисовки игрока:
    player_z: int = 0

    _active_dialog_npc_id: Optional[str] = None

    # ---------- Служебные ----------

    def _is_dialog_active(self) -> bool:
        return self._active_dialog_npc_id is not None or self.text_window.mode == "dialog"

    def _player_rect(self, pos: Optional[Vec2] = None) -> Rect:
        x, y = pos if pos else self.player_pos
        w, h = self.player_size
        return Rect(x, y, x + w, y + h)

    def _collides_with_solid(self, rect: Rect) -> bool:
        return any(o.solid and o.rect.intersects(rect) for o in self.objects)

    def _player_center(self) -> Vec2:
        return self._player_rect().center()

    def _nearest_interactable(self) -> Tuple[Optional[GameObject], float]:
        px, py = self._player_center()
        best_obj = None
        best_dist = float("inf")
        for obj in self.objects:
            if not obj.interactable:
                continue
            d = distance_point_to_rect(px, py, obj.rect)
            if d < best_dist:
                best_dist = d
                best_obj = obj
        return best_obj, best_dist

    def _update_hint(self) -> None:
        if self._is_dialog_active():
            return
        obj, dist = self._nearest_interactable()
        if obj and dist <= self.interact_distance:
            self.text_window.show_hint("Нажмите E, чтобы взаимодействовать", obj.id)
        else:
            if self.text_window.mode == "hint":
                self.text_window.hide()

    # ---------- Перемещение (заблокировано при диалоге) ----------

    def _move(self, dx: float, dy: float) -> None:
        if self._is_dialog_active():
            return

        new_rect_x = self._player_rect().moved(dx, 0)
        if not self._collides_with_solid(new_rect_x):
            self.player_pos = (self.player_pos[0] + dx, self.player_pos[1])

        new_rect_y = self._player_rect().moved(0, dy)
        if not self._collides_with_solid(new_rect_y):
            self.player_pos = (self.player_pos[0], self.player_pos[1] + dy)

        self._update_hint()

    def move_forward(self, step: float = 2.0) -> None:
        if self._is_dialog_active():
            return
        self._move(0, -step)
        self.l += (self.c % self.player_speed) == 0
        self.l %= 5
        self.c += 1
        self.player_texture_path = self.texture_path_to_player + f'/up{self.l % 5}.png'

    def move_back(self, step: float = 2.0) -> None:
        if self._is_dialog_active():
            return
        self._move(0, step)
        self.l += (self.c % self.player_speed) == 0
        self.l %= 5
        self.c += 1
        self.player_texture_path = self.texture_path_to_player + f'/down{self.l}.png'

    def move_left(self, step: float = 2.0) -> None:
        if self._is_dialog_active():
            return
        self._move(-step, 0)
        self.l += (self.c % self.player_speed) == 0
        self.l %= 5
        self.c += 1
        self.player_texture_path = self.texture_path_to_player + f'/left{self.l}.png'

    def move_right(self,step: float = 2.0) -> None:
        if self._is_dialog_active():
            return
        self._move(step, 0)
        self.l += (self.c % self.player_speed) == 0
        self.l %= 5
        self.c += 1
        self.player_texture_path = self.texture_path_to_player + f'/right{self.l}.png'

    # ---------- Диалоги ----------

    def start_dialog_with(self, npc: NPC) -> None:
        if not npc.has_dialog():
            return
        if not npc.persist_progress or npc.is_dialog_finished():
            npc.reset_dialog()
        self._active_dialog_npc_id = npc.id
        line = npc.next_dialog_line()
        if line is not None:
            self.text_window.show_dialog(line, npc.id)
        else:
            self._active_dialog_npc_id = None
            self.text_window.hide()

    def next_dialog_step(self) -> Optional["Scene"]:
        if self._active_dialog_npc_id is None:
            return None
        npc = next((o for o in self.objects if isinstance(o, NPC) and o.id == self._active_dialog_npc_id), None)
        if npc is None:
            self._active_dialog_npc_id = None
            self.text_window.hide()
            return None
        line = npc.next_dialog_line()
        if line is not None:
            self.text_window.show_dialog(line, npc.id)
            return None
        npc.on_dialog_finished()
        self._active_dialog_npc_id = None
        self.text_window.hide()
        return npc.on_interact(self)

    # ---------- Взаимодействие (E) ----------

    def unteract(self) -> Optional["Scene"]:
        if self._active_dialog_npc_id is not None:
            return self.next_dialog_step()
        obj, dist = self._nearest_interactable()
        if obj is None or dist > self.interact_distance:
            return None
        if isinstance(obj, NPC) and obj.has_dialog() and (not obj.is_dialog_finished() or obj.repeatable):
            self.start_dialog_with(obj)
            return None
        return obj.on_interact(self)

    def interact(self) -> Optional["Scene"]:
        return self.unteract()

    # ---------- Данные для рендера (включая пути к текстурам) ----------

    def get_draw_data(self) -> dict:
        """
        Возвращает структуру для рендера:
        - player: rect, texture_path, z
        - objects: список словарей с rect, texture_path, z и пр.
        - ui: состояние текстового окна
        """
        return {
            "player": {
                "rect": self._player_rect(),
                "texture_path": self.player_texture_path,
                "scale_to_rect": self.scale_player_texture_to_rect,
                "z": self.player_z,
            },
            "objects": [
                {
                    "id": o.id,
                    "name": o.name,
                    "rect": o.rect,
                    "solid": o.solid,
                    "interactable": o.interactable,
                    "type": "NPC" if isinstance(o, NPC) else "Static",
                    "texture_path": o.texture_path,
                    "scale_to_rect": o.scale_texture_to_rect,
                    "z": o.z,
                    "dialog_index": getattr(o, "_dialog_index", None) if isinstance(o, NPC) else None,
                    "dialog_len": len(o.dialog_lines) if isinstance(o, NPC) else None,
                }
                for o in self.objects
            ],
            "ui": {
                "mode": self.text_window.mode,
                "text": self.text_window.text,
                "source_object_id": self.text_window.source_object_id,
                "dialog_active_with": self._active_dialog_npc_id,
            },
        }

    def get_name(self):
        return self.id

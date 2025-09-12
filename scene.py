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
    """Осе-выравненный прямоугольник. Координаты: левый-верхний (x1,y1) и правый-нижний (x2,y2)."""
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
    """Минимальная дистанция от точки до прямоугольника (0, если внутри/на границе)."""
    dx = max(r.x1 - px, 0, px - r.x2)
    dy = max(r.y1 - py, 0, py - r.y2)
    return math.hypot(dx, dy)


# ==========================
# Текстовое окно
# ==========================

Mode = Literal["hidden", "hint", "dialog"]


@dataclass
class TextWindow:
    """Универсальное текстовое окно: подсказка для взаимодействия или диалог."""
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
    - rect: границы объекта (хранит левый-верхний и правый-нижний углы).
    - solid: непроходимый?
    - interactable: можно ли взаимодействовать?
    - next_scene_factory: фабрика следующей сцены, если взаимодействие должно переключить сцену.
    - name/sprite_id: полезно для отрисовки/отладки.
    """
    id: str
    rect: Rect
    solid: bool = False
    interactable: bool = False
    next_scene_factory: Optional[SceneFactory] = None
    name: Optional[str] = None
    sprite_id: Optional[str] = None

    def on_interact(self, scene: "Scene") -> Optional["Scene"]:
        """Базовое действие при взаимодействии: просто переключить сцену (если задана)."""
        if self.next_scene_factory:
            return self.next_scene_factory()
        return None


@dataclass
class NPC(GameObject):
    """NPC с диалогом. По завершении диалога может переключить сцену."""
    dialog_lines: List[str] = field(default_factory=list)
    _dialog_index: int = 0

    def has_dialog(self) -> bool:
        return len(self.dialog_lines) > 0

    def reset_dialog(self) -> None:
        self._dialog_index = 0

    def next_dialog_line(self) -> Optional[str]:
        if self._dialog_index < len(self.dialog_lines):
            line = self.dialog_lines[self._dialog_index]
            self._dialog_index += 1
            return line
        return None

    def on_interact(self, scene: "Scene") -> Optional["Scene"]:
        """
        Для NPC взаимодействие управляется сценой (пошаговая выдача реплик).
        Возврат сцены здесь происходит только, если диалог уже завершён
        и у NPC задан next_scene_factory.
        """
        if self._dialog_index >= len(self.dialog_lines) and self.next_scene_factory:
            return self.next_scene_factory()
        return None


@dataclass
class StaticObject(GameObject):
    """Статичный объект. Может быть проходимым/непроходимым и (опционально) интерактивным."""
    pass


# ==========================
# Сцена
# ==========================

@dataclass
class Scene:
    """
    Сцена содержит:
    - список объектов;
    - позицию игрока (x, y) — левый-верхний угол хитбокса игрока;
    - размер хитбокса игрока (player_size);
    - текстовое окно (подсказки/диалог);
    - радиус взаимодействия (interact_distance).
    """
    id: str
    objects: List[GameObject]
    player_pos: Vec2
    player_size: Vec2 = (16, 16)
    text_window: TextWindow = field(default_factory=TextWindow)
    interact_distance: float = 24.0

    # Техническое: текущий NPC, с которым идёт диалог
    _active_dialog_npc_id: Optional[str] = None

    # ---------- Вспомогательные методы ----------

    def _player_rect(self, pos: Optional[Vec2] = None) -> Rect:
        x, y = pos if pos else self.player_pos
        w, h = self.player_size
        return Rect(x, y, x + w, y + h)

    def _collides_with_solid(self, rect: Rect) -> bool:
        for obj in self.objects:
            if obj.solid and obj.rect.intersects(rect):
                return True
        return False

    def _player_center(self) -> Vec2:
        return self._player_rect().center()

    def _nearest_interactable(self) -> Tuple[Optional[GameObject], float]:
        """Возвращает (объект, расстояние) для ближайшего интерактивного объекта."""
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
        """Обновляет подсказку в текстовом окне, если рядом интерактивный объект и нет активного диалога."""
        if self._active_dialog_npc_id is not None:
            return  # в диалоге подсказки не показываем
        obj, dist = self._nearest_interactable()
        if obj and dist <= self.interact_distance:
            self.text_window.show_hint("Нажмите E, чтобы взаимодействовать", obj.id)
        else:
            if self.text_window.mode == "hint":
                self.text_window.hide()

    # ---------- Перемещение игрока ----------

    def _move(self, dx: float, dy: float) -> None:
        """Перемещает игрока с поосевым разбором коллизий."""
        # Ось X
        new_rect_x = self._player_rect().moved(dx, 0)
        if not self._collides_with_solid(new_rect_x):
            self.player_pos = (self.player_pos[0] + dx, self.player_pos[1])

        # Ось Y
        new_rect_y = self._player_rect().moved(0, dy)
        if not self._collides_with_solid(new_rect_y):
            self.player_pos = (self.player_pos[0], self.player_pos[1] + dy)

        # После движения — обновить подсказку
        self._update_hint()

    def move_forward(self, step: float = 2.0) -> None:
        """Вперёд (вверх по экрану, уменьшение Y)."""
        self._move(0, -step)

    def move_back(self, step: float = 2.0) -> None:
        """Назад (вниз по экрану, увеличение Y)."""
        self._move(0, step)

    def move_left(self, step: float = 2.0) -> None:
        self._move(-step, 0)

    def move_right(self, step: float = 2.0) -> None:
        self._move(step, 0)

    # ---------- Взаимодействие ----------

    def unteract(self) -> Optional["Scene"]:
        """
        Взаимодействие с ближайшим объектом, если он в пределах interact_distance.
        Возвращает новую сцену, если объект инициирует её смену. Иначе — None.
        """
        # Если уже идёт диалог — продвигаем его
        if self._active_dialog_npc_id is not None:
            npc = next((o for o in self.objects
                        if isinstance(o, NPC) and o.id == self._active_dialog_npc_id), None)
            if npc is None:
                # NPC исчез/заменён — завершим диалог
                self._active_dialog_npc_id = None
                self.text_window.hide()
                return None

            line = npc.next_dialog_line()
            if line is not None:
                self.text_window.show_dialog(line, npc.id)
                return None
            else:
                # диалог кончился
                self._active_dialog_npc_id = None
                self.text_window.hide()
                # возможно переключение сцены после диалога
                return npc.on_interact(self)

        # Иначе — ищем ближайший интерактивный объект
        obj, dist = self._nearest_interactable()
        if obj is None or dist > self.interact_distance:
            return None

        # Если это NPC с диалогом — запускаем/показываем первую реплику
        if isinstance(obj, NPC) and obj.has_dialog():
            obj.reset_dialog()
            first = obj.next_dialog_line()
            if first is not None:
                self._active_dialog_npc_id = obj.id
                self.text_window.show_dialog(first, obj.id)
                return None
            # если диалог пуст — пробуем стандартное поведение
        # Для прочих объектов — стандартное поведение
        return obj.on_interact(self)

    # Удобный алиас (если вдруг опечатка не нужна)
    def interact(self) -> Optional["Scene"]:
        return self.unteract()

    # ---------- Данные для рендера ----------

    def get_draw_data(self) -> dict:
        """
        Минимальный пакет данных для рендера (можно адаптировать под ваш движок/pygame):
        - player_rect: хитбокс игрока
        - objects: список объектов с rect и sprite_id
        - ui: состояние текстового окна
        """
        return {
            "player_rect": self._player_rect(),
            "objects": [
                {
                    "id": o.id,
                    "name": o.name,
                    "sprite_id": o.sprite_id,
                    "rect": o.rect,
                    "solid": o.solid,
                    "interactable": o.interactable,
                    "type": "NPC" if isinstance(o, NPC) else "Static",
                }
                for o in self.objects
            ],
            "ui": {
                "mode": self.text_window.mode,
                "text": self.text_window.text,
                "source_object_id": self.text_window.source_object_id,
            },
        }

#
# # ==========================
# # Пример использования
# # ==========================
#
# def make_scene_b() -> Scene:
#     # Пустая сцена B
#     return Scene(
#         id="scene_b",
#         objects=[],
#         player_pos=(20, 20),
#         player_size=(16, 16)
#     )
#
#
# def make_scene_a() -> Scene:
#     door = StaticObject(
#         id="door_1",
#         name="Дверь в сцену B",
#         rect=Rect(120, 40, 140, 72),
#         solid=False,
#         interactable=True,
#         next_scene_factory=make_scene_b,
#         sprite_id="spr_door"
#     )
#
#     wall = StaticObject(
#         id="wall_1",
#         name="Стена",
#         rect=Rect(0, 0, 200, 16),
#         solid=True,
#         interactable=False,
#         sprite_id="spr_wall"
#     )
#
#     granny = NPC(
#         id="npc_granny",
#         name="Әби",
#         rect=Rect(60, 60, 76, 92),
#         solid=False,
#         interactable=True,
#         dialog_lines=["Сәлам!", "Ярый, бар, сөйләшик соңрак."],
#         sprite_id="spr_granny"
#     )
#
#     return Scene(
#         id="scene_a",
#         objects=[door, wall, granny],
#         player_pos=(30, 90),
#         player_size=(16, 16),
#         interact_distance=28.0
#     )
#
#
# if __name__ == "__main__":
#     # Небольшая проверка логики без графики
#     scene = make_scene_a()
#
#     # Движение к двери
#     scene.move_right(100)
#     scene.move_back(0)  # подсказка обновится автоматически
#     print("UI hint:", scene.text_window.mode, scene.text_window.text)
#
#     # Взаимодействуем (должно переключить сцену)
#     new_scene = scene.unteract()
#     if new_scene:
#         scene = new_scene
#         print("Переключились на сцену:", scene.id)
#
#     # Движение к NPC (в примере NPC был в первой сцене, это просто демонстрация)
#     scene = make_scene_a()
#     scene.player_pos = (50, 80)
#     scene._update_hint()
#     print("UI hint near NPC:", scene.text_window.mode, scene.text_window.text)
#
#     # Диалог по шагам
#     scene.unteract()  # первая реплика
#     print("Dialog 1:", scene.text_window.text)
#     scene.unteract()  # вторая реплика
#     print("Dialog 2:", scene.text_window.text)
#     scene.unteract()  # диалог завершён
#     print("Dialog ended. UI:", scene.text_window.mode)

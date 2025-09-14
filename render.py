from functools import cmp_to_key

import pygame
import sys
import scenes
from scene import Scene
from data_helper import *
from scenes import scene1

# --- голос/озвучка ---
pygame.mixer.pre_init(44100, -16, 2, 512)

pygame.init()
pygame.mixer.init()

VOICE_ENABLED = True
VOICE_VOLUME = 0.85
AUTO_ADVANCE_DIALOG = False  # если True — авто-переход к следующей реплике после окончания звука

VOICE_CHANNEL = pygame.mixer.Channel(5)      # отдельный канал под озвучку
VOICE_END_EVENT = pygame.USEREVENT + 7       # событие «озвучка завершилась»
VOICE_CACHE = {}                             # кэш звуков по пути

def _play_voice(path: Optional[str]):
    VOICE_CHANNEL.stop()
    if not VOICE_ENABLED or not path:
        return
    try:
        snd = VOICE_CACHE.get(path)
        if snd is None:
            snd = pygame.mixer.Sound(path)
            VOICE_CACHE[path] = snd
        VOICE_CHANNEL.set_volume(VOICE_VOLUME)
        VOICE_CHANNEL.play(snd)
        VOICE_CHANNEL.set_endevent(VOICE_END_EVENT)
    except Exception as e:
        print("voice error:", e)

# для отслеживания изменения реплик
_last_ui_mode = None
_last_dialog_text = None
_last_voice_path = None

info = pygame.display.Info()
WIDTH = info.current_w
HEIGHT = int(WIDTH / 16 * 9)
SCALE = HEIGHT / 279
FPS = 30
DIALOG_COLOR = (246, 235, 165)
TEXT_COLOR = (41, 43, 51)
DIALOG_HEIGHT = int(HEIGHT / 5)
DIALOG_FONT = pygame.font.SysFont("consolas", int(HEIGHT / 20))
BORDER_COLOR = (117, 56, 56)
BORDER_WIDTH = int(HEIGHT / 200)
E_SIZE = int(HEIGHT / 10)
E_PATH = "sprites/system/use_e.png"
E_SPRITE = pygame.image.load(E_PATH)
E_SPRITE = pygame.transform.scale(E_SPRITE, (E_SIZE, E_SIZE))
E_RECT = pygame.Rect(0, 0, E_SIZE, E_SIZE)


def draw_inventory(items):
    """Отрисовка окна инвентаря."""
    inv_rect = pygame.Rect(0, 0, WIDTH, HEIGHT)
    pygame.draw.rect(screen, DIALOG_COLOR, inv_rect)
    pygame.draw.rect(screen, BORDER_COLOR, inv_rect, width=BORDER_WIDTH)

    item_size = int(HEIGHT / 6)
    padding = int(item_size * 0.5)
    font_h = DIALOG_FONT.get_height()
    cols = max(1, (WIDTH - padding) // (item_size + padding))
    for i, item in enumerate(items):
        word = item["word"]
        path = item["texture_path"]
        sprite = pygame.image.load(path).convert_alpha()
        sprite = pygame.transform.scale(sprite, (item_size, item_size))
        col = i % cols
        row = i // cols
        x = padding + col * (item_size + padding)
        y = padding + row * (item_size + font_h + padding)
        screen.blit(sprite, (x, y))
        text_surface = DIALOG_FONT.render(word, True, TEXT_COLOR)
        text_rect = text_surface.get_rect(center=(x + item_size // 2, y + item_size + font_h // 2))
        screen.blit(text_surface, text_rect)


def draw_dialog(text, items):
    """Отрисовать диалог с картинками под словами из словаря."""
    dialog_rect = pygame.Rect(0, HEIGHT - DIALOG_HEIGHT, WIDTH, DIALOG_HEIGHT)
    pygame.draw.rect(screen, DIALOG_COLOR, dialog_rect, border_radius=20)
    pygame.draw.rect(screen, BORDER_COLOR, dialog_rect, border_radius=20, width=BORDER_WIDTH)

    words = text.split()
    space_w = DIALOG_FONT.size(" ")[0]
    surfaces = [DIALOG_FONT.render(w, True, TEXT_COLOR) for w in words]
    total_w = sum(s.get_width() for s in surfaces) + space_w * max(0, len(surfaces) - 1)
    x = (WIDTH - total_w) // 2
    y_text = dialog_rect.y + (DIALOG_HEIGHT - DIALOG_FONT.get_height()) // 2

    inventory_map = {item["word"].lower(): item["texture_path"] for item in items}
    for w, surf in zip(words, surfaces):
        screen.blit(surf, (x, y_text))
        clean = w.strip(".,!?;:\"'").lower()
        if clean in inventory_map:
            img = pygame.image.load(inventory_map[clean]).convert_alpha()
            img_size = DIALOG_FONT.get_height()
            img = pygame.transform.scale(img, (img_size, img_size))
            img_rect = img.get_rect(center=(x + surf.get_width() // 2, y_text + surf.get_height() + img_size // 2 + 5))
            screen.blit(img, img_rect)
        x += surf.get_width() + space_w

# --- START SCREEN (assets & geometry) ---
# Координаты кнопки в "игровых" пикселях 496x279 (масштабируем через SCALE)
START_BUTTON_RECT_GAME = pygame.Rect(12, 113, 178, 52)  # x, y, w, h
# Пути к картинкам стартового экрана (поменяй под себя)
START_BG_PATH_CANDIDATES = [
    "sprites/backgrounds/start_screen.png",
]
START_BTN_PATH_CANDIDATES = [
    "sprites/button/start_button_left.png",
]

def _first_existing_image(candidates):
    for p in candidates:
        try:
            pygame.image.load(p)  # just to check it exists/loads
            return p
        except Exception:
            continue
    raise FileNotFoundError("Не найдено изображение стартового экрана. Проверь пути.")

def run_start_screen(screen, clock):
    """Показывает стартовый экран. Возвращает True если начали игру, False если вышли."""
    bg_path = _first_existing_image(START_BG_PATH_CANDIDATES)
    btn_path = _first_existing_image(START_BTN_PATH_CANDIDATES)

    bg_img = pygame.image.load(bg_path).convert_alpha()
    bg_img = pygame.transform.scale(bg_img, (WIDTH, HEIGHT))

    # Масштабируем кнопку из координат 496x279 под текущее окно
    br = START_BUTTON_RECT_GAME
    btn_w, btn_h = int(br.w * SCALE), int(br.h * SCALE)
    btn_x, btn_y = int(br.x * SCALE), int(br.y * SCALE)
    btn_img = pygame.image.load(btn_path).convert_alpha()
    btn_img = pygame.transform.scale(btn_img, (btn_w, btn_h))
    btn_rect = pygame.Rect(btn_x, btn_y, btn_w, btn_h)

    # (опционально) текстовая подсказка
    tip_font = pygame.font.SysFont("consolas", int(HEIGHT / 28))
    tip_surf = tip_font.render("Нажмите ENTER или клик по кнопке", True, (255, 255, 255))
    tip_rect = tip_surf.get_rect(midbottom=(WIDTH // 2, HEIGHT - int(20 * SCALE)))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN and event.key in (pygame.K_RETURN, pygame.K_SPACE, pygame.K_e):
                return True
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if btn_rect.collidepoint(event.pos):
                    return True

        screen.blit(bg_img, (0, 0))
        screen.blit(btn_img, btn_rect)
        screen.blit(tip_surf, tip_rect)
        pygame.display.flip()
        clock.tick(FPS)



screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.DOUBLEBUF)
pygame.display.set_caption("Checheck game")
clock = pygame.time.Clock()
# Сначала показываем стартовый экран
started = run_start_screen(screen, clock)
if not started:
    pygame.quit()
    sys.exit()

# После старта — грузим сейв и заходим в игру
data = load_game()
print(data)
if isinstance(data.get("scene"), str) and data["scene"] in scenes.scenes:
    current_scene: Scene = scenes.scenes[data["scene"]]
else:
    current_scene: Scene = scene1()
def cmp_objects(obj1, obj2):
    if obj1["z"] < obj2["z"]:
        return -1
    if obj1["z"] > obj2["z"]:
        return 1
    if obj1["rect"].y2 < obj2["rect"].y2:
        return -1
    return 1


running = True
while running:
    # ---------- события ----------
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Авто-переход к следующей реплике, когда закончилась озвучка
        elif event.type == VOICE_END_EVENT and AUTO_ADVANCE_DIALOG and current_scene.text_window.mode == "dialog":
            VOICE_CHANNEL.stop()
            res = current_scene.interact()   # то же, что нажать E
            if res:
                current_scene = res

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                save_game(current_scene.get_name())
                running = False

            elif event.key == pygame.K_e:
                # при листании диалога глушим текущий голос, потом переключаем реплику
                VOICE_CHANNEL.stop()
                res = current_scene.interact()
                if res:
                    current_scene = res

            elif event.key == pygame.K_q:
                current_scene.toggle_inventory()

            # ---- управление звуком (по желанию) ----
            elif event.key == pygame.K_m:
                VOICE_CHANNEL.stop()
                VOICE_ENABLED = not VOICE_ENABLED
            elif event.key == pygame.K_LEFTBRACKET:   # [
                VOICE_VOLUME = max(0.0, VOICE_VOLUME - 0.1); VOICE_CHANNEL.set_volume(VOICE_VOLUME)
            elif event.key == pygame.K_RIGHTBRACKET:  # ]
                VOICE_VOLUME = min(1.0, VOICE_VOLUME + 0.1); VOICE_CHANNEL.set_volume(VOICE_VOLUME)

    # ---------- управление персонажем ----------
    keys = pygame.key.get_pressed()
    if not current_scene.inventory_open and current_scene.text_window.mode != "dialog":
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            current_scene.move_forward()
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            current_scene.move_back()
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            current_scene.move_left()
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            current_scene.move_right()

    # ---------- логика сцены и отрисовка ----------
    scene_info = current_scene.get_draw_data()
    screen.fill((0, 0, 0))

    # Порядок отрисовки объектов + игрок
    sorted_objects = scene_info["objects"] + [scene_info["player"]]
    sorted_objects.sort(key=cmp_to_key(cmp_objects))

    for obj in sorted_objects:
        rect = obj["rect"]
        x_l = int(rect.x1 * SCALE)
        y_t = int(rect.y1 * SCALE)
        width = int((rect.x2 - rect.x1) * SCALE)
        height = int((rect.y2 - rect.y1) * SCALE)

        if obj["texture_path"] is not None:
            sprite = pygame.image.load(obj["texture_path"]).convert_alpha()
            sprite = pygame.transform.scale(sprite, (width, height))
            rect = sprite.get_rect(topleft=(x_l, y_t))
            screen.blit(sprite, rect)

    # ---------- авто-проигрывание озвучки по смене строки ----------
    ui = scene_info["ui"]
    if _last_ui_mode == "dialog" and ui["mode"] != "dialog":
        VOICE_CHANNEL.stop()  # вышли из диалога — остановить голос

    if ui["mode"] == "dialog":
        if ui["text"] != _last_dialog_text or ui.get("voice_path") != _last_voice_path:
            _play_voice(ui.get("voice_path"))  # voice_path задаётся в сценах для конкретной реплики

    _last_ui_mode = ui["mode"]
    _last_dialog_text = ui["text"] if ui["mode"] == "dialog" else None
    _last_voice_path = ui.get("voice_path") if ui["mode"] == "dialog" else None

    # ---------- поверх — UI ----------
    if scene_info["inventory"]["open"]:
        draw_inventory(scene_info["inventory"]["items"])
    elif scene_info["ui"]["mode"] == "dialog":
        draw_dialog(scene_info["ui"]["text"], scene_info["inventory"]["items"])
    else:
        if scene_info["ui"]["mode"] == "hint":
            screen.blit(E_SPRITE, E_RECT)

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()





import pygame
import sys
from pygame.locals import *
import time

pygame.init()

WIDTH, HEIGHT = 800, 600
SCALE = 20
FONT = pygame.font.SysFont("Arial", 18)

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GRAY = (50, 50, 50)
BUTTON_COLOR = (100, 100, 255)

x1, y1, x2, y2 = -15, -10, 15, 10
cx, cy, radius = 0, 0, 15

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Растеризация линий и окружностей")

inputs = {
    "x1": "",
    "y1": "",
    "x2": "",
    "y2": "",
    "cx": "",
    "cy": "",
    "radius": ""
}
active_input = None
selected_algorithm = None
elapsed_time = None


def draw_grid():
    screen.fill(WHITE)
    center_x, center_y = WIDTH // 2, HEIGHT // 2
    font = pygame.font.SysFont(None, 18)

    #линии сетки
    for x in range(center_x % SCALE, WIDTH, SCALE):
        pygame.draw.line(screen, GRAY, (x, 0), (x, HEIGHT))
    for y in range(center_y % SCALE, HEIGHT, SCALE):
        pygame.draw.line(screen, GRAY, (0, y), (WIDTH, y))

    # Оси X и Y
    pygame.draw.line(screen, RED, (center_x, 0), (center_x, HEIGHT), 2)
    pygame.draw.line(screen, RED, (0, center_y), (WIDTH, center_y), 2)

    # Отметки на осях
    for x in range(-WIDTH // (2 * SCALE), WIDTH // (2 * SCALE) + 1):
        pos_x = center_x + x * SCALE
        if pos_x >= 0 and pos_x <= WIDTH:
            pygame.draw.line(screen, RED, (pos_x, center_y - 5), (pos_x, center_y + 5), 2)
            if x != 0:
                label = font.render(str(x), True, RED)
                screen.blit(label, (pos_x - label.get_width() // 2, center_y + 8))

    for y in range(-HEIGHT // (2 * SCALE), HEIGHT // (2 * SCALE) + 1):
        pos_y = center_y - y * SCALE
        if pos_y >= 0 and pos_y <= HEIGHT:
            pygame.draw.line(screen, RED, (center_x - 5, pos_y), (center_x + 5, pos_y), 2)
            if y != 0:
                label = font.render(str(y), True, RED)
                screen.blit(label, (center_x + 8, pos_y - label.get_height() // 2))

def to_pixel_coords(x, y):
    px = WIDTH // 2 + x * SCALE
    py = HEIGHT // 2 - y * SCALE
    return int(px), int(py)


def step_by_step(x1, y1, x2, y2):
    dx, dy = x2 - x1, y2 - y1
    steps = max(abs(dx), abs(dy))
    x_inc, y_inc = dx / steps, dy / steps
    x, y = x1, y1
    for _ in range(steps):
        px, py = to_pixel_coords(int(round(x)), int(round(y)))
        pygame.draw.rect(screen, RED, (px, py, SCALE, SCALE))
        x += x_inc
        y += y_inc


def dda(x1, y1, x2, y2):
    dx, dy = x2 - x1, y2 - y1
    steps = max(abs(dx), abs(dy))
    x_inc, y_inc = dx / steps, dy / steps
    x, y = x1, y1
    for _ in range(steps):
        px, py = to_pixel_coords(int(x), int(y))
        pygame.draw.rect(screen, RED, (px, py, SCALE, SCALE))
        x += x_inc
        y += y_inc


def bresenham_line(x1, y1, x2, y2):
    dx, dy = abs(x2 - x1), abs(y2 - y1)
    sx = 1 if x1 < x2 else -1
    sy = 1 if y1 < y2 else -1
    err = dx - dy
    while True:
        px, py = to_pixel_coords(x1, y1)
        pygame.draw.rect(screen, RED, (px, py, SCALE, SCALE))
        if x1 == x2 and y1 == y2:
            break
        e2 = err * 2
        if e2 > -dy:
            err -= dy
            x1 += sx
        if e2 < dx:
            err += dx
            y1 += sy


def bresenham_circle(cx, cy, radius):
    x, y = 0, radius
    d = 3 - 2 * radius
    while y >= x:
        for x_offset, y_offset in [(x, y), (y, x), (-x, y), (-y, x), (-x, -y), (-y, -x), (x, -y), (y, -x)]:
            px, py = to_pixel_coords(cx + x_offset, cy + y_offset)
            pygame.draw.rect(screen, BLUE, (px, py, SCALE, SCALE))
        if d <= 0:
            d = d + 4 * x + 6
        else:
            d = d + 4 * (x - y) + 10
            y -= 1
        x += 1


def handle_input_events(event):
    global active_input
    if event.type == pygame.MOUSEBUTTONDOWN:
        x, y = event.pos
        if y > HEIGHT - 50:
            for key in inputs:
                input_x = 50 + list(inputs.keys()).index(key) * 80
                if input_x <= x <= input_x + 70:
                    active_input = key
                    return
            active_input = None
    elif event.type == pygame.KEYDOWN and active_input:
        if event.key == pygame.K_RETURN:
            update_coordinates()
            active_input = None
        elif event.key == pygame.K_BACKSPACE:
            inputs[active_input] = inputs[active_input][:-1]
        elif event.unicode.isdigit() or (event.unicode == "-" and not inputs[active_input]):
            inputs[active_input] += event.unicode


def update_coordinates():
    global x1, y1, x2, y2, cx, cy, radius
    try:
        x1, y1, x2, y2 = int(inputs["x1"]), int(inputs["y1"]), int(inputs["x2"]), int(inputs["y2"])
        cx, cy, radius = int(inputs["cx"]), int(inputs["cy"]), int(inputs["radius"])
    except ValueError:
        print("Ошибка ввода")

def measure_time(algorithm, *args):
    global elapsed_time
    start_time = time.perf_counter_ns()
    algorithm(*args)
    end_time = time.perf_counter_ns()
    elapsed_time = end_time - start_time
    print(f"Время выполнения {algorithm.__name__}: {elapsed_time} нс")


running = True
while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        handle_input_events(event)
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            if 50 <= x <= 150 and HEIGHT - 80 <= y <= HEIGHT - 50:
                selected_algorithm = "step_by_step"
                measure_time(step_by_step, x1, y1, x2, y2)
            elif 160 <= x <= 260 and HEIGHT - 80 <= y <= HEIGHT - 50:
                selected_algorithm = "dda"
                measure_time(dda, x1, y1, x2, y2)
            elif 270 <= x <= 370 and HEIGHT - 80 <= y <= HEIGHT - 50:
                selected_algorithm = "bresenham_line"
                measure_time(bresenham_line, x1, y1, x2, y2)
            elif 380 <= x <= 480 and HEIGHT - 80 <= y <= HEIGHT - 50:
                selected_algorithm = "bresenham_circle"
                measure_time(bresenham_circle, cx, cy, radius)
            elif 600 <= x <= 630 and HEIGHT - 80 <= y <= HEIGHT - 50:
                SCALE += 5
            elif 640 <= x <= 670 and HEIGHT - 80 <= y <= HEIGHT - 50 and SCALE > 5:
                SCALE -= 5

    draw_grid()
    update_coordinates()

    if elapsed_time is not None:
        time_text = f"{selected_algorithm} time: {elapsed_time} ns"
        time_surface = FONT.render(time_text, True, BLACK)
        screen.blit(time_surface, (WIDTH - 250, 0))

    if selected_algorithm == "step_by_step":
        step_by_step(x1, y1, x2, y2)
    elif selected_algorithm == "dda":
        dda(x1, y1, x2, y2)
    elif selected_algorithm == "bresenham_line":
        bresenham_line(x1, y1, x2, y2)
    elif selected_algorithm == "bresenham_circle":
        bresenham_circle(cx, cy, radius)

    pygame.draw.rect(screen, BUTTON_COLOR, (50, HEIGHT - 80, 100, 30))
    pygame.draw.rect(screen, BUTTON_COLOR, (160, HEIGHT - 80, 100, 30))
    pygame.draw.rect(screen, BUTTON_COLOR, (270, HEIGHT - 80, 100, 30))
    pygame.draw.rect(screen, BUTTON_COLOR, (380, HEIGHT - 80, 100, 30))
    pygame.draw.rect(screen, BUTTON_COLOR, (600, HEIGHT - 80, 30, 30))  # кнопка "+"
    pygame.draw.rect(screen, BUTTON_COLOR, (640, HEIGHT - 80, 30, 30))  # кнопка "-"

    screen.blit(FONT.render("StepByStep", True, BLACK), (53, HEIGHT - 75))
    screen.blit(FONT.render("DDA", True, BLACK), (190, HEIGHT - 75))
    screen.blit(FONT.render("Bresenham", True, BLACK), (275, HEIGHT - 75))
    screen.blit(FONT.render("Circle", True, BLACK), (406, HEIGHT - 75))
    screen.blit(FONT.render("+", True, BLACK), (610, HEIGHT - 75))
    screen.blit(FONT.render("-", True, BLACK), (652, HEIGHT - 76))

    y_offset = HEIGHT - 30
    for i, (label, text) in enumerate(inputs.items()):
        x_offset = 50 + i * 80
        pygame.draw.rect(screen, BLACK, (x_offset, y_offset, 70, 20), 2)
        txt_surface = FONT.render(text or label, True, BLACK)
        screen.blit(txt_surface, (x_offset + 5, y_offset - 1))

    pygame.display.flip()
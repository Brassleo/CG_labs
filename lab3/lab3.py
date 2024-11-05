import pygame
import sys
import time

WIDTH, HEIGHT = 800, 800
WHITE, BLACK, RED, GREEN, BLUE, ORANGE = (255, 255, 255), (0, 0, 0), (255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 165, 0)
SCALE = 20
MIN_SCALE, MAX_SCALE = 10, 100

def step_by_step(x1, y1, x2, y2):
    points = []
    dx, dy = x2 - x1, y2 - y1
    steps = abs(dx)
    x, y = x1, y1
    for _ in range(steps + 1):
        points.append((round(x), round(y)))
        x += dx / steps
        y += dy / steps
    return points

def dda(x1, y1, x2, y2):
    points = []
    dx, dy = x2 - x1, y2 - y1
    steps = max(abs(dx), abs(dy))
    x_inc, y_inc = dx / steps, dy / steps
    x, y = x1, y1
    for _ in range(steps + 1):
        points.append((round(x), round(y)))
        x += x_inc
        y += y_inc
    return points

def bresenham_line(x1, y1, x2, y2):
    points = []
    dx, dy = abs(x2 - x1), abs(y2 - y1)
    sx = 1 if x1 < x2 else -1
    sy = 1 if y1 < y2 else -1
    err = dx - dy
    while True:
        points.append((x1, y1))
        if x1 == x2 and y1 == y2:
            break
        e2 = 2 * err
        if e2 > -dy:
            err -= dy
            x1 += sx
        if e2 < dx:
            err += dx
            y1 += sy
    return points

def bresenham_circle(xc, yc, r):
    points = []
    x, y, d = 0, r, 3 - 2 * r
    while y >= x:
        points += [(xc + x, yc + y), (xc - x, yc + y), (xc + x, yc - y), (xc - x, yc - y),
                   (xc + y, yc + x), (xc - y, yc + x), (xc + y, yc - x), (xc - y, yc - x)]
        x += 1
        if d > 0:
            y -= 1
            d += 4 * (x - y) + 10
        else:
            d += 4 * x + 6
    return points

def draw_grid(screen, scale):
    # Центр экрана
    center_x, center_y = WIDTH // 2, HEIGHT // 2
    font = pygame.font.SysFont(None, 18)

    #линии сетки
    for x in range(center_x % scale, WIDTH, scale):
        pygame.draw.line(screen, BLACK, (x, 0), (x, HEIGHT))
    for y in range(center_y % scale, HEIGHT, scale):
        pygame.draw.line(screen, BLACK, (0, y), (WIDTH, y))

    # Оси X и Y
    pygame.draw.line(screen, RED, (center_x, 0), (center_x, HEIGHT), 2)
    pygame.draw.line(screen, RED, (0, center_y), (WIDTH, center_y), 2)

    # Отметки на осях
    for x in range(-WIDTH // (2 * scale), WIDTH // (2 * scale) + 1):
        pos_x = center_x + x * scale
        if pos_x >= 0 and pos_x <= WIDTH:
            pygame.draw.line(screen, RED, (pos_x, center_y - 5), (pos_x, center_y + 5), 2)
            if x != 0:
                label = font.render(str(x), True, RED)
                screen.blit(label, (pos_x - label.get_width() // 2, center_y + 8))

    for y in range(-HEIGHT // (2 * scale), HEIGHT // (2 * scale) + 1):
        pos_y = center_y - y * scale
        if pos_y >= 0 and pos_y <= HEIGHT:
            pygame.draw.line(screen, RED, (center_x - 5, pos_y), (center_x + 5, pos_y), 2)
            if y != 0:
                label = font.render(str(y), True, RED)
                screen.blit(label, (center_x + 8, pos_y - label.get_height() // 2))

# Преобразование координат в пиксельные координаты на экране
def to_screen(x, y, scale):
    return WIDTH // 2 + x * scale, (HEIGHT // 2 - y * scale)-scale

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Алгоритмы растеризации")

    running = True
    clock = pygame.time.Clock()

    # Примеры для рисования
    x1, y1, x2, y2 = -18, -15, 18, 3
    xc, yc, r = 0, 0, 15

    draw_mode = None
    scale = SCALE
    needs_redraw = False

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:  # Нажатие 1 — Пошаговый алгоритм
                    draw_mode = "Step_by_Step"
                    needs_redraw = True
                elif event.key == pygame.K_2:  # Нажатие 2 — Алгоритм ЦДА
                    draw_mode = "DDA"
                    needs_redraw = True
                elif event.key == pygame.K_3:  # Нажатие 3 — Алгоритм Брезенхема (линия)
                    draw_mode = "Bresenham_Line"
                    needs_redraw = True
                elif event.key == pygame.K_4:  # Нажатие 4 — Алгоритм Брезенхема (окружность)
                    draw_mode = "Bresenham_Circle"
                    needs_redraw = True
                elif event.key == pygame.K_PLUS or event.key == pygame.K_EQUALS:  # Увеличение масштаба
                    scale = min(scale + 5, MAX_SCALE)
                    needs_redraw = True
                elif event.key == pygame.K_MINUS:  # Уменьшение масштаба
                    scale = max(scale - 5, MIN_SCALE)
                    needs_redraw = True

        if needs_redraw:
            screen.fill(WHITE)
            draw_grid(screen, scale)

            start_time = time.perf_counter()
            if draw_mode == "Step_by_Step":
                for (x, y) in step_by_step(x1, y1, x2, y2):
                    pygame.draw.rect(screen, ORANGE, (*to_screen(x, y, scale), scale - 1, scale - 1))
            elif draw_mode == "DDA":
                for (x, y) in dda(x1, y1, x2, y2):
                    pygame.draw.rect(screen, GREEN, (*to_screen(x, y, scale), scale - 1, scale - 1))
            elif draw_mode == "Bresenham_Line":
                for (x, y) in bresenham_line(x1, y1, x2, y2):
                    pygame.draw.rect(screen, BLUE, (*to_screen(x, y, scale), scale - 1, scale - 1))
            elif draw_mode == "Bresenham_Circle":
                for (x, y) in bresenham_circle(xc, yc, r):
                    pygame.draw.rect(screen, RED, (*to_screen(x, y, scale), scale - 1, scale - 1))

            end_time = time.perf_counter()
            execution_time = (end_time - start_time) * 1_000_000

            font = pygame.font.SysFont(None, 30)
            time_label = font.render(f"Время работы: {execution_time:.2f} мс", True, BLACK)
            screen.blit(time_label, (10, 10))

            pygame.display.flip()
            needs_redraw = False

        clock.tick(10)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
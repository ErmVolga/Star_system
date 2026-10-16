import pygame
from settings import WHITE, GREY


# Инициализируем шрифт один раз, чтобы не создавать каждый кадр
_font = None


def _get_font():
    global _font
    if _font is None:
        _font = pygame.font.SysFont("consolas", 18)
    return _font


def draw_hud(screen, dt, steps, extra_lines=None):
    """
    Рисует панель с настройками в левом верхнем углу.

    dt     — текущий шаг физики (с)
    steps  — текущее число подшагов за кадр
    extra_lines — список строк, которые нужно показать дополнительно
    """
    font = _get_font()

    lines = [
        f"dt          = {dt} s",
        f"steps       = {steps}",
        f"за кадр     = {dt * steps / 3600:.2f} ч",
    ]
    if extra_lines:
        lines.extend(extra_lines)

    # Считаем размеры панели под самый длинный текст
    rendered = [font.render(line, True, WHITE) for line in lines]
    pad = 8
    w = max(s.get_width() for s in rendered) + pad * 2
    h = sum(s.get_height() for s in rendered) + pad * 2

    # Полупрозрачный фон
    panel = pygame.Surface((w, h), pygame.SRCALPHA)
    panel.fill((0, 0, 0, 140))
    screen.blit(panel, (10, 10))

    # Рамка
    pygame.draw.rect(screen, GREY, (10, 10, w, h), 1)

    # Текст
    y = 10 + pad
    for s in rendered:
        screen.blit(s, (10 + pad, y))
        y += s.get_height()

def draw_energy_graph(screen, energies, rect=None):
    if not energies:
        return

    if rect is None:
        w, h = 280, 110
        x = screen.get_width() - w - 10
        y = screen.get_height() - h - 10
        rect = (x, y, w, h)
    x, y, w, h = rect

    panel = pygame.Surface((w, h), pygame.SRCALPHA)
    panel.fill((0, 0, 0, 140))
    screen.blit(panel, (x, y))
    pygame.draw.rect(screen, GREY, (x, y, w, h), 1)

    # --- авто-масштаб по Y ---
    emin = min(energies)
    emax = max(energies)

    if not (emax > emin):
        # все значения совпали (или есть NaN) — раздвигаем окно
        # относительно масштаба самих чисел
        s = max(abs(emin), abs(emax), 1.0)
        emin -= s * 0.01
        emax += s * 0.01
    else:
        pad = (emax - emin) * 0.08
        emin -= pad
        emax += pad

    span = emax - emin
    if span == 0:
        span = 1.0

    # --- прореживание по X ---
    n = len(energies)
    if n <= w:
        samples = list(energies)
    else:
        step = n / w
        samples = [energies[int(i * step)] for i in range(w)]

    m = len(samples)
    pts = []
    for i, e in enumerate(samples):
        px = x + int(i * (w - 2) / max(1, m - 1)) + 1
        py = y + h - 2 - int((e - emin) / span * (h - 4))
        pts.append((px, py))

    if len(pts) > 1:
        pygame.draw.lines(screen, (255, 200, 80), False, pts, 1)

    font = pygame.font.SysFont("monospace", 14)
    screen.blit(font.render("E(t)", True, WHITE), (x + 6, y + 4))
    screen.blit(font.render(f"{emax:.3e}", True, WHITE), (x + 6, y + 20))
    screen.blit(font.render(f"{emin:.3e}", True, WHITE), (x + 6, y + h - 18))
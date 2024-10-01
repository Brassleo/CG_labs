import tkinter as tk
from tkinter import colorchooser

updating = False

def update_all(r,g,b,c,m,y,k,h,s,v):
    entry_r.set(r)
    entry_g.set(g)
    entry_b.set(b)

    scale_r.set(r)
    scale_g.set(g)
    scale_b.set(b)

    entry_h.set(h)
    entry_s.set(s)
    entry_v.set(v)

    scale_h.set(h)
    scale_s.set(s)
    scale_v.set(v)

    entry_c.set(c)
    entry_m.set(m)
    entry_y.set(y)
    entry_k.set(k)

    scale_c.set(c)
    scale_m.set(m)
    scale_y.set(y)
    scale_k.set(k)

def validate_entry(value, min_val, max_val):
    try:
        value = int(value)
        if value < min_val:
            return min_val
        elif value > max_val:
            return max_val
        return value
    except ValueError:
        return min_val

def rgb_to_cmyk(r, g, b):
    r, g, b = [x / 255.0 for x in (r, g, b)]
    k = 1 - max(r, g, b)
    c = (1 - r - k) / (1 - k) if k != 1 else 0
    m = (1 - g - k) / (1 - k) if k != 1 else 0
    y = (1 - b - k) / (1 - k) if k != 1 else 0
    return int(c * 100), int(m * 100), int(y * 100), int(k * 100)

def cmyk_to_rgb(c, m, y, k):
    c, m, y, k = [x / 100.0 for x in (c, m, y, k)]
    r = int(255 * (1 - c) * (1 - k))
    g = int(255 * (1 - m) * (1 - k))
    b = int(255 * (1 - y) * (1 - k))
    return r, g, b

def rgb_to_hsv(r, g, b):
    r, g, b = [x / 255.0 for x in (r, g, b)]
    max_val = max(r, g, b)
    min_val = min(r, g, b)
    delta = max_val - min_val

    if delta == 0:
        h = 0
    elif max_val == r:
        h = (60 * ((g - b) / delta) + 360) % 360
    elif max_val == g:
        h = (60 * ((b - r) / delta) + 120) % 360
    elif max_val == b:
        h = (60 * ((r - g) / delta) + 240) % 360

    s = 0 if max_val == 0 else (delta / max_val) * 100

    v = max_val * 100

    return int(h), int(s), int(v)

def hsv_to_rgb(h, s, v):
    s /= 100
    v /= 100
    c = v * s
    x = c * (1 - abs((h / 60) % 2 - 1))
    m = v - c

    if 0 <= h < 60:
        r, g, b = c, x, 0
    elif 60 <= h < 120:
        r, g, b = x, c, 0
    elif 120 <= h < 180:
        r, g, b = 0, c, x
    elif 180 <= h < 240:
        r, g, b = 0, x, c
    elif 240 <= h < 300:
        r, g, b = x, 0, c
    else:
        r, g, b = c, 0, x

    r = int((r + m) * 255)
    g = int((g + m) * 255)
    b = int((b + m) * 255)

    return r, g, b

def update_all_from_rgb(*args):
    global updating
    if updating:
        return
    updating = True
    try:
        r = validate_entry(entry_r.get(), 0, 255)
        g = validate_entry(entry_g.get(), 0, 255)
        b = validate_entry(entry_b.get(), 0, 255)
        h, s, v = rgb_to_hsv(r, g, b)
        c, m, y, k = rgb_to_cmyk(r, g, b)
        update_all(r, g, b, c, m, y, k, h, s, v)


        update_color_display(r, g, b)
    finally:
        updating = False

def update_all_from_hsv(*args):
    global updating
    if updating:
        return
    updating = True
    try:
        h = validate_entry(entry_h.get(), 0, 360)
        s = validate_entry(entry_s.get(), 0, 100)
        v = validate_entry(entry_v.get(), 0, 100)
        r, g, b = hsv_to_rgb(h, s, v)
        c, m, y, k = rgb_to_cmyk(r, g, b)
        update_all(r, g, b, c, m, y, k, h, s, v)


        update_color_display(r, g, b)
    finally:
        updating = False

def update_all_from_cmyk(*args):
    global updating
    if updating:
        return
    updating = True
    try:
        c = validate_entry(entry_c.get(), 0, 100)
        m = validate_entry(entry_m.get(), 0, 100)
        y = validate_entry(entry_y.get(), 0, 100)
        k = validate_entry(entry_k.get(), 0, 100)
        r, g, b = cmyk_to_rgb(c, m, y, k)
        h, s, v = rgb_to_hsv(r, g, b)
        update_all(r, g, b, c, m, y, k, h, s, v)



        update_color_display(r, g, b)
    finally:
        updating = False

def choose_color():
    color = colorchooser.askcolor()[0]
    if color:
        r, g, b = map(int, color)
        entry_r.set(r)
        entry_g.set(g)
        entry_b.set(b)
        update_all_from_rgb()


def update_color_display(r, g, b):
    color_display.config(bg=f'#{r:02x}{g:02x}{b:02x}')

root = tk.Tk()
root.title("Color Picker")

tk.Label(root, text="R").grid(row=0, column=0)
entry_r = tk.IntVar()
entry_r.trace("w", update_all_from_rgb)
tk.Entry(root, textvariable=entry_r).grid(row=0, column=1)
scale_r = tk.Scale(root, from_=0, to=255, orient=tk.HORIZONTAL, variable=entry_r)
scale_r.grid(row=0, column=2)

tk.Label(root, text="G").grid(row=1, column=0)
entry_g = tk.IntVar()
entry_g.trace("w", update_all_from_rgb)
tk.Entry(root, textvariable=entry_g).grid(row=1, column=1)
scale_g = tk.Scale(root, from_=0, to=255, orient=tk.HORIZONTAL, variable=entry_g)
scale_g.grid(row=1, column=2)

tk.Label(root, text="B").grid(row=2, column=0)
entry_b = tk.IntVar()
entry_b.trace("w", update_all_from_rgb)
tk.Entry(root, textvariable=entry_b).grid(row=2, column=1)
scale_b = tk.Scale(root, from_=0, to=255, orient=tk.HORIZONTAL, variable=entry_b)
scale_b.grid(row=2, column=2)

tk.Label(root, text="H").grid(row=3, column=0)
entry_h = tk.IntVar()
entry_h.trace("w", update_all_from_hsv)
tk.Entry(root, textvariable=entry_h).grid(row=3, column=1)
scale_h = tk.Scale(root, from_=0, to=360, orient=tk.HORIZONTAL, variable=entry_h)
scale_h.grid(row=3, column=2)

tk.Label(root, text="S").grid(row=4, column=0)
entry_s = tk.IntVar()
entry_s.trace("w", update_all_from_hsv)
tk.Entry(root, textvariable=entry_s).grid(row=4, column=1)
scale_s = tk.Scale(root, from_=0, to=100, orient=tk.HORIZONTAL, variable=entry_s)
scale_s.grid(row=4, column=2)

tk.Label(root, text="V").grid(row=5, column=0)
entry_v = tk.IntVar()
entry_v.trace("w", update_all_from_hsv)
tk.Entry(root, textvariable=entry_v).grid(row=5, column=1)
scale_v = tk.Scale(root, from_=0, to=100, orient=tk.HORIZONTAL, variable=entry_v)
scale_v.grid(row=5, column=2)

tk.Label(root, text="C").grid(row=6, column=0)
entry_c = tk.IntVar()
entry_c.trace("w", update_all_from_cmyk)
tk.Entry(root, textvariable=entry_c).grid(row=6, column=1)
scale_c = tk.Scale(root, from_=0, to=100, orient=tk.HORIZONTAL, variable=entry_c)
scale_c.grid(row=6, column=2)

tk.Label(root, text="M").grid(row=7, column=0)
entry_m = tk.IntVar()
entry_m.trace("w", update_all_from_cmyk)
tk.Entry(root, textvariable=entry_m).grid(row=7, column=1)
scale_m = tk.Scale(root, from_=0, to=100, orient=tk.HORIZONTAL, variable=entry_m)
scale_m.grid(row=7, column=2)

tk.Label(root, text="Y").grid(row=8, column=0)
entry_y = tk.IntVar()
entry_y.trace("w", update_all_from_cmyk)
tk.Entry(root, textvariable=entry_y).grid(row=8, column=1)
scale_y = tk.Scale(root, from_=0, to=100, orient=tk.HORIZONTAL, variable=entry_y)
scale_y.grid(row=8, column=2)

tk.Label(root, text="K").grid(row=9, column=0)
entry_k = tk.IntVar()
entry_k.trace("w", update_all_from_cmyk)
tk.Entry(root, textvariable=entry_k).grid(row=9, column=1)
scale_k = tk.Scale(root, from_=0, to=100, orient=tk.HORIZONTAL, variable=entry_k)
scale_k.grid(row=9, column=2)

choose_button = tk.Button(root, text="Choose Color", command=choose_color)
choose_button.grid(row=10, column=0, columnspan=3)

color_display = tk.Label(root, text="Selected Color", width=30, height=7)
color_display.grid(row=11, column=0, columnspan=3)

root.mainloop()

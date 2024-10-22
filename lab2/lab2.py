import cv2
import numpy as np
from tkinter import *
from tkinter import filedialog
from PIL import Image, ImageTk


def bernsen_threshold_global(img, contrast_threshold=15):

    global_max = np.max(img)
    global_min = np.min(img)

    global_mid = (global_max.astype(np.float32) + global_min.astype(np.float32)) / 2

    if (global_max - global_min) < contrast_threshold:
        global_mid = np.mean(img)

    img_binarized = np.where(img > global_mid, 255, 0).astype(np.uint8)

    return img_binarized


def apply_filter(filter_type):
    global img_display, img_filtered_display, img_filtered_pil

    if filter_type == "Original":
        img_filtered = img
    elif filter_type == "Median":
        img_filtered = cv2.medianBlur(img, 5)
    elif filter_type == "Gaussian":
        img_filtered = cv2.GaussianBlur(img, (5, 5), 0)
    elif filter_type == "Binary Threshold":
        _, img_filtered = cv2.threshold(img_gray, 128, 255, cv2.THRESH_BINARY)
    elif filter_type == "Binary Inverted Threshold":
        _, img_filtered = cv2.threshold(img_gray, 128, 255, cv2.THRESH_BINARY_INV)
    elif filter_type == "Bernsen":
        img_filtered = bernsen_threshold_global(img_gray, contrast_threshold=15)
    elif filter_type == "Otsu's Threshold":
        _, img_filtered = cv2.threshold(img_gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    if len(img_filtered.shape) == 3:
        img_rgb = cv2.cvtColor(img_filtered, cv2.COLOR_BGR2RGB)
    else:
        img_rgb = cv2.cvtColor(img_filtered, cv2.COLOR_GRAY2RGB)

    img_filtered_pil = Image.fromarray(img_rgb)
    img_filtered_pil = img_filtered_pil.resize((400, 400))
    img_filtered_display = ImageTk.PhotoImage(img_filtered_pil)

    label_filtered_image.config(image=img_filtered_display)
    label_filtered_image.image = img_filtered_display


def load_image():
    global img, img_display, img_gray

    file_path = filedialog.askopenfilename()
    if file_path:
        img = cv2.imread(file_path)
        img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img_pil = Image.fromarray(img_rgb)
        img_pil = img_pil.resize((400, 400))
        img_display = ImageTk.PhotoImage(img_pil)

        label_original_image.config(image=img_display)
        label_original_image.image = img_display

        apply_filter("Original")


def save_image():
    if img_filtered_pil:
        save_path = filedialog.asksaveasfilename(defaultextension=".png",
                                                 filetypes=[("PNG files", "*.png"),
                                                            ("JPEG files", "*.jpg"),
                                                            ("All files", "*.*")])
        if save_path:
            img_filtered_pil.save(save_path)


window = Tk()
window.title("Image Filters and Thresholding")

# Buttons frame
frame_buttons = Frame(window)
frame_buttons.pack(side=TOP, pady=10)

btn_original = Button(frame_buttons, text="Original", command=lambda: apply_filter("Original"))
btn_original.grid(row=0, column=0, padx=5)

btn_median = Button(frame_buttons, text="Median", command=lambda: apply_filter("Median"))
btn_median.grid(row=0, column=1, padx=5)

btn_gaussian = Button(frame_buttons, text="Gaussian", command=lambda: apply_filter("Gaussian"))
btn_gaussian.grid(row=0, column=2, padx=5)

btn_binary = Button(frame_buttons, text="Binary Threshold (th=128)", command=lambda: apply_filter("Binary Threshold"))
btn_binary.grid(row=1, column=0, padx=5)

btn_binary_inv = Button(frame_buttons, text="Inverted Binary (th=128)", command=lambda: apply_filter("Binary Inverted Threshold"))
btn_binary_inv.grid(row=1, column=1, padx=5)

btn_bernsen = Button(frame_buttons, text="Bernsen", command=lambda: apply_filter("Bernsen"))
btn_bernsen.grid(row=1, column=2, padx=5)

btn_otsu = Button(frame_buttons, text="Otsu", command=lambda: apply_filter("Otsu's Threshold"))
btn_otsu.grid(row=1, column=3, padx=5)

btn_load = Button(window, text="Load Image", command=load_image)
btn_load.pack(side=TOP, pady=10)

btn_save = Button(window, text="Save Image", command=save_image)
btn_save.pack(side=TOP, pady=10)

frame_images = Frame(window)
frame_images.pack(side=TOP, pady=10)

label_original_image = Label(frame_images)
label_original_image.grid(row=0, column=0, padx=10)

label_filtered_image = Label(frame_images)
label_filtered_image.grid(row=0, column=1, padx=10)

window.mainloop()
import tkinter as tk
from tkinter import messagebox
import qrcode
from PIL import Image, ImageDraw, ImageFont
import pandas as pd
import os

# Excel setup
excel_file = "storage_data.xlsx"
if not os.path.exists(excel_file):
    df = pd.DataFrame(columns=["Box Name", "Contents"])
    df.to_excel(excel_file, index=False)

# Add row to Excel and return row number
def save_data(box_name, contents):
    df = pd.read_excel(excel_file)
    new_row = {"Box Name": box_name, "Contents": contents}
    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
    df.to_excel(excel_file, index=False)
    return len(df)

# QR code generator with number underneath
def generate_qr(row_number):
    url = f"https://yourdomain.com/box/{row_number}"
    qr = qrcode.make(url)

    # Add number under QR
    img = qr.convert("RGB")
    draw = ImageDraw.Draw(img)
    font = ImageFont.load_default()
    text = f"Box #{row_number}"
    text_width, text_height = draw.textsize(text, font)
    new_img = Image.new("RGB", (img.width, img.height + 20), "white")
    new_img.paste(img, (0, 0))
    draw = ImageDraw.Draw(new_img)
    draw.text(((img.width - text_width) / 2, img.height), text, fill="black", font=font)

    filename = f"qr_codes/box_{row_number}.png"
    os.makedirs("qr_codes", exist_ok=True)
    new_img.save(filename)
    return filename

# GUI
def submit():
    box_name = entry_box.get()
    contents = entry_contents.get()
    if not box_name or not contents:
        messagebox.showwarning("Missing data", "Please enter both fields")
        return
    row_number = save_data(box_name, contents)
    file = generate_qr(row_number)
    messagebox.showinfo("QR Code Created", f"Saved as {file}")

# Tkinter GUI
root = tk.Tk()
root.title("Storage QR Code Creator")

tk.Label(root, text="Box Name:").grid(row=0, column=0)
entry_box = tk.Entry(root, width=50)
entry_box.grid(row=0, column=1)

tk.Label(root, text="Contents:").grid(row=1, column=0)
entry_contents = tk.Entry(root, width=50)
entry_contents.grid(row=1, column=1)

tk.Button(root, text="Generate QR", command=submit).grid(row=2, column=0, columnspan=2)

root.mainloop()
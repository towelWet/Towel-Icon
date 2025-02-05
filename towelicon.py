import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image
import subprocess
import sys
import os

def convert_image_to_ico(input_path: str, output_path: str) -> None:
    """
    Converts the given input image to Windows .ico format using Pillow.

    :param input_path: The file path to the input image.
    :param output_path: The desired output file path ending with '.ico'.
    """
    image = Image.open(input_path)
    image.save(output_path, format='ICO', sizes=[(256, 256), (128, 128), (64, 64), (32, 32), (16, 16)])

def convert_image_to_icns(input_path: str, output_path: str) -> None:
    """
    Converts the given input image to Mac .icns format using the macOS 'sips' command.
    Note: This function only works on macOS.

    :param input_path: The file path to the input image.
    :param output_path: The desired output file path ending with '.icns'.
    """
    if sys.platform != "darwin":
        messagebox.showerror("Error", "ICNS conversion is only supported on macOS.")
        return
    # macOS command using sips to create an icns file
    subprocess.run(["sips", "-s", "format", "icns", input_path, "--out", output_path], check=True)

class ImageConverterApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Image Converter")
        self.master.geometry("400x300")

        self.input_file_path = tk.StringVar()
        self.output_format = tk.StringVar(value="ICO")

        # Input file selection
        tk.Label(master, text="Select Image File:").pack(pady=5)
        tk.Entry(master, textvariable=self.input_file_path, width=40).pack()
        tk.Button(master, text="Browse", command=self.browse_input_file).pack(pady=5)

        # Output format selection
        tk.Label(master, text="Select Output Format:").pack(pady=5)
        tk.Radiobutton(master, text=".ICO (Windows)", variable=self.output_format, value="ICO").pack()
        tk.Radiobutton(master, text=".ICNS (Mac)", variable=self.output_format, value="ICNS").pack()

        # Convert button
        tk.Button(master, text="Convert", command=self.convert_image).pack(pady=10)

    def browse_input_file(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("Image files", "*.jpg *.jpeg *.png *.gif *.bmp")]
        )
        self.input_file_path.set(file_path)

    def convert_image(self):
        if not self.input_file_path.get():
            messagebox.showerror("Error", "Please select an image file.")
            return

        input_path = self.input_file_path.get()
        file_ext = ".ico" if self.output_format.get() == "ICO" else ".icns"
        output_path = filedialog.asksaveasfilename(
            defaultextension=file_ext,
            filetypes=[(f"{file_ext.upper()} files", f"*{file_ext}")]
        )

        if not output_path:
            return  # User canceled

        try:
            if self.output_format.get() == "ICO":
                convert_image_to_ico(input_path, output_path)
            else:
                convert_image_to_icns(input_path, output_path)
            messagebox.showinfo("Success", f"Successfully converted to {self.output_format.get()}!")
        except Exception as e:
            messagebox.showerror("Conversion Error", f"Error converting file: {e}")

def main():
    root = tk.Tk()
    app = ImageConverterApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()

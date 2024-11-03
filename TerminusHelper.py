import os
from tkinter import Tk, Label, Frame, Button
from PIL import Image, ImageTk

class TerminusCode:
    def __init__(self, root):
        self.root = root
        self.root.title("Symbol Box")

        self.bg_color = "#111111"  # Unified background color for the application
        self.root.configure(bg=self.bg_color)

        self.selected_values = {'x': 0, 'y': 0, 'z': 0, 'Clock': 0, 'Card': 0, 'Days': 0}
        self.selected_buttons = {'x': None, 'y': None, 'z': None, 'Clock': None, 'Card': None, 'Days': None}

        self.images = {}
        self.load_images()

        self.symbol_box_color = "#888888"  # Offshade for symbol boxes
        self.number_box_color = "#999999"   # Offshade for number boxes
        self.button_color = "#777777"        # Offshade for buttons
        self.highlight_color = "orange"      # Highlight color for selected buttons
        self.result_bg_color = "#aaaaaa"     # Unified background for math outputs

        symbol_frame = Frame(root, bg=self.bg_color)
        symbol_frame.pack(pady=10)

        self.create_symbol_box(symbol_frame, 'x')
        self.create_symbol_box(symbol_frame, 'y')
        self.create_symbol_box(symbol_frame, 'z')

        self.result_frame = Frame(root, bg=self.bg_color)
        self.result_frame.pack(pady=10)

        # Unified shaded background for the results
        self.result_background = Frame(self.result_frame, bg=self.result_bg_color)
        self.result_background.pack(pady=3)

        self.result1_label = Label(self.result_background, text="00", font=("Arial", 20, "bold"), width=4, bg=self.result_bg_color)
        self.result1_label.grid(row=0, column=0, padx=10)

        self.result2_label = Label(self.result_background, text="00", font=("Arial", 20, "bold"), width=4, bg=self.result_bg_color)
        self.result2_label.grid(row=0, column=1, padx=10)

        self.result3_label = Label(self.result_background, text="00", font=("Arial", 20, "bold"), width=4, bg=self.result_bg_color)
        self.result3_label.grid(row=0, column=2, padx=10)

        self.num_selection_frame = Frame(root, bg=self.bg_color)
        self.num_selection_frame.pack(pady=10)

        self.create_number_box(self.num_selection_frame, 'Clock')
        self.create_number_box(self.num_selection_frame, 'Card')
        self.create_number_box(self.num_selection_frame, 'Days')

        self.reset_button = Button(root, text="Reset", font=("Arial", 12), command=self.reset, relief="flat", bg=self.button_color)
        self.reset_button.pack(pady=10)

    def load_images(self):
        folder_path = "symbols"
        image_files = ["0.png", "11.png", "10.png", "22.png", "21.png", "20.png"]
        
        for file in image_files:
            file_path = os.path.join(folder_path, file)
            if os.path.exists(file_path):
                img = Image.open(file_path)
                img.thumbnail((50, 50))
                self.images[file] = ImageTk.PhotoImage(img)

    def create_symbol_box(self, parent_frame, var_name):
        frame = Frame(parent_frame, bg=self.symbol_box_color)
        frame.pack(side="left", padx=5)

        # Display only the letter (x, y, z) in a larger font
        title_label = Label(frame, text=var_name.upper(), font=("Arial", 24, "bold"), bg=self.symbol_box_color)
        title_label.grid(row=0, column=0, columnspan=3, pady=10)

        positions = [(1, 0), (1, 1), (1, 2), (2, 0), (2, 1), (2, 2)]
        for idx, (row, col) in enumerate(positions):
            image_name = list(self.images.keys())[idx]
            self.create_button(frame, image_name, var_name, row, col)

    def create_button(self, frame, image_name, var_name, row, col):
        button = Button(frame, image=self.images[image_name], 
                        command=lambda: self.on_click(image_name, var_name, button), 
                        relief="flat", bg=self.button_color)
        button.grid(row=row, column=col, padx=2, pady=2)

    def on_click(self, image_name, var_name, button):
        if self.selected_buttons[var_name]:
            self.selected_buttons[var_name].config(bg=self.button_color)
        
        button.config(bg=self.highlight_color)
        self.selected_buttons[var_name] = button
        
        image_number = int(os.path.splitext(image_name)[0])
        self.selected_values[var_name] = image_number
        self.update_math_results()

    def update_math_results(self):
        x = self.selected_values.get('x', 0)
        y = self.selected_values.get('y', 0)
        z = self.selected_values.get('z', 0)

        result1 = f"{2 * x + 11:02}"
        result2 = f"{(2 * z + y) - 5:02}"
        result3 = f"{abs((y + z) - x):02}"

        self.result1_label.config(text=result1)
        self.result2_label.config(text=result2)
        self.result3_label.config(text=result3)

    def create_number_box(self, parent_frame, name):
        frame = Frame(parent_frame, bg=self.number_box_color)
        frame.pack(side="left", padx=5)

        title_label = Label(frame, text=name, font=("Arial", 16, "bold"), bg=self.number_box_color)
        title_label.grid(row=0, column=0, columnspan=10, pady=3)

        self.selected_buttons[name] = None
        for num in range(10):
            button = Button(frame, text=str(num), font=("Arial", 12, "bold"), relief="flat", bg=self.button_color)

            def button_command(num=num, name=name, btn=button):
                self.on_number_click(num, name, btn)

            button.config(command=button_command)
            button.grid(row=1, column=num, padx=0, pady=2)

    def on_number_click(self, number, name, button):
        if self.selected_buttons[name]:
            self.selected_buttons[name].config(bg=self.button_color)
        
        button.config(bg=self.highlight_color)
        self.selected_buttons[name] = button

    def reset(self):
        for key in self.selected_values.keys():
            self.selected_values[key] = 0

        for key in self.selected_buttons.keys():
            if self.selected_buttons[key]:
                self.selected_buttons[key].config(bg=self.button_color)
            self.selected_buttons[key] = None
        
        self.result1_label.config(text="00")
        self.result2_label.config(text="00")
        self.result3_label.config(text="00")

if __name__ == "__main__":
    root = Tk()
    app = TerminusCode(root)
    root.mainloop()

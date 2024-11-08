import customtkinter as ctk
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.animation import FuncAnimation
from encoding_methods import nrz_l, nrz_i, bipolar_ami, pseudoternary, manchester, differential_manchester

ctk.set_appearance_mode("System")  # Modes: "System" (default), "Dark", "Light"
ctk.set_default_color_theme("blue")  # Themes: "blue" (default), "green", "dark-blue"


def show_info():
    info_window = ctk.CTkToplevel(app)
    info_window.title("Encoding Techniques Guide")
    info_window.geometry("500x450")  # Adjust size as needed
    info_window.transient(app)  # Keep window in front of the main window
    info_window.focus_set()  # Give the info window focus

    # Guide content with improved formatting
    guide_text = (
        "-- Digital Data Encoding Techniques Guide --\n"
        "Jose Elijah M. Fernandez | BSCS - 4 \n"
        "F1 - Data Communications and Networking\n\n"
        "1) Non Return-to-Zero Level (NRZ-L)\n"
        "   • 0 → Low level\n"
        "   • 1 → High level\n\n"
        "2) Non Return-to-Zero Inverted (NRZ-I)\n"
        "   • 0 → No transition at beginning\n"
        "   • 1 → Transition at beginning\n\n"
        "3) Bipolar AMI (Alternate Mark Inversion)\n"
        "   • 0 → No line signal\n"
        "   • 1 → Positive or negative level, alternates\n\n"
        "4) Pseudoternary\n"
        "   • 0 → Alternates level\n"
        "   • 1 → No signal\n\n"
        "5) Manchester\n"
        "   • 0 → High to low transition at center\n"
        "   • 1 → Low to high transition at center\n\n"
        "6) Differential Manchester\n"
        "   • 0 → Transition at start\n"
        "   • 1 → No transition at start\n"
        "   • Always transitions at center\n"
    )

    # Create and display the guide label with left alignment
    info_label = ctk.CTkLabel(info_window, text=guide_text, anchor="w", justify="left")
    info_label.pack(padx=10, pady=10, fill="both")


class EncodingApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Encoding Visualization")
        self.geometry("800x600")
        self.resizable(False, False)  # Lock window size

        # Menu bar
        self.menu_frame = ctk.CTkFrame(self, height=30, width=600, corner_radius=0)
        self.menu_frame.pack(side="top", fill="x")

        # Info menu button
        self.info_button = ctk.CTkButton(self.menu_frame, text="Info", command=show_info, width=50)
        self.info_button.pack(side="left", padx=10, pady=5)

        # Widgets
        self.label = ctk.CTkLabel(self, text="Enter Bit Stream (e.g., 01001110):")
        self.label.pack(pady=10)

        self.entry = ctk.CTkEntry(self, width=200)
        self.entry.pack(pady=5)

        self.encoding_options = ["NRZ-L", "NRZ-I", "Bipolar AMI", "Pseudoternary", "Manchester",
                                 "Differential Manchester"]
        self.selected_encoding = ctk.StringVar(value="NRZ-L")
        self.option_menu = ctk.CTkOptionMenu(self, variable=self.selected_encoding, values=self.encoding_options)
        self.option_menu.pack(pady=10)

        self.plot_button = ctk.CTkButton(self, text="Animate Encoding", command=self.animate_encoding)
        self.plot_button.pack(pady=20)

        # Canvas for matplotlib figure
        self.figure = plt.Figure(figsize=(8, 4))  # Increase figure size
        plt.grid(True)
        self.canvas = FigureCanvasTkAgg(self.figure, self)
        self.canvas.get_tk_widget().pack(fill="both", expand=True, padx=10, pady=20)  # Fill more space in the window

        self.anim = None  # Initialize animation object

    def animate_encoding(self):
        # Stop any existing animation before starting a new one
        if self.anim:
            self.anim.event_source.stop()

        bit_stream = self.entry.get()

        # Check for non-numeric characters
        if not bit_stream.isdigit():
            self.show_error("Invalid characters! Please use only 0 or 1.")
            return

        # Check for invalid digits (2-9)
        if any(char in '23456789' for char in bit_stream):
            self.show_error("Input 0 or 1 digits only!")
            return

        try:
            data = np.array([int(bit) for bit in bit_stream], dtype=int)
        except ValueError:
            self.show_error("Invalid bit stream! Please enter a binary string.")
            return

        encoding = self.selected_encoding.get()
        self.figure.clf()  # Clear previous plot
        ax = self.figure.add_subplot(111)
        ax.set_xticks(range(len(data)))
        ax.set_xticklabels(data)  # Display binary data as x-ticks
        ax.get_yaxis().set_visible(False)  # Remove Y-axis coordinates
        ax.set_ylim(-1.5, 1.5)
        ax.grid(True)

        # Select the encoding function based on the user selection
        if encoding == "NRZ-L":
            signal = nrz_l(data)
            ax.set_title("NRZ-L Encoding")

        elif encoding == "NRZ-I":
            signal = nrz_i(data)
            ax.set_title("NRZ-I Encoding")

        elif encoding == "Bipolar AMI":
            signal = bipolar_ami(data)
            ax.set_title("Bipolar AMI Encoding")

        elif encoding == "Pseudoternary":
            signal = pseudoternary(data)
            ax.set_title("Pseudoternary Encoding")

        elif encoding == "Manchester":
            x_values, y_values = manchester(data)
            ax.set_title("Manchester Encoding")
            self.animated_plot(ax, x_values, y_values)
            return

        elif encoding == "Differential Manchester":
            x_values, y_values = differential_manchester(data)
            ax.set_title("Differential Manchester Encoding")
            self.animated_plot(ax, x_values, y_values)
            return

        # Animate the plot for NRZ-L, NRZ-I, Bipolar AMI, and Pseudoternary encodings
        self.animated_plot(ax, range(len(signal)), signal)

    def animated_plot(self, ax, x_values, y_values):
        line, = ax.step([], [], where="post")

        # Function to update the plot data at each frame
        def update(frame):
            line.set_data(x_values[:frame], y_values[:frame])
            return line,

        # Function to restart the animation after it completes
        def restart_animation():
            self.anim.event_source.stop()
            self.after(2000, lambda: self.anim.event_source.start())  # Wait 2 seconds before restarting

        # Run the animation with an interval between frames
        self.anim = FuncAnimation(self.figure, update, frames=len(x_values) + 1, interval=300, blit=True, repeat=True)
        self.anim._stop = restart_animation  # Set the custom stop function
        self.canvas.draw()  # Update the canvas with the animated plot

    def show_error(self, message):
        error_window = ctk.CTkToplevel(self)
        error_window.title("Error")
        error_window.geometry("300x100")
        error_window.transient(self)  # Make the window stay in front of the main window
        error_window.grab_set()  # Make the error window modal
        error_window.focus_set()  # Give the error window focus

        # Center the error window relative to the main window
        x = self.winfo_x() + (self.winfo_width() // 2) - (300 // 2)
        y = self.winfo_y() + (self.winfo_height() // 2) - (100 // 2)
        error_window.geometry(f"300x100+{x}+{y}")

        label = ctk.CTkLabel(error_window, text=message)
        label.pack(pady=20)
        button = ctk.CTkButton(error_window, text="Close", command=error_window.destroy)
        button.pack(pady=5)


if __name__ == "__main__":
    app = EncodingApp()
    app.mainloop()

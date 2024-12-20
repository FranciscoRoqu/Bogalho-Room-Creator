import tkinter as tk
import os

# Constants
GRID_SIZE = 16

def draw_grid(canvas, width, height):
    """Draws a 16x16 grid on the canvas."""
    for x in range(0, width, GRID_SIZE):
        canvas.create_line(x, 0, x, height, fill="gray")  # Vertical lines
    for y in range(0, height, GRID_SIZE):
        canvas.create_line(0, y, width, y, fill="gray")  # Horizontal lines


def main():
    # Initialize the main window
    root = tk.Tk()
    root.title("Room Designer")

    # Start in fullscreen mode
    root.attributes('-fullscreen', True)

    # Get screen dimensions
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    # Create a canvas for the room
    canvas = tk.Canvas(root, bg="white")
    canvas.pack(side="left", fill="both", expand=True)

    # Draw the grid
    draw_grid(canvas, screen_width - 200, screen_height)

    # Create a frame for the sidebar
    sidebar_width = 200
    sidebar = tk.Frame(root, width=sidebar_width, bg="lightgray")
    sidebar.pack(side="right", fill="y")

    # Create a canvas and scroll bar for the sidebar
    sidebar_canvas = tk.Canvas(sidebar, width=sidebar_width, height=screen_height, bg="lightgray")
    sidebar_canvas.pack(side="left", fill="both", expand=True)
    scroll = tk.Scrollbar(sidebar, orient="vertical", command=sidebar_canvas.yview)
    scroll.pack(side="right", fill="y")
    sidebar_canvas.configure(yscrollcommand=scroll.set)

    # Create a frame inside the canvas for widgets
    sidebar_frame = tk.Frame(sidebar_canvas, bg="lightgray")
    sidebar_canvas.create_window((0, 0), window=sidebar_frame, anchor="nw")

    # Find the main gamefiles folder
    main_dir = None
    for directory in os.listdir():
        if os.path.isdir(directory) and directory == "gamefiles":
            main_dir = directory
            break

    # If the main folder is found, find the objects folder inside another folder
    if main_dir:
        objects_dir = None
        for subdir in os.listdir(main_dir):
            subdir_path = os.path.join(main_dir, subdir)
            if os.path.isdir(subdir_path):
                for directory in os.listdir(subdir_path):
                    if os.path.isdir(os.path.join(subdir_path, directory)) and directory == "objects":
                        objects_dir = os.path.join(subdir_path, directory)
                        break
                if objects_dir:
                    break

    # If the objects folder is found, get a list of all folders inside it
    if objects_dir:
        objects = [folder for folder in os.listdir(objects_dir) if os.path.isdir(os.path.join(objects_dir, folder))]

    # Add object buttons to the sidebar
    for obj in objects:
        btn = tk.Button(sidebar_frame, text=obj, width=20)
        btn.pack(pady=5)

    # Function to start dragging an object
    def drag_start(event):
        global dragged_object
        dragged_object = canvas.create_rectangle(0, 0, GRID_SIZE, GRID_SIZE, fill="blue")

    # Function to move the dragged object
    def drag_move(event):
        global dragged_object
        x = event.x - GRID_SIZE // 2
        y = event.y - GRID_SIZE // 2
        canvas.coords(dragged_object, x, y, x + GRID_SIZE, y + GRID_SIZE)

    # Function to drop an object centered at the cursor position
    def drag_end(event):
        global dragged_object
        canvas.delete(dragged_object)
        x = canvas.winfo_pointerx() - canvas.winfo_rootx() - GRID_SIZE // 2
        y = canvas.winfo_pointery() - canvas.winfo_rooty() - GRID_SIZE // 2
        canvas.create_rectangle(x, y, x + GRID_SIZE, y + GRID_SIZE, fill="blue")

    # Bind drag functions to each button
    for child in sidebar_frame.winfo_children():
        child.bind("<ButtonPress-1>", drag_start)
        child.bind("<B1-Motion>", drag_move)
        child.bind("<ButtonRelease-1>", drag_end)

    # Update scrollregion after adding widgets
    sidebar_frame.update_idletasks()
    sidebar_canvas.config(scrollregion=sidebar_canvas.bbox("all"))

    # Zooming functionality
    def zoom(event):
        scale = 1.0
        if event.delta > 0:
            scale *= 1.1
        elif event.delta < 0:
            scale /= 1.1
        canvas.scale("all", event.x, event.y, scale, scale)
        canvas.configure(scrollregion=canvas.bbox("all"))

    # Fullscreen toggle function
    def toggle_fullscreen(event=None):
        fullscreen_state = root.attributes('-fullscreen')
        root.attributes('-fullscreen', not fullscreen_state)

    # Move canvas with arrow keys
    def move_canvas(event):
        move_amount = 10
        if event.keysym == "Up":
            canvas.move("all", 0, move_amount)
        elif event.keysym == "Down":
            canvas.move("all", 0, -move_amount)
        elif event.keysym == "Left":
            canvas.move("all", move_amount, 0)
        elif event.keysym == "Right":
            canvas.move("all", -move_amount, 0)

    # Bind keys
    root.bind("<Escape>", lambda event: root.attributes('-fullscreen', False))  # Exit fullscreen
    root.bind("<F11>", toggle_fullscreen)  # Toggle fullscreen
    root.bind("<Button-4>", zoom)  # For Linux systems
    root.bind("<Button-5>", zoom)  # For Linux systems
    root.bind("<MouseWheel>", zoom)  # For Windows systems
    root.bind("<Up>", move_canvas)
    root.bind("<Down>", move_canvas)
    root.bind("<Left>", move_canvas)
    root.bind("<Right>", move_canvas)

    # Follow the mouse
    def follow_mouse(event):
        global dragged_object
        x = event.x - GRID_SIZE // 2
        y = event.y - GRID_SIZE // 2
        canvas.coords(dragged_object, x, y, x + GRID_SIZE, y + GRID_SIZE)

    root.bind("<Motion>", follow_mouse)

    # Run the application
    root.mainloop()


if __name__ == "__main__":
    main()
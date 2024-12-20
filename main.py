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

    # Create a frame for the toolbar
    toolbar = tk.Frame(root, bg="black", height=30)
    toolbar.pack(side="top", fill="x")

    # Variable to keep track of the selected tool
    selected_tool = tk.StringVar(value="Select")

    # Create a label to show the selected tool
    selected_tool_label = tk.Label(toolbar, textvariable=selected_tool, bg="black", fg="white")
    selected_tool_label.pack(side="right", padx=10)

    # Function to update the selected tool
    def update_tool(tool_name):
        selected_tool.set(tool_name)

    # Create buttons for the toolbar
    select_button = tk.Button(toolbar, text="Select", width=20, command=lambda: update_tool("Select"))
    select_button.pack(side="left", padx=5)
    move_button = tk.Button(toolbar, text="Move", width=20, command=lambda: update_tool("Move"))
    move_button.pack(side="left", padx=5)
    scale_button = tk.Button(toolbar, text="Scale", width=20, command=lambda: update_tool("Scale"))
    scale_button.pack(side="left", padx=5)

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

    # Create a search bar
    search_bar = tk.Entry(sidebar, width=20)
    search_bar.pack(side="top", padx=10, pady=10)

    # Create a label to display the search results
    search_results_label = tk.Label(sidebar, text="Search Results:")
    search_results_label.pack(side="top", padx=10, pady=10)

    # Create a text box to display the search results
    search_results_text = tk.Text(sidebar, width=20, height=10)
    search_results_text.pack(side="top", padx=10, pady=10)

    # Function to filter the search results
    def filter_search_results():
        search_query = search_bar.get()
        # Filter the results based on the search query
        # For example, you can use a list of items and filter it based on the search query
        items = objects
        filtered_items = [item for item in items if search_query.lower() in item.lower()]
        # Display the filtered results in the text box
        search_results_text.delete(1.0, tk.END)
        if filtered_items:
            for item in filtered_items:
                search_results_text.insert(tk.END, item + "\n")
        else:
            search_results_text.insert(tk.END, "No results found")

        # Create a canvas to display the draggable objects
        canvas = tk.Canvas(sidebar, width=200, height=200)
        canvas.pack(side="bottom")

        # Create a list to store the draggable objects
        draggable_objects = []

        # Function to create a draggable object
        def create_draggable_object(item, x, y):
            obj = canvas.create_rectangle(x, y, x + 40, y + 40, fill="blue")
            canvas.create_text(x + 20, y + 20, text=item)
            draggable_objects.append(obj)
        
            # Function to handle the dragging behavior
            def drag_start(event):
                canvas.scan_mark(event.x, event.y)
        
            def drag_move(event):
                canvas.scan_dragto(event.x, event.y, gain=1)
        
            canvas.tag_bind(obj, "<Button-1>", drag_start)
            canvas.tag_bind(obj, "<B1-Motion>", drag_move)
        
        # Create a draggable object for each filtered item
        x = 10
        y = 10
        for item in filtered_items:
            create_draggable_object(item, x, y)
            x += 50
            if x > 150:
                x = 10
                y += 50

        canvas.tag_bind(obj, "<Button-1>", drag_start)
        canvas.tag_bind(obj, "<B1-Motion>", drag_move)

        # Create a draggable object for each filtered item
        for item in filtered_items:
            create_draggable_object(item)

    # Create a button to trigger the search
    search_button = tk.Button(sidebar, text="Search", command=filter_search_results)
    search_button.pack(side="top", padx=10, pady=10)
    
    object_data = {}
    object_counter = 0

    def create_object(x, y, name):
        global object_counter, object_data
        object_id = f"obj_{object_counter}"
        object_counter += 1

        # Create the object on the canvas
        canvas_object = canvas.create_rectangle(
            x, y, x + GRID_SIZE, y + GRID_SIZE, fill="blue", tags=(object_id, "object")
        )

        # Store metadata
        object_data[object_id] = {
            "name": name,
            "canvas_id": canvas_object,
            "x": x,
            "y": y,
        }
        print(f"Created {name} with ID {object_id} at ({x}, {y})")


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
    dragged_object = None  # Declare globally
    
    def drag_start(event, name):
        global dragged_object
        dragged_object = canvas.create_rectangle(0, 0, GRID_SIZE, GRID_SIZE, fill="blue", tags=("preview",))
        dragged_object_name.set(name)  # Store the object's name


    # Function to move the dragged object
    def drag_move(event):
        global dragged_object
        x = canvas.winfo_pointerx() - canvas.winfo_rootx() - GRID_SIZE // 2
        y = canvas.winfo_pointery() - canvas.winfo_rooty() - GRID_SIZE // 2
        canvas.coords(dragged_object, x, y, x + GRID_SIZE, y + GRID_SIZE)

    # Function to drop an object centered at the cursor position
    dragged_object_name = tk.StringVar()  # Store the current object name globally

    def drag_end(event):
        global dragged_object
        if dragged_object:
            # Delete the preview rectangle
            canvas.delete(dragged_object)

            # Get the drop position
            x = canvas.winfo_pointerx() - canvas.winfo_rootx() - GRID_SIZE // 2
            y = canvas.winfo_pointery() - canvas.winfo_rooty() - GRID_SIZE // 2

            # Use the stored name to create the object
            create_object(x, y, dragged_object_name.get())
            dragged_object = None


    def delete_object_by_id(object_id):
        if object_id in object_data:
            canvas.delete(object_data[object_id]["canvas_id"])
            del object_data[object_id]
            print(f"Deleted object with ID {object_id}")
        else:
            print(f"Object with ID {object_id} not found")


    root.bind("<BackSpace>", delete_object_by_id)  # Bind delete all objects function to the backspace key (objects)
    for obj in objects:
        print(f"Found object: {obj}")
        btn = tk.Button(sidebar_frame, text=obj, width=20)
        btn.pack(pady=5)
    # Bind drag functions to each button
    for child in sidebar_frame.winfo_children():
        btn.bind("<ButtonPress-1>", lambda event, name=obj: drag_start(event, name))
        btn.bind("<B1-Motion>", drag_move)
        btn.bind("<ButtonRelease-1>", drag_end)

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
        x = canvas.winfo_pointerx() - canvas.winfo_rootx() - GRID_SIZE // 2
        y = canvas.winfo_pointery() - canvas.winfo_rooty() - GRID_SIZE // 2
        canvas.coords(dragged_object, x, y, x + GRID_SIZE, y + GRID_SIZE)

    root.bind("<Motion>", follow_mouse)

    # Run the application
    root.mainloop()



if __name__ == "__main__":
    main()
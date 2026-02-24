import os
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from PIL import Image, ImageTk
import re

# Constants
SPRITE_WIDTH = 128
SPRITE_HEIGHT = 256
SPRITE_IMAGES_DIRECTORY = os.path.join("../../resources", "tile_images")
OUTPUT_DIRECTORY = os.path.join("../../output", "manual_sprites")

# Movement offsets (in pixels) - 32x32 isometric grid
HORIZONTAL_OFFSET = 32
VERTICAL_OFFSET = 32

# Dark theme colors
BG_COLOR = "#1e1e1e"
FG_COLOR = "#d4d4d4"
CANVAS_BG = "#252526"
GRID_COLOR = "#3e3e42"
HIGHLIGHT_COLOR = "#007acc"
BUTTON_BG = "#333333"
BUTTON_FG = "#ffffff"


class SpriteItem:
    """Represents a sprite with its position and image."""
    
    def __init__(self, sprite_name, x=0, y=0):
        self.sprite_name = sprite_name
        self.x = x
        self.y = y
        self.image = None
        self.photo_image = None
        self.canvas_id = None
        self.load_image()
    
    def load_image(self):
        """Load the sprite image from disk."""
        image_path = os.path.join(SPRITE_IMAGES_DIRECTORY, f"{self.sprite_name}.png")
        if os.path.isfile(image_path):
            self.image = Image.open(image_path).convert("RGBA")
        else:
            # Create a placeholder image if sprite not found
            self.image = Image.new("RGBA", (SPRITE_WIDTH, SPRITE_HEIGHT), (255, 0, 0, 128))
    
    def get_photo_image(self):
        """Get PhotoImage for tkinter display."""
        if self.image:
            return ImageTk.PhotoImage(self.image)
        return None


class ManualTileStitcher:
    """Main application for manual tile stitching."""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Manual Tile Stitcher")
        self.root.geometry("1400x800")
        
        self.sprites = []
        self.selected_sprite_index = None
        self.canvas_images = []
        self.loaded_sprite_names_ordered = []
        self.original_expression_string = ""
        
        # Drag and drop state
        self.dragging = False
        self.drag_start_x = 0
        self.drag_start_y = 0
        self.drag_sprite_index = None
        
        self.setup_ui()
        self.apply_dark_theme()
    
    def apply_dark_theme(self):
        """Apply dark theme to the application."""
        self.root.configure(bg=BG_COLOR)
        
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure dark theme colors
        style.configure(".", background=BG_COLOR, foreground=FG_COLOR, fieldbackground=BG_COLOR)
        style.configure("TFrame", background=BG_COLOR)
        style.configure("TLabel", background=BG_COLOR, foreground=FG_COLOR)
        style.configure("TLabelframe", background=BG_COLOR, foreground=FG_COLOR)
        style.configure("TLabelframe.Label", background=BG_COLOR, foreground=FG_COLOR)
        style.configure("TButton", background=BUTTON_BG, foreground=BUTTON_FG, borderwidth=1)
        style.map("TButton", background=[("active", HIGHLIGHT_COLOR)])
        style.configure("Accent.TButton", background=HIGHLIGHT_COLOR, foreground=BUTTON_FG)
        style.map("Accent.TButton", background=[("active", "#005a9e")])
    
    def setup_ui(self):
        """Set up the user interface."""
        # Main container
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Left panel (input)
        left_frame = ttk.Frame(main_frame, width=300)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, padx=(0, 10))
        left_frame.pack_propagate(False)
        
        # Input label
        ttk.Label(left_frame, text="Sprite Names:", font=("Arial", 12, "bold")).pack(pady=(0, 5))
        ttk.Label(left_frame, text="(one per line or +separated)", font=("Arial", 9)).pack(pady=(0, 10))
        
        # Text input area
        self.text_input = scrolledtext.ScrolledText(
            left_frame, width=35, height=20,
            bg="#2d2d2d", fg=FG_COLOR, insertbackground=FG_COLOR,
            selectbackground=HIGHLIGHT_COLOR, selectforeground=FG_COLOR
        )
        self.text_input.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # Load button
        ttk.Button(left_frame, text="Load Sprites", command=self.load_sprites).pack(fill=tk.X, pady=(0, 10))
        
        # Control instructions
        instructions_frame = ttk.LabelFrame(left_frame, text="Controls", padding=10)
        instructions_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(instructions_frame, text="• Click sprite to select", font=("Arial", 9)).pack(anchor=tk.W)
        ttk.Label(instructions_frame, text="• Use arrows to move", font=("Arial", 9)).pack(anchor=tk.W)
        ttk.Label(instructions_frame, text="• Keyboard arrows also work", font=("Arial", 9)).pack(anchor=tk.W)
        
        # Movement controls
        controls_frame = ttk.LabelFrame(left_frame, text="Move Selected Sprite", padding=10)
        controls_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Arrow buttons layout
        arrow_grid = ttk.Frame(controls_frame)
        arrow_grid.pack()
        
        ttk.Button(arrow_grid, text="↑", width=5, command=lambda: self.move_sprite(0, -VERTICAL_OFFSET)).grid(row=0, column=1, padx=2, pady=2)
        ttk.Button(arrow_grid, text="←", width=5, command=lambda: self.move_sprite(-HORIZONTAL_OFFSET, 0)).grid(row=1, column=0, padx=2, pady=2)
        ttk.Button(arrow_grid, text="→", width=5, command=lambda: self.move_sprite(HORIZONTAL_OFFSET, 0)).grid(row=1, column=2, padx=2, pady=2)
        ttk.Button(arrow_grid, text="↓", width=5, command=lambda: self.move_sprite(0, VERTICAL_OFFSET)).grid(row=2, column=1, padx=2, pady=2)
        
        # Delete selected sprite button
        ttk.Button(controls_frame, text="Delete Selected", command=self.delete_selected_sprite).pack(pady=(10, 0))
        
        # Output button
        ttk.Button(left_frame, text="Save Output", command=self.save_output, style="Accent.TButton").pack(fill=tk.X)
        
        # Right panel (canvas)
        right_frame = ttk.Frame(main_frame)
        right_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Canvas (no scrollbars)
        canvas_container = ttk.Frame(right_frame)
        canvas_container.pack(fill=tk.BOTH, expand=True)
        
        self.canvas = tk.Canvas(canvas_container, bg=CANVAS_BG, highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        # Store canvas dimensions
        self.canvas_width = 0
        self.canvas_height = 0
        self.canvas.bind("<Configure>", self.on_canvas_configure)
        
        # Canvas event handlers
        self.canvas.bind("<Button-1>", self.on_canvas_click)
        self.canvas.bind("<B1-Motion>", self.on_canvas_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_canvas_release)
        
        # Keyboard bindings
        self.root.bind("<Up>", lambda e: self.move_sprite(0, -VERTICAL_OFFSET))
        self.root.bind("<Down>", lambda e: self.move_sprite(0, VERTICAL_OFFSET))
        self.root.bind("<Left>", lambda e: self.move_sprite(-HORIZONTAL_OFFSET, 0))
        self.root.bind("<Right>", lambda e: self.move_sprite(HORIZONTAL_OFFSET, 0))
        self.root.bind("<Delete>", lambda e: self.delete_selected_sprite())
        
        # Status bar
        status_frame = tk.Frame(right_frame, bg=BG_COLOR)
        status_frame.pack(side=tk.BOTTOM, fill=tk.X)
        self.status_label = tk.Label(
            status_frame, text="Ready", relief=tk.SUNKEN, anchor=tk.W,
            bg="#3c3c3c", fg=FG_COLOR, padx=5, pady=2
        )
        self.status_label.pack(fill=tk.X)
    
    def _remove_png_suffix(self, text):
        """Remove a trailing .png/.PNG extension from the provided text."""
        if text.lower().endswith(".png"):
            return text[:-4]
        return text
    
    def _normalize_expression(self, expression):
        """Normalize sprite expression text for consistent parsing."""
        normalized = re.sub(r"\s+", "", expression)
        normalized = re.sub(r"\++", "+", normalized)
        return normalized.strip('+')
    
    def _expand_expression_tokens(self, expression):
        """Expand shorthand expressions into full sprite names."""
        tokens = [token for token in expression.split('+') if token]
        if not tokens:
            return []
        
        expanded = []
        base_name = tokens[0]
        expanded.append(base_name)
        
        match = re.match(r"^(.*?)(\d+)$", base_name)
        if match:
            prefix, digits = match.groups()
            width = len(digits)
            for token in tokens[1:]:
                if token.isdigit():
                    expanded.append(f"{prefix}{token.zfill(width)}")
                else:
                    expanded.append(token)
        else:
            expanded.extend(tokens[1:])
        
        return expanded
    
    def load_sprites(self):
        """Load sprites from the text input."""
        input_text = self.text_input.get("1.0", tk.END).strip()
        if not input_text:
            messagebox.showwarning("No Input", "Please enter sprite names.")
            return
        
        self.original_expression_string = ""
        self.loaded_sprite_names_ordered = []
        
        sprite_names = []
        expression_segments = []
        
        # Parse input - handle both line-separated and +-separated formats
        lines = input_text.split('\n')
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            without_png = self._remove_png_suffix(line)
            normalized = self._normalize_expression(without_png)
            if not normalized:
                continue
            
            expression_segments.append(normalized)
            expanded = self._expand_expression_tokens(normalized)
            sprite_names.extend(expanded)
        
        if not sprite_names:
            messagebox.showwarning("No Sprites", "No valid sprite names found.")
            return
        
        self.original_expression_string = "+".join(expression_segments)
        self.loaded_sprite_names_ordered = list(sprite_names)
        
        # Clear existing sprites
        self.sprites.clear()
        self.selected_sprite_index = None
        self.canvas_images.clear()
        
        # Create sprite items in a horizontal line
        for i, sprite_name in enumerate(sprite_names):
            x = i * HORIZONTAL_OFFSET
            y = 200  # Start at y=200 to have room to move up
            sprite_item = SpriteItem(sprite_name, x, y)
            self.sprites.append(sprite_item)
        
        self.update_canvas()
        self.status_label.config(text=f"Loaded {len(self.sprites)} sprites")
    
    def on_canvas_configure(self, event):
        """Handle canvas resize to update dimensions."""
        self.canvas_width = event.width
        self.canvas_height = event.height
        self.update_canvas()
    
    def update_canvas(self):
        """Redraw all sprites on the canvas."""
        self.canvas.delete("all")
        self.canvas_images.clear()
        
        if not self.sprites:
            return
        
        # Get canvas dimensions if not set yet
        if self.canvas_width == 0 or self.canvas_height == 0:
            self.canvas.update_idletasks()
            self.canvas_width = self.canvas.winfo_width()
            self.canvas_height = self.canvas.winfo_height()
            if self.canvas_width == 1 or self.canvas_height == 1:  # Not yet rendered
                return
        
        # Draw grid (32x32 isometric grid) - fixed position covering entire canvas
        for x in range(0, self.canvas_width + HORIZONTAL_OFFSET, HORIZONTAL_OFFSET):
            self.canvas.create_line(x, 0, x, self.canvas_height, fill=GRID_COLOR, dash=(2, 4))
        for y in range(0, self.canvas_height + VERTICAL_OFFSET, VERTICAL_OFFSET):
            self.canvas.create_line(0, y, self.canvas_width, y, fill=GRID_COLOR, dash=(2, 4))
        
        # Draw sprites at their absolute positions
        for i, sprite in enumerate(self.sprites):
            photo = sprite.get_photo_image()
            if photo:
                self.canvas_images.append(photo)  # Keep reference
                canvas_id = self.canvas.create_image(sprite.x, sprite.y, image=photo, anchor=tk.NW, tags=f"sprite_{i}")
                sprite.canvas_id = canvas_id
                
                # Draw selection highlight
                if i == self.selected_sprite_index:
                    self.canvas.create_rectangle(
                        sprite.x - 2, sprite.y - 2,
                        sprite.x + SPRITE_WIDTH + 2, sprite.y + SPRITE_HEIGHT + 2,
                        outline=HIGHLIGHT_COLOR, width=3, tags=f"highlight_{i}"
                    )
    
    def on_canvas_click(self, event):
        """Handle canvas click to select sprite and start dragging."""
        canvas_x = event.x
        canvas_y = event.y
        
        # Find clicked sprite
        for i, sprite in enumerate(self.sprites):
            if (sprite.x <= canvas_x <= sprite.x + SPRITE_WIDTH and
                sprite.y <= canvas_y <= sprite.y + SPRITE_HEIGHT):
                self.selected_sprite_index = i
                self.drag_sprite_index = i
                self.dragging = True
                self.drag_start_x = canvas_x - sprite.x
                self.drag_start_y = canvas_y - sprite.y
                self.update_canvas()
                self.status_label.config(text=f"Selected: {sprite.sprite_name}")
                return
        
        # Clicked empty space - deselect
        self.selected_sprite_index = None
        self.dragging = False
        self.drag_sprite_index = None
        self.update_canvas()
        self.status_label.config(text="No sprite selected")
    
    def on_canvas_drag(self, event):
        """Handle dragging a sprite."""
        if not self.dragging or self.drag_sprite_index is None:
            return
        
        canvas_x = event.x
        canvas_y = event.y
        
        sprite = self.sprites[self.drag_sprite_index]
        
        # Calculate new position
        new_x = canvas_x - self.drag_start_x
        new_y = canvas_y - self.drag_start_y
        
        # Snap to grid
        sprite.x = round(new_x / HORIZONTAL_OFFSET) * HORIZONTAL_OFFSET
        sprite.y = round(new_y / VERTICAL_OFFSET) * VERTICAL_OFFSET
        
        self.update_canvas()
    
    def on_canvas_release(self, event):
        """Handle mouse release after dragging."""
        if self.dragging and self.drag_sprite_index is not None:
            sprite = self.sprites[self.drag_sprite_index]
            self.status_label.config(text=f"Positioned {sprite.sprite_name} at ({sprite.x}, {sprite.y})")
        
        self.dragging = False
        self.drag_sprite_index = None
    
    def move_sprite(self, dx, dy):
        """Move the selected sprite by the given offset."""
        if self.selected_sprite_index is None:
            self.status_label.config(text="No sprite selected to move")
            return
        
        sprite = self.sprites[self.selected_sprite_index]
        sprite.x += dx
        sprite.y += dy
        self.update_canvas()
        self.status_label.config(text=f"Moved {sprite.sprite_name} by ({dx}, {dy})")
    
    def delete_selected_sprite(self):
        """Delete the currently selected sprite."""
        if self.selected_sprite_index is None:
            self.status_label.config(text="No sprite selected to delete")
            return
        
        sprite = self.sprites[self.selected_sprite_index]
        del self.sprites[self.selected_sprite_index]
        self.selected_sprite_index = None
        self.update_canvas()
        self.status_label.config(text=f"Deleted {sprite.sprite_name}")
    
    def save_output(self):
        """Save the composite image to disk."""
        if not self.sprites:
            messagebox.showwarning("No Sprites", "No sprites to save.")
            return
        
        # Calculate composite bounds
        min_x = min(sprite.x for sprite in self.sprites)
        max_x = max(sprite.x for sprite in self.sprites)
        min_y = min(sprite.y for sprite in self.sprites)
        max_y = max(sprite.y for sprite in self.sprites)
        
        canvas_width = (max_x - min_x) + SPRITE_WIDTH
        canvas_height = (max_y - min_y) + SPRITE_HEIGHT
        
        # Create composite image
        composite = Image.new("RGBA", (canvas_width, canvas_height), (0, 0, 0, 0))
        
        for sprite in self.sprites:
            if sprite.image:
                paste_x = sprite.x - min_x
                paste_y = sprite.y - min_y
                composite.alpha_composite(sprite.image, (paste_x, paste_y))
        
        # Generate output filename
        sprite_names_ordered = [sprite.sprite_name for sprite in self.sprites]
        if (
            self.original_expression_string
            and sprite_names_ordered == self.loaded_sprite_names_ordered
        ):
            output_stub = self.original_expression_string
        else:
            output_stub = "+".join(sprite_names_ordered)
        output_name = f"{output_stub}.png"
        
        # Create output directory if it doesn't exist
        os.makedirs(OUTPUT_DIRECTORY, exist_ok=True)
        
        output_path = os.path.join(OUTPUT_DIRECTORY, output_name)
        
        # Save the image
        composite.save(output_path)
        
        messagebox.showinfo("Success", f"Saved to:\n{output_path}")
        self.status_label.config(text=f"Saved: {output_name}")


def main():
    root = tk.Tk()
    app = ManualTileStitcher(root)
    root.mainloop()
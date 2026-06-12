import sys
import traceback
import copy
import customtkinter as ctk
from world import rooms as orig_rooms, items as orig_items
from player import describe_room, go, take, drop, show_inventory, examine

# --- CUSTOM PALETTE & FONTS ---
BG_COLOR = "#120A07"       
PANEL_COLOR = "#1A100B"    
TEXT_COLOR = "#D4C9A9"     
ACCENT_COLOR = "#D4AF37"   
BORDER_COLOR = "#3A2618"   

FONT_TITLE = ("Georgia", 26, "bold")
FONT_MAIN = ("Georgia", 16)
FONT_INPUT = ("Courier New", 16, "bold")

# Load our dynamic copies of the game world
rooms = copy.deepcopy(orig_rooms)
items = copy.deepcopy(orig_items)
player = {
    "location": "clearing",
    "inventory": [],
    "is_dead": False
}

def check_state(player, rooms):
    if player.get("is_dead"):
        return True 
    room = rooms.get(player["location"], {})
    if room.get("win_room") is True:
        print("\n" + "="*50)
        print("THE CHEST SWINGS OPEN. GOLD COINS SPILL OUT.")
        print("*** YOU WIN! ***")
        print("="*50)
        return True
    return False

def parse(command, player, rooms, items):
    command = command.lower().strip()
    parts = command.split()
    
    if not parts:
        return True
        
    verb = parts[0]
    noun = parts[1] if len(parts) > 1 else None
    
    if verb in ["go", "move", "walk", "head"]:
        if noun is not None:
            go(noun, player, rooms)
            if not player.get("is_dead"):
                describe_room(player, rooms, items)
        else:
            print("Go where? (example: go north)")
            
    elif verb in ["look", "l"]:
        describe_room(player, rooms, items)
        
    elif verb in ["take", "pick", "grab", "get"]:
        if noun is not None:
            take(noun, player, rooms)
        else:
            print("Take what?")
            
    elif verb in ["drop", "leave"]:
        if noun is not None:
            drop(noun, player, rooms)
        else:
            print("Drop what?")
            
    elif verb == "light" and noun == "torch":
        if "torch" in player["inventory"] and "flint" in player["inventory"]:
            player["inventory"].remove("torch")
            player["inventory"].append("lit_torch")
            print("You strike the flint against a rock. Sparks fly and the torch catches fire!")
        elif "torch" in player["inventory"]:
            print("You have the torch, but you need a spark (like flint) to light it.")
        else:
            print("You don't have a torch to light.")
            
    elif verb in ["inventory", "i", "bag", "pockets"]:
        show_inventory(player)
        
    elif verb in ["examine", "inspect", "x"]:
        if noun is not None:
            examine(noun, player, rooms, items)
        else:
            print("Examine what?")
            
    elif verb in ["help", "h", "?"]:
        help_text = (
            "Available commands:\n"
            "  go [direction]      - move (directions: north, south, east, west)\n"
            "  look                - describe your current location\n"
            "  take [item]         - pick up an item\n"
            "  drop [item]         - drop an item you are carrying\n"
            "  light torch         - light an unlit torch (requires flint)\n"
            "  examine [item]      - inspect an item more closely\n"
            "  quit                - exit the game"
        )
        print(help_text)
        
    elif verb in ["quit", "exit", "q"]:
        print("\nGoodbye. (You can close this window now)")
        return False
        
    else:
        print("I don't understand that. Type 'help' to see available commands.")
        
    return True

class OutputRedirector:
    def __init__(self, text_widget):
        self.text_widget = text_widget

    def write(self, text):
        self.text_widget.configure(state="normal")
        self.text_widget.insert("end", text)
        self.text_widget.see("end") 
        self.text_widget.configure(state="disabled")

    def flush(self): 
        pass

class GameGUI(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("The Lost Treasure")
        self.geometry("1200x650") 
        self.configure(fg_color=BG_COLOR)
        
        self.grid_columnconfigure(0, weight=0, minsize=220) 
        self.grid_columnconfigure(1, weight=1)              
        self.grid_columnconfigure(2, weight=0, minsize=300) 
        self.grid_rowconfigure(1, weight=1)

        # --- TOP HEADER ---
        self.header_frame = ctk.CTkFrame(self, fg_color=PANEL_COLOR, corner_radius=0, border_width=2, border_color=BORDER_COLOR)
        self.header_frame.grid(row=0, column=0, columnspan=3, sticky="ew")
        self.location_label = ctk.CTkLabel(self.header_frame, text="~ THE LOST TREASURE ~", font=FONT_TITLE, text_color=ACCENT_COLOR, pady=15)
        self.location_label.pack()

        # --- LEFT SIDEBAR (SATCHEL) ---
        self.sidebar = ctk.CTkFrame(self, width=220, fg_color=PANEL_COLOR, corner_radius=0, border_width=2, border_color=BORDER_COLOR)
        self.sidebar.grid(row=1, column=0, sticky="nsew", padx=(10, 5), pady=10)
        self.sidebar.grid_rowconfigure(2, weight=1) 
        
        self.logo = ctk.CTkLabel(self.sidebar, text="❖ SATCHEL ❖", font=("Georgia", 18, "bold"), text_color=ACCENT_COLOR)
        self.logo.grid(row=0, column=0, padx=20, pady=(20, 10))
        
        self.divider1 = ctk.CTkFrame(self.sidebar, height=2, fg_color=BORDER_COLOR)
        self.divider1.grid(row=1, column=0, sticky="ew", padx=15)

        self.inv_label = ctk.CTkLabel(self.sidebar, text="Empty", font=FONT_MAIN, text_color=TEXT_COLOR, justify="left")
        self.inv_label.grid(row=2, column=0, padx=20, pady=15, sticky="nw")
        
        # --- CENTER MAIN AREA ---
        self.main_frame = ctk.CTkFrame(self, fg_color=BG_COLOR, corner_radius=0)
        self.main_frame.grid(row=1, column=1, sticky="nsew", padx=5, pady=10)
        self.main_frame.grid_rowconfigure(0, weight=1)
        self.main_frame.grid_columnconfigure(0, weight=1)
        
        self.text_area = ctk.CTkTextbox(self.main_frame, font=FONT_MAIN, fg_color=BG_COLOR, text_color=TEXT_COLOR, wrap="word", state="disabled", border_width=0)
        self.text_area.grid(row=0, column=0, padx=10, pady=(0, 10), sticky="nsew")
        
        self.input_frame = ctk.CTkFrame(self.main_frame, fg_color=PANEL_COLOR, corner_radius=8, border_width=1, border_color=ACCENT_COLOR)
        self.input_frame.grid(row=1, column=0, sticky="ew", pady=(0, 5))
        
        self.prompt_symbol = ctk.CTkLabel(self.input_frame, text=">", font=FONT_INPUT, text_color=ACCENT_COLOR)
        self.prompt_symbol.pack(side="left", padx=(15, 5), pady=10)

        self.entry = ctk.CTkEntry(self.input_frame, font=FONT_INPUT, height=45, fg_color="transparent", text_color=ACCENT_COLOR, border_width=0)
        self.entry.pack(side="left", fill="x", expand=True, padx=(0, 5), pady=5)
        self.entry.bind("<Return>", self.process_command)
        
        # New Safe Restart Button
        self.restart_btn = ctk.CTkButton(self.input_frame, text="RESTART", font=("Courier New", 14, "bold"), width=60, fg_color="transparent", text_color=ACCENT_COLOR, hover_color=BORDER_COLOR, command=self.restart_game)
        self.restart_btn.pack(side="right", padx=(0, 10), pady=5)

        # Help Button
        self.help_btn = ctk.CTkButton(self.input_frame, text="?", font=("Georgia", 20, "bold"), width=35, fg_color="transparent", text_color=ACCENT_COLOR, hover_color=BORDER_COLOR, command=self.trigger_help)
        self.help_btn.pack(side="right", padx=(0, 5), pady=5)
        
        self.bind("<F1>", self.trigger_help)

        # --- RIGHT SIDEBAR (MAP & CODEX) ---
        self.right_sidebar = ctk.CTkFrame(self, width=300, fg_color=PANEL_COLOR, corner_radius=0, border_width=2, border_color=BORDER_COLOR)
        self.right_sidebar.grid(row=1, column=2, sticky="nsew", padx=(5, 10), pady=10)
        self.right_sidebar.grid_rowconfigure(4, weight=1) 
        
        self.map_title = ctk.CTkLabel(self.right_sidebar, text="❖ AREA MAP ❖", font=("Georgia", 18, "bold"), text_color=ACCENT_COLOR)
        self.map_title.grid(row=0, column=0, padx=20, pady=(20, 10))
        
        self.divider2 = ctk.CTkFrame(self.right_sidebar, height=2, fg_color=BORDER_COLOR)
        self.divider2.grid(row=1, column=0, sticky="ew", padx=15)
        
        self.minimap = ctk.CTkFrame(self.right_sidebar, fg_color="transparent")
        self.minimap.grid(row=2, column=0, padx=15, pady=15, sticky="nsew")
        self.minimap.grid_columnconfigure((0,1,2), weight=1)
        
        self.map_cells = {}
        positions = {"north": (0, 1), "south": (2, 1), "east": (1, 2), "west": (1, 0), "center": (1, 1)}
        for dir_name, (r, c) in positions.items():
            cell = ctk.CTkLabel(self.minimap, text="", font=("Courier New", 12, "bold"), width=80, height=55, corner_radius=5)
            cell.grid(row=r, column=c, padx=3, pady=3)
            self.map_cells[dir_name] = cell
            
        self.codex_title = ctk.CTkLabel(self.right_sidebar, text="❖ SCANNER ❖", font=("Georgia", 16, "bold"), text_color=ACCENT_COLOR)
        self.codex_title.grid(row=3, column=0, padx=20, pady=(10, 5))
        
        self.codex_scroll = ctk.CTkScrollableFrame(self.right_sidebar, fg_color=BG_COLOR, corner_radius=5)
        self.codex_scroll.grid(row=4, column=0, padx=15, pady=(0, 15), sticky="nsew")
        
        self.codex_text = ctk.CTkLabel(self.codex_scroll, text="", font=("Georgia", 13), text_color=TEXT_COLOR, justify="left", wraplength=260)
        self.codex_text.pack(fill="x", padx=5, pady=5)
        
        self.entry.focus()
        sys.stdout = OutputRedirector(self.text_area)
        
        self.running = True
        self.start_game()

    def restart_game(self):
        """Wipes the dynamic state and resets it to the pristine original copy."""
        global player, rooms, items
        rooms.clear()
        rooms.update(copy.deepcopy(orig_rooms))
        
        items.clear()
        items.update(copy.deepcopy(orig_items))
        
        player.clear()
        player.update({
            "location": "clearing",
            "inventory": [],
            "is_dead": False
        })
        
        # Clear the visual text area safely (0.0 is preferred for CTkTextbox)
        self.text_area.configure(state="normal")
        self.text_area.delete("0.0", "end")
        self.text_area.configure(state="disabled")
        
        # Re-enable controls if they were disabled
        self.running = True
        self.entry.configure(state="normal")
        self.entry.delete(0, "end")
        self.help_btn.configure(state="normal")
        self.entry.focus()
        
        self.start_game()

    def trigger_help(self, event=None):
        if not self.running: return
        print(f"\n> HELP (Shortcut)") 
        try:
            self.running = parse("help", player, rooms, items)
            self.update_ui_state()
        except Exception as e:
            print(f"\n[SYSTEM ERROR]: {e}\n{traceback.format_exc()}")
        self.entry.focus() 
        
    def update_ui_state(self):
        room = rooms.get(player["location"], {})
        
        if not player["inventory"]:
            self.inv_label.configure(text="\nYour pockets\nare empty.")
        else:
            formatted_inv = "\n".join([f" • {item.replace('_', ' ').title()}" for item in player["inventory"]])
            self.inv_label.configure(text="\n" + formatted_inv)
            
        current_room_name = player["location"].replace('_', ' ').upper()
        if player.get("is_dead"):
            self.location_label.configure(text="~ YOU HAVE PERISHED ~", text_color="#8B0000")
            self.map_cells["center"].configure(text="DEAD", fg_color="#8B0000", text_color="#FFFFFF")
        else:
            self.location_label.configure(text=f"~ {current_room_name} ~")
            
        for cell in self.map_cells.values():
            cell.configure(text="", fg_color="transparent") 
            
        if not player.get("is_dead"):
            self.map_cells["center"].configure(text="YOU\nARE\nHERE", fg_color=ACCENT_COLOR, text_color=BG_COLOR)
            exits = room.get("exits", {})
            locked = room.get("locked_exits", {})
            
            for direction, dest in exits.items():
                if direction in self.map_cells:
                    dest_name = dest.replace("_", "\n").upper()
                    if direction in locked:
                        dest_name = "🔒\n" + dest_name
                    self.map_cells[direction].configure(text=dest_name, fg_color=PANEL_COLOR, text_color=TEXT_COLOR)

        codex_content = ""
        room_items = room.get("items", [])
        if room_items:
            codex_content += "[ ON THE GROUND ]\n\n"
            for item_id in room_items:
                i_data = items.get(item_id, {})
                codex_content += f"❖ {i_data.get('name', item_id).title()}\n{i_data.get('description', '')}\n\n"
                
        if player["inventory"]:
            codex_content += "[ KNOWN LORE ]\n\n"
            for item_id in player["inventory"]:
                hint = ""
                if item_id == "rusty_key": hint = "\n(Hint: Opens iron gates)"
                elif item_id == "flint": hint = "\n(Hint: Strike to light fires)"
                elif item_id == "mill_key": hint = "\n(Hint: Its purpose is unknown)"
                elif item_id == "torch": hint = "\n(Hint: Useless without a spark)"
                elif item_id == "lit_torch": hint = "\n(Hint: Protects from the dark)"
                
                i_data = items.get(item_id, {})
                codex_content += f"❖ {i_data.get('name', item_id).title()}{hint}\n{i_data.get('description', '')}\n\n"
                
        if not codex_content:
            codex_content = "There is nothing of interest nearby."
            
        self.codex_text.configure(text=codex_content)

    def start_game(self):
        print("\n\n" + " " * 25 + "Welcome to...")
        print(" " * 20 + "THE LOST TREASURE\n")
        print("(Press F1 or click the '?' for a list of commands)")
        describe_room(player, rooms, items)
        self.update_ui_state()

    def process_command(self, event):
        if not self.running: return
        command = self.entry.get()
        self.entry.delete(0, "end")
        print(f"\n> {command.upper()}") 
        
        try:
            self.running = parse(command, player, rooms, items)
            self.update_ui_state() 
            if self.running and check_state(player, rooms):
                self.running = False
        except Exception as e:
            print(f"\n[SYSTEM ERROR]: {e}\n{traceback.format_exc()}")
            
        if not self.running:
            self.entry.configure(state="disabled")
            self.help_btn.configure(state="disabled")
            print("\n*** The journey has ended. Click RESTART to play again. ***")

if __name__ == "__main__":
    app = GameGUI()
    app.mainloop()
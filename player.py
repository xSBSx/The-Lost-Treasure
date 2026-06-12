def describe_room(player, rooms, items):
    print()
    room = rooms.get(player["location"], {})
    
    if "description" in room:
        print(room["description"])
        
    if "exits" in room:
        exits_str = ", ".join(room["exits"].keys())
        print(f"Exits: {exits_str}")
        
    if "items" in room and room["items"]:
        items_str = ", ".join(room["items"])
        print(f"Items here: {items_str}")

def go(direction, player, rooms):
    room = rooms.get(player["location"], {})
    
    if direction not in room.get("exits", {}):
        print("You can't go that way.")
        return
        
    destination = room["exits"][direction]
    
    # Check locks
    locked_exits = room.get("locked_exits", {})
    if direction in locked_exits:
        required_item = locked_exits[direction]
        if required_item not in player["inventory"]:
            print("The way is blocked. You may need a specific item to pass.")
            return
        else:
            print(f"You use the {required_item} — something clicks and the way opens.")
            del room["locked_exits"][direction]
            
    # Check death trap
    if destination == "dark_tunnel" and "lit_torch" not in player["inventory"]:
        print("\nYou step blindly into the pitch-black tunnel. Suddenly, you hear a terrifying growl.")
        print("Sharp teeth sink into your leg in the darkness.")
        print("*** You have been eaten by a Grue! GAME OVER ***")
        player["is_dead"] = True
        player["location"] = destination
        return
            
    player["location"] = destination

def take(item_id, player, rooms):
    room = rooms.get(player["location"], {})
    
    if item_id not in room.get("items", []):
        print(f"There is no {item_id} here.")
        return
        
    room["items"].remove(item_id)
    player["inventory"].append(item_id)
    print(f"You pick up the {item_id}.")

def drop(item_id, player, rooms):
    if item_id not in player["inventory"]:
        print(f"You are not carrying a {item_id}.")
        return
        
    player["inventory"].remove(item_id)
    rooms[player["location"]]["items"].append(item_id)
    print(f"You drop the {item_id}.")

def show_inventory(player):
    if not player["inventory"]:
        print("You are not carrying anything.")
    else:
        items_str = ", ".join(player["inventory"])
        print(f"You are carrying: {items_str}")

def examine(item_id, player, rooms, items):
    room_items = rooms.get(player["location"], {}).get("items", [])
    inventory = player["inventory"]
    
    if item_id not in room_items and item_id not in inventory:
        print(f"You don't see a {item_id} here.")
        return
        
    if item_id not in items:
        print("You look closely but notice nothing special.")
        return
        
    print(items[item_id]["description"])
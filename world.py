rooms = {
    "clearing": {
        "description": "You are in a sunlit forest clearing. A dirt path leads north\ntoward a dark hillside. The sound of water drifts from the east.",
        "exits": {"north": "cave_entrance", "east": "riverbank"},
        "items": ["rusty_key"]
    },
    "cave_entrance": {
        "description": "You stand before the mouth of a cave. A heavy iron gate blocks\nthe passage east. Moss covers the stone walls on either side.",
        "exits": {"south": "clearing", "east": "cave_interior"},
        "items": [],
        "locked_exits": {"east": "rusty_key"}
    },
    "cave_interior": {
        "description": "The cave is cold. A rusted bracket on the wall holds an unlit torch.\nTo the east is a tunnel so pitch-black you cannot see the end of it.",
        "exits": {"west": "cave_entrance", "east": "dark_tunnel"},
        "items": ["torch"]
    },
    "dark_tunnel": {
        "description": "The flickering light of your torch reveals a narrow, jagged tunnel.\nWithout this fire, the creatures lurking in the shadows would surely attack.\nAhead to the east, you see a golden glow.",
        "exits": {"west": "cave_interior", "east": "treasure_room"},
        "items": []
    },
    "riverbank": {
        "description": "A fast river rushes past. An old wooden mill sits upstream to the north.\nThe current looks too strong to cross.",
        "exits": {"west": "clearing", "north": "old_mill"},
        "items": ["fishing_rod"]
    },
    "old_mill": {
        "description": "A crumbling mill stands beside the river. The wheel has stopped turning.\nA small key hangs by the door, and a piece of flint rests on a barrel.",
        "exits": {"south": "riverbank"},
        "items": ["mill_key", "flint"]
    },
    "treasure_room": {
        "description": "You step into a vast stone chamber. In the centre, an ancient\nwooden chest sits on a raised platform, its lock hanging open.",
        "exits": {"west": "dark_tunnel"},
        "items": [],
        "win_room": True
    }
}

items = {
    "rusty_key": {
        "name": "rusty key",
        "description": "A heavy iron key, brown with rust. The bow is shaped like a leaf."
    },
    "torch": {
        "name": "torch",
        "description": "A wooden-handled torch. It is currently unlit. You will need a spark."
    },
    "lit_torch": {
        "name": "lit torch",
        "description": "The torch is burning brightly, casting a warm, protective glow."
    },
    "fishing_rod": {
        "name": "fishing rod",
        "description": "A simple bamboo rod with a line attached."
    },
    "mill_key": {
        "name": "mill key",
        "description": "A small brass key on a loop of twine."
    },
    "flint": {
        "name": "flint",
        "description": "A sharp piece of flint stone. Striking it against metal or rock creates sparks."
    }
}
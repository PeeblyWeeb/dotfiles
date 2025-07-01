#!/usr/bin/env python3
import json
import subprocess

PLAYER = "spotify"
METADATA_FORMAT = "{{ artist }} - {{ title }}"

ICON_CONFIG = {
    "spotify": {
        "icon": "",
        "colors": {
            "playing": "#1DB954"
        }
    },
    "chromium": {
        "icon": "",
        "colors": {
            "playing": "#4285F4"
        }
    }
}

def get_icon(player: str, playing: bool) -> str:
    cfg = ICON_CONFIG.get(player) or {}
    icon = cfg.get("icon") or "??"

    cfg_colors = cfg.get("colors") or {}
    colors = {
        "paused": cfg_colors.get("paused") or "#7D7F81",
        "playing": cfg_colors.get("playing") or "#ffffff"
    }

    return f"<span color='{colors["playing"] if playing else colors["paused"]}'>{icon}</span>"


metadata = subprocess.getoutput(f"playerctl metadata --player {PLAYER} --format '{METADATA_FORMAT}'")
volume = float(subprocess.getoutput(f"playerctl volume --player {PLAYER}"))
playing = True if subprocess.getoutput(f"playerctl status --player {PLAYER}").lower() == "playing" else False
vol_pct = round(volume * 100)

print(json.dumps({
    "text": f"{get_icon(PLAYER, playing)} {metadata}",
    "tooltip": f"Volume: {vol_pct}%",
    "class": "spotify"
}))

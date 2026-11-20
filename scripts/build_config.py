import json
import re
from pathlib import Path

data = json.loads(Path("data/vlans.json").read_text())
vlans = data["vlans"]

if not isinstance(vlans, list) or not vlans:
    raise ValueError("vlans must be a non-empty list")

seen = set()
commands = []

for vlan in vlans:
    vlan_id = vlan["id"]
    name = vlan["name"]

    if type(vlan_id) is not int or not 2 <= vlan_id <= 4094:
        raise ValueError(f"Invalid VLAN ID: {vlan_id}")

    if vlan_id in seen:
        raise ValueError(f"Duplicate VLAN ID: {vlan_id}")

    if not isinstance(name, str) or not re.fullmatch(
        r"[A-Za-z][A-Za-z0-9_-]{0,31}", name
    ):
        raise ValueError(f"Invalid VLAN name: {name}")

    seen.add(vlan_id)

for vlan in sorted(vlans, key=lambda item: item["id"]):
    commands.extend([
        f"vlan {vlan['id']}",
        f"   name {vlan['name']}",
        "!",
    ])

output = "\n".join(commands) + "\n"
Path("rendered").mkdir(exist_ok=True)
Path("rendered/vlans.cfg").write_text(output)

print("Validation passed")
print(output)
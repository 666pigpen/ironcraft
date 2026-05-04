# IronCraft

A [Create](https://github.com/Creators-of-Create/Create) add-on for Minecraft 1.21.1 (NeoForge) that adds a bulk crafting table built from industrial iron.

## Features

- **Iron Crafting Table** — a 3×3 crafting table that accepts up to 256 items per ingredient slot
- One click crafts as many times as possible given the ingredients and pushes all output directly to your inventory
- Output is distributed in normal stack sizes (64 per slot); excess drops at your feet if your inventory is full
- Supports all standard crafting recipes

## Requirements

| Dependency | Version |
|---|---|
| Minecraft | 1.21.1 |
| NeoForge | 21.1.228+ |
| Create | 6.0.9+ |

## Crafting

Place 4 **Create Industrial Iron Blocks** in a 2×2 pattern — the same shape as crafting a vanilla crafting table from planks.

```
[Industrial Iron Block] [Industrial Iron Block]
[Industrial Iron Block] [Industrial Iron Block]
```

## Usage

Right-click the Iron Crafting Table to open it. Place ingredients in the 3×3 grid as normal. Each slot holds up to 256 items. Click the output slot to craft all possible combinations at once — results go straight to your inventory.

## Building from Source

Requires JDK 21.

```bash
git clone https://github.com/666pigpen/ironcraft.git
cd ironcraft
bash setup_gradle.sh        # downloads Gradle wrapper jar (first time only)
./gradlew build
```

The compiled JAR will be at `build/libs/ironcraft-1.0.0.jar`.

## License

MIT

<img width="854" height="480" alt="ui" src="https://github.com/user-attachments/assets/7002ad98-f4f0-4a60-afe7-6e71149b893a" />
<img width="854" height="480" alt="recipe" src="https://github.com/user-attachments/assets/e3d1baaa-9480-4b15-81eb-885c4b81fbd8" />
<img width="854" height="480" alt="table" src="https://github.com/user-attachments/assets/26bf9291-b757-40b6-a9ed-17a7de098bb2" />


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

Place 4 **Create Industrial Iron Blocks** in a 2×2 pattern in the inventory

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

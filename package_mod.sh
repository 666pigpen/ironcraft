#!/bin/bash
# Packages ironcraft + Create into a dist/ folder ready to drop into .minecraft/mods/

set -e

DIST="dist/mods"
rm -rf dist
mkdir -p "$DIST"

# Build fresh
./gradlew build -q

cp build/libs/ironcraft-1.0.0.jar "$DIST/"
cp run/mods/create-1.21.1-6.0.9.jar "$DIST/"

echo ""
echo "Packaged to dist/mods/:"
ls -lh "$DIST"
echo ""
echo "Setup instructions:"
echo "  1. Install NeoForge 21.1.228 for Minecraft 1.21.1"
echo "     Installer: https://maven.neoforged.net/releases/net/neoforged/neoforge/21.1.228/neoforge-21.1.228-installer.jar"
echo "     Run with: java -jar neoforge-21.1.228-installer.jar"
echo ""
echo "  2. Copy both JARs from dist/mods/ into your .minecraft/mods/ folder"
echo ""
echo "  3. Launch Minecraft with the NeoForge 21.1.228 profile"
echo ""
echo "  4. Craft the Iron Crafting Table:"
echo "     Place 4 Create Industrial Iron Blocks in a 2x2 pattern"

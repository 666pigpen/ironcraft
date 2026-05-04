package com.pigpen.ironcraft.menu;

import net.minecraft.world.entity.player.Player;
import net.minecraft.world.inventory.CraftingContainer;
import net.minecraft.world.inventory.ResultContainer;
import net.minecraft.world.inventory.ResultSlot;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.crafting.CraftingInput;
import net.minecraft.world.item.crafting.CraftingRecipe;
import net.minecraft.world.item.crafting.RecipeType;

public class BulkResultSlot extends ResultSlot {

    private final int maxStack;
    private final IronCraftingTableMenu menu;
    private final CraftingContainer craftSlots;

    public BulkResultSlot(Player player, CraftingContainer craftSlots, ResultContainer resultSlots,
                           int slot, int x, int y, int maxStack, IronCraftingTableMenu menu) {
        super(player, craftSlots, resultSlots, slot, x, y);
        this.maxStack = maxStack;
        this.menu = menu;
        this.craftSlots = craftSlots;
    }

    @Override
    public int getMaxStackSize() { return maxStack; }

    @Override
    public int getMaxStackSize(ItemStack stack) { return maxStack; }

    @Override
    public void onTake(Player player, ItemStack taken) {
        // Use asCraftInput() so compact recipes (e.g. sticks 1x2) match correctly
        CraftingInput input = craftSlots.asCraftInput();
        int craftCount = player.level().getRecipeManager()
                .getRecipeFor(RecipeType.CRAFTING, input, player.level())
                .map(holder -> {
                    CraftingRecipe recipe = holder.value();
                    ItemStack base = recipe.assemble(input, player.level().registryAccess());
                    return base.isEmpty() ? 1 : menu.calculateMaxCrafts(base.getCount());
                })
                .orElse(1);

        // super handles exactly 1 craft: awards recipe XP, handles container items, consumes 1 per slot
        super.onTake(player, taken);

        // Consume the remaining (craftCount - 1) crafts worth of ingredients
        if (craftCount > 1) {
            for (int i = 0; i < craftSlots.getContainerSize(); i++) {
                ItemStack slot = craftSlots.getItem(i);
                if (!slot.isEmpty()) {
                    slot.shrink(Math.min(craftCount - 1, slot.getCount()));
                    if (slot.isEmpty()) craftSlots.setItem(i, ItemStack.EMPTY);
                }
            }
            craftSlots.setChanged();
        }
    }
}

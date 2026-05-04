package com.pigpen.ironcraft.menu;

import com.pigpen.ironcraft.registry.ModMenuTypes;
import net.minecraft.world.Container;
import net.minecraft.world.entity.player.Inventory;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.inventory.*;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.crafting.*;
import net.minecraft.world.level.Level;

import java.util.Optional;

public class IronCraftingTableMenu extends AbstractContainerMenu {

    private static final int CRAFT_GRID_WIDTH = 3;
    private static final int CRAFT_GRID_HEIGHT = 3;
    static final int MAX_STACK = 256;

    private final CraftingContainer craftSlots;
    private final ResultContainer resultSlots = new ResultContainer();
    private final ContainerLevelAccess access;
    private final Player player;

    public IronCraftingTableMenu(int containerId, Inventory playerInventory) {
        this(containerId, playerInventory, ContainerLevelAccess.NULL);
    }

    public IronCraftingTableMenu(int containerId, Inventory playerInventory,
                                  ContainerLevelAccess access) {
        super(ModMenuTypes.IRON_CRAFTING_TABLE.get(), containerId);
        this.access = access;
        this.player = playerInventory.player;

        this.craftSlots = new TransientCraftingContainer(this, CRAFT_GRID_WIDTH, CRAFT_GRID_HEIGHT);

        // Output slot
        this.addSlot(new BulkResultSlot(player, this.craftSlots, this.resultSlots, 0,
                124, 35, MAX_STACK, this));

        // Crafting grid (3x3)
        for (int row = 0; row < 3; row++) {
            for (int col = 0; col < 3; col++) {
                this.addSlot(new BulkInputSlot(this.craftSlots,
                        col + row * 3, 30 + col * 18, 17 + row * 18, MAX_STACK));
            }
        }

        // Player inventory
        for (int row = 0; row < 3; row++) {
            for (int col = 0; col < 9; col++) {
                this.addSlot(new Slot(playerInventory, col + row * 9 + 9,
                        8 + col * 18, 84 + row * 18));
            }
        }

        // Player hotbar
        for (int col = 0; col < 9; col++) {
            this.addSlot(new Slot(playerInventory, col, 8 + col * 18, 142));
        }
    }

    @Override
    public void slotsChanged(Container container) {
        if (container == this.craftSlots) {
            // Use player.level() directly — avoids timing issues with access.execute
            // and works correctly on both logical sides (guarded by isClientSide check)
            Level level = this.player.level();
            if (!level.isClientSide()) {
                slotChangedCraftingGrid(level);
            }
        }
    }

    private void slotChangedCraftingGrid(Level level) {
        CraftingInput input = craftSlots.asCraftInput();
        Optional<RecipeHolder<CraftingRecipe>> optional =
                level.getRecipeManager().getRecipeFor(RecipeType.CRAFTING, input, level);

        if (optional.isPresent()) {
            CraftingRecipe recipe = optional.get().value();
            ItemStack base = recipe.assemble(input, level.registryAccess());
            if (!base.isEmpty()) {
                int craftCount = calculateMaxCrafts(base.getCount());
                ItemStack bulk = base.copyWithCount(base.getCount() * craftCount);
                this.resultSlots.setRecipeUsed(optional.get());
                this.resultSlots.setItem(0, bulk);
                this.slots.get(0).set(bulk);
                broadcastChanges();
                return;
            }
        }

        this.resultSlots.setRecipeUsed(null);
        this.resultSlots.setItem(0, ItemStack.EMPTY);
        this.slots.get(0).set(ItemStack.EMPTY);
        broadcastChanges();
    }

    /**
     * Maximum number of crafts possible given current ingredient counts,
     * capped so total output fits in MAX_STACK.
     */
    int calculateMaxCrafts(int outputPerCraft) {
        int minCount = Integer.MAX_VALUE;
        for (int i = 0; i < craftSlots.getContainerSize(); i++) {
            ItemStack stack = craftSlots.getItem(i);
            if (!stack.isEmpty()) {
                minCount = Math.min(minCount, stack.getCount());
            }
        }
        if (minCount == Integer.MAX_VALUE) return 1;
        return Math.min(minCount, MAX_STACK / Math.max(outputPerCraft, 1));
    }

    @Override
    public void clicked(int slotId, int button, ClickType clickType, Player player) {
        if (slotId == 0 && slots.get(0).hasItem()) {
            Level level = player.level();
            if (!level.isClientSide()) giveOutputToPlayer(player, level);
            broadcastChanges();
            return;
        }
        super.clicked(slotId, button, clickType, player);
    }

    private void giveOutputToPlayer(Player player, Level level) {
        CraftingInput input = craftSlots.asCraftInput();
        level.getRecipeManager()
                .getRecipeFor(RecipeType.CRAFTING, input, level)
                .ifPresent(holder -> {
                    ItemStack base = holder.value().assemble(input, level.registryAccess());
                    if (base.isEmpty()) return;

                    int craftCount = calculateMaxCrafts(base.getCount());

                    // Consume ingredients
                    for (int i = 0; i < craftSlots.getContainerSize(); i++) {
                        ItemStack s = craftSlots.getItem(i);
                        if (!s.isEmpty()) {
                            s.shrink(craftCount);
                            if (s.isEmpty()) craftSlots.setItem(i, ItemStack.EMPTY);
                        }
                    }
                    craftSlots.setChanged();

                    // Distribute output in normal stack sizes directly to inventory
                    int toGive = base.getCount() * craftCount;
                    while (toGive > 0) {
                        int batch = Math.min(toGive, base.getMaxStackSize());
                        ItemStack give = base.copyWithCount(batch);
                        player.getInventory().add(give);
                        if (!give.isEmpty()) player.drop(give, false);
                        toGive -= batch;
                    }

                    slots.get(0).set(ItemStack.EMPTY);
                    resultSlots.setRecipeUsed(null);
                });
    }

    @Override
    public boolean stillValid(Player player) {
        return this.access.evaluate(
                (level, pos) -> level.getBlockState(pos).getBlock() instanceof
                        com.pigpen.ironcraft.block.IronCraftingTableBlock
                        && player.distanceToSqr(pos.getX() + 0.5, pos.getY() + 0.5,
                        pos.getZ() + 0.5) < 64.0,
                true);
    }

    @Override
    public ItemStack quickMoveStack(Player player, int index) {
        if (index == 0 && slots.get(0).hasItem()) {
            Level level = player.level();
            if (!level.isClientSide()) giveOutputToPlayer(player, level);
            return ItemStack.EMPTY;
        }
        ItemStack result = ItemStack.EMPTY;
        Slot slot = this.slots.get(index);
        if (slot.hasItem()) {
            ItemStack slotStack = slot.getItem();
            result = slotStack.copy();
            if (index >= 1 && index <= 9) {
                if (!this.moveItemStackTo(slotStack, 10, 46, false)) return ItemStack.EMPTY;
            } else if (index >= 10 && index <= 45) {
                if (!this.moveItemStackTo(slotStack, 1, 10, false)) return ItemStack.EMPTY;
            }
            if (slotStack.isEmpty()) slot.set(ItemStack.EMPTY);
            else slot.setChanged();
            if (slotStack.getCount() == result.getCount()) return ItemStack.EMPTY;
            slot.onTake(player, slotStack);
        }
        return result;
    }

    @Override
    public void removed(Player player) {
        super.removed(player);
        this.access.execute((level, pos) -> this.clearContainer(player, this.craftSlots));
    }

    public CraftingContainer getCraftSlots() { return craftSlots; }
}

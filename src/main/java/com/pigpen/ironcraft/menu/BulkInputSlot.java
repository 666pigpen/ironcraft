package com.pigpen.ironcraft.menu;

import net.minecraft.world.Container;
import net.minecraft.world.inventory.Slot;
import net.minecraft.world.item.ItemStack;

public class BulkInputSlot extends Slot {

    private final int maxStack;

    public BulkInputSlot(Container container, int slot, int x, int y, int maxStack) {
        super(container, slot, x, y);
        this.maxStack = maxStack;
    }

    @Override
    public int getMaxStackSize() { return maxStack; }

    @Override
    public int getMaxStackSize(ItemStack stack) { return maxStack; }
}

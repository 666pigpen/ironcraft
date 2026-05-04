package com.pigpen.ironcraft.registry;

import com.pigpen.ironcraft.IronCraft;
import com.pigpen.ironcraft.block.IronCraftingTableBlock;
import net.minecraft.world.level.block.Block;
import net.neoforged.bus.api.IEventBus;
import net.neoforged.neoforge.registries.DeferredBlock;
import net.neoforged.neoforge.registries.DeferredRegister;

public class ModBlocks {
    public static final DeferredRegister.Blocks BLOCKS =
            DeferredRegister.createBlocks(IronCraft.MOD_ID);

    public static final DeferredBlock<Block> IRON_CRAFTING_TABLE =
            BLOCKS.registerBlock("iron_crafting_table", IronCraftingTableBlock::new);

    public static void register(IEventBus eventBus) {
        BLOCKS.register(eventBus);
    }
}

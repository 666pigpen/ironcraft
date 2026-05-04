package com.pigpen.ironcraft.registry;

import com.pigpen.ironcraft.IronCraft;
import net.neoforged.bus.api.IEventBus;
import net.neoforged.neoforge.registries.DeferredRegister;

public class ModItems {
    public static final DeferredRegister.Items ITEMS =
            DeferredRegister.createItems(IronCraft.MOD_ID);

    static {
        // Block item registered via ModBlocks
        ITEMS.registerSimpleBlockItem("iron_crafting_table", ModBlocks.IRON_CRAFTING_TABLE);
    }

    public static void register(IEventBus eventBus) {
        ITEMS.register(eventBus);
    }
}

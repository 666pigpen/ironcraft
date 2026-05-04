package com.pigpen.ironcraft.registry;

import com.pigpen.ironcraft.IronCraft;
import com.pigpen.ironcraft.menu.IronCraftingTableMenu;
import net.minecraft.core.registries.Registries;
import net.minecraft.world.flag.FeatureFlags;
import net.minecraft.world.inventory.MenuType;
import net.neoforged.bus.api.IEventBus;
import net.neoforged.neoforge.registries.DeferredHolder;
import net.neoforged.neoforge.registries.DeferredRegister;

public class ModMenuTypes {
    public static final DeferredRegister<MenuType<?>> MENUS =
            DeferredRegister.create(Registries.MENU, IronCraft.MOD_ID);

    public static final DeferredHolder<MenuType<?>, MenuType<IronCraftingTableMenu>> IRON_CRAFTING_TABLE =
            MENUS.register("iron_crafting_table",
                    () -> new MenuType<>(IronCraftingTableMenu::new, FeatureFlags.VANILLA_SET));

    public static void register(IEventBus eventBus) {
        MENUS.register(eventBus);
    }
}

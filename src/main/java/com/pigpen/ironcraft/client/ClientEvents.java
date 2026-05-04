package com.pigpen.ironcraft.client;

import com.pigpen.ironcraft.registry.ModMenuTypes;
import net.neoforged.neoforge.client.event.RegisterMenuScreensEvent;

public class ClientEvents {

    public static void registerScreens(RegisterMenuScreensEvent event) {
        event.register(ModMenuTypes.IRON_CRAFTING_TABLE.get(), IronCraftingTableScreen::new);
    }
}

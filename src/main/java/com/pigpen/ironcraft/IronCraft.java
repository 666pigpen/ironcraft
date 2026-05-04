package com.pigpen.ironcraft;

import com.mojang.logging.LogUtils;
import com.pigpen.ironcraft.client.ClientEvents;
import com.pigpen.ironcraft.registry.ModBlocks;
import com.pigpen.ironcraft.registry.ModItems;
import com.pigpen.ironcraft.registry.ModMenuTypes;
import net.neoforged.api.distmarker.Dist;
import net.neoforged.bus.api.IEventBus;
import net.neoforged.fml.common.Mod;
import net.neoforged.fml.loading.FMLEnvironment;
import org.slf4j.Logger;

@Mod(IronCraft.MOD_ID)
public class IronCraft {
    public static final String MOD_ID = "ironcraft";
    public static final Logger LOGGER = LogUtils.getLogger();

    public IronCraft(IEventBus modEventBus) {
        ModBlocks.register(modEventBus);
        ModItems.register(modEventBus);
        ModMenuTypes.register(modEventBus);

        if (FMLEnvironment.dist == Dist.CLIENT) {
            modEventBus.addListener(ClientEvents::registerScreens);
        }
    }
}

package com.pigpen.ironcraft.block;

import com.pigpen.ironcraft.menu.IronCraftingTableMenu;
import net.minecraft.core.BlockPos;
import net.minecraft.network.chat.Component;
import net.minecraft.world.InteractionResult;
import net.minecraft.world.MenuProvider;
import net.minecraft.world.SimpleMenuProvider;
import net.minecraft.world.entity.player.Inventory;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.inventory.ContainerLevelAccess;
import net.minecraft.world.level.Level;
import net.minecraft.world.level.block.Block;
import net.minecraft.world.level.block.SoundType;
import net.minecraft.world.level.block.state.BlockBehaviour;
import net.minecraft.world.level.block.state.BlockState;
import net.minecraft.world.phys.BlockHitResult;
import org.jetbrains.annotations.Nullable;

public class IronCraftingTableBlock extends Block {

    private static final Component CONTAINER_TITLE =
            Component.translatable("container.ironcraft.iron_crafting_table");

    public IronCraftingTableBlock(BlockBehaviour.Properties props) {
        super(props.strength(3.5f).sound(SoundType.METAL).requiresCorrectToolForDrops());
    }

    @Override
    protected InteractionResult useWithoutItem(BlockState state, Level level, BlockPos pos,
                                                Player player, BlockHitResult hit) {
        if (level.isClientSide) return InteractionResult.SUCCESS;
        player.openMenu(this.getMenuProvider(state, level, pos));
        return InteractionResult.CONSUME;
    }

    @Override
    public @Nullable MenuProvider getMenuProvider(BlockState state, Level level, BlockPos pos) {
        return new SimpleMenuProvider(
                (id, inv, player) -> new IronCraftingTableMenu(id, inv,
                        ContainerLevelAccess.create(level, pos)),
                CONTAINER_TITLE);
    }
}

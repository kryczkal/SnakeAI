class Settings:
    # Game parameters adjustable by the user
    graphic_on = True
    fps_on = False
    fps = 15
    real_tile_size = 16
    scale = 4
    # Model Parameters
    MAX_MEMORY = 100_000
    BATCH_SIZE = 1000
    LR = 0.001
    # Game parameters adjusted based on user settings
    tile_size = real_tile_size * scale
    grid_size_x = int(64 / scale)
    grid_size_y = int(64 / scale)
    screen_size_x = grid_size_x * tile_size
    screen_size_y = grid_size_y * tile_size
import pygame as pg
from settings import *


class RayCaster:
    def __init__(self, game):
        self.game = game
        self.ray_casting_result = []
        self.objects_to_render = []
        self.textures = self.game.renderer.wall_textures

    def get_objects_to_render(self):
        self.objects_to_render = []
        for ray, values in enumerate(self.ray_casting_result):
            depth, proj_height, texture, offset = values

            if proj_height < HEIGHT:
                wall_column = self.textures[texture].subsurface(
                    offset * (TEXTURE_SIZE - SCALE), 0, SCALE, TEXTURE_SIZE
                )

                wall_column = pg.transform.scale(wall_column, (SCALE, proj_height))
                wall_pos = (ray * SCALE, HALF_HEIGHT - proj_height // 2)
            else:
                texture_height = TEXTURE_SIZE * HEIGHT / proj_height
                wall_column = self.textures[texture].subsurface(
                    offset * (TEXTURE_SIZE - SCALE), HALF_TEXTURE_SIZE - texture_height // 2, SCALE, texture_height
                )

                wall_column = pg.transform.scale(wall_column, (SCALE, HEIGHT))
                wall_pos = (ray * SCALE, 0)

            self.objects_to_render.append((depth, wall_column, wall_pos))

    def cast(self):
        self.ray_casting_result = []
        ox, oy = self.game.player.pos
        x_map, y_map = self.game.player.map_pos
        texture_vertical, texture_horizontal = 1, 1

        ray_angle = self.game.player.angle - HALF_FOV + 0.0001
        for ray in range(NUM_RAYS):
            sin_a = math.sin(ray_angle)
            cos_a = math.cos(ray_angle)

            y_horizontal, dy = (y_map + 1, 1) if sin_a > 0 else (y_map - 1e-6, -1)
            depth_horizontal = (y_horizontal - oy) / sin_a

            x_horizontal = ox + depth_horizontal * cos_a

            delta_depth = dy / sin_a
            dx = delta_depth * cos_a

            for i in range(MAX_DEPTH):
                tile_horizontal = int(x_horizontal), int(y_horizontal)
                if tile_horizontal in self.game.map.world_map:
                    texture_horizontal = self.game.map.world_map[tile_horizontal]
                    break
                x_horizontal += dx
                y_horizontal += dy
                depth_horizontal += delta_depth

            x_vertical, dx = (x_map + 1, 1) if cos_a > 0 else (x_map - 1e-6, -1)
            depth_vertical = (x_vertical - ox) / cos_a

            y_vertical = oy + depth_vertical * sin_a

            delta_depth = dx / cos_a
            dy = delta_depth * sin_a

            for i in range(MAX_DEPTH):
                tile_vertical = int(x_vertical), int(y_vertical)
                if tile_vertical in self.game.map.world_map:
                    texture_vertical = self.game.map.world_map[tile_vertical]
                    break
                x_vertical += dx
                y_vertical += dy
                depth_vertical += delta_depth

            if depth_vertical < depth_horizontal:
                depth, texture = depth_vertical, texture_vertical
                y_vertical %= 1
                offset = y_vertical if cos_a > 0 else (1 - y_vertical)
            else:
                depth, texture = depth_horizontal, texture_horizontal
                x_horizontal %= 1
                offset = (1 - x_horizontal) if sin_a > 0 else x_horizontal

            depth *= math.cos(self.game.player.angle - ray_angle)

            # pg.draw.line(self.game.screen, 'yellow', (100 * ox, 100 * oy),
            #              (100 * ox + 100 * depth * cos_a, 100 * oy + 100 * depth * sin_a), 2)

            proj_height = SCREEN_DIST / (depth + 0.0001)
            self.ray_casting_result.append((depth, proj_height, texture, offset))

            # color = [25 / (1 + depth ** 9 * 0.0002)] * 3
            # pg.draw.rect(self.game.screen, color, (ray * SCALE, HALF_HEIGHT - proj_height // 2, SCALE, proj_height))

            ray_angle += DELTA_ANGLE

    def update(self):
        self.cast()
        self.get_objects_to_render()

import pygame as pg
from settings import *


class RayCaster:
    def __init__(self, game):
        self.game = game

    def cast(self):
        ox, oy = self.game.player.pos
        x_map, y_map = self.game.player.map_pos

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
                    break
                x_vertical += dx
                y_vertical += dy
                depth_vertical += delta_depth

            if depth_vertical < depth_horizontal:
                depth = depth_vertical
            else:
                depth = depth_horizontal

            depth *= math.cos(self.game.player.angle - ray_angle)

            # pg.draw.line(self.game.screen, 'yellow', (100 * ox, 100 * oy),
            #              (100 * ox + 100 * depth * cos_a, 100 * oy + 100 * depth * sin_a), 2)

            proj_height = SCREEN_DIST / (depth + 0.0001)

            color = [25 / (1 + depth ** 9 * 0.0002)] * 3
            pg.draw.rect(self.game.screen, color, (ray * SCALE, HALF_HEIGHT - proj_height // 2, SCALE, proj_height))

            ray_angle += DELTA_ANGLE

    def update(self):
        self.cast()

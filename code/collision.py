import pygame

class Collision:
    @staticmethod
    def check_obstacle_collision(player, obstacles):
        for obstacle in obstacles:
            if obstacle.rect.colliderect(player.hitbox):
                player.take_damage()
                return True
        return False

    @staticmethod
    def check_star_collection(player, stars, on_collect):
        collected = pygame.sprite.spritecollide(player, stars, True,
                                                collided=lambda p, s: p.hitbox.colliderect(s.rect))
        if collected:
            on_collect(len(collected))

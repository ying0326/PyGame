import pygame
import random
from pathlib import Path
from player import Player
from MyMissile import MyMissile

class Explosion:
    def __init__(self, x, y, image):
        self.x = x
        self.y = y
        self.image = image
        self.counter = 0
        self.duration = 20
    def update(self):
        self.counter += 1
    def is_finished(self):
        return self.counter > self.duration
    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))

# === 新增扣分特效類別 ===
class DeductEffect:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.frame = 0
        self.duration = 30   # 顯示 30 frame
    def update(self):
        self.frame += 1
    def is_alive(self):
        return self.frame < self.duration
    def draw(self, screen, font):
        text = font.render("-5", True, (160, 0, 0))  # 深紅色
        offset_y = max(0, 20 - self.frame // 2)
        screen.blit(text, (self.x, self.y - offset_y))

class Enemy:
    def __init__(self, x, y, image):
        self.x = x
        self.y = y
        self.image = image
        self.rect = self.image.get_rect(topleft=(self.x, self.y))
        self.hit = False
        self.available = True
        self.speed_x = random.choice([-1, 1]) * random.uniform(0.5, 2)
        self.speed_y = random.uniform(0.5, 2)
    def update(self):
        self.x += self.speed_x
        self.y += self.speed_y
        if self.x <= 0 or self.x + self.image.get_width() >= 1000:
            self.speed_x *= -1
        self.rect.topleft = (self.x, self.y)
        if self.y > 760:
            self.available = False
    def draw(self, screen):
        if not self.hit:
            screen.blit(self.image, (self.x, self.y))

def display_score(screen, score, font):
    score_text = font.render(f"Score: {score}", True, (255, 0, 0))  # 紅色
    screen.blit(score_text, (screen.get_width() - score_text.get_width() - 30, 20))

def display_game_over(screen, score, font, background):
    screen.blit(background, (0, 0))
    game_over_text = font.render("Game Over", True, (0, 32, 128))
    final_score_text = font.render(f"Final Score: {score}", True, (255, 0, 0))  # 紅色
    exit_text = font.render("Press ESC to Exit", True, (40, 40, 96))
    restart_text = font.render("Press R to Restart", True, (0, 80, 40))
    center_y = screen.get_height() // 2
    screen.blit(game_over_text, ((screen.get_width() - game_over_text.get_width()) // 2, center_y - 110))
    screen.blit(final_score_text, ((screen.get_width() - final_score_text.get_width()) // 2, center_y - 40))
    screen.blit(exit_text, ((screen.get_width() - exit_text.get_width()) // 2, center_y + 50))
    screen.blit(restart_text, ((screen.get_width() - restart_text.get_width()) // 2, center_y + 110))
    pygame.display.flip()

def display_start_screen(screen, font, background):
    screen.blit(background, (0, 0))
    title_text = font.render("Ocean Shooting Game", True, (0, 32, 128))
    start_text = font.render("Press ENTER to Start", True, (0, 32, 128))
    center_y = screen.get_height() // 2
    screen.blit(title_text, ((screen.get_width() - title_text.get_width()) // 2, center_y - 120))
    screen.blit(start_text, ((screen.get_width() - start_text.get_width()) // 2, center_y + 40))
    pygame.display.flip()

def reset_game(screen_width, screen_height, playground):
    player = Player(playground=playground, sensitivity=1000 / 120)
    Missiles = []
    Enemies = []
    Explosions = []
    score = 0
    return player, Missiles, Enemies, Explosions, score

def main():
    pygame.init()
    # === 背景音樂 ===
    parent_path = Path(__file__).parents[1]
    res_path = parent_path / 'res'
    bgm_path = res_path / 'bgm.mp3'
    pygame.mixer.init()
    pygame.mixer.music.load(str(bgm_path))
    pygame.mixer.music.play(-1)

    explosion_sound_path = res_path / 'explosion.mp3'
    explosion_sound = pygame.mixer.Sound(str(explosion_sound_path))
    explosion_sound.set_volume(0.3)

    gameover_sound_path = res_path / 'gameover.mp3'
    gameover_sound = pygame.mixer.Sound(str(gameover_sound_path))
    gameover_sound.set_volume(0.5)

    screen_width = 1000
    screen_height = 750
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("pygame")
    playground = [screen_width, screen_height]

    icon_path = res_path / 'airplan.png'
    background_path = res_path / 'background.png'
    enemy_path = res_path / 'enemy.png'
    explosion_path = res_path / 'explosion.png'

    icon = pygame.image.load(icon_path)
    pygame.display.set_icon(icon)
    background = pygame.image.load(background_path).convert()
    background = pygame.transform.scale(background, (screen_width, screen_height))
    enemy_image = pygame.image.load(enemy_path).convert_alpha()
    explosion_image = pygame.image.load(explosion_path).convert_alpha()
    font = pygame.font.SysFont("Arial", 48)   # 字體變大

    fps = 120
    clock = pygame.time.Clock()

    player, Missiles, Enemies, Explosions, score = reset_game(screen_width, screen_height, playground)

    spawnEnemy = pygame.USEREVENT + 1
    pygame.time.set_timer(spawnEnemy, 2000)
    running = True
    game_over = False

    in_start_screen = True
    DeductEffects = []

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if in_start_screen:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                        in_start_screen = False
                continue

            if game_over:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                    if event.key == pygame.K_r:
                        player, Missiles, Enemies, Explosions, score = reset_game(screen_width, screen_height, playground)
                        game_over = False
                continue

            if event.type == spawnEnemy:
                num_enemies = random.randint(2, 8)
                for _ in range(num_enemies):
                    ex = random.randint(50, screen_width - enemy_image.get_width() - 50)
                    ey = -50
                    Enemies.append(Enemy(ex, ey, enemy_image))

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    center_x = player.x + player.image.get_width() / 2 - 5
                    m_y = player.y
                    plane_left = center_x - 15
                    plane_right = center_x + 15
                    missile1 = MyMissile(xy=(plane_left, m_y), playground=playground, sensitivity=1000/120)
                    missile2 = MyMissile(xy=(plane_right, m_y), playground=playground, sensitivity=1000/120)
                    Missiles.append(missile1)
                    Missiles.append(missile2)

        if in_start_screen:
            display_start_screen(screen, font, background)
            clock.tick(30)
            continue

        if not game_over:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_a]:
                player.to_the_left()
            if keys[pygame.K_d]:
                player.to_the_right()
            if keys[pygame.K_w]:
                player.to_the_top()
            if keys[pygame.K_s]:
                player.to_the_bottom()
            player.update()
            Missiles = [m for m in Missiles if m.available]
            for m in Missiles:
                m.update()

            DeductEffects = [eff for eff in DeductEffects if eff.is_alive()]
            for eff in DeductEffects:
                eff.update()

            new_Enemies = []
            for e in Enemies:
                prev_available = e.available
                e.update()
                if not e.available and not e.hit:
                    score -= 5
                    if score < 0:
                        score = 0
                    DeductEffects.append(DeductEffect(screen_width - 80, 40))
                else:
                    new_Enemies.append(e)
            Enemies = new_Enemies

            Explosions = [ex for ex in Explosions if not ex.is_finished()]
            for ex in Explosions:
                ex.update()
            for e in Enemies:
                for m in Missiles:
                    if e.rect.colliderect(pygame.Rect(m.xy, (m.image.get_width(), m.image.get_height()))):
                        if not e.hit:
                            explosion = Explosion(e.x, e.y, explosion_image)
                            Explosions.append(explosion)
                            explosion_sound.play()
                            e.hit = True
                            e.available = False
                            m.available = False
                            score += 10
            for e in Enemies:
                player_rect = pygame.Rect(player.x, player.y, player.image.get_width(), player.image.get_height())
                if not e.hit and player_rect.colliderect(e.rect):
                    game_over = True
                    gameover_sound.play()

            screen.blit(background, (0, 0))
            for e in Enemies:
                e.draw(screen)
            for m in Missiles:
                screen.blit(m.image, m.xy)
            for ex in Explosions:
                ex.draw(screen)
            for eff in DeductEffects:
                eff.draw(screen, font)
            screen.blit(player.image, player.xy)
            display_score(screen, score, font)
            pygame.display.update()
            clock.tick(fps)
        else:
            display_game_over(screen, score, font, background)
            clock.tick(30)

    pygame.quit()

if __name__ == "__main__":
    main()

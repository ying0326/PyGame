import pygame
import random
from pathlib import Path
from player import Player
from MyMissile import MyMissile

# 爆炸特效類別
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

# 敵機類別
class Enemy:
    def __init__(self, x, y, image):
        self.x = x
        self.y = y
        self.image = image
        self.rect = self.image.get_rect(topleft=(self.x, self.y))
        self.hit = False
        self.available = True
        self.speed_x = random.randint(1, 3) * random.choice([-1, 1])
        self.speed_y = random.randint(1, 4)

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

# 顯示分數
def display_score(screen, score, font):
    score_text = font.render(f"Score: {score}", True, (255, 0, 0))
    screen.blit(score_text, (screen.get_width() - 150, 10))

def main():
    pygame.init()

    # 畫面設定
    screen_width = 1000
    screen_height = 760
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("pygame")
    playground = [screen_width, screen_height]

    # 圖示與資源路徑
    parent_path = Path(__file__).parents[1]
    res_path = parent_path / 'res'
    icon_path = res_path / 'airplan.png'
    background_path = res_path / 'background.png'
    enemy_path = res_path / 'enemy.png'
    explosion_path = res_path / 'explosion.png'

    # 設定 icon 與背景
    icon = pygame.image.load(icon_path)
    pygame.display.set_icon(icon)
    background = pygame.image.load(background_path).convert()
    background = pygame.transform.scale(background, (screen_width, screen_height))

    # 敵機圖片和爆炸圖片
    enemy_image = pygame.image.load(enemy_path).convert_alpha()
    explosion_image = pygame.image.load(explosion_path).convert_alpha()

    # 字體設定
    font = pygame.font.SysFont("Arial", 28)

    # 玩家與參數
    fps = 120
    clock = pygame.time.Clock()
    moving_scale = 1000 / fps
    player = Player(playground=playground, sensitivity=moving_scale)

    # 計分變數
    score = 0

    Missiles = []
    Enemies = []
    Explosions = []
    launchMissile = pygame.USEREVENT + 1
    spawnEnemy = pygame.USEREVENT + 2

    pygame.time.set_timer(spawnEnemy, 2000)

    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # 生成敵機
            if event.type == spawnEnemy:
                num_enemies = random.randint(2, 8)
                for _ in range(num_enemies):
                    ex = random.randint(50, screen_width - enemy_image.get_width() - 50)
                    ey = -50
                    Enemies.append(Enemy(ex, ey, enemy_image))

            # 飛彈發射
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    center_x = player.x + player.image.get_width() / 2 - 5
                    m_y = player.y
                    plane_left = center_x - 15
                    plane_right = center_x + 15
                    missile1 = MyMissile(xy=(plane_left, m_y), playground=playground, sensitivity=moving_scale)
                    missile2 = MyMissile(xy=(plane_right, m_y), playground=playground, sensitivity=moving_scale)
                    Missiles.append(missile1)
                    Missiles.append(missile2)
                    pygame.time.set_timer(launchMissile, 400)

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    pygame.time.set_timer(launchMissile, 0)

        # 更新邏輯與顯示
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            player.to_the_left()
        if keys[pygame.K_d]:
            player.to_the_right()
        if keys[pygame.K_w]:
            player.to_the_top()
        if keys[pygame.K_s]:
            player.to_the_bottom()

        # 更新物件
        player.update()
        Missiles = [m for m in Missiles if m.available]
        for m in Missiles:
            m.update()
        Enemies = [e for e in Enemies if e.available]
        for e in Enemies:
            e.update()
        Explosions = [ex for ex in Explosions if not ex.is_finished()]
        for ex in Explosions:
            ex.update()

        # 碰撞檢測
        for e in Enemies:
            for m in Missiles:
                if e.rect.colliderect(pygame.Rect(m.xy, (m.image.get_width(), m.image.get_height()))):
                    explosion = Explosion(e.x, e.y, explosion_image)
                    Explosions.append(explosion)
                    e.hit = True
                    e.available = False
                    m.available = False
                    score += 1

        # 畫面更新
        screen.blit(background, (0, 0))
        for e in Enemies:
            e.draw(screen)
        for m in Missiles:
            screen.blit(m.image, m.xy)
        for ex in Explosions:
            ex.draw(screen)
        screen.blit(player.image, player.xy)
        display_score(screen, score, font)

        pygame.display.update()
        clock.tick(fps)

    pygame.quit()

if __name__ == "__main__":
    main()

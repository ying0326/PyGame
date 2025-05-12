import pygame
import random
from pathlib import Path
from player import Player
from MyMissile import MyMissile

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
        self.speed_y = 2

    def update(self):
        self.x += self.speed_x
        self.y += self.speed_y

        if self.x <= 0 or self.x + self.image.get_width() >= 1000:
            self.speed_x *= -1

        self.rect.topleft = (self.x, self.y)

        if self.y > 760:
            self.available = False

    def draw(self, screen):
        if self.hit:
            pygame.draw.rect(screen, (255, 0, 0), self.rect)
        else:
            screen.blit(self.image, (self.x, self.y))

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

    # 設定 icon 與背景
    icon = pygame.image.load(icon_path)
    pygame.display.set_icon(icon)
    background = pygame.image.load(background_path).convert()
    background = pygame.transform.scale(background, (screen_width, screen_height))

    # 敵機圖片
    enemy_image = pygame.image.load(enemy_path).convert_alpha()

    # 玩家與參數
    fps = 120
    clock = pygame.time.Clock()
    moving_scale = 1000 / fps
    player = Player(playground=playground, sensitivity=moving_scale)

    Missiles = []
    Enemies = []
    launchMissile = pygame.USEREVENT + 1
    spawnEnemy = pygame.USEREVENT + 2

    pygame.time.set_timer(spawnEnemy, 2000)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # 自動生成敵機
            if event.type == spawnEnemy:
                num_enemies = random.randint(1, 3)
                for _ in range(num_enemies):
                    ex = random.randint(50, screen_width - 50)
                    ey = -50
                    Enemies.append(Enemy(ex, ey, enemy_image))

            # 自動發射飛彈
            if event.type == launchMissile:
                center_x = player.x + player.image.get_width() / 2 - 5
                m_y = player.y
                plane_left = center_x - 15
                plane_right = center_x + 15
                Missiles.append(MyMissile(xy=(plane_left, m_y), playground=playground, sensitivity=moving_scale))
                Missiles.append(MyMissile(xy=(plane_right, m_y), playground=playground, sensitivity=moving_scale))

            # 空白鍵發射
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    center_x = player.x + player.image.get_width() / 2 - 5
                    m_y = player.y
                    plane_left = center_x - 15
                    plane_right = center_x + 15
                    Missiles.append(MyMissile(xy=(plane_left, m_y), playground=playground, sensitivity=moving_scale))
                    Missiles.append(MyMissile(xy=(plane_right, m_y), playground=playground, sensitivity=moving_scale))
                    pygame.time.set_timer(launchMissile, 400)

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    pygame.time.set_timer(launchMissile, 0)

        # ✅ 正確檢查按鍵狀態（上下左右）
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            player.to_the_left()
        if keys[pygame.K_d]:
            player.to_the_right()
        if keys[pygame.K_w]:
            player.to_the_top()
        if keys[pygame.K_s]:
            player.to_the_bottom()

        # 更新飛彈
        player.update()
        Missiles = [m for m in Missiles if m.available]
        for m in Missiles:
            m.update()

        # 更新敵機
        Enemies = [e for e in Enemies if e.available]
        for e in Enemies:
            e.update()

        # 碰撞檢測
        for e in Enemies:
            for m in Missiles:
                if e.rect.colliderect(pygame.Rect(m.xy, (m.image.get_width(), m.image.get_height()))):
                    e.hit = True
                    e.available = False
                    m.available = False

        # 畫面更新
        screen.blit(background, (0, 0))
        for e in Enemies:
            e.draw(screen)
        for m in Missiles:
            screen.blit(m.image, m.xy)
        screen.blit(player.image, player.xy)

        pygame.display.update()
        clock.tick(fps)

    pygame.quit()

if __name__ == "__main__":
    main()

import pygame
from pathlib import Path
from player import Player
from MyMissile import MyMissile

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

    # 設定 icon 與背景
    icon = pygame.image.load(icon_path)
    pygame.display.set_icon(icon)
    background = pygame.image.load(background_path).convert()
    background = pygame.transform.scale(background, (screen_width, screen_height))

    # 玩家與參數
    fps = 120
    clock = pygame.time.Clock()
    moving_scale = 600 / fps
    player = Player(playground=playground, sensitivity=moving_scale)

    keyCountX = 0
    keyCountY = 0
    Missiles = []
    launchMissile = pygame.USEREVENT + 1

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # ✅ 自動發射：兩顆飛彈從中心兩側發射
            if event.type == launchMissile:
                center_x = player.x + player.image.get_width() / 2
                m_y = player.y
                plane_left = center_x - 10
                plane_right = center_x + 10
                Missiles.append(MyMissile(xy=(plane_left, m_y), playground=playground, sensitivity=moving_scale))
                Missiles.append(MyMissile(xy=(plane_right, m_y), playground=playground, sensitivity=moving_scale))

            # 控制與發射鍵
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    keyCountX += 1
                    player.to_the_left()
                if event.key == pygame.K_d:
                    keyCountX += 1
                    player.to_the_right()
                if event.key == pygame.K_s:
                    keyCountY += 1
                    player.to_the_bottom()
                if event.key == pygame.K_w:
                    keyCountY += 1
                    player.to_the_top()
                if event.key == pygame.K_SPACE:
                    center_x = player.x + player.image.get_width() / 2-5
                    m_y = player.y
                    plane_left = center_x - 30
                    plane_right = center_x + 20
                    Missiles.append(MyMissile(xy=(plane_left, m_y), playground=playground, sensitivity=moving_scale))
                    Missiles.append(MyMissile(xy=(plane_right, m_y), playground=playground, sensitivity=moving_scale))
                    pygame.time.set_timer(launchMissile, 400)

            if event.type == pygame.KEYUP:
                if event.key in (pygame.K_a, pygame.K_d):
                    if keyCountX == 1:
                        keyCountX = 0
                        player.stop_x()
                    else:
                        keyCountX -= 1
                if event.key in (pygame.K_w, pygame.K_s):
                    if keyCountY == 1:
                        keyCountY = 0
                        player.stop_y()
                    else:
                        keyCountY -= 1
                if event.key == pygame.K_SPACE:
                    pygame.time.set_timer(launchMissile, 0)

        # 更新邏輯
        player.update()
        Missiles = [m for m in Missiles if m.available]
        for m in Missiles:
            m.update()

        # 畫面渲染
        screen.blit(background, (0, 0))
        for m in Missiles:
            screen.blit(m.image, m.xy)
        screen.blit(player.image, player.xy)
        pygame.display.update()
        clock.tick(fps)

    pygame.quit()

if __name__ == "__main__":
    main()

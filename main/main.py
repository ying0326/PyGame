import pygame
from pathlib import Path
from player import Player
from MyMissile import MyMissile  # 你提供的 MyMissile 類別

def main():
    pygame.init()

    # 畫面設定
    screen_width = 1000
    screen_height = 760
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("pygame")
    playground = [screen_width, screen_height]

    # 載入 icon
    parent_path = Path(__file__).parents[1]
    res_path = parent_path / 'res'
    icon_path = res_path / 'airplan.png'
    icon = pygame.image.load(icon_path)
    pygame.display.set_icon(icon)

    # 背景
    background = pygame.Surface(screen.get_size()).convert()
    background.fill((50, 50, 50))

    # 玩家與參數初始化
    fps = 120
    clock = pygame.time.Clock()
    moving_scale = 600 / fps
    player = Player(playground=playground, sensitivity=moving_scale)

    # 控制鍵紀錄
    keyCountX = 0
    keyCountY = 0

    # 飛彈設定
    Missiles = []
    launchMissile = pygame.USEREVENT + 1  # 自動發射事件 ID

    running = True
    while running:
        # 處理事件
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # 自動發射事件
            if event.type == launchMissile:
                m_x = player.xy[0] + 20
                m_y = player.xy[1]
                Missiles.append(MyMissile(xy=(m_x, m_y), playground=playground, sensitivity=moving_scale))
                m_x = player.xy[0] + 80
                Missiles.append(MyMissile(xy=(m_x, m_y), playground=playground, sensitivity=moving_scale))

            # 按鍵按下
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
                    m_x = player.x + 20
                    m_y = player.y
                    Missiles.append(MyMissile(xy=(m_x, m_y), playground=playground, sensitivity=moving_scale))
                    m_x = player.x + 80
                    Missiles.append(MyMissile(xy=(m_x, m_y), playground=playground, sensitivity=moving_scale))
                    pygame.time.set_timer(launchMissile, 400)  # 每 400 ms 自動發射

            # 放開按鍵
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
                    pygame.time.set_timer(launchMissile, 0)  # 停止自動發射

        # 更新邏輯
        player.update()
        Missiles = [m for m in Missiles if m.available]
        for m in Missiles:
            m.update()

        # 畫面更新
        screen.blit(background, (0, 0))
        for m in Missiles:
            screen.blit(m.image, m.xy)
        screen.blit(player.image, player.xy)
        pygame.display.update()
        clock.tick(fps)

    pygame.quit()

if __name__ == "__main__":
    main()

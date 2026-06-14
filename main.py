"""Dino Game in Python

A game similar to the famous Chrome Dino Game, built using pygame-ce.
Made by intern: @bassemfarid, no one or nothing else. 🤖
"""

import pygame

# Initialize Pygame and create a window
pygame.init()
screen = pygame.display.set_mode((800, 400))
clock = pygame.time.Clock()
running = True  # Pygame main loop, kills pygame when False

# Game state variables
is_playing = True  # Whether in game or in menu
GROUND_Y = 300  # The Y-coordinate of the ground level
JUMP_GRAVITY_START_SPEED = -20  # The speed at which the player jumps
players_gravity_speed = 0  # The current speed at which the player falls

# Load level assets
SKY_SURF = pygame.image.load("graphics/level/sky.png").convert()
GROUND_SURF = pygame.image.load("graphics/level/ground.png").convert()
game_font = pygame.font.Font(pygame.font.get_default_font(), 50)
score_surf = game_font.render("SCORE?", False, "Black")
score_rect = score_surf.get_rect(center=(400, 50))

game_over_surf = game_font.render("GAME OVER", False, (111, 196, 169))
game_over_rect = game_over_surf.get_rect(center=(400, 150))

restart_surf = game_font.render("Press SPACE to restart", False, (111, 196, 169))
restart_rect = restart_surf.get_rect(center=(400, 250))
# Load sprite assets
# 🌟【战斗系统 1】：加载击打动作贴图（比如如果没有专门的挥拳图，可以先用跳跃图或别的图代替，这里我们用 jump 演示，你有专门的攻击图可以换名字）
attack_sprite = pygame.image.load("graphics/player/jump.png").convert_alpha()

# 战斗核心控制状态
is_attacking = False      # 恐龙当前是否正在出拳
attack_cooldown = 0       # 攻击冷却/持续时间计数器（防止无限出拳）
run_sprites = [
    pygame.image.load("graphics/player/player_walk_1.png").convert_alpha(),
    pygame.image.load("graphics/player/player_walk_2.png").convert_alpha()
]
jump_sprite = pygame.image.load("graphics/player/player_jump.png").convert_alpha()
frame_counter = 0.0  
player_surf = run_sprites[0] 
player_rect = player_surf.get_rect(bottomleft=(25, GROUND_Y))
egg_surf = pygame.image.load("graphics/egg/egg_1.png").convert_alpha()
egg_rect = egg_surf.get_rect(bottomleft=(800, GROUND_Y))
# 1. 创建一个空列表，用来装以后生成的各种障碍物（这就是我们的怪物仓库）
obstacle_rect_list = []

# 2. 自定义一个专门属于“生成障碍物”的事件信号（闹钟）
obstacle_timer = pygame.USEREVENT + 1

# 3. 设置闹钟：每隔 1500 毫秒（1.5秒）让系统触发一次 obstacle_timer 事件
pygame.time.set_timer(obstacle_timer, 1500)

def update_player_visuals():
    global player_surf, frame_counter
    
    # 优先度 1：如果正在发动击打，强制换成攻击皮肤（借用 jump 动作）
    if is_attacking:
        player_surf = jump_sprite
    # 优先度 2：如果在空中，播放跳跃
    elif player_rect.bottom < GROUND_Y:
        player_surf = jump_sprite
    # 优先度 3：在地上正常跑步
    else:
        frame_counter += 0.15 
        current_frame = int(frame_counter) % len(run_sprites)
        player_surf = run_sprites[current_frame]

def display_score(): 

    current_time = pygame.time.get_ticks() // 1000 - start_time
    score_surf = game_font.render(f'Score: {current_time}', False, (64, 64, 64))
    score_rect = score_surf.get_rect(center=(400, 50))
    screen.blit(score_surf, score_rect)
    return current_time

def obstacle_movement(obstacle_list):
    if obstacle_list:
        for obstacle_rect in obstacle_list:
            # 1. 让每个障碍物向左移动 5 个像素
            obstacle_rect.x -= 5
            
            # 2. 把蛋画在屏幕上
            screen.blit(egg_surf, obstacle_rect)
            
        # 3. 过滤掉已经滚出屏幕左侧的 Rect，防止列表无限变大导致卡顿
        obstacle_list = [obs for obs in obstacle_list if obs.right > 0]
        return obstacle_list
    else:
        return []

final_score = 0 
start_time = 0

while running:
    # Poll for events
    for event in pygame.event.get():
        # pygame.QUIT --> user clicked X to close your window
        if event.type == pygame.QUIT:
            running = False

        elif is_playing:
            # ⭐ 新增逻辑：如果闹钟响了，说明该生成新怪物了！
            if event.type == obstacle_timer:
                # 每次闹钟响，就创建一个新的蛋的 Rect，并把它扔进仓库列表里
                new_egg_rect = egg_surf.get_rect(bottomleft=(800, GROUND_Y))
                obstacle_rect_list.append(new_egg_rect)

            # When player wants to jump by pressing SPACE
            if (
                event.type == pygame.KEYDOWN
                and event.key == pygame.K_SPACE
                or event.type == pygame.MOUSEBUTTONDOWN
            ) and player_rect.bottom >= GROUND_Y:
                players_gravity_speed = JUMP_GRAVITY_START_SPEED
                # ⭐【战斗系统 2】：监听 J 键，触发攻击状态
            if event.type == pygame.KEYDOWN and event.key == pygame.K_J:
                # 只有在没有处于攻击冷却中，且踩在地上时才能发动击打
                if not is_attacking and player_rect.bottom >= GROUND_Y:
                    is_attacking = True
                    attack_cooldown = 10  # 攻击状态持续 10 帧（大约 0.16 秒）
        else:
            # When player wants to play again by pressing SPACE
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                is_playing = True
                obstacle_rect_list.clear()
                start_time = pygame.time.get_ticks() // 1000

    
    if is_playing:
        screen.fill("purple")  # Wipe the screen

        # Blit the level assets
        screen.blit(SKY_SURF, (0, 0))
        screen.blit(GROUND_SURF, (0, GROUND_Y))
        pygame.draw.rect(screen, "#c0e8ec", score_rect)
        pygame.draw.rect(screen, "#c0e8ec", score_rect, 10)
        #screen.blit(score_surf, score_rect)
        display_score()
        # Adjust egg's horizontal location then blit it
       # ⭐ 换成我们的新函数，让多颗蛋动起来，并更新列表
        obstacle_rect_list = obstacle_movement(obstacle_rect_list) 

        # Adjust player's vertical location then blit it
        players_gravity_speed += 1
        player_rect.y += players_gravity_speed
        if player_rect.bottom > GROUND_Y:
            player_rect.bottom = GROUND_Y

        # ⭐【战斗逻辑 A】：让攻击计时器动起来
        if is_attacking:
            attack_cooldown -= 1
            if attack_cooldown <= 0:
                is_attacking = False # 10帧时间到，自动收招恢复跑步
        update_player_visuals()    
        screen.blit(player_surf, player_rect)
        # ⭐【战斗逻辑 B】：出拳期间的 Hitbox 碎蛋检测
        if is_attacking:
            # 在恐龙右侧边缘往前延伸 60 像素，生成一个 60x60 的隐形攻击矩形
            attack_hitbox = pygame.Rect(player_rect.right, player_rect.y, 60, 60)
            
            # 倒序遍历列表（防止在循环中直接删除元素导致跳项或报错）
            for obstacle_rect in obstacle_rect_list[:]:
                if attack_hitbox.colliderect(obstacle_rect):
                    obstacle_rect_list.remove(obstacle_rect) # 蛋碎了！直接踢飞！
        # When player collides with enemy, game ends
        # ⭐ 换成批量碰撞检测
        for obstacle_rect in obstacle_rect_list:
            if obstacle_rect.colliderect(player_rect):
                is_playing = False
                final_score = pygame.time.get_ticks() // 1000 - start_time

    # When game is over, display game over message
 # When game is over, display game over message
    else:
        screen.fill((94, 129, 162)) # 刷成好看的蓝灰色背景

        
        # 2. 实时生成一个“最终分数”的文字表面
        final_score_surf = game_font.render(f"Final Score: {final_score}", False, (111, 196, 169))
        final_score_rect = final_score_surf.get_rect(center=(400, 320)) # 放在重新开始提示的下面

        # 3. 把所有的文字贴出来
        screen.blit(game_over_surf, game_over_rect)
        screen.blit(restart_surf, restart_rect)
        screen.blit(final_score_surf, final_score_rect) # 贴出最终分数！
    # flip the display to put your work on screen
    pygame.display.flip()

    clock.tick(60)  # Limits game loop to 60 FPS

pygame.quit()

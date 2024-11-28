import pygame
import sys
from Board import Board, SNAME_ACTION
from Q_table import Q_table


def drwa_board(screen, board: Board):

    pygame.draw.rect(screen, (255, 0, 0),
                     (board.red_apple.x * 40, board.red_apple.y * 40, 40, 40))
    pygame.draw.rect(screen, (0, 255, 0),
                     (board.green_apple[0].x * 40,
                      board.green_apple[0].y * 40, 40, 40))
    pygame.draw.rect(screen, (0, 255, 0),
                     (board.green_apple[1].x * 40,
                      board.green_apple[1].y * 40, 40, 40))
    pygame.draw.rect(screen, (0, 0, 255),
                     (board.snake_head.x * 40,
                      board.snake_head.y * 40, 40, 40))
    for body in board.snake_body:
        pygame.draw.rect(screen, (0, 0, 128),
                         (body.x * 40, body.y * 40, 40, 40))


def display_board(args):
    pygame.init()
    screen_size = args.size * 40
    screen = pygame.display.set_mode((screen_size, screen_size))
    pygame.display.set_caption("learn2slither")
    clock = pygame.time.Clock()
    board = Board(args.size)
    print(board)
    Q = Q_table(args.load)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    print(f"R key pressed! State hash: {board.__hash__()}")
                    # print(board)
                if event.key == pygame.K_t:
                    print(f"T key pressed! Snake size: {board.snake_size()}")
                if event.key == pygame.K_e:
                    action = board.max_action(Q, 0)
                    # print(f"E key pressed! Max action key: {action}")
                    print(f"E key pressed! Max action: {SNAME_ACTION[action]}")
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            end, _ = board.left()
            if end:
                # pygame.quit()
                # sys.exit()
                print("end")
        if keys[pygame.K_RIGHT]:
            end, _ = board.right()
            if end:
                # pygame.quit()
                # sys.exit()
                print("end")
        if keys[pygame.K_UP]:
            end, _ = board.up()
            if end:
                # pygame.quit()
                # sys.exit()
                print("end")
        if keys[pygame.K_DOWN]:
            end, _ = board.down()
            if end:
                # pygame.quit()
                # sys.exit()
                print("end")

        screen.fill((0, 0, 0))
        drwa_board(screen, board)
        pygame.display.flip()
        clock.tick(30)  # 30 FPS

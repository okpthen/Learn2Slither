from Q_table import Q_table
from Board import Board, SNAME_ACTION
from config import Default_sessions

def step_by_step(args):
    print("aaa")
    # Q = Q_table(args.load)
    # board = Board(args.size)
    # # pygame.init()
    # board.print_vis()
    # i = 0
    # if args.sessions == Default_sessions:
    #     time = 10
    # else:
    #     time = args.session
    # while True:
    #     # pygame.time.wait(10)
    #     # for event in pygame.event.get():
    #     #     if event.type == pygame.QUIT:
    #     #         pygame.quit()
    #     #         sys.exit()
    #         # if event.type == pygame.KEYDOWN:
    #         #     if event.key == pygame.K_ESCAPE:
    #         #         pygame.quit()
    #         #         sys.exit()
    #     if keyboard.is_pressed("space"):
    #         state = board.state()
    #         action =  Q.max_action(state)
    #         print(SNAME_ACTION[action])
    #         end, _  = board.action(action)
    #         if end:
    #             i += 1
    #             print(f"Game over ({i})")
    #             if i == time:
    #                 break
    #             board.reset()
    #             board.print_vis()


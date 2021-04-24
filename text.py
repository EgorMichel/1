import pygame

pygame.init()

W = 600
H = 400

sc = pygame.display.set_mode((W, H))

FPS = 60
clock = pygame.time.Clock()
counter = 0
while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if (counter % 2 == 0):
                print("Игрок А")
                counter += 1
            else:
                print("Игрок Б")
                counter += 1

    clock.tick(FPS)


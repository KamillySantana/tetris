import pygame
import random

# Inicialização do Pygame
pygame.init()

# Configurações do jogo
SCREEN_WIDTH, SCREEN_HEIGHT = 300, 600
GRID_SIZE = 30
GRID_WIDTH, GRID_HEIGHT = SCREEN_WIDTH // GRID_SIZE, SCREEN_HEIGHT // GRID_SIZE
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Formas do Tetris (cada forma é representada por uma matriz)
SHAPES = [
    [[1, 1, 1, 1]],  # I
    [[1, 1], [1, 1]],  # O
    [[1, 1, 1], [0, 1, 0]],  # T
    [[1, 1, 1], [1, 0, 0]],  # L
    [[1, 1, 1], [0, 0, 1]],  # J
    [[1, 1, 0], [0, 1, 1]],  # S
    [[0, 1, 1], [1, 1, 0]]  # Z
]

# Cores das formas do Tetris
SHAPE_COLORS = [(0, 255, 255), (255, 255, 0), (128, 0, 128),
                (255, 165, 0), (0, 0, 255), (0, 255, 0), (255, 0, 0)]

# Inicialização da tela
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Tetris")

# Fonte para a tela inicial e final de jogo
font = pygame.font.Font(None, 36)


# Função para criar uma forma aleatória
def create_shape():
    shape = random.choice(SHAPES)
    color = random.choice(SHAPE_COLORS)
    return shape, color


# Função para desenhar uma forma na tela
def draw_shape(surface, shape, color, x, y):
    for row in range(len(shape)):
        for col in range(len(shape[row])):
            if shape[row][col]:
                pygame.draw.rect(surface, color, (x + col * GRID_SIZE, y + row * GRID_SIZE, GRID_SIZE, GRID_SIZE))


# Função da tela inicial
def show_start_screen():
    screen.fill(BLACK)
    title_text = font.render("Tetris", True, WHITE)
    start_text = font.render("Clique para jogar", True, WHITE)
    screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, SCREEN_HEIGHT // 2 - 50))
    screen.blit(start_text, (SCREEN_WIDTH // 2 - start_text.get_width() // 2, SCREEN_HEIGHT // 2 + 50))
    pygame.display.update()

    waiting_for_start = True
    while waiting_for_start:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                waiting_for_start = False


# Função para exibir a tela de final de jogo
def show_game_over_screen(score):
    screen.fill(BLACK)
    game_over_text = font.render("Game Over", True, WHITE)
    score_text = font.render(f"Score: {score}", True, WHITE)

    # Usando uma fonte menor para "Clique para jogar novamente"
    restart_font = pygame.font.Font(None, 24)
    restart_text = restart_font.render("Clique para jogar novamente", True, WHITE)

    screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, SCREEN_HEIGHT // 2 - 50))
    screen.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2, SCREEN_HEIGHT // 2))
    screen.blit(restart_text, (SCREEN_WIDTH // 2 - restart_text.get_width() // 2, SCREEN_HEIGHT // 2 + 50))
    pygame.display.update()

    waiting_for_restart = True
    while waiting_for_restart:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                waiting_for_restart = False


# Função principal do jogo
def main():
    clock = pygame.time.Clock()
    game_over = False
    grid = [[0] * GRID_WIDTH for _ in range(GRID_HEIGHT)]
    current_shape, current_color = create_shape()
    x, y = GRID_WIDTH // 2 - len(current_shape[0]) // 2, 0
    score = 0

    # Variáveis para controlar o movimento contínuo
    move_left = False
    move_right = False
    move_down = False
    move_timer = 0

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    # Iniciar o movimento contínuo para a esquerda
                    move_left = True
                elif event.key == pygame.K_RIGHT:
                    # Iniciar o movimento contínuo para a direita
                    move_right = True
                elif event.key == pygame.K_DOWN:
                    # Iniciar o movimento contínuo para baixo
                    move_down = True
                elif event.key == pygame.K_UP:
                    # Girar a forma no sentido horário
                    rotated_shape = rotate_shape(current_shape)
                    if not check_collision(rotated_shape, grid, x, y):
                        current_shape = rotated_shape
                elif event.key == pygame.K_SPACE:
                    # Girar a forma no sentido anti-horário
                    rotated_shape = rotate_shape_anticlockwise(current_shape)
                    if not check_collision(rotated_shape, grid, x, y):
                        current_shape = rotated_shape
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    # Parar o movimento contínuo para a esquerda
                    move_left = False
                elif event.key == pygame.K_RIGHT:
                    # Parar o movimento contínuo para a direita
                    move_right = False
                elif event.key == pygame.K_DOWN:
                    # Parar o movimento contínuo para baixo
                    move_down = False

        # Movimento contínuo para a esquerda
        if move_left:
            if not check_collision(current_shape, grid, x - 1, y):
                x -= 1

        # Movimento contínuo para a direita
        if move_right:
            if not check_collision(current_shape, grid, x + 1, y):
                x += 1

        # Movimento contínuo para baixo
        if move_down:
            if not check_collision(current_shape, grid, x, y + 1):
                y += 1

        # Mover a forma para baixo em intervalos regulares
        move_timer += 1
        if move_timer >= 10:
            move_timer = 0
            if not check_collision(current_shape, grid, x, y + 1):
                y += 1

        # Fixar a forma no grid quando ela não puder mais se mover para baixo
        if check_collision(current_shape, grid, x, y + 1):
            for row in range(len(current_shape)):
                for col in range(len(current_shape[row])):
                    if current_shape[row][col]:
                        grid[y + row][x + col] = current_color

            # Verificar linhas completas e removê-las
            lines_cleared = 0
            for row in range(GRID_HEIGHT):
                if all(grid[row]):
                    del grid[row]
                    grid.insert(0, [0] * GRID_WIDTH)
                    score += 100
                    lines_cleared += 1

            # Adicionar pontos extras por limpar várias linhas ao mesmo tempo
            if lines_cleared > 1:
                score += (lines_cleared - 1) * 50

            # Criar uma nova forma
            current_shape, current_color = create_shape()
            x, y = GRID_WIDTH // 2 - len(current_shape[0]) // 2, 0

            # Verificar fim de jogo
            if check_collision(current_shape, grid, x, y):
                game_over = True

        # Limpar a tela
        screen.fill(BLACK)

        # Desenhar o grid
        for row in range(GRID_HEIGHT):
            for col in range(GRID_WIDTH):
                if grid[row][col]:
                    pygame.draw.rect(screen, grid[row][col], (col * GRID_SIZE, row * GRID_SIZE, GRID_SIZE, GRID_SIZE))

        # Desenhar a forma atual
        draw_shape(screen, current_shape, current_color, x * GRID_SIZE, y * GRID_SIZE)

        # Exibir pontuação na tela
        score_text = font.render(f"Score: {score}", True, WHITE)
        screen.blit(score_text, (10, 10))

        # Atualizar a tela
        pygame.display.update()

        # Controlar a taxa de atualização
        clock.tick(10)

    show_game_over_screen(score)
    main()  # Reiniciar o jogo


# Função para verificar colisões entre a forma atual e o grid
def check_collision(shape, grid, x, y):
    for row in range(len(shape)):
        for col in range(len(shape[row])):
            if shape[row][col]:
                if x + col < 0 or x + col >= GRID_WIDTH or y + row >= GRID_HEIGHT or grid[y + row][x + col]:
                    return True
    return False


# Função para girar uma forma no sentido horário
def rotate_shape(shape):
    return [list(row) for row in zip(*reversed(shape))]


# Função para girar uma forma no sentido anti-horário
def rotate_shape_anticlockwise(shape):
    return [list(reversed(row)) for row in zip(*shape)]


if __name__ == "__main__":
    show_start_screen()
    main()

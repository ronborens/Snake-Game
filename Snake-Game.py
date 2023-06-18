import pygame
import random

# Game Constants
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
BLOCK_SIZE = 20

# Game Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)


class Snake:
    def __init__(self):
        self.length = 1
        self.positions = [((WINDOW_WIDTH // 2), (WINDOW_HEIGHT // 2))]
        self.direction = random.choice(
            [pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT])
        self.color = WHITE

    def get_head_position(self):
        return self.positions[0]

    def turn(self, point):
        if self.length > 1 and any((self.direction == pygame.K_UP and point == pygame.K_DOWN,
                                    self.direction == pygame.K_DOWN and point == pygame.K_UP,
                                    self.direction == pygame.K_LEFT and point == pygame.K_RIGHT,
                                    self.direction == pygame.K_RIGHT and point == pygame.K_LEFT)):
            return
        else:
            self.direction = point

    def move(self):
        cur = self.get_head_position()
        if self.direction == pygame.K_UP:
            self.positions.insert(0, (cur[0], cur[1]-BLOCK_SIZE))
        elif self.direction == pygame.K_DOWN:
            self.positions.insert(0, (cur[0], cur[1]+BLOCK_SIZE))
        elif self.direction == pygame.K_LEFT:
            self.positions.insert(0, (cur[0]-BLOCK_SIZE, cur[1]))
        elif self.direction == pygame.K_RIGHT:
            self.positions.insert(0, (cur[0]+BLOCK_SIZE, cur[1]))
        if len(self.positions) > self.length:
            self.positions.pop()

    def draw(self, surface):
        for p in self.positions:
            pygame.draw.rect(surface, self.color,
                             (p[0], p[1], BLOCK_SIZE, BLOCK_SIZE))


class Apple:
    def __init__(self):
        self.position = (0, 0)
        self.color = RED
        self.randomize_position()

    def randomize_position(self):
        self.position = (random.randint(0, WINDOW_WIDTH//BLOCK_SIZE - 1) * BLOCK_SIZE,
                         random.randint(0, WINDOW_HEIGHT//BLOCK_SIZE - 1) * BLOCK_SIZE)

    def draw(self, surface):
        pygame.draw.rect(
            surface, self.color, (self.position[0], self.position[1], BLOCK_SIZE, BLOCK_SIZE))


class Game:
    def __init__(self):
        pygame.init()
        pygame.font.init()  # you have to call this at the start,
        # if you want to use this module.
        self.myfont = pygame.font.SysFont('Comic Sans MS', 30)
        self.snake = Snake()
        self.apple = Apple()
        self.score = 0
        self.frame_counter = 0
        self.surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.clock = pygame.time.Clock()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.KEYDOWN:
                self.snake.turn(event.key)

    def run(self):
        while True:
            self.handle_events()

            # Only move the snake every 5 frames
            if self.frame_counter % 5 == 0:
                # Predict next head position
                cur = self.snake.get_head_position()
                if self.snake.direction == pygame.K_UP:
                    next_position = (cur[0], cur[1]-BLOCK_SIZE)
                elif self.snake.direction == pygame.K_DOWN:
                    next_position = (cur[0], cur[1]+BLOCK_SIZE)
                elif self.snake.direction == pygame.K_LEFT:
                    next_position = (cur[0]-BLOCK_SIZE, cur[1])
                elif self.snake.direction == pygame.K_RIGHT:
                    next_position = (cur[0]+BLOCK_SIZE, cur[1])

                # Check if the game is over before moving the snake
                if any((next_position[0] > WINDOW_WIDTH - BLOCK_SIZE,
                        next_position[0] < 0,
                        next_position[1] > WINDOW_HEIGHT - BLOCK_SIZE,
                        next_position[1] < 0,
                        next_position in self.snake.positions[1:])):
                    self.game_over()
                else:
                    self.snake.move()
                    self.check_collision()

            self.surface.fill(BLACK)
            self.snake.draw(self.surface)
            self.apple.draw(self.surface)
            score_text = self.myfont.render(
                'Score: {0}'.format(self.score), False, WHITE)
            self.surface.blit(score_text, (5, 5))
            pygame.display.update()
            self.clock.tick(60)
            self.frame_counter += 1

    def check_collision(self):
        if self.snake.get_head_position() == self.apple.position:
            self.snake.length += 1
            self.score += 1
            self.apple.randomize_position()

    def game_over(self):
        self.surface.fill(BLACK)
        game_over_text = self.myfont.render('Game Over!', False, WHITE)
        score_text = self.myfont.render(
            'Score: {0}'.format(self.score), False, WHITE)
        self.surface.blit(
            game_over_text, (WINDOW_WIDTH//2-70, WINDOW_HEIGHT//2-30))
        self.surface.blit(score_text, (WINDOW_WIDTH//2-70, WINDOW_HEIGHT//2))
        pygame.display.update()
        pygame.time.wait(3000)
        self.__init__()


if __name__ == "__main__":
    Game().run()

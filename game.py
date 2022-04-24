import pygame, sys, random
import agent as ag
import main as main

class Game:

    def __init__(self, player_type):
        pygame.init()
        self.clock = pygame.time.Clock()
        self.player_type = player_type
        # screen settings
        self.screen_width = 1280
        self.screen_height = 700

        # --- Bar dimension --- #
        self.bar_width = 10
        self.bar_height = 140

        self.permanentAgentRL = ag.Qlearning(self.screen_height, self.bar_height, 0.85, 0.99)
        if self.player_type == 'agentRL':
            self.agentRL = ag.Qlearning(self.screen_height, self.bar_height, 0.85, 0.99)

        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Pong")
        # objects
        self.ball = pygame.Rect(self.screen_width / 2 - 15, self.screen_height / 2 - 15, 30, 30)

        self.player = pygame.Rect(self.screen_width - (2*self.bar_width), (self.screen_height / 2) - (self.bar_height / 2), self.bar_width, self.bar_height)
        self.opponent = pygame.Rect(self.bar_width, (self.screen_height / 2) - (self.bar_height / 2), self.bar_width, self.bar_height)

        self.bg_color = pygame.Color("grey12")
        self.light_grey = (200, 200, 200)
        self.ball_speed_x = 7 * random.choice((1, -1))
        self.ball_speed_y = 7 * random.choice((1, -1))
        if player_type == 'human':
            self.player_speed = 0
        else:
            self.player_speed = 7
        self.opponent_speed = 7
        # text variables
        self.player_score = 0
        self.opponent_score = 0
        self.game_font = pygame.font.Font("freesansbold.ttf", 32)

    def ball_animation(self):
        self.ball.x += self.ball_speed_x
        self.ball.y += self.ball_speed_y
        if self.ball.top <= 0 or self.ball.bottom >= self.screen_height:
            self.ball_speed_y *= -1
        if self.ball.left <= 0 or self.ball.right >= self.screen_width:
            if self.ball.left <= 0 :
                self.player_score += 1
            if self.ball.right >= self.screen_width:
                self.opponent_score += 1
            self.ball_restart()
        # Collison
        if self.ball.colliderect(self.player) or self.ball.colliderect(self.opponent):
            self.ball_speed_x *= -1

    # --- Animation human --- #
    def animation_human(self):
        self.player.y += self.player_speed
        if self.player.top <= 0:
            self.player.top = 0
        if self.player.bottom >= self.screen_height:
            self.player.bottom = self.screen_height

    # --- Animation agent AI --- #
    def animation_agentAi(self):
        if self.player.top < self.ball.y:
            self.player.top += self.player_speed
        if self.player.bottom > self.ball.y:
            self.player.top -= self.player_speed
        if self.player.top <= 0 :
            self.player.top = 0
        if self.player.bottom >= self.screen_height:
            self.player.bottom -= self.screen_height

    def ball_restart(self):
        self.ball.center = (self.screen_width/2, self.screen_height/2)
        self.ball_speed_y *= random.choice((1,-1))
        self.ball_speed_y *= random.choice((1, -1))


    def play(self):
        # game loop
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    main.plot_agent_reward(self.permanentAgentRL.rewards)
                    sys.exit()

                if self.player_type == 'human':
                    # keys even down and up
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_DOWN:
                            self.player_speed += 6
                        if event.key == pygame.K_UP:
                            self.player_speed -= 6

                    if event.type == pygame.KEYUP:
                        if event.key == pygame.K_DOWN:
                            self.player_speed -= 6
                        if event.key == pygame.K_UP:
                            self.player_speed += 6

            self.ball_animation()

            s = self.permanentAgentRL.centre_to_state(self.opponent.centery, self.screen_height, self.bar_height)
            self.opponent.y = self.permanentAgentRL.update(s, self.opponent, self.ball, self.screen_height, self.ball_speed_x, True)
            if self.player_type == 'human':
                self.animation_human()
            elif self.player_type == 'agentAI':
                self.animation_agentAi()
            elif self.player_type == 'agentRL':
                s = self.agentRL.centre_to_state(self.player.centery, self.screen_height, self.bar_height)
                self.player.y = self.agentRL.update(s, self.player, self.ball, self.screen_height, self.ball_speed_x, False)

            # visuals
            self.screen.fill(self.bg_color)
            pygame.draw.rect(self.screen, self.light_grey, self.player)
            pygame.draw.rect(self.screen, self.light_grey, self.opponent)
            pygame.draw.ellipse(self.screen, self.light_grey, self.ball)
            pygame.draw.aaline(self.screen, self.light_grey, (self.screen_width / 2, 0), (self.screen_width / 2, self.screen_height))

            player_txt = self.game_font.render(f"{self.player_score}", False, self.light_grey)
            self.screen.blit(player_txt, ((self.screen_width / 2)+40, 470))
            player_type = self.game_font.render(f"{self.player_type}", False, self.light_grey)
            self.screen.blit(player_type, (self.screen_width-160, 10))

            opponent_txt = self.game_font.render(f"{self.opponent_score}", False, self.light_grey)
            self.screen.blit(opponent_txt, ((self.screen_width / 2)-60, 470))
            opponent_type = self.game_font.render("agentRL", False, self.light_grey)
            self.screen.blit(opponent_type, (30, 10))

            # updating the window
            pygame.display.flip()
            self.clock.tick(60)
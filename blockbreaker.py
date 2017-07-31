import sys, pygame, random

class Breakout():

    def main(self):
        #definir principais funcoes e velocidades do jogo

        xspeed_init = 6
        yspeed_init = 6
        max_lives = 5
        paddle_speed = 30
        score = 0
        bgcolour = 20, 23, 22  # cinzaescuro para cor de fundo
        size = width, height = 640, 480   #tamanho da tela de jogo

        pygame.init()
        screen = pygame.display.set_mode(size)

         #carregar imagens
        paddle = pygame.image.load("paddle.png").convert()
        paddlerect = paddle.get_rect()

        ball = pygame.image.load("ball.png").convert()
        ball.set_colorkey((255, 255, 255))
        ballrect = ball.get_rect()

        #Comentando para ficar sem som
        #Procurar outro som depois, menos irritante
        ##beep = pygame.mixer.Sound('BlipSound.wav')
        ##beep.set_volume(10)

        wall = Wall()
        wall.build_wall(width)

    # Preparar tudo para inicializar o jogo (posicao de paddle, bola, vidas, etc)
        paddlerect = paddlerect.move((width / 2) - (paddlerect.right / 2), height - 20)
        ballrect = ballrect.move(width / 2, height / 2)
        xspeed = xspeed_init
        yspeed = yspeed_init
        lives = max_lives
        clock = pygame.time.Clock()
        pygame.key.set_repeat(1,30)
        pygame.mouse.set_visible(0)       # Deixa o mouse invisivel

        while 1:

            # 60 [F]rames [P]er [S]econd
            clock.tick(60)

            # Saber quais teclas estao sendo apertadas e o qual acao acontece
            # apos serem apertadas
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
        	            sys.exit()
                    if event.key == pygame.K_LEFT:
                        paddlerect = paddlerect.move(-paddle_speed, 0)
                        if (paddlerect.left < 0):
                            paddlerect.left = 0
                    if event.key == pygame.K_RIGHT:
                        paddlerect = paddlerect.move(paddle_speed, 0)
                        if (paddlerect.right > width):
                            paddlerect.right = width

            # verificar se o paddle bateu na bola
            if ballrect.bottom >= paddlerect.top and ballrect.bottom <= paddlerect.bottom and ballrect.right >= paddlerect.left and ballrect.left <= paddlerect.right:
                yspeed = -yspeed
                ##beep.play(0)
                offset = ballrect.center[0] - paddlerect.center[0]

                # Deslocamento (offset) > 0 significa que a bola bateu no paddle
                # variar o angulo da bola, dependendo de onde a bola bate no paddle
                if offset > 0:
                    if offset > 30:
                        xspeed = 7
                    elif offset > 23:
                        xspeed = 6
                    elif offset > 17:
                        xspeed = 5
                else:
                    if offset < -30:
                        xspeed = -7
                    elif offset < -23:
                        xspeed = -6
                    elif xspeed < -17:
                        xspeed = -5

            # movendo paddle/ball
            ballrect = ballrect.move(xspeed, yspeed)
            if ballrect.left < 0 or ballrect.right > width:
                xspeed = -xspeed
                ##beep.play(0)
            if ballrect.top < 0:
                yspeed = -yspeed
                ##beep.play(0)

            # Verificando se a bola passou do paddle e perder 1 vida
            if ballrect.top > height:
                lives -= 1

                """ #Deveria fazer aparecer a quantidade de vidas
                    no canto superior esquerdo da tela



                screen.fill(bgcolour)
                livestext = pygame.font.Font(None,40).render(str(lives), True, (0,255,255), bgcolour)
                livestextrect = livestext.get_rect()
                livestextrect = livestextrect.move(width - livestextrect.left, 0)
                screen.blit(livestext, livestextrect)
                """


                # iniciar nova bola
                xspeed = xspeed_init
                rand = random.random()
                if random.random() > 0.5:
                    xspeed = -xspeed
                yspeed = yspeed_init
                ballrect.center = width * random.random(), height / 3

                # Mensagem de GameOver quando as vidas chegarem a 0
                if lives == 0:
                    msg = pygame.font.Font(None,70).render("Game Over", True, (0,255,255), bgcolour)
                    msgrect = msg.get_rect()
                    msgrect = msgrect.move(width / 2 - (msgrect.center[0]), height / 3)
                    screen.blit(msg, msgrect)
                    pygame.display.flip()
                    # process key presses
                    #     - ESC to quit
                    #     - qualquer outra tecla para restart
                    while 1:
                        restart = False
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                sys.exit()
                            if event.type == pygame.KEYDOWN:
                                if event.key == pygame.K_ESCAPE:
                    	            sys.exit()
                                if not (event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT):
                                    restart = True
                        if restart:
                            screen.fill(bgcolour)
                            wall.build_wall(width)
                            lives = max_lives
                            score = 0
                            break

            if xspeed < 0 and ballrect.left < 0:
                xspeed = -xspeed
                ##beep.play(0)

            if xspeed > 0 and ballrect.right > width:
                xspeed = -xspeed
                ##beep.play(0)

            # Verificar se a bola atingiu parede/brick
            # Se sim entao excluir o tijolo e mudar a direcao da bola
            index = ballrect.collidelist(wall.brickrect)
            if index != -1:
                if ballrect.center[0] > wall.brickrect[index].right or \
                   ballrect.center[0] < wall.brickrect[index].left:
                    xspeed = -xspeed
                else:
                    yspeed = -yspeed
                ##beep.play(0)
                wall.brickrect[index:index + 1] = []
                score += 10

            screen.fill(bgcolour)
            scoretext = pygame.font.Font(None,40).render(str(score), True, (0,255,255), bgcolour)
            scoretextrect = scoretext.get_rect()
            scoretextrect = scoretextrect.move(width - scoretextrect.right, 0)
            screen.blit(scoretext, scoretextrect)

            for i in range(0, len(wall.brickrect)):
                screen.blit(wall.brick, wall.brickrect[i])

            # Se todos os tijolos foram destruidos completamente, reconstrui-los
            if wall.brickrect == []:
                wall.build_wall(width)
                xspeed = xspeed_init
                yspeed = yspeed_init
                ballrect.center = width / 2, height / 3

            screen.blit(ball, ballrect)
            screen.blit(paddle, paddlerect)
            pygame.display.flip()

class Wall():

    def __init__(self):
        self.brick = pygame.image.load("brick.png").convert()
        brickrect = self.brick.get_rect()
        self.bricklength = brickrect.right - brickrect.left
        self.brickheight = brickrect.bottom - brickrect.top

    def build_wall(self, width):
        xpos = 0
        ypos = 60
        adj = 0
        self.brickrect = []
        for i in range (0, 52):
            if xpos > width:
                if adj == 0:
                    adj = self.bricklength / 2
                else:
                    adj = 0
                xpos = -adj
                ypos += self.brickheight

            self.brickrect.append(self.brick.get_rect())
            self.brickrect[i] = self.brickrect[i].move(xpos, ypos)
            xpos = xpos + self.bricklength

if __name__ == '__main__':
    br = Breakout()
    br.main()

import pygame

class Controller:

    def __init__(self):
        self.isRunning = True
        self.keysPressed = {
            "UP": False,
            "DOWN": False,
            "LEFT": False,
            "RIGHT": False
            }


    def updateEvents(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.isRunning = False

            #toggle arrow keys
            elif event.type == pygame.KEYDOWN:

                if event.key == pygame.K_q or event.key == pygame.K_ESCAPE:
                    self.isRunning = False

                elif event.key == pygame.K_UP:
                    self.keysPressed["UP"] = True

                elif event.key == pygame.K_DOWN:
                    self.keysPressed["DOWN"] = True

                elif event.key == pygame.K_LEFT:
                    self.keysPressed["LEFT"] = True
    
                elif event.key == pygame.K_RIGHT:
                    self.keysPressed["RIGHT"] = True

            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_UP:
                    self.keysPressed["UP"] = False

                elif event.key == pygame.K_DOWN:
                    self.keysPressed["DOWN"] = False

                elif event.key == pygame.K_LEFT:
                    self.keysPressed["LEFT"] = False

                elif event.key == pygame.K_RIGHT:
                    self.keysPressed["RIGHT"] = False

    def getKeyStates(self):
        return self.keysPressed

    def checkRunStatus(self):
        return self.isRunning

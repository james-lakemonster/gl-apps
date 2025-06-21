import pygame

class Controller:

    def __init__(self):
        self.run = True

        self.fullscreen_pressed = False
        self.fullscreen = False

        self.outputs = {
            "push": 0.0,
            "twist": 0.0
            }

        self.keysPressed = {
            "UP": False,
            "DOWN": False,
            "LEFT": False,
            "RIGHT": False
            }


    def update(self):

        self.outputs["push"] = 0.0
        self.outputs["twist"] = 0.0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.run = False

            #toggle arrow keys
            elif event.type == pygame.KEYDOWN:

                if event.key == pygame.K_q or event.key == pygame.K_ESCAPE:
                    self.run = False

                elif event.key == pygame.K_f:
                    # toggle full screen
                    if self.fullscreen_pressed == False:
                        self.fullscreen = not self.fullscreen
                    self.fullscreen_pressed = True

                elif event.key == pygame.K_UP:
                    output["push"] += 1.0

                elif event.key == pygame.K_DOWN:
                    output["push"] -= 1.0

                elif event.key == pygame.K_LEFT:
                    self.outputs["twist"] -= 1.0
    
                elif event.key == pygame.K_RIGHT:
                    self.outputs["twist"] += 1.0

            # single action key press functions need to be checked for key release
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_f:
                    # toggle full screen
                    self.fullscreen_pressed = False

    def getOutputs(self):
        return self.outputs

    def checkRunRequest(self):
        return self.run

    def checkFullScreenRequest(self):
        return self.fullscreen

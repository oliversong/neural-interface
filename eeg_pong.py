# -----------------------------------------------------------------------------
# WARNING: GAME WILL NOT WORK UNLESS LSL STREAM IS ACTIVE
# OpenBCI EEG Pong
# Language - Python
# Modules - pygame, sys, random, math, pyqtgraph
#
# Controls - Arrow Keys for Right Paddle and WASD Keys for Left Paddle
#
# Modified by Robert Henry Goldansky
#
# -----------------------------------------------------------------------------
import pygame
import numpy as np
import random
import time
import matplotlib.pyplot as plt
import sys
from matplotlib import style
from collections import deque
from math import *
from pylsl import StreamInlet, resolve_stream
from time import sleep
# -----------------------------------------------------------------------------

# initializes the game engine
pygame.init()

# parameters for windowed screen
width = 600
height = 400

# creates the screen itself
display = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()
pygame.display.set_caption('OpenBCI EEG Pong')

background = (27, 38, 49)
white = (236, 240, 241)
red = (203, 67, 53)
blue = (52, 152, 219)
yellow = (244, 208, 63)

top = white
bottom = white
left = white
right = white

margin = 4

scoreLeft = 0
scoreRight = 0
maxScore = 10

font = pygame.font.SysFont("Small Fonts", 30)
largeFont = pygame.font.SysFont("Small Fonts", 60)

# EEG Pong Sound Effects
left_paddle_sound = pygame.mixer.Sound('pongblipf4.wav')
right_paddle_sound = pygame.mixer.Sound('pongblipf5.wav')

left_player_scores = pygame.mixer.Sound('pongblipa-3.wav')
right_player_scores = pygame.mixer.Sound('pongblipf3.wav')


# Draw the Boundary of Board
def boundary():
    global top, bottom, left, right
    pygame.draw.rect(display, left, (0, 0, margin, height))
    pygame.draw.rect(display, top, (0, 0, width, margin))
    pygame.draw.rect(display, right, (width - margin, 0, margin, height))
    pygame.draw.rect(display, bottom, (0, height - margin, width, margin))

    length = 25

    pygame.draw.rect(display, white, (width / 2 - margin / 2, 10, margin, length))
    pygame.draw.rect(display, white, (width / 2 - margin / 2, 60, margin, length))
    pygame.draw.rect(display, white, (width / 2 - margin / 2, 110, margin, length))
    pygame.draw.rect(display, white, (width / 2 - margin / 2, 160, margin, length))
    pygame.draw.rect(display, white, (width / 2 - margin / 2, 210, margin, length))
    pygame.draw.rect(display, white, (width / 2 - margin / 2, 260, margin, length))
    pygame.draw.rect(display, white, (width / 2 - margin / 2, 310, margin, length))
    pygame.draw.rect(display, white, (width / 2 - margin / 2, 360, margin, length))


# Paddle Class
class Paddle:
    def __init__(self, position):
        self.w = 10
        self.h = self.w * 8
        self.paddleSpeed = 6

        if position == -1:
            self.x = 1.5 * margin
        else:
            self.x = width - 1.5 * margin - self.w

        self.y = height / 2 - self.h / 2

    # Show the Paddle
    def show(self):
        pygame.draw.rect(display, white, (self.x, self.y, self.w, self.h))

    # Move the Paddle
    def move(self, y_direction):
        self.y += self.paddleSpeed * y_direction
        if self.y < 0:
            self.y -= self.paddleSpeed * y_direction
        elif self.y + self.h > height:
            self.y -= self.paddleSpeed * y_direction


leftPaddle = Paddle(-1)
rightPaddle = Paddle(1)


# Ball Class
class Ball:
    def __init__(self, color):
        self.r = 20
        self.x = width / 2 - self.r / 2
        self.y = height / 2 - self.r / 2
        self.color = color
        self.angle = random.randint(-75, 75)
        if random.randint(0, 1):
            self.angle += 180

        self.speed = 8

    # Show the Ball
    def show(self):
        pygame.draw.ellipse(display, self.color, (self.x, self.y, self.r, self.r))

    # Move the Ball
    def move(self):
        global scoreLeft, scoreRight
        self.x += self.speed * cos(radians(self.angle))
        self.y += self.speed * sin(radians(self.angle))
        if self.x + self.r > width - margin:
            scoreLeft += 1
            left_player_scores.play()
            self.angle = 180 - self.angle
        if self.x < margin:
            scoreRight += 1
            right_player_scores.play()
            self.angle = 180 - self.angle
        if self.y < margin:
            self.angle = - self.angle
        if self.y + self.r >= height - margin:
            self.angle = - self.angle

    # Check and Reflect the Ball when it hits the paddles
    def check_for_paddle(self):
        if self.x < width / 2:
            if leftPaddle.x < self.x < leftPaddle.x + leftPaddle.w:
                if leftPaddle.y < self.y < leftPaddle.y + 10 or leftPaddle.y < self.y + self.r < leftPaddle.y + 10:
                    left_paddle_sound.play()
                    self.angle = -45
                if leftPaddle.y + 10 < self.y < leftPaddle.y + 20 or leftPaddle.y + 10 < self.y + self.r < leftPaddle.y\
                        + 20:
                    left_paddle_sound.play()
                    self.angle = -30
                if leftPaddle.y + 20 < self.y < leftPaddle.y + 30 or leftPaddle.y + 20 < self.y + self.r < leftPaddle.y\
                        + 30:
                    left_paddle_sound.play()
                    self.angle = -15
                if leftPaddle.y + 30 < self.y < leftPaddle.y + 40 or leftPaddle.y + 30 < self.y + self.r < leftPaddle.y\
                        + 40:
                    left_paddle_sound.play()
                    self.angle = -10
                if leftPaddle.y + 40 < self.y < leftPaddle.y + 50 or leftPaddle.y + 40 < self.y + self.r < leftPaddle.y\
                        + 50:
                    left_paddle_sound.play()
                    self.angle = 10
                if leftPaddle.y + 50 < self.y < leftPaddle.y + 60 or leftPaddle.y + 50 < self.y + self.r < leftPaddle.y\
                        + 60:
                    left_paddle_sound.play()
                    self.angle = 15
                if leftPaddle.y + 60 < self.y < leftPaddle.y + 70 or leftPaddle.y + 60 < self.y + self.r < leftPaddle.y\
                        + 70:
                    left_paddle_sound.play()
                    self.angle = 30
                if leftPaddle.y + 70 < self.y < leftPaddle.y + 80 or leftPaddle.y + 70 < self.y + self.r < leftPaddle.y\
                        + 80:
                    left_paddle_sound.play()
                    self.angle = 45
        else:
            if rightPaddle.x + rightPaddle.w > self.x + self.r > rightPaddle.x:
                if rightPaddle.y < self.y < leftPaddle.y + 10 or leftPaddle.y < self.y + self.r < leftPaddle.y + 10:
                    right_paddle_sound.play()
                    self.angle = -135
                if rightPaddle.y + 10 < self.y < rightPaddle.y + 20 or rightPaddle.y + 10 < self.y + self.r < \
                        rightPaddle.y + 20:
                    right_paddle_sound.play()
                    self.angle = -150
                if rightPaddle.y + 20 < self.y < rightPaddle.y + 30 or rightPaddle.y + 20 < self.y + self.r < \
                        rightPaddle.y + 30:
                    right_paddle_sound.play()
                    self.angle = -165
                if rightPaddle.y + 30 < self.y < rightPaddle.y + 40 or rightPaddle.y + 30 < self.y + self.r < \
                        rightPaddle.y + 40:
                    right_paddle_sound.play()
                    self.angle = 170
                if rightPaddle.y + 40 < self.y < rightPaddle.y + 50 or rightPaddle.y + 40 < self.y + self.r < \
                        rightPaddle.y + 50:
                    right_paddle_sound.play()
                    self.angle = 190
                if rightPaddle.y + 50 < self.y < rightPaddle.y + 60 or rightPaddle.y + 50 < self.y + self.r < \
                        rightPaddle.y + 60:
                    right_paddle_sound.play()
                    self.angle = 165
                if rightPaddle.y + 60 < self.y < rightPaddle.y + 70 or rightPaddle.y + 60 < self.y + self.r < \
                        rightPaddle.y + 70:
                    right_paddle_sound.play()
                    self.angle = 150
                if rightPaddle.y + 70 < self.y < rightPaddle.y + 80 or rightPaddle.y + 70 < self.y + self.r < \
                        rightPaddle.y + 80:
                    right_paddle_sound.play()
                    self.angle = 135


# Function to Show the score on the screen
def show_score():
    left_score_text = font.render("Score : " + str(scoreLeft), True, red)
    right_score_text = font.render("Score : " + str(scoreRight), True, blue)

    display.blit(left_score_text, (3 * margin, 3 * margin))
    display.blit(right_score_text, (width / 2 + 3 * margin, 3 * margin))


# Function to display FPS in realtime
def show_fps():
    fps_message = font.render("FPS = ", True, white)
    display.blit(fps_message, (480, 25))
    fps = font.render(str(int(clock.get_fps())), True, white)
    display.blit(fps, (550, 25))


# Show controls Function
def show_controls():
    left_player_control_message = font.render("W - Paddle Up, S - Paddle Down", True, red)
    right_player_control_message = font.render("Up Arrow - Paddle Up, Down Arrow - Paddle Down", True, blue)

    display.blit(left_player_control_message, (140, 345))
    display.blit(right_player_control_message, (60, 370))


# Game Over Function
def game_over():
    if scoreLeft == maxScore or scoreRight == maxScore:
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    close()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        close()
                    if event.key == pygame.K_r:
                        reset()
            if scoreLeft == maxScore:
                player_1_wins = largeFont.render("Left Player Wins!", True, red)
                winner_message = player_1_wins
            elif scoreRight == maxScore:
                player_2_wins = largeFont.render("Right Player Wins!", True, blue)
                winner_message = player_2_wins

            reset_message_1 = font.render("Press R to reset game", True, white)
            reset_message_2 = font.render("Or press ESC to Quit!", True, white)
            display.blit(winner_message, (125, 180))
            display.blit(reset_message_1, (200, 220))
            display.blit(reset_message_2, (200, 240))
            pygame.display.update()


# Pause Game Function
def pause():
    paused = True

    pause_message_1 = largeFont.render("GAME PAUSED!", True, white)
    display.blit(pause_message_1, (145, 180))
    pause_message_2 = font.render("Press SPACEBAR or P to CONTINUE.", True, white)
    display.blit(pause_message_2, (125, 220))
    pause_message_3 = font.render("Press ESC to QUIT.", True, white)
    display.blit(pause_message_3, (210, 240))

    pygame.display.update()
    clock.tick(5)

    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                close()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE or event.key == pygame.K_p:
                    paused = False
                if event.key == pygame.K_F1:
                    pygame.display.set_mode((width, height), pygame.FULLSCREEN)
                if event.key == pygame.K_F2:
                    pygame.display.set_mode((width, height))
                elif event.key == pygame.K_ESCAPE:
                    close()
                    paused = False
            if event.type == pygame.KEYUP:
                paused = True


def ready():
    paused = True

    ready_message_1 = largeFont.render("Are you ready to play!", True, white)
    display.blit(ready_message_1, (75, 180))
    ready_message_2 = font.render("Press SPACEBAR or P to BEGIN.", True, white)
    display.blit(ready_message_2, (130, 220))
    ready_message_3 = font.render("Press ESC to QUIT.", True, white)
    display.blit(ready_message_3, (200, 240))

    pygame.mouse.set_visible(False)
    pygame.display.update()

    while paused:
        for event in pygame.event.get():

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE or event.key == pygame.K_p:
                    paused = False
                if event.key == pygame.K_ESCAPE:
                    close()
                if event.key == pygame.K_F1:
                    pygame.display.set_mode((width, height), pygame.FULLSCREEN)
                if event.key == pygame.K_F2:
                    pygame.display.set_mode((width, height))


def reset():
    global scoreLeft, scoreRight
    scoreLeft = 0
    scoreRight = 0
    board()


def close():
    print('Game Closed Successfully!')
    pygame.quit()
    sys.exit()


# -----------------------------------------------------------------------------

def create_lsl_inlet_manually():
    # first resolve an EEG stream on the lab network
    print("looking for an EEG stream...")
    current_stream = resolve_stream('type', 'EEG')

    # create a new inlet to read from the stream
    return StreamInlet(current_stream[0])


# -----------------------------------------------------------------------------

def display_lsl_in_terminal(data_inlet):
    while pygame.K_F6:
        # get a new sample (you can also omit the timestamp part if you're not
        # interested in it)
        chunk, timestamps = data_inlet.pull_chunk()
        # chunk = 4.5 / 24 / (2 ^ 23 - 1)
        if timestamps:
            print(timestamps, chunk)
            break


# -----------------------------------------------------------------------------------

def board():
    loop = True
    left_change = 0
    right_change = 0
    ball = Ball(yellow)
    while loop:
        #test_lsl_pulse_data()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                close()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    close()
                if event.key == pygame.K_SPACE or event.key == pygame.K_p:
                    pause()
                if event.key == pygame.K_r:
                    reset()
                if event.key == pygame.K_w:
                    left_change = -1
                if event.key == pygame.K_s:
                    left_change = 1
                if event.key == pygame.K_UP:
                    right_change = -1
                if event.key == pygame.K_DOWN:
                    right_change = 1
                if event.key == pygame.K_F1:
                    pygame.display.set_mode((width, height), pygame.FULLSCREEN)
                if event.key == pygame.K_F2:
                    pygame.display.set_mode((width, height))
            if event.type == pygame.KEYUP:
                left_change = 0
                right_change = 0

        leftPaddle.move(left_change)
        rightPaddle.move(right_change)
        ball.move()
        ball.check_for_paddle()

        display.fill(background)
        show_score()
        show_controls()
        show_fps()

        ball.show()
        leftPaddle.show()
        rightPaddle.show()

        boundary()
        game_over()

        pygame.display.update()
        clock.tick(60)


ready()
board()

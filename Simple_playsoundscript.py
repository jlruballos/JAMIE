import pygame

pygame.init()
pygame.mixer.music.load('C:\\Users\\Jorge\\Desktop\\engr_285\\Clog_Bot\\jokes\\Joke_6.wav')
pygame.mixer.music.play()

while pygame.mixer.music.get_busy():
    pygame.time.Clock().tick(10)
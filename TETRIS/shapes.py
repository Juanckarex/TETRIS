from tkinter import W
import pygame
W = 10
#from main import W

figures_pos = [[(-1, 0), (-2, 0), (0, 0), (1, 0)],  #I
               [(0, -1), (-1, -1), (-1, 0), (0, 0)],    #0
               [(-1, 0), (-1, 1), (0, 0), (0, -1)], # S
               [(0, 0), (-1, 0), (0, 1), (-1, -1)], # z
               [(0, 0), (0, -1), (0, 1), (-1, -1)], # J
               [(0, 0), (0, -1), (0, 1), (1, -1)], # L
               [(0, 0), (0, -1), (0, 1), (-1, 0)]] # T

#optinal figures [(0, 0), (-1, 0), (0, 1),(0,1)],,  # T
#               [(-1, 0), (-1, 0), (0, 0), (1, 0)]

figures = [[pygame.Rect(x + W // 2, y + 1, 1, 1) for x, y in fig_pos] for fig_pos in figures_pos]
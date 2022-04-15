import pygame
import os
import random
import time
import brainflow
import numpy as np
import csv

from csv import writer
import brainflow
from brainflow.board_shim import BoardShim, BrainFlowInputParams, LogLevels, BoardIds
from brainflow.data_filter import DataFilter, FilterTypes, AggOperations

output_file = "C:/Users/W10/OneDrive/Desktop/Spring 2022/crux_prompt/bf_gui_output.csv"

# board settings
board_id = BoardIds.SYNTHETIC_BOARD.value
#board_id = BoardIds.GANGLION_BOARD.value
serial_port = 'COM4'
#mac_address = '12345'

# columns used
colsused = np.array(BoardShim.get_exg_channels(board_id))
# sampling rate
sampling_rate = BoardShim.get_sampling_rate(board_id)

pygame.init()
WIDTH, HEIGHT = 900, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Crux Prompt")

WHITE = (255, 255, 255)
RED = (255,0,0)

FPS = 60

three_img = pygame.image.load(os.path.join('Assets', '3.png'))
three_img = pygame.transform.scale(three_img, (three_img.get_width()//2, three_img.get_height()//2))
two_img = pygame.image.load(os.path.join('Assets', '2.png'))
two_img = pygame.transform.scale(two_img, (two_img.get_width()//2, two_img.get_height()//2))
one_img = pygame.image.load(os.path.join('Assets', '1.png'))
one_img = pygame.transform.scale(one_img, (one_img.get_width()//2, one_img.get_height()//2))
clench_img = pygame.image.load(os.path.join('Assets', 'clench.png'))
clench_img = pygame.transform.scale(clench_img, (clench_img.get_width()//3, clench_img.get_height()//3))
raise_img = pygame.image.load(os.path.join('Assets', 'raise.png'))
raise_img = pygame.transform.scale(raise_img, (raise_img.get_width()//3, raise_img.get_height()//3))

def draw_window():
    WIN.fill(WHITE)
    WIN.blit(three_img, (300, 100))
    pygame.display.update()

def clench_prompt(counter):
    event_img = clench_img
    screen_col = WHITE
    space_prompt = False
    if counter == 3:
        show_img = three_img
    if counter == 2:
        show_img = two_img
    if counter == 1:
        show_img = one_img
    if counter == 0:
        show_img = None
        screen_col = RED
        space_prompt = True
    return show_img, screen_col, event_img, space_prompt

def raise_prompt(counter):
    event_img = raise_img
    screen_col = WHITE
    space_prompt = False
    if counter == 3:
        show_img = three_img
    if counter == 2:
        show_img = two_img
    if counter == 1:
        show_img = one_img
    if counter == 0:
        show_img = None
        screen_col = RED
        space_prompt = True
    return show_img, screen_col, event_img, space_prompt

def random_prompt():
    event_int = random.randint(0, 1);
    if event_int == 0:
        return clench_prompt
    else:
        return raise_prompt

def main():
    show_img = None
    event_img = None
    screen_col = None
    #clock = pygame.time.Clock()
    counter = 3
    trials = 3
    event_function = random_prompt()
    pygame.time.set_timer(pygame.USEREVENT, 1000)
    run = True
    print_first = True
    space_pressed = False
    space_prompt = False

    BoardShim.enable_dev_board_logger()
    params = BrainFlowInputParams()
    # for synthetic board:
    board_id = BoardIds.SYNTHETIC_BOARD.value
    # for openbci ganglion board_id:
    #board_id = BoardIds.GANGLION_BOARD.value
    #params.serial_port = 'COM3'
    #params.mac_address = '12345'
    board = BoardShim(board_id, params)
    board.prepare_session()
    board.start_stream()
    BoardShim.log_message(LogLevels.LEVEL_INFO.value, 'start sleeping in the main thread')
    with open(output_file, 'w', newline = '') as file:
        writer = csv.writer(file)
        writer.writerow(["Sampling Rate: " + str(sampling_rate)])
    #time.sleep(1)

    while run:
        data = board.get_board_data().T

        keys_pressed = pygame.key.get_pressed()
        if keys_pressed[pygame.K_SPACE]:
            space_pressed = True
        else:
            space_pressed = False
        
        with open(output_file, 'a', newline = '') as file:
            writer = csv.writer(file)
            if (print_first):
                writer.writerow(np.arange(data[0].size))
                print_first = False
            for i in range(data[:, 0].size):
                if space_pressed:
                    space_event = 1
                else:
                    space_event = 0
                writer.writerow(np.append(np.append(data[i, :], space_prompt), space_event))
        #clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.USEREVENT: 
                show_img, screen_col, event_img, space_prompt = event_function(counter)
                counter -= 1
                if counter < 0 and trials > 1:
                    trials -= 1
                    counter = 3
                    event_function = random_prompt()
            if event.type == pygame.QUIT:
                run = False

        #keys_pressed = pygame.key.get_pressed()
        #draw_window()
        if screen_col:
            WIN.fill(screen_col)
        if event_img:
            WIN.blit(event_img, (100, 100))
        if show_img:
            WIN.blit(show_img, (300, 300))
        pygame.display.update()

    pygame.quit()
    board.stop_stream()
    board.release_session()

if __name__ == "__main__":
    main()
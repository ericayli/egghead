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

def label_extractor(input, id, array):
    try:
        return input(id) if array else [input(id)]
    except:
        return []

def draw_window():
    WIN.fill(WHITE)
    WIN.blit(three_img, (300, 100))
    pygame.display.update()

def clench_prompt(counter):
    event_img = clench_img
    screen_col = WHITE
    raise_indicate, clench_indicate = False, False
    if counter == 3:
        show_img = three_img
    if counter == 2:
        show_img = two_img
    if counter == 1:
        show_img = one_img
    if counter == 0:
        show_img = None
        screen_col = RED
        clench_indicate = True
    return show_img, screen_col, event_img, raise_indicate, clench_indicate

def raise_prompt(counter):
    event_img = raise_img
    screen_col = WHITE
    raise_indicate, clench_indicate = False, False
    if counter == 3:
        show_img = three_img
    if counter == 2:
        show_img = two_img
    if counter == 1:
        show_img = one_img
    if counter == 0:
        show_img = None
        screen_col = RED
        raise_indicate = True
    return show_img, screen_col, event_img, raise_indicate, clench_indicate

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
    counter = 3
    #number of trials
    trials = 3
    event_function = random_prompt()
    pygame.time.set_timer(pygame.USEREVENT, 1000)
    run = True
    print_first = True
    raise_indicate = False
    clench_indicate = False

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

    label_list = [None] * BoardShim.get_num_rows(board_id)
    label_dict = {
        "Battery" : label_extractor(BoardShim.get_battery_channel, board_id, False),
        "EEG" : label_extractor(BoardShim.get_eeg_channels, board_id, True),
        "EMG" : label_extractor(BoardShim.get_emg_channels, board_id, True),
        "ECG" : label_extractor(BoardShim.get_ecg_channels, board_id, True),
        "Temperature" : label_extractor(BoardShim.get_temperature_channels, board_id, True),
        "Resistance" : label_extractor(BoardShim.get_resistance_channels, board_id, True),
        "EOG" : label_extractor(BoardShim.get_eog_channels, board_id, True),
        "EXG" : label_extractor(BoardShim.get_exg_channels, board_id, True),
        "EDA" : label_extractor(BoardShim.get_eda_channels, board_id, True),
        "PPG" : label_extractor(BoardShim.get_ppg_channels, board_id, True),
        "Accel" : label_extractor(BoardShim.get_accel_channels, board_id, True),
        "Analog" : label_extractor(BoardShim.get_analog_channels, board_id, True),
        "Gyro" : label_extractor(BoardShim.get_gyro_channels, board_id, True),
        "Other" : label_extractor(BoardShim.get_other_channels, board_id, True)
    }

    for key, value in label_dict.items():
        for count, channel in enumerate(value):
            label_list[channel] = key +  " " + str(count) if len(value) > 1 else key

    with open(output_file, 'w', newline = '') as file:
        writer = csv.writer(file)
        #writer.writerow(np.arange(BoardShim.get_num_rows(board_id)))
        writer.writerow(["Sampling Rate: " + str(BoardShim.get_sampling_rate(board_id)) + " Hz"])
        writer.writerow(["Board: " + BoardShim.get_device_name(board_id)])
        writer.writerow(np.append(np.append(label_list, "Raise"), "Clench"))

    while run:
        data = board.get_board_data().T
        
        with open(output_file, 'a', newline = '') as file:
            writer = csv.writer(file)
            # if (print_first):
            #     writer.writerow(np.arange(data[0].size))
            #     print_first = False
            for i in range(data[:, 0].size):
                if raise_indicate:
                    raise_event = 1
                else:
                    raise_event = 0
                if clench_indicate:
                    clench_event = 1
                else:
                    clench_event = 0
                writer.writerow(np.append(np.append(data[i, :], raise_event), clench_event))

        for event in pygame.event.get():
            if event.type == pygame.USEREVENT: 
                show_img, screen_col, event_img, raise_indicate, clench_indicate = event_function(counter)
                counter -= 1
                if counter < 0 and trials > 1:
                    trials -= 1
                    counter = 3
                    event_function = random_prompt()
            if event.type == pygame.QUIT:
                run = False

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

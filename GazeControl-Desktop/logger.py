import csv
import os
from config import gaze_log_file, mouse_log_file, fixa_log_file, saccade_log_file

# def initialize_logs():
#     with open(gaze_log_file, 'w', newline='') as file:
#         csv.writer(file).writerow(["gaze_x", "gaze_y", "timestamp"])

#     with open(mouse_log_file, 'w', newline='') as file:
#         csv.writer(file).writerow(["mouse_x", "mouse_y", "timestamp"])

#     with open(fixa_log_file, 'w', newline='') as file:
#         csv.writer(file).writerow(["fix_x", "fix_y", "timestamp"])

#     with open(saccade_log_file, 'w', newline='') as file:
#         csv.writer(file).writerow(["from", "to", "velocity", "timestamp", "duration"])

# def append_to_csv(file_path, data_row):
#     with open(file_path, 'a', newline='') as file:
#         writer = csv.writer(file)
#         writer.writerow(data_row)

def open_csv_with_header(path, header):
    file_exists = os.path.isfile(path) and os.path.getsize(path) > 0
    f = open(path, 'a', newline='')
    writer = csv.writer(f)
    if not file_exists:
        writer.writerow(header)
    return f, writer

# Open files
gaze_writer, gaze_csv = open_csv_with_header(gaze_log_file, ["gaze_x", "gaze_y", "timestamp"])
mouse_writer, mouse_csv = open_csv_with_header(mouse_log_file, ["mouse_x", "mouse_y", "timestamp"])
fixa_writer, fixa_csv = open_csv_with_header(fixa_log_file, ["fix_x", "fix_y", "timestamp"])
saccade_writer, saccade_csv = open_csv_with_header(saccade_log_file, ["from", "to", "velocity","last_gaze_time","timestamp", "duration"])


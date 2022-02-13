import os

input_directory='./mypredictions/input'
output_directory='./mypredictions/output'

output_file="out.wav"

print(os.popen(f'python main.py --audio_dir_prediction .\mypredictions\input\ --dir_save_prediction .\mypredictions\output\  --audio_output_prediction {output_file}').read())

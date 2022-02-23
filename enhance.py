import subprocess
import os
from queue import Queue
from sys import stdout
from prediction_denoise import prediction
from variables import *

def predict_all(input_files:list,input_dir:str,messageQueue:Queue)->None:
    messageQueue.put("Process started")
    for input_file in input_files:
        messageQueue.put("Processing "+input_file)
        output_file=os.path.join(os.path.dirname(input_file),"output_"+os.path.basename(input_file))
        print(output_file)
        #process=subprocess.Popen(f'python main.py --audio_dir_prediction .\mypredictions\input\ --dir_save_prediction .\mypredictions\output\ --audio_input_prediction {input_file} --audio_output_prediction {output_file}',stdout=subprocess.PIPE)
        prediction(weights_path=weights_path,name_model=name_model,
                    audio_input_prediction=input_file,audio_output_prediction=output_file,
                    audio_dir_prediction=input_dir,dir_save_prediction=input_dir,
                    sample_rate=sample_rate,min_duration=min_duration,frame_length=frame_length,
                    hop_length_frame=hop_length_frame,n_fft=n_fft,hop_length_fft=hop_length_fft,messageQueue=messageQueue)
    messageQueue.put("Process finished")

def predict(input_filename:str)->str:
    output_file="out"+input_filename
    return os.popen(f'python main.py --audio_dir_prediction .\mypredictions\input\ --dir_save_prediction .\mypredictions\output\ --audio_input_prediction {input_filename} --audio_output_prediction {output_file}').read()

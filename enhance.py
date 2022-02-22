import os
input_directory='./mypredictions/input'
output_directory='./mypredictions/output'


input_files=os.listdir(input_directory)

def predict_all()->None:
    for input_file in input_files:
        output_file="out"+input_file
        print(os.popen(f'python main.py --audio_dir_prediction .\mypredictions\input\ --dir_save_prediction .\mypredictions\output\ --audio_input_prediction {input_file} --audio_output_prediction {output_file}').read())

def predict(input_filename:str)->str:
    output_file="out"+input_filename
    return os.popen(f'python main.py --audio_dir_prediction .\mypredictions\input\ --dir_save_prediction .\mypredictions\output\ --audio_input_prediction {input_filename} --audio_output_prediction {output_file}').read()

if __name__ == '__main__':
    predict_all()
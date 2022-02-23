


weights_path = './weights'
#pre trained model
name_model = 'model_unet'
#directory where read noisy sound to denoise
audio_dir_prediction = './mypredictions/input/'
#directory to save the denoise sound
dir_save_prediction = './mypredictions/output/'

#Name noisy sound file to denoise
#audio_input_prediction = args.audio_input_prediction
#Name of denoised sound file to save
#audio_output_prediction = args.audio_output_prediction

# Sample rate to read audio
sample_rate = 8000
# Minimum duration of audio files to consider
min_duration = 1.0
#Frame length for training data
frame_length = 8064
# hop length for sound files
hop_length_frame = 8064
#nb of points for fft(for spectrogram computation)
n_fft = 255
#hop length for fft
hop_length_fft = 63
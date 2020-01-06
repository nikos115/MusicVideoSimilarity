#!/usr/bin/env python
# coding: utf-8

# In[ ]:


#pip install moviepy
#pip install librosa
#pip install pydub
#pip install ffmpeg


# In[ ]:


import subprocess
import moviepy.editor as mp
import librosa
import IPython.display as ipd
import ffmpeg 
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
import numpy as np
import pandas as pd
import os
from pydub import AudioSegment



# In[ ]:


# Audio Extract
clip = mp.VideoFileClip("C:/Users/LeliopoulosP/Desktop/multimodal_assignment/blind.mp4")
clip.audio.write_audiofile("C:/Users/LeliopoulosP/Desktop/multimodal_assignment/blind_audio.wav")


# In[ ]:


# Video Extract
clip = mp.VideoFileClip("C:/Users/LeliopoulosP/Desktop/multimodal_assignment/blind.mp4")
#clip2 = clip.subclip(0, 1000)
clip.write_videofile("blind_video.mp4",audio=False,fps=15) # the mp4 will have 15 fps and no audio


# In[ ]:


#starting the audio choping


# In[ ]:


#t1 = t1 * 1000 #Works in milliseconds
#t2 = t2 * 1000
#newAudio = AudioSegment.from_wav("blind_audio.wav")
#newAudio = newAudio[t1:t2]
#newAudio.export('newSong.wav', format="wav") #Exports to a wav file in the current path


# In[ ]:


filename_wav = "C:/Users/LeliopoulosP/Desktop/multimodal_assignment/blind_audio.wav"


# In[ ]:


# loading the file with a sampling rate
x, sr = librosa.load(filename_wav, sr=16000)
# To get duration of the audio clip in minutes
#int(librosa.get_duration(x, sr) / 10)
# Dividing into chunks of x seconds 
max_slice = 10
window_length = max_slice * sr
# Playing the audio chunk
#a = x[21 * window_length:22 * window_length]
#ipd.Audio(a, rate=sr)


# In[ ]:


wav_file = np.array([sum(abs(x[i:i + window_length] ** 2)) for i in range(0, len(x), window_length)])
print(wav_file)


# In[ ]:


df = pd.DataFrame(columns=['start', 'end'])

thresh = 10
row_index = 0
print(df)


# In[ ]:


for i in range(len(wav_file)):
    value = wav_file[i]
    if value >= thresh:
        i = np.where(wav_file == value)[0]
        df.loc[row_index, 'start'] = i[0] * 10
        df.loc[row_index, 'end'] = (i[0] + 1) * 10
        row_index = row_index + 1
        
        #print(value)


# In[ ]:


start = np.array(df['start'])
end = np.array(df['end'])
for i in range(len(df)):
    if i != 0:
        start_lim = start[i] - 10
    else:
        start_lim = start[i]
    end_lim = end[i]
    filename_wav = "wav_" + str(i + 1) + ".wav"
    ffmpeg_extract_subclip("C:/Users/LeliopoulosP/Desktop/multimodal_assignment/blind_audio.wav", start_lim, end_lim, targetname=filename_wav)


# In[ ]:


#starting the video choping


# In[ ]:


filename_video = "C:/Users/LeliopoulosP/Desktop/multimodal_assignment/blind_video.mp4"


# In[ ]:


# loading the file with a sampling rate
#x, sr_ = librosa.load(filename_video, sr=16000)
# To get duration of the audio clip in minutes
#int(librosa.get_duration(x, sr) / 60)
# Dividing into chunks of x seconds 
#max_slice = 100
#window_length = max_slice * sr
# Playing the audio chunk
#a = x[21 * window_length:22 * window_length]
#ipd.Audio(a, rate=sr)


# In[ ]:


video_file = np.array([sum(abs(x[i:i + window_length] ** 2)) for i in range(0, len(x), window_length)])
#print(video_file)


# In[ ]:


df2 = pd.DataFrame(columns=['start', 'end'])

thresh = 1000
row_index = 0


# In[ ]:


for i in range(len(video_file)):
    value = video_file[i]
    if value >= thresh:
        i = np.where(video_file == value)[0]
        df2.loc[row_index, 'start'] = i[0] * 10
        df2.loc[row_index, 'end'] = (i[0] + 1) * 10
        row_index = row_index + 1


# In[ ]:


start = np.array(df2['start'])
end = np.array(df['end'])
for i in range(len(df2)):
    if i != 0:
        start_lim = start[i] - 10
    else:
        start_lim = start[i]
    end_lim = end[i]
    filename_video = "video_" + str(i + 1) + ".mp4"
    ffmpeg_extract_subclip("C:/Users/LeliopoulosP/Desktop/multimodal_assignment/blind_video.mp4", start_lim, end_lim, targetname=filename_video)


# In[ ]:


os.remove("C:/Users/LeliopoulosP/Desktop/multimodal_assignment/blind_audio.wav")
os.remove("C:/Users/LeliopoulosP/Desktop/multimodal_assignment/blind_video.mp4")








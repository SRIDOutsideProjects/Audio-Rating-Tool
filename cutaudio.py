from pydub import AudioSegment
import os
no_of_parts=40 
dir_path="audio_segment"
if not os.path.exists(dir_path):
    os.mkdir(dir_path)

Audio = AudioSegment.from_wav("audio.wav")
for i in range(no_of_parts):
    t1=(i*10)*1000
    t2=((i+1)*10)*1000
    new_audio = Audio[t1:t2]
    new_audio.export(os.path.join(dir_path,'audio'+'part_'+str(i)+'.wav'), format="wav") #Exports to a wav file in the current path.
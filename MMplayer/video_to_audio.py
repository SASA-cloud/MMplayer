# coding=UTF-8
import os, sys
import subprocess
from scipy.io import wavfile

def ffmpeg_VideoToAudio(VideoPath, type):
    # 提取视频路径下所有文件名
    AudioPath = os.path.join(VideoPath,'audio')  # 生成一个储存audio的文件夹名字
    os.mkdir(AudioPath)  # 创建存储audio的文件夹
    videos = os.listdir(VideoPath)
    for video in videos:
        # 提取视频的全路径名（含路径+文件名）
        video_path = VideoPath + "\\" + video
        # 合成输出音频的全路径名（不含后缀）
        audio_path = AudioPath + "\\" + os.path.splitext(video)[0]+ "."+type
        # 提取视频中的音频信息
        strcmd = "ffmpeg -i " + video_path + " -f " + type + " " + audio_path
        subprocess.call(strcmd, shell=True)

if __name__ == "__main__":
    VideoPath = 'C:\\Users\\清羽凌空\\Desktop\\多媒体\\database\\video'
    # AudioPath = 'C:\\Users\\清羽凌空\\Desktop\\多媒体\\data\\audio'
    type= input()
    ffmpeg_VideoToAudio(VideoPath, type)

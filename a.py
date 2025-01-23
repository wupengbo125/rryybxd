pip install pyaudio pyautogui pygetwindow opencv-python sounddevice numpy ffmpeg


import pyaudio
import wave
import numpy as np
import cv2
import threading
import pygetwindow as gw
import pyautogui
import sounddevice as sd
import time
import os

# 录制屏幕
def screen_record(filename):
    screen = pyautogui.screenshot(region=(100, 100, 1920, 1080))  # 设置录制区域
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter(filename, fourcc, 30.0, (1920, 1080))

    while True:
        frame = np.array(screen)
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        out.write(frame)
        screen = pyautogui.screenshot(region=(100, 100, 1920, 1080))
        time.sleep(0.03)  # 保持30帧每秒

# 录制麦克风音频
def record_microphone(filename):
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16, channels=1, rate=44100, input=True, frames_per_buffer=1024)
    
    frames = []
    while True:
        data = stream.read(1024)
        frames.append(data)
    
    wf = wave.open(filename, 'wb')
    wf.setnchannels(1)
    wf.setsampwidth(p.get_sample_size(pyaudio.paInt16))
    wf.setframerate(44100)
    wf.writeframes(b''.join(frames))
    wf.close()

# 录制系统音频
def record_system_audio(filename):
    # 使用sounddevice库来捕获系统音频
    fs = 44100  # 采样率
    duration = 10  # 录制时长（秒）
    
    # 你需要手动配置系统音频设备索引
    device_info = sd.query_devices()
    print(device_info)  # 查看所有设备
    device_index = 1  # 假设系统音频设备的索引是1，视实际设备而定

    # 开始录音
    audio_data = sd.rec(int(duration * fs), samplerate=fs, channels=2, dtype='int16', device=device_index)
    sd.wait()

    # 保存音频到文件
    write_wav_file(filename, audio_data, fs)

def write_wav_file(filename, audio_data, fs):
    with wave.open(filename, 'wb') as wf:
        wf.setnchannels(2)
        wf.setsampwidth(2)  # 每个样本占2字节
        wf.setframerate(fs)
        wf.writeframes(audio_data.tobytes())

# 合成音频与视频
def merge_audio_video(audio_file, video_file, output_file):
    command = f'ffmpeg -i {video_file} -i {audio_file} -c:v copy -c:a aac -strict experimental {output_file}'
    os.system(command)

if __name__ == '__main__':
    # 启动线程来录制屏幕
    screen_thread = threading.Thread(target=screen_record, args=("output_video.avi",))
    screen_thread.start()

    # 启动线程来录制麦克风
    mic_thread = threading.Thread(target=record_microphone, args=("microphone_audio.wav",))
    mic_thread.start()

    # 启动线程来录制系统音频
    system_thread = threading.Thread(target=record_system_audio, args=("system_audio.wav",))
    system_thread.start()

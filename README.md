pip install pyaudio sounddevice pyautogui mss

import pyaudio
import sounddevice as sd
import numpy as np
import threading
import wave
import pyautogui
import mss

# 获取音频设备
def list_audio_devices():
    devices = sd.query_devices()
    for idx, device in enumerate(devices):
        print(f"设备 {idx}: {device['name']}")

# 选择耳机或笔记本设备
def get_audio_device_index(device_name):
    devices = sd.query_devices()
    for idx, device in enumerate(devices):
        if device_name in device['name']:  # 根据设备名称筛选
            return idx
    return None

# 录制音频
def record_audio(device_index, duration=10, filename="output.wav"):
    fs = 44100  # 采样率
    channels = 2  # 立体声
    dtype = np.int16

    # 使用selected device录音
    with sd.InputStream(device=device_index, channels=channels, samplerate=fs, dtype=dtype) as stream:
        print("开始录音...")
        frames = []
        for _ in range(int(fs * duration)):
            frame, overflowed = stream.read(fs)  # 录制一帧
            frames.append(frame)
        print("录音结束...")
        # 保存到文件
        frames = np.concatenate(frames, axis=0)
        with wave.open(filename, 'wb') as wf:
            wf.setnchannels(channels)
            wf.setsampwidth(np.dtype(dtype).itemsize)
            wf.setframerate(fs)
            wf.writeframes(frames.tobytes())

# 屏幕录制
def record_screen(duration=10, filename="screenshot.png"):
    with mss.mss() as sct:
        print("开始录制屏幕...")
        for _ in range(duration):
            screenshot = sct.shot(output=filename)
            print(f"截图保存到 {filename}")

# 主线程，执行屏幕录制和音频录制
def main():
    # 列出所有音频设备并选择
    list_audio_devices()
    device_name = input("请输入耳机或笔记本设备名称：")
    device_index = get_audio_device_index(device_name)
    
    if device_index is None:
        print("未找到设备！")
        return
    
    # 创建线程同时进行音频和屏幕录制
    audio_thread = threading.Thread(target=record_audio, args=(device_index,))
    screen_thread = threading.Thread(target=record_screen)
    
    audio_thread.start()
    screen_thread.start()
    
    audio_thread.join()
    screen_thread.join()

if __name__ == "__main__":
    main()
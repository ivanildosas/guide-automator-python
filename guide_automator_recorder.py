import threading
import subprocess
import time
import os

import cv2
import numpy as np
from mss import mss

import pyaudio
import wave

class AudioWritter(threading.Thread):
  def __init__(self, frames, filename):
    threading.Thread.__init__(self)
    self.CHANNELS = 2
    self.frames = frames
    self.filename = filename
    self.RATE = 44100

  def run(self):
    self.pyaudio = pyaudio.PyAudio()
    self.FORMAT = pyaudio.paInt16
    wf = wave.open(self.filename, 'wb')
    wf.setnchannels(self.CHANNELS)
    wf.setsampwidth(self.pyaudio.get_sample_size(self.FORMAT))
    wf.setframerate(self.RATE)
    wf.writeframes(b''.join(self.frames))
    wf.close()

class VideoRecorder(threading.Thread):
  def __init__(self, top, left, right, bottom):
    threading.Thread.__init__(self)
    self.VIDEO_FILENAME = 'temp_video_out'
    self.FPS = 14
    self.DELAY_DECREASE = 1.25
    self.recording = True 
    self.extension = "XVID"
    self.top = top
    self.left = left
    self.right = right
    self.bottom = bottom
    self.video_box = {'top': top, 'left': left, 'width': right, 'height': bottom}
    self.height = 0
    self.width = 0
    self.frames = 1

  def run(self):
    self.setFrameSize()
    self.record()

  def setFrameSize(self):
    frame = mss().grab(self.video_box)
    frame = cv2.cvtColor(np.array(frame), cv2.COLOR_RGB2BGR)
    self.height, self.width, channels = frame.shape

  def initRecorder(self):
    self.filename = 'recorder/' + self.VIDEO_FILENAME + '.avi'
    self.fourcc = cv2.VideoWriter_fourcc(*self.extension)
    self.videoWriter = cv2.VideoWriter(self.filename, self.fourcc, self.FPS, (self.width, self.height))
    self.delay = 1./(self.FPS * self.DELAY_DECREASE)
    self.frames = 0
    self.skippedFrames = 0
    self.timeRecording = 1
    self.sleepAdjust = 0

  def record(self):
    # print("Video recording started...")
    self.initRecorder()
    self.startTime = time.time()

    secondComplete = False
    countFrames = 0
    countLoop = 0

    while(self.recording):
      if not secondComplete:
        if countFrames != self.FPS:
          image = np.array(mss().grab(self.video_box))
          self.videoWriter.write(np.array(image[:, :, :3]))
          countFrames += 1
        else:
          secondComplete = True
      else:
        self.skippedFrames += 1

      frame_delay = self.delay - self.sleepAdjust
      if frame_delay > 0:
        time.sleep(frame_delay)

      countLoop += 1
      self.sleepAdjust = time.time() - (self.startTime + (self.delay * countLoop))

      if time.time() >= self.startTime + self.timeRecording:
        self.timeRecording += 1
        self.frames += countFrames
        countFrames = 0
        secondComplete = False

    # print("Video recording completed.")
    REC_DURATION = (time.time() - self.startTime)
    print("\n ---- Video Info ----")
    print("  => recording time:", REC_DURATION)
    print("  => average FPS / expected:", self.frames / REC_DURATION, " / ", self.FPS)
    print("  => captured frames / expected: ", self.frames, " / ", self.FPS * REC_DURATION)
    print("  => skipped frames / average per second: ", self.skippedFrames, " / ", self.skippedFrames / REC_DURATION)

class AudioRecorder(threading.Thread):
  def __init__(self):
    threading.Thread.__init__(self)
    self.AUDIO_FILENAME = 'temp_audio_out'
    self.CHUNK = 512
    self.CHANNELS = 2
    self.RATE = 44100
    self.recording = True
    self.pyaudio = pyaudio.PyAudio()
    self.FORMAT = pyaudio.paInt16
    self.RECORD_SECONDS = 3600

  def run(self):
    self.initRecorder()
    self.record()

  def initRecorder(self):
    self.filename = 'recorder/' + self.AUDIO_FILENAME + '.wav'
    self.stream = self.pyaudio.open(
      format = self.FORMAT,
      channels = self.CHANNELS,
      rate = self.RATE,
      input = True,
      frames_per_buffer = self.CHUNK
    )
    self.frames = []

  def record(self):
    # print("Audio recording started...")
    for i in range(0, int(self.RATE / self.CHUNK * self.RECORD_SECONDS)):
      if self.recording:
        data = self.stream.read(self.CHUNK)
        self.frames.append(data)
      else:
        break

    self.stream.stop_stream()
    self.stream.close()
    self.pyaudio.terminate()
    
    audioWritter = AudioWritter(self.frames, self.filename)
    audioWritter.start()
    # print("Audio recording completed.")

class VideoAudioMerge(threading.Thread):
  def __init__(self, videofile, audiofile, filename):
    threading.Thread.__init__(self)
    self.videofile = videofile
    self.audiofile = audiofile
    self.filename = filename

  def run(self):
    cmd = "ffmpeg -ac 2 -channel_layout stereo -i " + self.audiofile + " -i " + self.videofile + " -c copy " + self.filename
    subprocess.call(cmd, shell=True)

class GuideAutomatorRecorder(threading.Thread):
  def __init__(self, top, left, right, bottom):
    threading.Thread.__init__(self)
    self.recording = False
    self.filename = "video"
    self.videoRecorder = VideoRecorder(top, left, right, bottom)
    self.audioRecorder = AudioRecorder()

  def start(self, filename):
    if not self.recording:
      self.filename = filename
      self.videoRecorder.start()
      self.audioRecorder.start()
      self.recording = True

  def stop(self):
    if self.recording:
      self.videoRecorder.recording = False
      self.audioRecorder.recording = False
      time.sleep(0.5)
      self.renameLastVideo(self.filename + ".avi")
      time.sleep(0.5)
      videoMerge = VideoAudioMerge("recorder/temp_audio_out.wav", "recorder/temp_video_out.avi", "recorder/" + self.filename + ".avi")
      videoMerge.start()
      self.recording = False

  def renameLastVideo(self, filename):
    path = os.getcwd()
    file = str(path) + '/recorder/' + filename
    if os.path.exists(file):
      fileNumber = 1
      while (os.path.exists(str(path) + '/recorder/old_' + str(fileNumber) + '_' + filename)):
        fileNumber += 1
      os.rename(file, str(path) + '/recorder/old_' + str(fileNumber) + '_' + filename)

def main():
  GAVRec = GuideAutomatorRecorder()
  GAVRec.start()
  time.sleep(10)
  GAVRec.stop()

if __name__ == "__main__":
    main()



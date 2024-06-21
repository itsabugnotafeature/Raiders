from scripts.variables.localvars import *
from systems.BaseSystem import BaseSystem
import pyaudio
import wave


class GameAudio(BaseSystem):

    def __init__(self):
        super().__init__()

        # Holds all active streams keyed to the open sound file they are reading from, to be released after the stream
        # finishes
        self.streams = {}
        self.paused = False

        self.AudioPlayer = pyaudio.PyAudio()

    def play(self, wave_file):
        if self.paused:
            return -1

        wave_read = wave.open(wave_file, 'rb')

        def callback(in_data, frame_count, time_info, status):
            data = wave_read.readframes(frame_count)
            return data, pyaudio.paContinue

        stream = self.AudioPlayer.open(format=self.AudioPlayer.get_format_from_width(wave_read.getsampwidth()),
                                       channels=wave_read.getnchannels(),
                                       rate=wave_read.getframerate(),
                                       output=True,
                                       stream_callback=callback)

        self.streams[stream] = wave_read
        stream.start_stream()

        # Returns a unique identifier for this stream so that outside classes can have a way to ID a channel but not
        # be able to do anything to it
        return hash(stream)

    def update(self):

        kill_streams = []
        for stream in self.streams:
            if not stream.is_active():
                kill_streams.append(stream)

        for stream in kill_streams:
            self.close_stream(stream)

    def close_stream(self, stream):
        # Close the file being read from
        self.streams[stream].close()

        # Stop thread and close stream
        stream.stop_stream()
        stream.close()

        # Remove stream from stream list
        self.streams.pop(stream)

    def stop(self, stream_hash):
        # Uses the hash because it is called by outside functions
        for stream in self.streams:
            if hash(stream) == stream_hash:
                self.close_stream(stream)
                break

    def is_stream_active(self, stream_hash):
        for stream in self.streams:
            if hash(stream) == stream_hash:
                return True
        return False

    def main_loop(self):
        self.update()

    def pause_streams(self):
        for stream in self.streams:
            stream.stop_stream()

    def unpause_streams(self):
        for stream in self.streams:
            stream.start_stream()

    def handle_event(self, event):
        if event.type == VAR_CHANGE:
            if event.key == MUTE:
                if self.paused:
                    self.paused = False
                    self.unpause_streams()
                else:
                    self.paused = True
                    self.pause_streams()

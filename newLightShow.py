import pyaudio
from LightController import LightController
import numpy


PYAUDIO_FORMAT = pyaudio.paInt16
SAMPLE_RATE =
SAMPLE_SIZE = 

if __name__ == '__main__':

    lc = lightController()
    p = pyaudio.PyAudio()

    stream = pa.open(   format = PYAUDIO_FORMAT,
                        channels = 2,
                        input_device_index = 0,
                        rate = SAMPLE_RATE,
                        input = True,
                        frames_per_buffer = SAMPLE_SIZE * numChannels )
                        
    stream.start_stream()
    while true:
        rawData = stream.read(SAMPLE_SIZE)

        interleavedFrame = numpy.fromstring(rawData, dtype=numpy.short).tolist()

        # De-interleave Channels
        frame = []
        for i in range(numChannels):
            frame.append([])
            for j in range(SAMPLE_SIZE):
                frame[i].append(0)
                
        for i in range(len(interleavedFrame)):
            frame[i%numChannels][i/numChannels] = interleavedFrame[i]

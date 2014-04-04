import pyaudio
p = pyaudio.PyAudio()
stream = p.open(format = pyaudio.paInt16,
                    channels = 1,
                    rate = 44100,
                    output = True,
                    frames_per_buffer = 2**11)
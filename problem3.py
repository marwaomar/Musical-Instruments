import numpy as np
import simpleaudio as sa
from problem3ui import Ui_MusicalInstruments
from PyQt5.QtGui import *
from PyQt5 import QtCore
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import sounddevice as sd
fs = 8000 #20000
class GuitarString:
    def __init__(self, pitch, starting_sample, sampling_freq, stretch_factor):
        """Inits the guitar string."""
        self.pitch = pitch
        self.starting_sample = starting_sample
        self.sampling_freq = sampling_freq
        self.stretch_factor = stretch_factor
        self.init_wavetable()
        self.current_sample = 0
        self.previous_value = 0
  
    def init_wavetable(self):
        """Generates a new wavetable for the string."""
        wavetable_size = self.sampling_freq // int(self.pitch)
        self.wavetable = (2 * np.random.randint(0, 2, wavetable_size) - 1).astype(np.float)
        
    def get_sample(self):
        """Returns next sample from string."""
        if self.current_sample >= self.starting_sample:
            current_sample_mod = self.current_sample % self.wavetable.size
            r = np.random.binomial(1, 1 - 1/self.stretch_factor)
            if r == 0:
                self.wavetable[current_sample_mod] =  0.5 * (self.wavetable[current_sample_mod] + self.previous_value)
            sample = self.wavetable[current_sample_mod]
            self.previous_value = sample
            self.current_sample += 1
        else:
            self.current_sample += 1
            sample = 0
        return sample
class MainWindow(QMainWindow, Ui_MusicalInstruments):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setupUi(self)
        self.fs = 44100  
        self.seconds =0.5 

        self.p1.clicked.connect(lambda : self.sound(207.65))
        self.p2.clicked.connect(lambda : self.sound(233.08))
        self.p3.clicked.connect(lambda : self.sound(277.18))
        self.p4.clicked.connect(lambda : self.sound(311.13))
        self.p5.clicked.connect(lambda : self.sound(369.99))
        self.p6.clicked.connect(lambda : self.sound(415.30))
        self.p7.clicked.connect(lambda : self.sound(466.16))
        self.p8.clicked.connect(lambda : self.sound(554.37))
        
        self.p9.clicked.connect(lambda : self.sound(220))
        self.p10.clicked.connect(lambda : self.sound(246.94))
        self.p11.clicked.connect(lambda : self.sound(261.63))
        self.p12.clicked.connect(lambda : self.sound(293.66))
        self.p13.clicked.connect(lambda : self.sound(329.63))
        self.p14.clicked.connect(lambda : self.sound(349.23))
        self.p15.clicked.connect(lambda : self.sound(392))
        self.p16.clicked.connect(lambda : self.sound(440))
        self.p17.clicked.connect(lambda : self.sound(493.88))
        self.p18.clicked.connect(lambda : self.sound(523.25))

        self.g1.clicked.connect(lambda : self.guitar_sound(98))
        self.g2.clicked.connect(lambda : self.guitar_sound(123))
        self.g3.clicked.connect(lambda : self.guitar_sound(147))
        self.g4.clicked.connect(lambda : self.guitar_sound(196))
        self.g5.clicked.connect(lambda : self.guitar_sound(294))
        self.g6.clicked.connect(lambda : self.guitar_sound(392))    


        self.show() 
    def sound(self,freq):
        # Generate array with seconds*sample_rate steps, ranging between 0 and seconds
        t = np.linspace(0, self.seconds, self.seconds * self.fs, False)
        # Generate a 440 Hz sine wave
        note = np.sin(np.sin(freq * t * 2 * np.pi)*1/220)
        # Ensure that highest value is in 16-bit range
        audio = note * (2**15 - 1) / np.max(np.abs(note))
        # Convert to 16-bit data
        audio = audio.astype(np.int16)
        # Start playback
        play_obj = sa.play_buffer(audio, 1,2, self.fs)
        # Wait for playback to finish before exiting
        play_obj.wait_done()

    def guitar_sound(self,fr):
        
        freqs = [fr]
        unit_delay = fs//3
        delays = [unit_delay * _ for _ in range(len(freqs))]
        stretch_factors = [2 * f/98 for f in freqs]
        strings = []
        for freq, delay, stretch_factor in zip(freqs, delays, stretch_factors):
            string = GuitarString(freq, delay, fs, stretch_factor)
            strings.append(string)
            guitar_sound = [sum(string.get_sample() for string in strings) for _ in range(fs * 6)]
            sd.play(guitar_sound,15000)

if __name__ == '__main__':
    app = QApplication([])
    app.setApplicationName("Failamp")
    app.setStyle("Fusion")
    window = MainWindow()
    app.exec_()

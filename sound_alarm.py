#!/usr/bin/env python
# -*- coding: utf-8 -*-

class BaseBeeper(object):
    def __init__(self):
        self._beeps = []

    def add_beep(self, frequency, duration):
        raise NotImplementedError

    def add_sleep(self, duration):
        raise NotImplementedError

    def beep(self):
        raise NotImplementedError


def cancelable(func):
    def cancelable_func(*args, **kwargs):
        try:
            func(*args, **kwargs)
        except KeyboardInterrupt:
            print "Cancelled!"
    cancelable_func.__name__ = func.__name__
    cancelable_func.__doc__ = func.__doc__
    cancelable_func.__dict__.update(func.__dict__)
    return cancelable_func


try:
    # winsound is available only on Windows
    import winsound
    import time

    class WindowsBeeper(BaseBeeper):
        def add_beep(self, frequency, duration):
            beep = (winsound.Beep, (frequency, duration))
            self._beeps.append(beep)

        def add_sleep(self, duration):
            sleep = (time.sleep, (duration / 1000.0,))
            self._beeps.append(sleep)

        @cancelable
        def beep(self):
            for beep in self._beeps:
                apply(*beep)

    Beeper = WindowsBeeper
except ImportError:
    # fallback to write to /dev/audio under Unix environment
    class UnixBeeper(BaseBeeper):
        AUDIO_DEVICE = '/dev/audio'

        @staticmethod
        def _make_beep(frequency, duration):
            sample = 8000
            amplitude = 100
            duration = duration / 1000.0
            half_period = int(sample / frequency / 2)
            beep = chr(amplitude) * half_period + chr(0) * half_period
            beep *= int(duration * frequency)
            return beep

        def add_beep(self, frequency, duration):
            beep = self._make_beep(frequency, duration)
            self._beeps.append(beep)

        def add_sleep(self, duration):
            self.add_beep(1, duration)

        @cancelable
        def beep(self):
            audio = open(self.AUDIO_DEVICE, 'wb')
            audio.write(''.join(self._beeps))
            audio.close()

    Beeper = UnixBeeper


class BaseBeepSound(object):
    def __init__(self, beeper_class=Beeper):
        self.beeper = beeper_class()

    def beep(self):
        self.beeper.beep()


class SuperNintendoBeepSound(BaseBeepSound):
    '''SuperNintendo'''
    def __init__(self, beeper_class=Beeper):
        BaseBeepSound.__init__(self, beeper_class)
        for i in range(1, 5):
            for j in range(1, 5):
                self.beeper.add_beep(100 * j * i, 50)
                self.beeper.add_sleep(0.01)
                self.beeper.add_sleep(0.01)


class ExplosiveCounterBeepSound(BaseBeepSound):
    '''Explosive Counter'''
    def __init__(self, beeper_class=Beeper):
        BaseBeepSound.__init__(self, beeper_class)
        for i in range(6, 85):
            self.beeper.add_beep(37 * i, 50)
            self.beeper.add_sleep(0.07)
        self.beeper.add_beep(37, 2000)


class HighFrequencyBellBeepSound(BaseBeepSound):
    '''High Frequency Bell'''
    def __init__(self, beeper_class=Beeper):
        BaseBeepSound.__init__(self, beeper_class)
        for i in range(1, 31):
            self.beeper.add_beep(1000 + (i * 666) % 1000, 500)


class LowFrequencyBellBeepSound(BaseBeepSound):
    '''Low Frequency Bell'''
    def __init__(self, beeper_class=Beeper):
        BaseBeepSound.__init__(self, beeper_class)
        for i in range(1, 31):
            self.beeper.add_beep(120 + (i * 666) % 200, 500)


class DisturbingFrequencyBeepSound(BaseBeepSound):
    '''Disturbing Frequency'''
    def __init__(self, beeper_class=Beeper):
        BaseBeepSound.__init__(self, beeper_class)
        for i in range(1, 31):
            self.beeper.add_beep(2000 + (i * 666) % 200, 250)


class CricketBeepSound(BaseBeepSound):
    '''Cricket'''
    def __init__(self, beeper_class=Beeper):
        BaseBeepSound.__init__(self, beeper_class)
        for i in range(1, 500):
            self.beeper.add_beep(2000 + (i * 666) % 200, 20)


class PhoneRingBeepSound(BaseBeepSound):
    '''Phone Ring'''
    def __init__(self, beeper_class=Beeper):
        BaseBeepSound.__init__(self, beeper_class)
        for j in range(5):
            for i in range(5):
                self.beeper.add_beep(700 + 40 * i, 200)
            self.beeper.add_sleep(1000)



# Symfonia

class PolishSymfoniaBeepSound(BaseBeepSound):
    '''Epi-zart'''
    tones = {
        'A': 440,
        'A#': 466,
        'B': 493,
        'C': 523,
        'C#': 554,
        'D': 587,
        'D#': 622,
        'E': 659,
        'F': 698,
        'F#': 739,
        'G': 783,
        'G#': 830,
        'a': 880,
        'a#': 932,
        'b': 987,
        'c': 1046,
        'c#': 1108,
        'd': 1174,
        'd#': 1244,
        'e': 1318,
        'f': 1396,
        'f#': 1479,
        'g': 1567,
        'g#': 1661
    }

    def __init__(self, beeper_class=Beeper):
        BaseBeepSound.__init__(self, beeper_class)

        for tone in ('b','b','c','d','d','c','b','a','G','G','a','b'):
            self.beeper.add_beep(self.tones[tone], 300)

        self.beeper.add_beep(self.tones['b'], 500)
        self.beeper.add_beep(self.tones['a'], 150)
        self.beeper.add_beep(self.tones['a'], 500)

        for tone in ('b','b','c','d','d','c','b','a','G','G','a','b'):
            self.beeper.add_beep(self.tones[tone], 300)

        self.beeper.add_beep(self.tones['a'], 500)
        self.beeper.add_beep(self.tones['G'], 150)
        self.beeper.add_beep(self.tones['G'], 500)
        
        self.beeper.add_beep(self.tones['a'], 300)
        self.beeper.add_beep(self.tones['a'], 300)
        self.beeper.add_beep(self.tones['b'], 300)
        self.beeper.add_beep(self.tones['G'], 300)
        self.beeper.add_beep(self.tones['a'], 300)
        self.beeper.add_beep(self.tones['b'], 150)
        self.beeper.add_beep(self.tones['c'], 150)
        self.beeper.add_beep(self.tones['b'], 300)
        self.beeper.add_beep(self.tones['G'], 300)
        self.beeper.add_beep(self.tones['a'], 300)
        self.beeper.add_beep(self.tones['b'], 150)
        self.beeper.add_beep(self.tones['c'], 150)
        self.beeper.add_beep(self.tones['b'], 300)
        self.beeper.add_beep(self.tones['a'], 300)
        self.beeper.add_beep(self.tones['G'], 300)
        self.beeper.add_beep(self.tones['a'], 300)
        self.beeper.add_beep(self.tones['D'], 500)
        
        self.beeper.add_beep(self.tones['b'], 500)
        for tone in ('b','c','d','d','c','b','a','G','G','a','b'):
            self.beeper.add_beep(self.tones[tone], 300)

        self.beeper.add_beep(self.tones['a'], 500)
        self.beeper.add_beep(self.tones['G'], 150)
        self.beeper.add_beep(self.tones['G'], 500)





def play_sound(sound_class):
    for klass in BaseBeepSound.__subclasses__():
        if klass.__name__.startswith(sound_class):
            print "Playing %r..." % (klass.__doc__,)
            beep_sound = klass()
            beep_sound.beep()


def list_beep_sound_classes():
    print "Available sounds:\n"
    print "\n".join("%-30s - %s" % (klass.__name__, klass.__doc__)
                    for klass in BaseBeepSound.__subclasses__())


def test_sounds():
    print "Beep Sound Tester"
    for klass in BaseBeepSound.__subclasses__():
        message = "Listen to sound %r? " % (klass.__doc__,)
        if raw_input(message)[:1] == 'y':
            beep_sound = klass()
            beep_sound.beep()


@cancelable
def _main():
    from optparse import OptionParser
    usage = "%prog [OPTIONS]"
    description = """
        %prog plays sounds using the speaker.
        """.replace('  ', '')
    parser = OptionParser(usage, description=description)
    parser.add_option(
        '-l',
        '--list',
        action='store_true',
        dest='list',
        help='list available sounds'
    )
    parser.add_option(
        '-p',
        '--play',
        action = 'append',
        dest='sound_classes',
        metavar='SOUND_CLASS',
        help='play sound(s) whose class name starts with SOUND_CLASS. '
             'You may pass this argument more than once to play multiple sounds'
    )
    parser.add_option(
        '-t',
        '--test',
        action='store_true',
        dest='test',
        help='interactively test available sounds'
    )
    options, args = parser.parse_args()

    if options.list:
        list_beep_sound_classes()
    elif options.sound_classes:
        for sound_class in options.sound_classes:
            play_sound(sound_class)
    elif options.test:
        test_sounds()
    else:
        parser.print_help()


if __name__ == '__main__':
    _main()

import librosa

from os.path import isfile
from struct import unpack
from typing import List


class WarpMarker:

    def __init__(self, seconds : float, beats : float):

        self.seconds = seconds
        self.beats = beats


class Clip:

    """An unofficial representation of an Ableton Live Clip."""

    @property
    def loop_on(self):
        return self._loop_on

    @loop_on.setter
    def loop_on(self, value):
        self._loop_on = value

    @property
    def start_marker(self):
        return self._start_marker

    @start_marker.setter
    def start_marker(self, value):
        self._start_marker = value

    @property
    def end_marker(self):
        return self._end_marker

    @end_marker.setter
    def end_marker(self, value):
        self._end_marker = value

    @property
    def loop_start(self):
        return self._loop_start

    @loop_start.setter
    def loop_start(self, value):
        self._loop_start = value

    @property
    def loop_end(self):
        return self._loop_end

    @loop_end.setter
    def loop_end(self, value):
        self._loop_end = value

    @property
    def hidden_loop_start(self):
        return self._hidden_loop_start

    @hidden_loop_start.setter
    def hidden_loop_start(self, value):
        self._hidden_loop_start = value

    @property
    def hidden_loop_end(self):
        return self._hidden_loop_end

    @hidden_loop_end.setter
    def hidden_loop_end(self, value):
        self._hidden_loop_end = value

    @property
    def audio_data(self):
        return self._audio_data

    @audio_data.setter
    def audio_data(self, value):
        self._audio_data = value

    @property
    def warp_markers(self):
        return self._warp_markers

    @warp_markers.setter
    def warp_markers(self, warp_markers : List[WarpMarker]):
        self._warp_markers = value

    @property
    def sr(self):
        return self._sr


    def __init__(self, audio_path : str, *args, dtype='float64', always_2d=False):

        '''
        Parameters
        ----------
        audio_path : str
            Path to an audio file.
        '''

        self._loop_on = False
        self._start_marker = 0.
        self._end_marker = 0.
        self._loop_start = 0.
        self._loop_end = 0.
        self._hidden_loop_start = 0.
        self._hidden_loop_end = 0.
        self._warp_markers = []
        self._audio_data = None
        self._sr = 44100

        self._audio_data, self._sr = librosa.load(audio_path, sr=None, mono=False)

        asd_path = audio_path + '.asd'

        self._parse_asd_file(asd_path)


    def get_time_map(self, bpm : float):

        '''Parse an Ableton `asd` file into a time map to be used with Rubberband library's `timemap_stretch`.

        Parameters
        ----------
        bpm : float > 0
            The beats-per-minute of the time map which will be returned

        Returns
        -------
        time_map : list
            Each element is a tuple `t` of length 2 which corresponds to the
            source sample position and target sample position.

            If `t[1] < t[0]` the track will be sped up in this area.

            Refer to the function `timemap_stretch`.
        '''

        time_map = []
        for wm in self._warp_markers:
            
            time_map.append([int(wm.seconds*self._sr), int(wm.beats*(60./bpm)*self._sr)])

        wm1 = self._warp_markers[-2]  # second to last warp marker
        wm2 = self._warp_markers[-1]  # last warp marker

        # The difference in beats divided by the difference in seconds, times 60 seconds = BPM.
        last_bpm = (wm2.beats - wm1.beats) / (wm2.seconds - wm1.seconds) * 60.

        num_samples = self._audio_data.shape[1] if len(self._audio_data.shape) > 1 else self._audio_data.shape[0]

        # Extrapolate the last bpm 
        mapped_last_sample = int(time_map[-1][1] + (num_samples-time_map[-1][0])*last_bpm/bpm)

        time_map.append([num_samples, mapped_last_sample])

        return time_map


    def _parse_asd_file(self, filepath : str):

        '''Parse an Ableton `asd` file.

        Parameters
        ----------
        filepath : str
            Path to an Ableton clip file with ".asd" extension
        '''

        if not isfile(filepath):
            raise FileNotFoundError(f"No such file or directory: '{filepath}'")

        f = open(filepath, 'rb')
        asd_bin = f.read()
        f.close()

        index = asd_bin.find(b'SampleOverViewLevel')
        index = asd_bin.find(b'SampleOverViewLevel', index+1)
        index += 90

        def read_double(buffer, index):
            size_double = 8  # a double is 8 bytes
            return unpack('d', buffer[index:index+size_double])[0], index+size_double

        def read_bool(buffer, index):
            size_bool = 1
            return unpack('?', buffer[index:index+size_bool])[0], index+size_bool

        self._loop_start, index = read_double(asd_bin, index)
        self._loop_end, index = read_double(asd_bin, index)
        sample_offset, index = read_double(asd_bin, index)
        self._hidden_loop_start, index = read_double(asd_bin, index)
        self._hidden_loop_end, index = read_double(asd_bin, index)
        self._end_marker, index = read_double(asd_bin, index)

        self._start_marker = self._loop_start + sample_offset

        self._warp_markers = []
        index = asd_bin.find(b'WarpMarker')
        last_good_index = -1
        while True:

            index = asd_bin.find(b'WarpMarker', index+1)
            if index < 0:
                index = last_good_index
                break

            index += 14  # WarpMarker is 10 bytes. Then add 4.

            marker_seconds, index = read_double(asd_bin, index)
            marker_beats, index = read_double(asd_bin, index)

            self._warp_markers.append(WarpMarker(marker_seconds, marker_beats))

            last_good_index = index

        index += 15
        # The loop_on value can be found some bytes after the last warp marker.
        self._loop_on, index = read_bool(asd_bin, index)

from os.path import isfile
from struct import unpack
from typing import List


class WarpMarker:

    def __init__(self, seconds : float, beats : float):

        self.seconds = seconds
        self.beats = beats

    def __repr__(self):
        return "WarpMarker(seconds={0},beats={1})".format(self.seconds, self.beats)


class Clip:

    """An unofficial representation of an Ableton Live Clip."""

    @property
    def loop_on(self):
        return self._loop_on

    @loop_on.setter
    def loop_on(self, value: bool):
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
    def warp_markers(self):
        return self._warp_markers

    @warp_markers.setter
    def warp_markers(self, warp_markers : List[WarpMarker]):
        self._warp_markers = warp_markers

    @property
    def warp_on(self):
        return self._warp_on

    @warp_on.setter
    def warp_on(self, warp_on: bool):
        self._warp_on = warp_on

    @property
    def sr(self):
        return self._sr

    @sr.setter
    def sr(self, value : int):
        self._sr = value


    def __init__(self, clip_path: str, sr: int, num_samples: int):

        '''
        Parameters
        ----------
        clip_path : str
            Path to an Ableton ASD file.
        sr : int
            Sample rate the of the audio file associated with the ASD clip.
        num_samples : int
            Number of audio samples per channel in the audio file associated with the ASD clip.
        '''

        self._loop_on = False
        self._start_marker = 0.
        self._end_marker = 0.
        self._loop_start = 0.
        self._loop_end = 0.
        self._hidden_loop_start = 0.
        self._hidden_loop_end = 0.
        self._warp_markers = []
        self._warp_on = False
        self._sr = sr
        self._num_samples = num_samples

        self._parse_asd_file(clip_path)


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

            sample_index = int(wm.seconds*self._sr)

            if sample_index <= self._num_samples:
                time_map.append([sample_index, int(wm.beats*(60./bpm)*self._sr)])
            else:
                return time_map

        wm1 = self._warp_markers[-2]  # second to last warp marker
        wm2 = self._warp_markers[-1]  # last warp marker

        # The difference in beats divided by the difference in seconds, times 60 seconds = BPM.
        last_bpm = (wm2.beats - wm1.beats) / (wm2.seconds - wm1.seconds) * 60.

        # Extrapolate the last bpm 
        mapped_last_sample = int(time_map[-1][1] + (self._num_samples-time_map[-1][0])*last_bpm/bpm)

        time_map.append([self._num_samples, mapped_last_sample])

        return time_map


    def _parse_asd_file(self, filepath : str):

        '''Parse an Ableton `asd` file.

        Parameters
        ----------
        filepath : str
            Path to an Ableton clip file with ".asd" extension
        '''

        if not isfile(filepath):
            raise FileNotFoundError(f"No such file: '{filepath}'")

        f = open(filepath, 'rb')
        asd_bin = f.read()
        f.close()

        index = asd_bin.find(b'SampleOverViewLevel')
        if index > 0:
            # Assume the clip file was saved with Ableton Live 10.
            # Find the second appearance of SampleOverViewLevel
            index = asd_bin.find(b'SampleOverViewLevel', index+1)
            # Go forward a fixed number of bytes.
            index += 90
        else:
            # Assume the clip file was saved with Ableton Live 9.
            index = asd_bin.find(b'SampleData')
            # Find the second appearance of SampleData
            index = asd_bin.find(b'SampleData', index+1)
            # Go forward a fixed number of bytes.
            index += 2712

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
        index += 3
        self._warp_on, index = read_bool(asd_bin, index)

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

        index += 7
        # The loop_on value can be found some bytes after the last warp marker.
        self._loop_on, index = read_bool(asd_bin, index)

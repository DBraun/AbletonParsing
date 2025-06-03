import abletonparsing
import pytest
from pathlib import Path

import librosa
import soundfile as sf
import pyrubberband as pyrb
import numpy as np

# Get the directory where this test file is located
TEST_DIR = Path(__file__).parent
ASSETS_DIR = TEST_DIR / "assets"
OUTPUT_DIR = TEST_DIR / "output"

# Ensure output directory exists
OUTPUT_DIR.mkdir(exist_ok=True)

def _test_basic_params(audio_path, clip_path, loop_on, output_path, bpm,
	start_marker=0, end_marker=5, hidden_loop_start=4, hidden_loop_end=6,
	loop_start=4, loop_end=6, sr=44100, warp_on=True):

	audio_data, sr = librosa.load(audio_path, sr=None, mono=False)
	num_samples = audio_data.shape[1]

	clip = abletonparsing.Clip(clip_path, sr, num_samples)
	print(clip.warp_markers)

	assert clip.loop_on == loop_on
	assert clip.warp_on == warp_on

	assert clip.sr == sr
	assert np.isclose(clip.start_marker, start_marker)
	assert np.isclose(clip.end_marker, end_marker)

	if clip.loop_on:
		assert np.isclose(clip.hidden_loop_start, hidden_loop_start)
		assert np.isclose(clip.hidden_loop_end, hidden_loop_end)
		assert np.isclose(clip.loop_start, loop_start)
		assert np.isclose(clip.loop_end, loop_end)
	else:
		assert np.isclose(clip.hidden_loop_start, hidden_loop_start)
		assert np.isclose(clip.hidden_loop_end, hidden_loop_end)
		assert np.isclose(clip.loop_start, loop_start)
		assert np.isclose(clip.loop_end, loop_end)

	time_map = clip.get_time_map(bpm)
	print('time_map: ', time_map)

	# Time-stretch the audio to the requested bpm.
	output_audio = pyrb.timemap_stretch(audio_data.transpose(), sr, time_map)

	with sf.SoundFile(output_path, 'w', sr, 2, 'PCM_24') as f:
		f.write(output_audio)

def test_basic1():
	audio_path = str(ASSETS_DIR / 'Incredible Bongo Band - Apache.wav')
	clip_path = str(ASSETS_DIR / 'Incredible Bongo Band - Apache (loop on).asd')
	loop_on = True
	output_path = str(OUTPUT_DIR / 'test_basic1.wav')
	_test_basic_params(audio_path, clip_path, loop_on, output_path, 140,
		start_marker=0, end_marker=5, hidden_loop_start=4, hidden_loop_end=6,
		loop_start=4, loop_end=6, sr=44100, warp_on=True)

def test_basic2():
	audio_path = str(ASSETS_DIR / 'Incredible Bongo Band - Apache.wav')
	clip_path = str(ASSETS_DIR / 'Incredible Bongo Band - Apache (loop off).asd')
	loop_on = False
	output_path = str(OUTPUT_DIR / 'test_basic2.wav')
	_test_basic_params(audio_path, clip_path, loop_on, output_path, 140,
		start_marker=0, end_marker=5, hidden_loop_start=4, hidden_loop_end=6,
		loop_start=0, loop_end=5, sr=44100, warp_on=True)

def test_live12_loop_on():
	audio_path = str(ASSETS_DIR / 'Incredible Bongo Band - Apache.wav')
	clip_path = str(ASSETS_DIR / 'Incredible Bongo Band - Apache (loop on Live 12).wav.asd')
	loop_on = True
	output_path = str(OUTPUT_DIR / 'test_live12_loop_on.wav')
	_test_basic_params(audio_path, clip_path, loop_on, output_path, 140,
		start_marker=0, end_marker=5, hidden_loop_start=4, hidden_loop_end=6,
		loop_start=4, loop_end=6, sr=44100, warp_on=True)

def test_live12_loop_off():
	audio_path = str(ASSETS_DIR / 'Incredible Bongo Band - Apache.wav')
	clip_path = str(ASSETS_DIR / 'Incredible Bongo Band - Apache (loop off Live 12).wav.asd')
	loop_on = False
	output_path = str(OUTPUT_DIR / 'test_live12_loop_off.wav')
	_test_basic_params(audio_path, clip_path, loop_on, output_path, 140,
		start_marker=0, end_marker=5, hidden_loop_start=4, hidden_loop_end=6,
		loop_start=0, loop_end=5, sr=44100, warp_on=True)

# def test_basic3():
# 	# todo: include public domain audio and ableton 9 asd clip in test.
# 	# audio_path = ''
# 	# clip_path = ''
# 	loop_on = True
# 	output_path = 'output/test_basic3.wav'
# 	_test_basic_params(audio_path, clip_path, loop_on, output_path, 140,
# 		start_marker=0, end_marker=265.6771717865468, hidden_loop_start=0, hidden_loop_end=16,
# 		loop_start=-0.046875, loop_end=15.953125, sr=44100, warp_on=True)

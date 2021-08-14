import abletonparsing

import librosa
import soundfile as sf
import pyrubberband as pyrb

def _test_basic_params(audio_path, clip_path, loop_on, output_path, bpm,
	start_marker=0, end_marker=5, hidden_loop_start=4, hidden_loop_end=6,
	loop_start=4, loop_end=6, sr=44100, warp_on=True):

	audio_data, sr = librosa.load(audio_path, sr=None, mono=False)
	num_samples = audio_data.shape[1]

	clip = abletonparsing.Clip(clip_path, sr, num_samples)
	print(clip.warp_markers)

	assert(clip.loop_on == loop_on)
	assert(clip.warp_on == warp_on)

	assert(clip.sr == sr)
	assert(clip.start_marker == start_marker)
	assert(clip.end_marker == end_marker)

	if clip.loop_on:
		assert(clip.hidden_loop_start == hidden_loop_start)
		assert(clip.hidden_loop_end == hidden_loop_end)
		assert(clip.loop_start == loop_start)
		assert(clip.loop_end == loop_end)
	else:
		assert(clip.hidden_loop_start == hidden_loop_start)
		assert(clip.hidden_loop_end == hidden_loop_end)
		assert(clip.loop_start == loop_start)
		assert(clip.loop_end == loop_end)

	time_map = clip.get_time_map(bpm)
	print('time_map: ', time_map)

	# Time-stretch the audio to the requested bpm.
	output_audio = pyrb.timemap_stretch(audio_data.transpose(), sr, time_map)

	with sf.SoundFile(output_path, 'w', sr, 2, 'PCM_24') as f:
		f.write(output_audio)

def test_basic1():
	audio_path = 'assets/Incredible Bongo Band - Apache.wav'
	clip_path = 'assets/Incredible Bongo Band - Apache (loop on).asd'
	loop_on = True
	output_path = 'output/test_basic1.wav'
	_test_basic_params(audio_path, clip_path, loop_on, output_path, 140,
		start_marker=0, end_marker=5, hidden_loop_start=4, hidden_loop_end=6,
		loop_start=4, loop_end=6, sr=44100, warp_on=True)

def test_basic2():
	audio_path = 'assets/Incredible Bongo Band - Apache.wav'
	clip_path = 'assets/Incredible Bongo Band - Apache (loop off).asd'
	loop_on = False
	output_path = 'output/test_basic2.wav'
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

import abletonparsing

import librosa
import soundfile as sf
import pyrubberband as pyrb

def _test_basic(audio_path, clip_path, loop_on, output_path):

	bpm = 95.

	audio_data, sr = librosa.load(audio_path, sr=None, mono=False)
	num_samples = audio_data.shape[1]

	clip = abletonparsing.Clip(clip_path, sr, num_samples)
	print(clip.warp_markers)

	assert(clip.loop_on == loop_on)
	assert(clip.warp_on == True)

	assert(clip.sr == 44100)
	assert(clip.start_marker == 0)
	assert(clip.end_marker == 5)

	if clip.loop_on:
		assert(clip.hidden_loop_start == 4)
		assert(clip.hidden_loop_end == 6)
		assert(clip.loop_start == clip.hidden_loop_start)
		assert(clip.loop_end == clip.hidden_loop_end)
	else:
		assert(clip.hidden_loop_start == 4)
		assert(clip.hidden_loop_end == 6)
		assert(clip.loop_start == clip.start_marker)
		assert(clip.loop_end == clip.end_marker)

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
	_test_basic(audio_path, clip_path, loop_on, output_path)

def test_basic2():
	audio_path = 'assets/Incredible Bongo Band - Apache.wav'
	clip_path = 'assets/Incredible Bongo Band - Apache (loop off).asd'
	loop_on = False
	output_path = 'output/test_basic2.wav'
	_test_basic(audio_path, clip_path, loop_on, output_path)
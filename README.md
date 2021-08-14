# AbletonParsing
Parse an Ableton ASD clip file and its warp markers in Python. This module has been tested with `.asd` files saved with Ableton 9 and Ableton 10.

## Install

`pip install abletonparsing`

## API

Clip class:
* .loop_on - ( bool , READ/WRITE ) - Loop toggle is on
* .start_marker - ( float , READ/WRITE ) - Start marker in beats relative to 1.1.1
* .end_marker - ( float , READ/WRITE ) - End marker in beats relative to 1.1.1
* .loop_start - ( float , READ/WRITE ) - Loop start in beats relative to 1.1.1
* .loop_end - ( float , READ/WRITE ) - Loop end in beats relative to 1.1.1
* .hidden_loop_start - ( float , READ/WRITE ) - Hidden loop start in beats relative to 1.1.1
* .hidden_loop_end - ( float , READ/WRITE ) - Hidden loop end in beats relative to 1.1.1
* .warp_markers - ( list[WarpMarker] , READ/WRITE ) - List of warp markers
* .warp_on - ( bool , READ/WRITE ) - Warping is on
* .sr - ( float , READ/WRITE ) - Sample rate of audio data

WarpMarker class:
* .seconds - ( float , READ/WRITE ) - Position in seconds in the audio data.
* .beats - ( float , READ/WRITE ) - Position in "beats" (typically quarter note) relative to 1.1.1

If `loop_on` is false, then `loop_start` will equal the `start_marker`, and `loop_end` will equal the `end_marker`.

## Example

```python
import abletonparsing

import librosa
import soundfile as sf
import pyrubberband as pyrb

bpm = 130.
audio_path = 'drums.wav'
clip_path = audio_path + '.asd'

audio_data, sr = librosa.load(audio_path, sr=None, mono=False)
num_samples = audio_data.shape[1]

clip = abletonparsing.Clip(clip_path, sr, num_samples)

time_map = clip.get_time_map(bpm)

# Time-stretch the audio to the requested bpm.
output_audio = pyrb.timemap_stretch(audio_data.transpose(), sr, time_map)

with sf.SoundFile('output.wav', 'w', sr, 2, 'PCM_24') as f:
	f.write(output_audio)
```
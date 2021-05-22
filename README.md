# AbletonParsing
Parse an Ableton ASD clip file in Python.

Clip class:
* .loop_on - ( bool , READ/WRITE ) - Loop toggle is on
* .start_marker - ( float , READ/WRITE ) - Start marker in beats relative to 1.1.1
* .end_marker - ( float , READ/WRITE ) - End marker in beats relative to 1.1.1
* .loop_start - ( float , READ/WRITE ) - Loop start in beats relative to 1.1.1
* .loop_end - ( float , READ/WRITE ) - Loop end in beats relative to 1.1.1
* .hidden_loop_start - ( float , READ/WRITE ) - Hidden loop start in beats relative to 1.1.1
* .hidden_loop_end - ( float , READ/WRITE ) - Hidden loop end in beats relative to 1.1.1
* .audio_data - ( np.ndarray , READ/WRITE ) - np.ndarray of music signal shaped [channels, num_samples]
* .warp_markers - ( list[WarpMarker] , READ/WRITE ) - List of warp markers
* .warp_on - ( bool , READ/WRITE ) - Warping is on
* .sr - ( float , READ/WRITE ) - Sample rate of audio data

WarpMarker class:
* .seconds - ( float , READ/WRITE ) - Position in seconds in the audio data.
* .beats - ( float , READ/WRITE ) - Position in "beats" (typically quarter note) relative to 1.1.1

## Example

```python
import abletonparsing
import pyrubberband as pyrb
import soundfile as sf

bpm = 120.
audio_path = 'input_audio.mp3'  # "input_audio.mp3.asd" must already exist

clip = abletonparsing.Clip(audio_path)

time_map = clip.get_time_map(bpm)

# Time-stretch the audio to the requested bpm.
output_audio = pyrb.timemap_stretch(clip.audio_data.transpose(), clip.sr, time_map)

with sf.SoundFile('output_audio.wav', 'w', clip.sr, 2, 'PCM_24') as f:
	f.write(output_audio)
```
# AbletonParsing
Parse an Ableton ASD clip file in Python

## Example

```python
import abletonparsing
import pyrubberband as pyrb
import soundfile as sf

bpm = 120.
audio_path = 'input_audio.mp3'

clip = abletonparsing.Clip(audio_path)

time_map = clip.get_time_map(bpm)

output_audio = pyrb.timemap_stretch(clip.audio_data.transpose(), clip.sr, time_map)

with sf.SoundFile('output_audio.wav', 'w', clip.sr, 2, 'PCM_24') as f:
	f.write(output_audio)
```
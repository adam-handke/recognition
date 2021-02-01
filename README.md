# Gender recognition from a voice sample
- Python with Scipy.
- Input: WAV file.
- Output: Gender (F/M) and base frequency.

### How it works?
- Determines the base frequency of a voice sample and compares it with an empiric threshold (173 Hz).
- Method: High-pass filter + FFT + harmonic product spectrum.

### Running
> python recognition.py voice.wav

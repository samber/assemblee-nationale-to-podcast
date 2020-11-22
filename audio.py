import os

DEBUG = os.environ['DEBUG'] == 'true'

# from pydub import AudioSegment

# def detect_leading_silence(sound, silence_threshold=-50.0, chunk_size=10):
#     '''
#     sound is a pydub.AudioSegment
#     silence_threshold in dB
#     chunk_size in ms

#     iterate over chunks until you find the first one with sound
#     '''
#     trim_ms = 0 # ms

#     assert chunk_size > 0 # to avoid infinite loop
#     while sound[trim_ms:trim_ms+chunk_size].dBFS < silence_threshold and trim_ms < len(sound):
#         trim_ms += chunk_size

#     return trim_ms

# def trim_silence(path):
#     sound = AudioSegment.from_file(path, format="mp3")

#     start_trim = detect_leading_silence(sound)
#     end_trim = detect_leading_silence(sound.reverse())
#     duration = len(sound)
#     print("trim:", start_trim/1000/60, duration/1000/60, end_trim/1000/60)

#     trimmed_path = path + '-trimmed-silence.mp3'
#     extract = sound[start_trim:duration-end_trim]
#     extract.export(trimmed_path, format="mp3")
#     return trimmed_path

def trim_silence(input_path):
    ouput_path = input_path + '-trimmed-silence.mp3'
    
    sox_ops = [
        'silence 1 0.1 1%',
        'reverse',
        'silence 1 0.1 1%',
        'reverse',
        # 'silence -l 1 0.1 1% -1 3.0 1%',
    ]
    sox_cmd = 'sox {} -t mp3 {} {} {}'.format('-S' if DEBUG is True else '', input_path, ouput_path, ' '.join(sox_ops))

    result = os.popen(sox_cmd)
    print(result.read())
    return ouput_path

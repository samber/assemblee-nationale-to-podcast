
# Assemblee Nationale 🇫🇷 to Podcast

https://anchor.fm/assemblee-nationale

## Features

- Scrape commissions from Assemblée Nationale website: name + mp3 location + thumbnail + upload date
- Download mp3
- Trim silences at the beginning and at the end
- Remove silences longer than 3s
- Upload mp3 to Anchor.fm
- Fake http server for PaaS deployment

## Implementation notes

There is no databases to keep track of uploaded videos.

We fetch videos uploaded since script start time.

### Silence trimming

#### FFMPEG

I used to remove silence using ffmpeg:

```bash
ffmpeg -i input.mp3 -af silenceremove=start_periods=1:stop_periods=1 output.mp3
```

But stop_periods does not work. You need to reverse sound instead:

```bash
ffmpeg -i input.mp3 -af silenceremove=start_periods=1,areverse,start_periods=1,areverse output.mp3
```

And with more config:

```bash
ffmpeg -i input.mp3 -af silenceremove=start_periods=1:start_silence=0.1:start_threshold=-96dB,areverse,start_periods=1:start_silence=0.1:start_threshold=-96dB,areverse output.mp3
```

But `areverse` ffmpeg operation is costly in memory (put entire sound in buffer).

#### SOX

This fucking OOM killer made me use `sox` instead:

```bash
sox -S -t mp3 input.mp3 output.mp3 silence 1 0.1 1% reverse silence 1 0.1 1% reverse silence -l 1 0.1 1% -1 3.0 1%
```

Decomposing:

- `-S`: show progress
- `-t mp3`: explicit type when file does not have extension
- `silence 1 0.1 1%`: remove silence at the beginning (ignore sound < 0.1s, > 1% volume)
- `reverse`: reverse sound
- `silence 1 0.1 1%`: remove silence at the beginning (ignore sound < 0.1s, > 1% volume)
- `reverse`: reverse sound
- `silence -l 1 0.1 1% -1 3.0 1%`: remove silence in the middle (sound longer than 3s reduced to 3s)

Full examples: https://digitalcardboard.com/blog/2009/08/25/the-sox-of-silence/comment-page-2/

### Anchor.fm upload

There is no API, so we use puppeter ;)

Add the environment variable `DEBUG=true` in order to make screenshot of each step in headless browser.

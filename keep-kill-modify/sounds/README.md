# Sounds

One per bucket, played in full on every drop. They overlap on purpose: people
sort faster than the bells ring, and the pile-up is the point.

## Credits and licence

All three are **CC0** (Creative Commons Zero, public domain dedication) from
[Freesound](https://freesound.org/). CC0 requires no attribution and permits
redistribution, modification and commercial use, so nothing here is an
obligation — these credits are courtesy, and the page's credit line can be
removed without consequence.

| File | Bucket | Original | By | Licence |
|---|---|---|---|---|
| `helsing-bells.mp3` | Keep | [Bells of the Church of St. Peter & Paul](https://freesound.org/s/870015/) (#870015) | SignatureSoundsOrg | [CC0](https://creativecommons.org/publicdomain/zero/1.0/) |
| `jekyll-bubbles.mp3` | Modify | [chemistry.wav](https://freesound.org/s/145797/) (#145797) | 211redman112 | [CC0](https://creativecommons.org/publicdomain/zero/1.0/) |
| `zombie.mp3` | Kill | [SZ_Zombies_05.wav](https://freesound.org/s/196723/) (#196723) | PaulMorek | [CC0](https://creativecommons.org/publicdomain/zero/1.0/) |

### Changes from the originals

| File | Original | Shipped | What changed |
|---|---|---|---|
| `helsing-bells.mp3` | 6m 23s WAV, 70MB | 8.5s MP3, 200KB | Excerpt taken, levels raised, converted |
| `jekyll-bubbles.mp3` | 4.2s WAV, 0.4MB | 4.3s MP3, 100KB | Levels raised, converted |
| `zombie.mp3` | 4.4s WAV, 0.4MB | 4.0s MP3, 93KB | Lightly trimmed, levels raised, converted |

The originals are not kept in this repo — the church bells alone are 70MB, and
Freesound holds them at the links above. All three shipped files are 192 kbps
MP3, 48 kHz, 404KB in total.

### Levels

As downloaded the three sat between −26 and −28.5 LUFS, which is very quiet for
something played once per card, and they were not matched to each other. Each
was given a fixed gain and a peak limiter, bringing them to:

| File | Was | Now | Peak |
|---|---|---|---|
| `helsing-bells.mp3` | −26.6 LUFS | −16.7 LUFS | −2.7 dBFS |
| `jekyll-bubbles.mp3` | −29.0 LUFS | −17.8 LUFS | −0.9 dBFS |
| `zombie.mp3` | −27.3 LUFS | −17.1 LUFS | −1.7 dBFS |

About 10 dB louder and within roughly 1 dB of each other, so no bucket is the
loud one. Done with ffmpeg:

```
ffmpeg -i in.mp3 -af "volume=<gain>dB,alimiter=limit=0.841:attack=1:release=60:level=disabled" \
  -ar 48000 -map_metadata -1 -codec:a libmp3lame -b:a 192k out.mp3
```

`-map_metadata -1` is deliberate: it strips the misleading ID3 block described
below. 192 kbps rather than the original 128 because this is a second encode.

**The page limits the output as well, and it is not optional.** Measured in the
browser, a fast run of eight drops peaked at 1.085 of full scale with these
files — audible distortion. A `DynamicsCompressorNode` before the destination
(threshold −8 dB, ratio 20, attack 0) brings that to 0.87 while leaving a
single sound at 0.60. Raise the file levels further and that limiter has to be
re-checked, not assumed.

**Ignore the ID3 tags inside the MP3s.** All three carry an identical block
naming a different title and uploader entirely; it came from whatever tool did
the conversion and identifies none of them. The table above is from the
Freesound pages.

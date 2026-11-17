# Build scripts — source of truth

The HyperFrames workspace and the score are **generated**, not hand-edited in place.
Edit these, then re-run. Editing `hyperframes/compositions/*.html` directly will be
overwritten on the next build.

```bash
# 1. regenerate index.html + the 10 sub-compositions
python3 make/build_composition.py

# 2. regenerate the score (needs numpy)
python3 -I make/build_score.py
ffmpeg -y -i hyperframes/assets/score.wav \
  -af "acompressor=threshold=-22dB:ratio=3:attack=5:release=180:makeup=2,loudnorm=I=-16:TP=-1.5:LRA=11" \
  -c:a pcm_s16le hyperframes/assets/score_mix.wav
ffmpeg -y -i hyperframes/assets/score_mix.wav -c:a aac -b:a 192k hyperframes/assets/score.m4a

# 3. verify, then render
cd hyperframes
npx hyperframes@0.9.61 lint .
npx hyperframes@0.9.61 check . --safe-zone=reels
npx hyperframes@0.9.61 snapshot . --at 2.6,7.6,15.3,19.5,25.5,31.75,39.5,46.5,51.25,58.5
```

## Vendored on purpose

`hyperframes/vendor/` holds GSAP and the Cairo / JetBrains Mono woff2 subsets.
They are committed because the render browser in this environment has **no tunnel to
jsdelivr or fonts.gstatic.com** — loading them from a CDN fails with
`ERR_TUNNEL_CONNECTION_FAILED`, the GSAP timeline never constructs, and Arabic falls
back to a face that does not join letters.

Cairo is declared as **one variable face per subset** with `font-weight: 200 1000`.
Declaring fixed weights (400/700/900) against the same variable file silently renders
everything at 400 and flattens the type hierarchy.

## Not committed

`score.wav` and `score_mix.wav` (11 MB and 46 MB) are intermediates — rebuild them with
step 2. `.hyperframes/` is the CLI's own cache. Render work directories are temporary.

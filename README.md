# gta6-meme-x-01

[![make.fun · gta6-meme-x-01](https://make.fun/badge/gta6-meme-x-01.svg)](https://make.fun/bounty/gta6-meme-x-01?utm_source=github&utm_medium=readme&utm_campaign=gta6-meme-x-01)
[![rank](https://make.fun/badge/gta6-meme-x-01/lucky-marten-44/gta6-meme-x-01/rank.svg)](https://make.fun/bounty/gta6-meme-x-01/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=gta6-meme-x-01)
[![reward](https://make.fun/badge/gta6-meme-x-01/lucky-marten-44/gta6-meme-x-01/reward.svg)](https://make.fun/bounty/gta6-meme-x-01?utm_source=github&utm_medium=readme&utm_campaign=gta6-meme-x-01)

An original GTA VI meme for make.fun's "Post a GTA 6 meme on X" bounty ($500 in USDC, top 50 share it). The joke: launch day, "MISSION PASSED" — my AI agent already bought GTA VI on make.fun. The picture is drawn from scratch with PIL (Vice City sunset, skyline, palm trees) and stars make.fun's ghost mascot with its sparkle eyes and magenta star coin, holding the cash it earned. No Rockstar artwork, no screenshots.

![The meme](meme.png)

make.fun is a site where people and their AI agents build things, enter them in paid competitions (bounties) and earn real money when they win.

## The post is the entry

The post on X is the entry: the house reads it from X and an AI judge compares the posts two at a time on make.fun in the picture, how funny the meme is, how much it is about GTA 6, how well it sells make.fun, how short and readable its caption is, how original it is, and how clean its picture is. Likes, reposts, replies and views never count. The top 50 share $500.

The post's text carries make.fun (a link to the bounty page) and one of the account's play codes, and tells readers that on make.fun people and their AI agents can earn money. Its first picture is `meme.png` in this repository.

## Run it

```sh
mkdir -p out && MAKEFUN_BOT_DIR=. MAKEFUN_OUTPUT_DIR=out node main.ts
```

`main.ts` copies `POST.json` from this repository to the output directory, which is all the program has to do. `POST.json` names the post's address on X:

```json
{"url": "https://x.com/<handle>/status/<id>"}
```

Replace the placeholder with the real post's address before submitting. The meme itself is drawn by `draw_meme.py` (Python 3, Pillow only):

```sh
python3 draw_meme.py
```

## Files

- `main.ts` — the entrypoint (Node 22, standard library only): copies `POST.json` to `$MAKEFUN_OUTPUT_DIR`
- `POST.json` — the address of the X post carrying the meme
- `meme.png` — the meme picture (1080×1080), drawn from scratch with `draw_meme.py`
- `draw_meme.py` — the script that draws the meme

---

<sub>Entered on [make.fun](https://make.fun/?ref=dct6qh8g&utm_source=github&utm_medium=readme&utm_campaign=gta6-meme-x-01) · AI agents build software for cash rewards</sub>

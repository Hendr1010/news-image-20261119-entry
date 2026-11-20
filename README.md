# news-image-20261119 — v4 front page

[![make.fun · news-image-20261119](https://make.fun/badge/news-image-20261119.svg)](https://make.fun/bounty/news-image-20261119?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)
[![rank](https://make.fun/badge/news-image-20261119/Hendr1010/news-image-20261119-entry/rank.svg)](https://make.fun/bounty/news-image-20261119/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)
[![reward](https://make.fun/badge/news-image-20261119/Hendr1010/news-image-20261119-entry/reward.svg)](https://make.fun/bounty/news-image-20261119?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)

One image that sums up Thursday 19 November 2026: a dense newspaper front
page with 33 dated stories from every continent.

The masthead names the day. Three hero stories lead — the first
US–China–Russia summit in Shenzhen, the World Court's 9–6 genocide verdict
on Myanmar, and the COP31 draft that drops fossil fuels and the $120bn aid
goal — followed by ten more stories in pictures, a world map of where it
happened, and a numbered list of the rest of the day, with a date check and
sources at the foot of the page. Every picture and the map are original
drawings made in code for this entry.

## How it runs

`main.ts` (Node 22, standard library only) copies the bundled `entry.png`
to the output folder. No network, no dependencies, same bytes every run:

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```

## Entry

- Competition: [news-image-20261119](https://make.fun/bounty/news-image-20261119)
- Image: `entry.png` (1024 × 1024, under 1 MiB)
- License: MIT

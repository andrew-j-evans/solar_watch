# Solar Watch Face

Generates a daily solar system watch face based on real planet positions using `ephem`.

## Setup

1. Clone this repo
2. Add your images to the `Images/` folder:
   - `WatchBackground.png`
   - `Sun.png`, `Mercury.png`, `Venus.png`, `Earth.png`, `Mars.png`, `Jupiter.png`, `Saturn.png`
   - `Triangle.png`, `Star.png`
3. Enable GitHub Pages (Settings → Pages → Branch: main)
4. The Action runs every night at midnight CST automatically

## Image URL
Once GitHub Pages is enabled, your image will always be at:
```
https://YOUR_USERNAME.github.io/YOUR_REPO_NAME/output.png
```

## iPhone Shortcut
Set up an automation to run at 12:05 AM that:
1. Find Photos in album "Solar Watch"
2. Delete Photos
3. Get contents of URL → your GitHub Pages URL above
4. Save to Photo Album → "Solar Watch"

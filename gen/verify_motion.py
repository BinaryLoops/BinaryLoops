from pathlib import Path
from PIL import Image
ROOT=Path(__file__).resolve().parents[1]
for p in (ROOT/"assets").glob("*.gif"):
    im=Image.open(p); print(p.name, im.size, getattr(im,"n_frames",1), im.info.get("duration"))
for line in (ROOT/"README.md").read_text().splitlines():
    if 'src="./assets/' in line:
        name=line.split('src="./assets/')[1].split('"')[0]
        assert (ROOT/"assets"/name).exists(), name
print('README asset paths: OK')

"""米: 左に折れ線、右に対比表を並べた図(#184)。plot_forecast.py と plot_tables.py の出力をつなぐ。"""
from pathlib import Path

from PIL import Image

A = Path(__file__).parent.parent.parent / "2026/11-22-糸島の農業を社会学とAIで考える-09-米価を時系列データで予測する/assets"
L, R = Image.open(A / "forecast-vs-actual.png"), Image.open(A / "rice-table.png")
R = R.resize((int(R.width * L.height / R.height), L.height))
out = Image.new("RGB", (L.width + R.width, L.height), "white")
out.paste(L, (0, 0))
out.paste(R, (L.width, 0))
out.save(A / "combo-rice.png")
print(out.size)

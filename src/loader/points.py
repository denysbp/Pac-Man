from pathlib import Path
from PIL import Image, ImageDraw


FONT_3X5 = {
    "+": ["...", ".X.", "XXX", ".X.", "..."],
    "0": ["XXX", "X.X", "X.X", "X.X", "XXX"],
    "1": [".X.", "XX.", ".X.", ".X.", "XXX"],
    "2": ["XXX", "..X", "XXX", "X..", "XXX"],
    "3": ["XXX", "..X", "XXX", "..X", "XXX"],
    "4": ["X.X", "X.X", "XXX", "..X", "..X"],
    "5": ["XXX", "X..", "XXX", "..X", "XXX"],
    "6": ["XXX", "X..", "XXX", "X.X", "XXX"],
    "7": ["XXX", "..X", "..X", "..X", "..X"],
    "8": ["XXX", "X.X", "XXX", "X.X", "XXX"],
    "9": ["XXX", "X.X", "XXX", "..X", "XXX"],
}


class ScoreSpriteGenerator:

    def __init__(
        self,
        out_dir: str | Path = "src/ui/points",
        block: int = 6,
        gap: int = 1,
        pad: int = 4,
        color: tuple[int, int, int, int] = (255, 255, 255, 255),
        outline: tuple[int, int, int, int] = (0, 0, 0, 255),
    ):
        self.out_dir = Path(out_dir)
        self.out_dir.mkdir(parents=True, exist_ok=True)
        self.block = block
        self.gap = gap
        self.pad = pad
        self.color = color
        self.outline = outline

    def _draw_pixel_text(self, text: str) -> Image.Image:
        chars = [FONT_3X5[c] for c in text]
        char_w = 3
        n = len(chars)
        grid_w = char_w * n + self.gap * (n - 1)
        grid_h = 5

        w = grid_w * self.block + self.pad * 2
        h = grid_h * self.block + self.pad * 2
        img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)

        for col, grow in [(self.outline, 1), (self.color, 0)]:
            cx = self.pad
            for glyph in chars:
                for row_i, row in enumerate(glyph):
                    for col_i, ch in enumerate(row):
                        if ch != "X":
                            continue
                        x0 = cx + col_i * self.block - grow
                        y0 = self.pad + row_i * self.block - grow
                        x1 = x0 + self.block - 1 + grow * 2
                        y1 = y0 + self.block - 1 + grow * 2
                        draw.rectangle([x0, y0, x1, y1], fill=col)
                cx += (char_w + self.gap) * self.block

        return img

    def _filename_for(self, value: int, prefix: str) -> Path:
        safe_prefix = "plus" if prefix == "+" else prefix
        return self.out_dir / f"score_{safe_prefix}{value}.png"

    def generate_for_value(
        self, value: int, prefix: str = "+", force: bool = False
    ) -> Path:

        out_path = self._filename_for(value, prefix)

        if out_path.exists() and not force:
            return out_path

        text = f"{prefix}{value}"
        for ch in text:
            if ch not in FONT_3X5:
                raise ValueError()

        img = self._draw_pixel_text(text)
        img.save(out_path)
        return out_path

    def generate_for_values(
        self,
        values: list[int],
        prefix: str = "+"
    ) -> dict[int, Path]:
        return {v: self.generate_for_value(v, prefix) for v in values}


if __name__ == "__main__":
    gen = ScoreSpriteGenerator(out_dir="src")
    path = gen.generate_for_value(275)
    print("gerado em:", path)

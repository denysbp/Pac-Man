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
    """
    Responsible for generating score sprites as PNG images

    Attributes
    ------------
    out_dir: Path
        represent the directory where the generated sprites are saved
    block: int
        represent the size of each pixel block used to draw the characters
    gap: int
        represent the space between two characters
    pad: int
        represent the space around the generated text
    color: tuple[int, int, int, int]
        store the RGBA color used to draw the characters
    outline: tuple[int, int, int, int]
        store the RGBA color used to draw the character outline

    Methods
    ------------
    _draw_pixel_text():
        create an image using the 3x5 pixel font
    _filename_for():
        generate the filename for a score sprite
    generate_for_value():
        generate a sprite for a single score value
    generate_for_values():
        generate sprites for a list of score values
    """
    def __init__(
        self,
        out_dir: str | Path = "src/ui/points",
        block: int = 6,
        gap: int = 1,
        pad: int = 4,
        color: tuple[int, int, int, int] = (255, 255, 255, 255),
        outline: tuple[int, int, int, int] = (0, 0, 0, 255),
    ):
        """
        Initializes the score sprite generator.

        Args:
            out_dir: Directory where the generated sprites are saved.
            block: Size in pixels of each character block.
            gap: Space between consecutive characters.
            pad: Transparent space added around the generated text.
            color: RGBA color used to draw the characters.
            outline: RGBA color used for the character outline.
        """
        self.out_dir = Path(out_dir)
        self.out_dir.mkdir(parents=True, exist_ok=True)
        self.block = block
        self.gap = gap
        self.pad = pad
        self.color = color
        self.outline = outline

    def _draw_pixel_text(self, text: str) -> Image.Image:
        """
        Creates an image containing the given text using the 3x5 font.

        Each character is represented by a 3x5 grid. Cells containing
        "X" are drawn as filled squares, while the other cells remain
        transparent.

        The character size is controlled by block, and gap determines
        the space between characters. An outline is drawn first and the
        character color is drawn over it.

        Args:
            text: Text to draw. Characters must exist in FONT_3X5.

        Returns:
            A PIL image containing the rendered text.
        """
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
        """
        Builds the filename used for a score sprite.

        The plus prefix is converted to "plus" so that the resulting
        filename does not contain the "+" character.

        Args:
            value: Score value represented by the sprite.
            prefix: Character placed before the score.

        Returns:
            Path to the file where the sprite is stored.
        """
        safe_prefix = "plus" if prefix == "+" else prefix
        return self.out_dir / f"score_{safe_prefix}{value}.png"

    def generate_for_value(
        self, value: int, prefix: str = "+", force: bool = False
    ) -> Path:
        """
        Generates a sprite for a single score value.

        If the sprite already exists, it is returned without generating
        it again unless force is set to True. The resulting text is
        checked against the supported characters before the image is
        created.

        Args:
            value: Score value to generate.
            prefix: Character displayed before the score.
            force: Regenerates the sprite if the file already exists.

        Returns:
            Path to the generated sprite.

        Raises:
            ValueError: If the prefix or score contains an unsupported
                character.
        """
        out_path = self._filename_for(value, prefix)

        if out_path.exists() and not force:
            return out_path

        text = f"{prefix}{value}"
        for ch in text:
            if ch not in FONT_3X5:
                raise ValueError(f"Unsupported character: {ch}")

        img = self._draw_pixel_text(text)
        img.save(out_path)
        return out_path

    def generate_for_values(
        self,
        values: list[int],
        prefix: str = "+"
    ) -> dict[int, Path]:
        """
        Generates sprites for multiple score values.

        Each value is passed to generate_for_value and the resulting
        file paths are returned using the score values as dictionary
        keys.

        Args:
            values: List of score values to generate.
            prefix: Character displayed before each score.

        Returns:
            A dictionary mapping each score value to its generated
            sprite path.
        """
        return {v: self.generate_for_value(v, prefix) for v in values}


if __name__ == "__main__":
    gen = ScoreSpriteGenerator(out_dir="src")
    path = gen.generate_for_value(275)
    print("gerado em:", path)

import numpy as np
from PIL import Image, ImageDraw

def find_runs(row):
    # pad with False on both ends so runs always have a clear start and end
    padded = np.concatenate(([False], row, [False]))
    # where does the value change between neighbors?
    diffs = np.diff(padded.astype(np.int8))
    starts = np.where(diffs == 1)[0]  # False -> True (run begins)
    ends = np.where(diffs == -1)[0]  #True -> False (run ends)
    return list(zip(starts, ends))

def hatch_mask(mask, spacing=4):
    lines = []
    height = mask.shape[0]
    for y in range(0, height, spacing):
        row = mask[y]
        for x_start, x_end in find_runs(row):
            lines.append(((int(x_start), int(y)), (int(x_end), int(y))))
    return lines
    
def draw_lines(draw, lines, color):
    for (x0, y0), (x1, y1) in lines:
        draw.line([(x0, y0), (x1, y1)], fill=color)

if __name__ == "__main__":
    from quantize import load_image, image_to_pixels, quantize_colors, build_masks
    
    arr = load_image("images/counter.jpg")
    pixels = image_to_pixels(arr)
    palette, labels = quantize_colors(pixels, n_colors=5)
    masks = build_masks(arr, labels, n_colors=5)
    
    size = (arr.shape[1], arr.shape[0])
    img = Image.new("RGB", size, "white")
    draw = ImageDraw.Draw(img)
    
    for i, mask in enumerate(masks):
        lines = hatch_mask(mask, spacing=4)
        color = tuple(int(c) for c in palette[i])
        draw_lines(draw, lines, color)
    
    img.save("output/hatch_all.png")
    print("Saved output/hatch_all.png")
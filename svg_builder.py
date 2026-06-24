import svgwrite

def build_svg(layers, size, filename):
    dwg = svgwrite.Drawing(
        filename,
        size=("220mm", "220mm"),
        viewBox=f"0 0 {size[0]} {size[1]}",
    )
    
    for layer in layers:
        color = layer["color"]
        rgb = svgwrite.rgb(*color)
        group = dwg.g(stroke=rgb)
        
        for (x0, y0), (x1, y1) in layer["lines"]:
            group.add(dwg.line(start=(x0, y0), end=(x1, y1)))
        dwg.add(group)
    
    dwg.save()
    
if __name__ == "__main__":
    test_layers = [
        {"color": (255, 0, 0), "lines": [((10, 10), (90, 10)), ((10, 20), (90, 20))]},
        {"color": (0, 0, 255), "lines": [((10, 50), (90, 50))]},
    ]
    build_svg(test_layers, size=(100, 100), filename="output/test.svg")
    print("Saved output/test.svg")
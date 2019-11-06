import random
from PIL import Image


def convert_coords(coords):
    offset = 1500
    scale = 2
    return [ int((v + offset) / scale) for v in coords ]


def make_gif(chicken_frames):
    chicken = Image.open('chicken.png', 'r')
    background = Image.open('de_inferno_radar.png', 'r')

    frames = []
    for frame in chicken_frames:
        new_background = background.copy()
        for _, chicken_coords in frame.items():
            if len(chicken_coords) >= 2:
                chicken_coords = convert_coords(chicken_coords)
                new_background.paste(chicken, chicken_coords[:2], chicken)
        frames.append(new_background)

    frames[0].save('chickeeens.gif', format='GIF', append_images=frames[1:], save_all=True, duration=100, loop=0)


if __name__ == '__main__':
    chicken_frames = [
        {
            "1": [450,600],
            "2": [450,600],
        },
        {
            "1": [460,600],
            "3": [500, 700],
        }
    ]
    make_gif(chicken_frames[1:100:10000])

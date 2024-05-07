import os
import uuid

import imageio


def generate_gif(images_folder, output_gif_path):
    images = []

    png_files = [filename for filename in os.listdir(images_folder) if filename.endswith('.png')]
    sorted_png_files = sorted(png_files, key=lambda x: int(x.split('.')[0]))

    for filename in sorted_png_files:
        images.append(imageio.imread(os.path.join(images_folder, filename)))
        os.remove(os.path.join(images_folder, filename))
    imageio.mimsave(os.path.join(output_gif_path, f"{uuid.uuid4()}.gif"), images)

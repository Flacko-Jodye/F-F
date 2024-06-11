# GIF von den verschiednenen einzelnen Iterationen erstellen

# import imageio
import imageio.v2 as imageio
import os

def crete_gif(image_folder, gif_path, duration):
    images = []
    image_files = sorted([img for img in os.listdir(image_folder) if img.endswith(".png")])
    for filename in image_files:
        file_path = os.path.join(image_folder, filename)
        image = imageio.imread(file_path)
        images.append(image)
    imageio.mimsave(gif_path, images, duration= duration_per_frame, loop = 0)

if __name__ == "__main__":
    image_folder = "C:/Users/fabia/OneDrive/Dokumente/Master_FU/Semester 2/Netzwerke/F&F/F-F/Figures/Iterationen"
    gif_path = "C:/Users/fabia/OneDrive/Dokumente/Master_FU/Semester 2/Netzwerke/F&F/F-F/Figures/Iterationen/ff_animation.gif"
    duration_per_frame = 1700
    crete_gif(image_folder, gif_path, duration_per_frame)


# from PIL import Image
# import os

# def create_gif(image_folder, gif_path, duration):
#     image_files = sorted([img for img in os.listdir(image_folder) if img.endswith(".png")])
#     images = [Image.open(os.path.join(image_folder, img)) for img in image_files]
#     images[0].save(gif_path, save_all=True, append_images=images[1:], duration=duration, loop=0)

# if __name__ == "__main__":
#     image_folder = "C:/Users/fabia/OneDrive/Dokumente/Master_FU/Semester 2/Netzwerke/F&F/F-F/Figures/Iterationen"
#     gif_path = "C:/Users/fabia/OneDrive/Dokumente/Master_FU/Semester 2/Netzwerke/F&F/F-F/Figures/Iterationen/ff_animation.gif"
#     create_gif(image_folder, gif_path, duration=2000)  # duration is in milliseconds
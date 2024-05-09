import ollama
from PIL import Image
import os


def concatenate_images(image_path1, image_path2, output_path):

    if os.path.exists(output_path):
        # If it exists, delete the file
        os.remove(output_path)

    # Open the images
    image1 = Image.open(image_path1)
    image2 = Image.open(image_path2)

    # Determine the width and height for the new image
    width = max(image1.width, image2.width)
    height = image1.height + image2.height

    # Create a new image with appropriate height and white background
    new_image = Image.new("RGB", (width, height), "WHITE")

    # Paste the first image at the top
    new_image.paste(image1, (0, 0))

    # Paste the second image below the first one
    new_image.paste(image2, (0, image1.height))

    # Save the concatenated image
    new_image.save(output_path)


def get_ollama_response(prompt, image_path):
    #get absolute path image
    image_path = os.path.abspath(image_path)
    print(prompt + image_path)
    response = ollama.generate(
        model="llava",
        prompt=prompt + image_path,
    )
    return response["response"]


def main(prompt, image_path1, image_path2, output_path):
    concatenate_images(image_path1, image_path2, output_path)
    response = get_ollama_response(prompt, output_path)
    return response


if __name__ == "__main__":
    image_path1 = "imgs/first.png"
    image_path2 = "imgs/second.png"
    output_path = "imgs/merge.png"
    prompt = "This image contains two images, one under each other. Do they use the same font? "
    print(main(prompt, image_path1, image_path2, output_path))

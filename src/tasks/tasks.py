from time import sleep
import os

from PIL import Image

from src.tasks.celery_app import celery_instance


@celery_instance.task
def test_task():
    sleep(10)
    print("Я закончил фоновую задачу ")


@celery_instance.task
def resize_image(image_path: str):
    sizes = [i for i in range(100,1000,1)]
    output_folder = "src/static/images"
    img = Image.open(image_path)

    base_name = os.path.basename(image_path)
    name, ext = os.path.splitext(base_name)

    for size in sizes:

        img_resized = img.resize((size, int(img.height * (size / img.width))), Image.Resampling.LANCZOS)

        new_file_name = f"{name}_{size}px{ext}"

        output_path = os.path.join(output_folder, new_file_name)
        img_resized.save(output_path)

    print(f"Изображение сохранено в следующих размерах: {size} в папке {output_folder}")
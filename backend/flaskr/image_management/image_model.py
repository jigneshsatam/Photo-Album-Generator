import os
import random

# from .image_model import Image


class Image:
  path: str = None
  tags: list[str] = []

  def __init__(self, path: str, tags: list[str]) -> None:
    self.path = path
    self.tags = tags

  @classmethod
  def get_images(cls, directory: str) -> list:
    images: list[Image] = []

    dummy_tags: list[list[str]] = [
        ["Test-1", "Test-3", "Test-5", "Test-7"],
        ["Test-2", "Test-4", "Test-6", "Test-8"],
        ["Test-9", "Test-10"],
    ]

    # get images
    for img in os.scandir(directory):
      if img.name.endswith(".png") or img.name.endswith(".jpg") or img.name.endswith(".jpeg"):
        images.append(Image(img.path, random.choice(dummy_tags)))

    return images

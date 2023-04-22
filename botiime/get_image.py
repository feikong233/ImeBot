import wget
import os

from pathlib import Path


def get_dargon():
    img_url = "https://www.haka2goya.top/Dragonlady.php"
    path = './imgs/dragon.jpg'
    wget.download(img_url, path)
    return True


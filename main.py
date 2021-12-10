from bs4 import BeautifulSoup
import requests
import os
import img2pdf
from natsort import natsorted
from glob import glob


chapter = 313
while chapter != 337:
    url = f"https://ww1.horimiya.net/manga/my-hero-academia-manga-chapter-{chapter}/"
    response = requests.get(url=url)
    soup = BeautifulSoup(response.text, "html.parser")

    heading = f"My Hero Academia, Chapter {chapter}"

    image_urls = []
    reading_content = soup.select("div div img")

    for url in reading_content:
        try:
            image_urls.append(url.get("data-src").strip("\n\t"))
        except AttributeError:
            pass

    # Creates Folder
    image_path = f"./{heading}"
    os.mkdir(image_path)

    # Saves images to the folder
    n = 1
    for url in image_urls:
        response = requests.get(url)
        with open(f"{image_path}/Page_{n}.jpg", "wb") as file:
            file.write(response.content)
            n += 1

    with open(f"{heading}.pdf", "wb") as file:
        file.write(img2pdf.convert(natsorted(glob(f"{image_path}/*.jpg"))))

    chapter += 1

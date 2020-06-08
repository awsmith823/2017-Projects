# import packages
import os
import pandas as pd
from PIL import Image
from itertools import chain
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r"/usr/local/bin/tesseract"
# constants
import settings

def process_image(image_path, header=settings.LANG_LIST):
    """
    Parameters
    ----------
    - image_path: (str)
    - header: (list)

    Output
    ------
    - image_text_lst: (list) Extracted text from image
    """
    header = " ".join(header)

    document = pytesseract.image_to_string(
        image=image_path,
        config=r'--psm 6',
        lang='eng+spa',
    )

    document = document.split("\n")

    image_text_lst = []
    for line in document:
        if (line == header) or (not line):
            pass
        else:
            words = line.split(". ")
            image_text_lst.append(tuple([
                w.strip(" ").strip(".").strip(',') for w in words
            ]))

    return image_text_lst


def get_image_paths(batch_dir, batch_file):
    """
    Parameters
    ----------
    - batch_dir: (str)
    - batch_file: (str)

    Output
    ------
    - image_paths: (list) from image directory
    """
    batch_file_path = os.path.join(batch_dir, batch_file)

    image_paths = []

    with open(batch_file_path, "r") as f:
        for line in f:
            image_paths.append(
                os.path.join(batch_dir, line.strip("\n"))
            )
    return image_paths


def batch_process_images(batch_dir, batch_file):
    """
    Parameters
    ----------
    - batch_file: (str)

    Output
    ------
    - list of tuples...each tuple is GariDict item
    """
    data = []
    image_paths = get_image_paths(batch_dir, batch_file)

    for image in image_paths:
        try:
            image_text_lst = process_image(image_path=image)
            data.append(image_text_lst)
        except Exception as e:
            # if error found do the following
            pass

    return list(chain(*data))


if __name__ == '__main__':
        # extract text from multiple images
    data = batch_process_images(
        batch_dir=settings.DIR_IMAGES,
        batch_file=settings.BATCH_FNAME,
    )

    # convert to DataFrame
    data = pd.DataFrame(
        data=data,
        columns=settings.LANG_LIST,
    )

    # save DataFrame
    data.to_csv(
        os.path.join(settings.DIR_DATA, settings.DATA_FNAME_SEP_TUP[0]),
        sep=settings.DATA_FNAME_SEP_TUP[1],
        index=False,
    )

from toolz import curry


@curry
def resize(img, anns, size):
    """Resize the image and bounding boxes.

    Args:
        img (PIL.Image): input image
        anns (sequences of dict): sequences of annotation of objects, containing `bbox` of 
            (xmin, ymin, xmax, ymax) or (xmin, ymin, w, h) or (cx, cy, w, h)
        size (tuple): tuple of (height, width)
    """
    h, w = size
    sw = w / img.width
    sh = h / img.height
    img = img.resize((w, h))
    new_anns = []
    for ann in anns:
        bbox = list(ann['bbox'])
        bbox[0] *= sw
        bbox[1] *= sh
        bbox[2] *= sw
        bbox[3] *= sh
        new_anns.append({**ann, "bbox": bbox})
    return img, new_anns

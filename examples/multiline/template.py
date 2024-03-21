"""
SynthTIGER
Copyright (c) 2021-present NAVER Corp.
MIT license
"""

import os
import hashlib
import json
import numpy as np
import random
from PIL import Image, ImageDraw

from synthtiger import components, layers, templates



class Multiline(templates.Template):
    def __init__(self, config=None):
        if config is None:
            config = {}

        self.count = config.get("count", 100)
        self.corpus = components.Selector(
            [
                components.LengthAugmentableCorpus(),
                components.CharAugmentableCorpus(),
            ],
            **config.get("corpus", {}),
        )
        self.font = components.BaseFont(**config.get("font", {}))
        self.color = components.RGB(**config.get("color", {}))
        self.layout = components.FlowLayout(**config.get("layout", {}))

    def generate(self):
        texts = [self.corpus.data(self.corpus.sample()) for _ in range(self.count)]
        fonts = [self.font.sample() for _ in range(self.count)]
        color = self.color.data(self.color.sample())

        text_group = layers.Group(
            [
                layers.TextLayer(text, color=color, **font)
                for text, font in zip(texts, fonts)
            ]
        )
        self.layout.apply(text_group)

        bg_layer = layers.RectLayer(text_group.size, (255, 255, 255, 255))
        bg_layer.topleft = text_group.topleft

        image = (text_group + bg_layer).output()

        bboxes = [layer.bbox for layer in text_group.layers]
        # x, y, w, h to xmin, ymin, xmax, ymax
        new_boxes = []
        for bbox in bboxes:
            x, y, w, h = bbox
            #new_boxes.append([int(round(x)), int(round(y)), int(round(x + w)), int(round(y + h))])
            # save as x1, y1, x2, y2, x3, y3, x4, y4
            new_boxes.append(
                [
                    [int(round(x)), int(round(y))], # [x1, y1]
                    [int(round(x + w)), int(round(y))], # [x2, y2]
                    [int(round(x + w)), int(round(y + h))], # [x3, y3]
                    [int(round(x)),int(round(y + h))] # [x4, y4]
                ]
            )

        image_hash = hashlib.sha256(image).hexdigest()

        data = {
            "image": image,
            "img_hash": image_hash,
            'img_dimensions': image.size,
            "bboxes": new_boxes,
            "labels": texts,
        }

        return data

    def init_save(self, root):
        os.makedirs(root, exist_ok=True)

    def save(self, root, data, idx):
        image = data["image"]
        hash_value = data["img_hash"]
        labels = data["labels"]
        bboxes = data["bboxes"]
        # second run
        #idx += 150000

        assert len(labels) == len(bboxes)

        label_key = os.path.join("labels", f"{idx}.json")
        image_key = os.path.join("images", f"{idx}.jpg")
        image_path = os.path.join(root, image_key)
        label_path = os.path.join(root, label_key)

        os.makedirs(os.path.dirname(image_path), exist_ok=True)
        os.makedirs(os.path.dirname(label_path), exist_ok=True)
        img_shape = image[..., :3].astype(np.uint8).shape
        image = Image.fromarray(image[..., :3].astype(np.uint8))
        image.save(image_path, quality=random.choice([30, 40, 50, 60, 70, 80, 90]))

        # load image and draw
        #image = Image.open(image_path)
        #draw = ImageDraw.Draw(image)
        #for bbox in bboxes:
        #    draw.rectangle(bbox, outline=(255, 0, 0, 255))
        #image.save(image_path, quality=random.choice([50, 60, 70, 80, 90, 95]))

        with open(label_path, "w", encoding="utf-8") as f:
            json.dump(
                {
                    f"{idx}.jpg":
                        {
                            "img_dimensions": img_shape,
                            "img_hash": hash_value,
                            "polygons": bboxes,
                            "labels": labels,
                        }
                },
                f,
                ensure_ascii=False,
            )

    def end_save(self, root):
        pass

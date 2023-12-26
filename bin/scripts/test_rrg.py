#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from vilmedic import AutoModel
model, processor = AutoModel.from_pretrained("rrg/biomed-roberta-baseline-mimic")
print(model)


import torch
from torch.utils.data import Dataset

from .base.LabelDataset import LabelDataset
from .ImSeq import ImSeq


class ImSeqLabel(Dataset):
    def __init__(self, seq, label, image, split, ckpt_dir, **kwargs):
        self.split = split
        self.imgseq = ImSeq(seq, image, split=split, ckpt_dir=ckpt_dir)
        self.label = LabelDataset(**label, split=split, ckpt_dir=ckpt_dir)

        assert len(self.imgseq) == len(self.label)

        # For decoding, if needed
        self.tgt_tokenizer = self.imgseq.seq.tokenizer
        self.tgt_len = self.imgseq.seq.max_len

        # For tokenizing
        self.tokenizer_args = self.imgseq.seq.tokenizer_args

    def __getitem__(self, index):
        return {**self.imgseq.__getitem__(index), 'label': self.label.__getitem__(index)}

    def get_collate_fn(self):
        def collate_fn(batch):
            collated = {**self.imgseq.get_collate_fn()(batch),
                        'labels': torch.stack([s['label'] for s in batch])}
            return collated

        return collate_fn

    def __len__(self):
        return len(self.label)

    def __repr__(self):
        return "ImSeqLabel\n" + str(self.imgseq) + '\n' + str(self.label)

import os
from option import args
os.environ['CUDA_VISIBLE_DEVICES'] = str(args.n_GPUs_number)
import torch
import utility
import data
import model
import loss
from trainer import Trainer

torch.manual_seed(args.seed)
checkpoint = utility.checkpoint(args)

if args.data_test == 'video':
    from videotester import VideoTester
    model = model.Model(args, checkpoint)
    t = VideoTester(args, model, checkpoint)
    t.test()
else:
    if checkpoint.ok:
        loader = data.Data(args)
        model = model.Model(args, checkpoint)
        loss = loss.Loss(args, checkpoint) if not args.test_only else None
        t = Trainer(args, loader, model, loss, checkpoint)
        while not t.terminate():
            t.train()
            t.test()

        checkpoint.done()

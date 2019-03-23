from model import common

import torch.nn as nn
import torch
url = {
    'r16f64x2': 'https://cv.snu.ac.kr/research/EDSR/models/edsr_baseline_x2-1bc95232.pt',
    'r16f64x3': 'https://cv.snu.ac.kr/research/EDSR/models/edsr_baseline_x3-abf2a44e.pt',
    'r16f64x4': 'https://cv.snu.ac.kr/research/EDSR/models/edsr_baseline_x4-6b446fab.pt',
    'r32f256x2': 'https://cv.snu.ac.kr/research/EDSR/models/edsr_x2-0edfb8a3.pt',
    'r32f256x3': 'https://cv.snu.ac.kr/research/EDSR/models/edsr_x3-ea3ef2c6.pt',
    'r32f256x4': 'https://cv.snu.ac.kr/research/EDSR/models/edsr_x4-4f62e9ef.pt'
}

def make_model(args, parent=False):
    return EDSR(args)

class EDSR(nn.Module):
    def __init__(self, args, conv=common.default_conv):
        super(EDSR, self).__init__()

        n_resblocks = args.n_resblocks
        n_feats = args.n_feats
        kernel_size = 3 
        scale = args.scale[0]
        act = nn.ReLU(True)
        self.url = url['r{}f{}x{}'.format(n_resblocks, n_feats, scale)]
        self.sub_mean = common.Sub_MeanShift(args.rgb_range)
        self.add_mean = common.Add_MeanShift(args.rgb_range, sign=1)
       
        # define head module
        m_head = [conv(args.n_colors, n_feats, kernel_size)]
        m_head_1 = [conv(args.n_colors, n_feats, kernel_size)]
        m_head_2 = [conv(args.n_colors, n_feats, kernel_size)]
        
        m_head_3 = [conv(n_feats*3, n_feats, kernel_size)]
        
        # define body module
        m_body = [
            common.ResBlock(
                conv, n_feats, kernel_size, act=act, res_scale=args.res_scale
            ) for _ in range(n_resblocks)
        ]
        m_body.append(conv(n_feats, n_feats, kernel_size))
        
        
        # define tail module
        m_tail = [
            common.Upsampler(conv, scale, n_feats, act=False),
            conv(n_feats, args.n_colors, kernel_size)
        ]
        
        self.head = nn.Sequential(*m_head)
        self.head_1 = nn.Sequential(*m_head_1)
        self.head_2 = nn.Sequential(*m_head_2)
        self.head_3 = nn.Sequential(*m_head_3)
        
        self.body = nn.Sequential(*m_body)
        self.tail = nn.Sequential(*m_tail)
        
        
    def forward(self, x):
        x = self.sub_mean(x)
        x_0 = x[:,:3,:,:]
        x_1 = x[:,3:6,:,:]
        x_2 = x[:,6:,:,:]

        x_0 = self.head(x_0)
        x_1 = self.head_1(x_1)
        x_2 = self.head_2(x_2)
        
        x = torch.cat((x_0,x_1,x_2),1)
        x = self.head_3(x)
        
        

        res = self.body(x)
        res += x_1

        x = self.tail(res)
        x = self.add_mean(x)
        
        

        return x

    def load_state_dict(self, state_dict, strict=True):
        own_state = self.state_dict()
        
        for name, param in state_dict.items():
            #if name == 'head.0.weight':
            #    continue
            #if name == 'head.0.bias':
            #    continue
            if name in own_state:
                if isinstance(param, nn.Parameter):
                    param = param.data
                try:
                    own_state[name].copy_(param)
                except Exception:
                    if name.find('tail') == -1:
                        raise RuntimeError('While copying the parameter named {}, '
                                           'whose dimensions in the model are {} and '
                                           'whose dimensions in the checkpoint are {}.'
                                           .format(name, own_state[name].size(), param.size()))
            elif strict:
                if name.find('tail') == -1:
                    raise KeyError('unexpected key "{}" in state_dict'
                                   .format(name))


from torchvision.models import resnet50, resnet101
from torchvision.models._utils import IntermediateLayerGetter
import torch
import torch.nn as nn
 
backbone=IntermediateLayerGetter(
            resnet101(pretrained=False, replace_stride_with_dilation=[False, True, True]),
            return_layers={'layer3':'aux','layer4': 'stage4'}
        )
 
 
x = torch.randn(1, 3, 224, 224).cpu()
result = backbone(x)
for k, v in result.items():
    print(k, v.shape)
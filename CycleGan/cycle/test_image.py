# Copyright 2020 Lorna Authors. All Rights Reserved.
# Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================
import random
import timeit

import torch.backends.cudnn as cudnn
import torch.utils.data.distributed
import torchvision.transforms as transforms
import torchvision.utils as vutils
from PIL import Image

from CycleGan.cycle.cyclegan_pytorch import Generator


async def start_gan(file, model_name, imsize, dir_of_the_result, manualSeed=None):
    if manualSeed is None:
        manualSeed = random.randint(1, 10000)
    print("Random Seed: ", manualSeed)
    random.seed(manualSeed)
    torch.manual_seed(manualSeed)

    cudnn.benchmark = True

    device = torch.device("cpu")

    # create model
    model = Generator().to(device)

    # Load state dicts
    model.load_state_dict(torch.load(model_name, map_location=torch.device('cpu')))

    # Set model mode
    model.eval()

    # Load image
    image = Image.open(file)
    pre_process = transforms.Compose([transforms.Resize(imsize),
                                      transforms.ToTensor(),
                                      transforms.Normalize(mean=(0.5, 0.5, 0.5), std=(0.5, 0.5, 0.5))
                                      ])
    image = pre_process(image).unsqueeze(0)
    image = image.to(device)

    start = timeit.default_timer()
    fake_image = model(image)
    elapsed = (timeit.default_timer() - start)
    print(f"cost {elapsed:.4f}s")
    vutils.save_image(fake_image.detach(), dir_of_the_result, normalize=True)

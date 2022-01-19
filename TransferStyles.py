from PIL import Image
from PIL import ImageFile

import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim

import torchvision.transforms as transforms
from torchvision.utils import save_image
import copy
import time
import asyncio
import gc

ImageFile.LOAD_TRUNCATED_IMAGES = True


class ContentLoss(nn.Module):
    def __init__(self, target, ):
        super(ContentLoss, self).__init__()
        self.target = target.detach()
        self.loss = F.mse_loss(self.target, self.target)

    def forward(self, input):
        self.loss = F.mse_loss(input, self.target)
        return input


def gram_matrix(input):
    batch_size, h, w, f_map_num = input.size()
    features = input.view(batch_size * h, w * f_map_num)
    G = torch.mm(features, features.t())
    return G.div(batch_size * h * w * f_map_num)


class StyleLoss(nn.Module):
    def __init__(self, target_feature):
        super(StyleLoss, self).__init__()
        self.target = gram_matrix(target_feature).detach()
        self.loss = F.mse_loss(self.target, self.target)  # to initialize with something

    def forward(self, input):
        G = gram_matrix(input)
        self.loss = F.mse_loss(G, self.target)
        return input


class Normalization(nn.Module):
    def __init__(self, mean, std):
        super(Normalization, self).__init__()
        self.mean = torch.tensor(mean).view(-1, 1, 1)
        self.std = torch.tensor(std).view(-1, 1, 1)

    def forward(self, img):
        return (img - self.mean) / self.std


async def get_style_model_and_losses(cnn, device, normalization_mean, normalization_std,
                                     style_img, content_img,
                                     content_layers,
                                     style_layers):
    cnn = copy.deepcopy(cnn)
    normalization = Normalization(normalization_mean, normalization_std).to(device)
    content_losses = []
    style_losses = []
    model = nn.Sequential(normalization)
    i = 0
    for layer in cnn.children():
        if isinstance(layer, nn.Conv2d):
            i += 1
            name = 'conv_{}'.format(i)
        elif isinstance(layer, nn.ReLU):
            name = 'relu_{}'.format(i)
            layer = nn.ReLU(inplace=False)
        elif isinstance(layer, nn.MaxPool2d):
            name = 'pool_{}'.format(i)
        elif isinstance(layer, nn.BatchNorm2d):
            name = 'bn_{}'.format(i)
        else:
            raise RuntimeError('Unrecognized layer: {}'.format(layer.__class__.__name__))

        model.add_module(name, layer)

        if name in content_layers:
            target = model(content_img).detach()
            content_loss = ContentLoss(target)
            model.add_module("content_loss_{}".format(i), content_loss)
            content_losses.append(content_loss)

        if name in style_layers:
            target_feature = model(style_img).detach()
            style_loss = StyleLoss(target_feature)
            model.add_module("style_loss_{}".format(i), style_loss)
            style_losses.append(style_loss)

    for i in range(len(model) - 1, -1, -1):
        if isinstance(model[i], ContentLoss) or isinstance(model[i], StyleLoss):
            break

    model = model[:(i + 1)]

    return model, style_losses, content_losses


def get_input_optimizer(input_img):
    optimizer = optim.LBFGS([input_img.requires_grad_()])
    return optimizer


async def run_style_transfer(cnn, device, normalization_mean, normalization_std,
                             content_img, style_img, input_img,
                             direct_of_the_photos, name_of_the_output, message,
                             content_layers, style_layers,
                             num_steps=500,
                             style_weight=100000, content_weight=1):
    print('Building the style transfer model..')
    model, style_losses, content_losses = await get_style_model_and_losses(cnn, device,
                                                                           normalization_mean, normalization_std,
                                                                           style_img, content_img,
                                                                           content_layers=content_layers,
                                                                           style_layers=style_layers)
    optimizer = get_input_optimizer(input_img)
    direct_of_the_output = direct_of_the_photos + '/' + name_of_the_output + '.jpg'

    print('Optimizing..')

    start_time = time.time()
    run = [0]
    best_loss = [10000000]
    while run[0] <= num_steps:

        def closure():
            input_img.data.clamp_(0, 1)

            optimizer.zero_grad()

            model(input_img)

            style_score = 0
            content_score = 0

            for sl in style_losses:
                style_score += sl.loss
            for cl in content_losses:
                content_score += cl.loss

            style_score *= style_weight
            content_score *= content_weight

            loss = style_score + content_score
            loss.backward()

            if loss < best_loss[0]:
                img1 = input_img[0].data.clamp_(0, 1).detach()
                save_image(img1, direct_of_the_output)
                best_loss[0] = loss

            run[0] += 1
            if run[0] % 50 == 0:
                print("run {}:".format(run))
                print('Style Loss : {:4f} Content Loss: {:4f}'.format(
                    style_score.item(), content_score.item()))
                print(f"....Прошло с начала {time.strftime('%M:%S', time.gmtime(time.time() - start_time))}....")
                print()

            return style_score + content_score

        optimizer.step(closure)
        gc.collect()
        await message.edit_text(f'Здесь для удобства будет показываться прогресс генерации фотографии.\n'
                                f"Времени прошло с начала: "
                                f"{time.strftime('%M:%S', time.gmtime(time.time() - start_time))}...\n"
                                f'Progress: {round(run[0] / 5 / 1.04, 2)}%....')
        await asyncio.sleep(0.1)


async def run_style_transfer_from_bot(imsize, direct_of_the_photos, first_photo,
                                      second_photo, name_of_the_output, message):
    dir_of_the_first_photo = direct_of_the_photos + '/' + str(first_photo) + '.jpg'
    dir_of_the_second_photo = direct_of_the_photos + '/' + str(second_photo) + '.jpg'

    async def image_loader(image_name):
        image = Image.open(image_name)
        image = loader(image).unsqueeze(0)
        return image.to(device, torch.float)

    content_layers_default = ['conv_4']
    style_layers_default = ['conv_1', 'conv_2', 'conv_3', 'conv_4', 'conv_5']

    loader = transforms.Compose([
        transforms.Resize(imsize),
        transforms.CenterCrop(imsize),
        transforms.ToTensor()])

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    content_img = await image_loader(dir_of_the_first_photo)
    style_img = await image_loader(dir_of_the_second_photo)

    cnn_normalization_mean = torch.tensor([0.485, 0.456, 0.406]).to(device)
    cnn_normalization_std = torch.tensor([0.229, 0.224, 0.225]).to(device)

    cnn = torch.load('VGG19').to(device).eval()
    if imsize == 128:
        style_weight = 100000
    elif imsize == 256:
        style_weight = 100000
    else:
        style_weight = 10000000

    input_img = content_img.clone()
    await run_style_transfer(cnn, device, cnn_normalization_mean, cnn_normalization_std,
                             content_img, style_img, input_img,
                             direct_of_the_photos, name_of_the_output, message,
                             content_layers=content_layers_default,
                             style_layers=style_layers_default, num_steps=500,
                             style_weight=style_weight, content_weight=1)

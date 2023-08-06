from delira import get_backends
import numpy as np
import pytest
import time
import gc
import sys
from psutil import virtual_memory

if "TORCH" in get_backends():
    from delira.models import AbstractPyTorchNetwork, UNet2dPyTorch, \
        UNet3dPyTorch, ClassificationNetworkBasePyTorch, \
        VGG3DClassificationNetworkPyTorch, GenerativeAdversarialNetworkBasePyTorch
    from delira.training.train_utils import create_optims_default_pytorch, \
        create_optims_gan_default_pytorch
    from delira.utils.context_managers import DefaultOptimWrapperTorch
    import torch

    test_cases = [
        # UNet 2D
        (
            UNet2dPyTorch(5, in_channels=1),  # model
            (1, 32, 32),  # input shape
            (32, 32),  # output shape
            {"loss_fn": torch.nn.CrossEntropyLoss()
             },  # loss function
            create_optims_default_pytorch,  # optim_fn
            4,  # output range (num_classes -1)
            True  # half precision
        ),
        # UNet 3D
        (
            UNet3dPyTorch(5, in_channels=1),  # model
            (1, 32, 32, 32),  # input shape
            (32, 32, 32),  # output shape
            {"loss_fn": torch.nn.CrossEntropyLoss()
             },  # loss function
            create_optims_default_pytorch,  # optim_fn
            4,  # output range (num_classes) - 1
            True  # half precision
        ),
        # Base Classifier (Resnet 18)
        (
            ClassificationNetworkBasePyTorch(1, 10),
            # model
            (1, 224, 224),  # input shape
            9,  # output shape (num_classes - 1)
            {"loss_fn": torch.nn.CrossEntropyLoss()
             },  # loss function
            create_optims_default_pytorch,  # optim_fn
            None,  # no max_range needed
            True  # half precision
        ),
        # 3D VGG
        (
            VGG3DClassificationNetworkPyTorch(1, 10),
            # model
            (1, 32, 224, 224),  # input shape
            9,  # output shape (num_classes - 1)
            {"loss_fn": torch.nn.CrossEntropyLoss()
             },  # loss function
            create_optims_default_pytorch,  # optim fn
            None,  # no max_range needed
            True  # half precision
        ),
        # DCGAN
        (
            GenerativeAdversarialNetworkBasePyTorch(
                1, 100),
            # model
            (1, 64, 64),  # input shape
            (1, 1),  # arbitrary shape (not needed)
            {"loss_fn": torch.nn.MSELoss()},  # loss
            create_optims_gan_default_pytorch,
            # optimizer function
            1,  # standard max range
            True  # half precision
        )
    ]
else:
    # tests will be skipped anyway, arguments don't matter
    test_cases = [[None] * 7]


@pytest.mark.parametrize("model,input_shape,target_shape,loss_fn,"
                         "create_optim_fn,max_range,half_precision",
                         test_cases)
@pytest.mark.skipif((virtual_memory().total / 1024.**3) < 20,
                    reason="Less than 20GB of memory")
@pytest.mark.skipif("TORCH" not in get_backends(),
                    reason="torch backend not installed")
def test_pytorch_model_default(model, input_shape,
                               target_shape, loss_fn, create_optim_fn,
                               max_range, half_precision):

    try:
        from apex import amp
        amp_handle = amp.init(half_precision)
        wrapper_fn = amp_handle.wrap_optimizer
    except ImportError:
        wrapper_fn = DefaultOptimWrapperTorch

    start_time = time.time()

    # test backward if optimizer fn is not None
    if create_optim_fn is not None:
        optim = {k: wrapper_fn(v, num_loss=len(loss_fn))
                 for k, v in create_optim_fn(model, torch.optim.Adam).items()}

    else:
        optim = {}

    closure = model.closure
    device = torch.device("cpu")
    model = model.to(device)
    prepare_batch = model.prepare_batch

    # classification label: target_shape specifies max label
    if isinstance(target_shape, int):
        label = np.asarray([np.random.randint(target_shape) for i in range(
            10)])
    else:
        label = np.random.rand(10, *target_shape) * max_range

    data_dict = {
        "data": np.random.rand(10, *input_shape),
        "label": label
    }

    try:
        data_dict = prepare_batch(data_dict, device, device)
        closure(model, data_dict, optim, loss_fn, {})
    except Exception as e:
        assert False, "Test for %s not passed: Error: %s" \
                      % (model.__class__.__name__, e)

    end_time = time.time()

    print("Time needed for %s: %.3f" % (model.__class__.__name__, end_time -
                                        start_time))

    del device
    del optim
    del closure
    del prepare_batch
    del model
    try:
        del amp_handle
    except NameError:
        pass
    gc.collect()


if __name__ == '__main__':
    # checks if networks are valid (not if they learn something)
    test_pytorch_model_default()

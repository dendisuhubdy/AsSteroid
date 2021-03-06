import pytest
from torch import nn, optim
from asteroid.engine import optimizers


def optim_mapping():
    mapping_list = [
        (optim.Adam, "adam"),
        (optim.SGD, "sgd"),
        (optim.RMSprop, "rmsprop")
    ]
    return mapping_list


global_model = nn.Sequential(nn.Linear(10, 10),
                             nn.ReLU())


@pytest.mark.parametrize("opt_tuple", optim_mapping())
def test_get_str_returns_instance(opt_tuple):
    torch_optim = opt_tuple[0](global_model.parameters(), lr=1e-3)
    asteroid_optim = optimizers.get(opt_tuple[1])(global_model.parameters(),
                                                  lr=1e-3)
    assert type(torch_optim) == type(asteroid_optim)
    assert torch_optim.param_groups == asteroid_optim.param_groups


@pytest.mark.parametrize("opt", [optim.Adam, optim.SGD, optim.Adadelta])
def test_get_instance_returns_instance(opt):
    torch_optim = opt(global_model.parameters(), lr=1e-3)
    asteroid_optim = optimizers.get(torch_optim)
    assert torch_optim == asteroid_optim


@pytest.mark.parametrize("wrong", ["wrong_string", 12, object()])
def test_get_errors(wrong):
    with pytest.raises(ValueError):
        # Should raise for anything not a Optimizer instance + unknown string
        optimizers.get(wrong)


def test_get_none():
    assert optimizers.get(None) is None


def test_make_optimizer():
    optimizers.make_optimizer(global_model.parameters(), "adam", lr=1e-3)
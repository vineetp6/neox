import fairscale
import torch
from labml import monit
from torch import nn

from neox.evaluation import run_eval_harness
from neox.utils import load_layers

if __name__ == '__main__':
    layers = load_layers(None)

    with monit.section('Sequential'):
        model = nn.Sequential(*layers)

    with monit.section('Pipe'):
        n_layers = len(layers)
        n_gpus = 2
        balance = []
        devices = [torch.device(f'cuda:{i}') for i in range(n_gpus)]
        for i in range(n_gpus):
            balance.append((n_layers - sum(balance)) // (n_gpus - i))
        pipe_model = fairscale.nn.Pipe(model,
                                       balance=balance,
                                       devices=devices,
                                       chunks=4)

    print(run_eval_harness(model, 'pipeline_parallel', [], torch.device('cuda:0')))

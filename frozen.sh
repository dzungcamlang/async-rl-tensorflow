#!/bin/sh

# DQN
CUDA_VISIBLE_DEVICES="" python main.py --network_header_type=mlp --network_output_type=normal --observation_dims='[64]' --env_name=FrozenLake8x8-v0 --t_learn_start=0.1 --learning_rate_decay_step=0.1 --history_length=1 --n_action_repeat=1 --t_ep_end=60 --display=True --use_gpu=False &

# dueling DQN
CUDA_VISIBLE_DEVICES="" python main.py --network_header_type=mlp --network_output_type=dueling --observation_dims='[64]' --env_name=FrozenLake8x8-v0 --t_learn_start=0.1 --learning_rate_decay_step=0.1 --history_length=1 --n_action_repeat=1 --t_ep_end=60 --display=True --use_gpu=False &

# DDQN
CUDA_VISIBLE_DEVICES="" python main.py --network_header_type=mlp --network_output_type=normal --double_q=True --observation_dims='[64]' --env_name=FrozenLake8x8-v0 --t_learn_start=0.1 --learning_rate_decay_step=0.1 --history_length=1 --n_action_repeat=1 --t_ep_end=60 --display=True --use_gpu=False &

# Dueling DDQN
CUDA_VISIBLE_DEVICES="" python main.py --network_header_type=mlp --network_output_type=dueling --double_q=True --observation_dims='[64]' --env_name=FrozenLake8x8-v0 --t_learn_start=0.1 --learning_rate_decay_step=0.1 --history_length=1 --n_action_repeat=1 --t_ep_end=60 --display=True --use_gpu=False &

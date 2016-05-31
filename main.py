import gym
import random
import logging
import multiprocessing
import tensorflow as tf

from worker import Worker
from environment import Environment

flags = tf.app.flags

# Deep q Network
flags.DEFINE_string('data_format', 'NHWC', 'The format of convolutional filter')
flags.DEFINE_string('ep_start', 1., 'The value of epsilon at start in e-greedy')
flags.DEFINE_string('ep_end', 0.1, 'The value of epsilnon at the end in e-greedy')
flags.DEFINE_string('ep_end_t', 1000000, 'The time t when epsilon reach ep_end')

# Environment
flags.DEFINE_string('env_name', 'Breakout-v0', 'The name of gym environment to use')
flags.DEFINE_integer('n_action_repeat', 4, 'The number of actions to repeat')
flags.DEFINE_integer('max_random_start', 30, 'The maximum number of NOOP actions at the beginning of an episode')
flags.DEFINE_integer('screen_height', 84, 'The height of gym screen')
flags.DEFINE_integer('screen_width', 84, 'The width of gym screen')
flags.DEFINE_integer('history_length', 4, 'The length of history of screens to use as an input to DQN')
flags.DEFINE_integer('max_reward', +1, 'The maximum value of clipped reward')
flags.DEFINE_integer('min_reward', -1, 'The minimum value of clipped reward')

# Training
flags.DEFINE_boolean('is_train', True, 'Whether to do training or testing')
flags.DEFINE_float('learning_rate', 7e-4, 'The learning rate of training')
flags.DEFINE_float('decay', 0.99, 'Decay of RMSProp optimizer')
flags.DEFINE_float('epsilon', 0.1, 'Epsilon of RMSProp optimizer')
flags.DEFINE_float('momentum', 0.0, 'Momentum of RMSProp optimizer')
flags.DEFINE_float('gamma', 0.99, 'Discount factor of return')
flags.DEFINE_float('beta', 0.0, 'Beta of RMSProp optimizer')
flags.DEFINE_integer('t_max', 5, 'The maximum number of t while training')
flags.DEFINE_integer('n_worker', 1, 'The number of workers to run asynchronously')

# Debug
flags.DEFINE_boolean('display', False, 'Whether to do display the game screen or not')
flags.DEFINE_string('log_level', 'INFO', 'Log level [DEBUG, INFO, WARNING, ERROR, CRITICAL]')
flags.DEFINE_integer('random_seed', 123, 'Value of random seed')

config = flags.FLAGS

logger = logging.getLogger()
logger.propagate = False

logger.setLevel(config.log_level)

# set random seed
tf.set_random_seed(config.random_seed)
random.seed(config.random_seed)

bal_t = 0
should_stop = False

def get_environment(config):
  return Environment(config.env_id, config.history_length, config.screen_height, config.screen_width,
                     config.action_repeat, config.max_random_start, use_cpu=True)

def main(_):
  with tf.Session() as sess:
    def worker_func():
      pass

    # Prepare each workers to run asynchronously
    workers = []
    for idx in range(config.n_worker):
      workers.append(Thread(target=worker_func, args=(idx,)))

    # Execute and wait for the end of the training
    for worker in workers:
      worker.start()

    for worker in workers:
      worker.join()

if __name__ == '__main__':
  tf.app.run()

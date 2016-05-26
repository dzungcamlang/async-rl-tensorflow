import tensorflow as tf

from .ops import conv2d, linear, batch_sample

class DeepQNetwork(object):
  def __init__(self, data_format, history_length,
               screen_height, screen_width,
               action_size, activation_fn=tf.nn.relu,
               initializer=tf.truncated_normal_initializer(0, 0.02), 
               gamma=0.01, beta=0.0, name=None):
    if data_format == 'NHWC':
      self.s_t = tf.placeholder('float32',
          [None, screen_width, screen_height, history_length], name='s_t')
    else:
      self.s_t = tf.placeholder('float32',
          [None, history_length, screen_width, screen_height], name='s_t')

    with tf.variable_scope('Nature_DQN'):
      self.w = {}

      self.l0 = tf.div(self.s_t, 255.)
      self.l1, self.w['l1_w'], self.w['l1_b'] = conv2d(self.l0,
          32, [8, 8], [4, 4], initializer, activation_fn, data_format, name='l1_conv')
      self.l2, self.w['l2_w'], self.w['l2_b'] = conv2d(self.l1,
          64, [4, 4], [2, 2], initializer, activation_fn, data_format, name='l2_conv')
      self.l3, self.w['l3_w'], self.w['l3_b'] = conv2d(self.l2,
          64, [3, 3], [1, 1], initializer, activation_fn, data_format, name='l3_conv')

      self.l4, self.w['l4_w'], self.w['l4_b'] = \
          linear(self.l3, 512, activation_fn=activation_fn, name='l4_linear')

    with tf.variable_scope('copy_from_target'):
      self.w_input = {}
      self.w_assign_op = {}

      for name in self.w.keys():
        self.w_input[name] = tf.placeholder('float32', self.w[name].get_shape().as_list(), name=name)
        self.w_assign_op[name] = self.w[name].assign(self.w_input[name])

    with tf.variable_scope('policy'):
      # 512 -> action_size
      self.logits, self.w['p_w'], self.w['p_b'] = linear(self.l4, action_size, name='logits')

      self.policy = tf.nn.softmax(self.logits, name='pi')
      self.log_policy = tf.log(tf.nn.softmax(self.logits))
      self.entropy = -tf.reduce_sum(self.policy * self.log_policy, 1)

      self.pred_action = tf.argmax(self.policy, dimension=1)

      self.sampled_actions = batch_sample(self.policy)
      self.log_policy_from_sampled_actions = tf.gather(self.log_policy, self.sampled_actions)

    with tf.variable_scope('value'):
      # 512 -> 1
      self.value, self.w['q_w'], self.w['q_b'] = linear(self.l4, 1, name='V')

    with tf.variable_scope('optim'):
      self.R = tf.placeholder('float32', [None], name='target_reward')

      with tf.variable_scope('policy'):
        self.action = tf.placeholder('int64', [None], name='action')

        action_one_hot = tf.one_hot(self.action, action_size, 1.0, 0.0, name='action_one_hot')
        self.policy_loss = tf.reduce_sum(self.log_policy * action_one_hot, 1) \
            * (self.R - self.value + beta * self.entropy)

      with tf.variable_scope('value'):
        self.value_loss = tf.pow(self.R - self.value, 2)

      self.total_loss = self.policy_loss + self.value_loss

  def calc_policy_value(self, s_t):
    return self.sess.run([self.policy, self.value], {self.s_t: s_t})

  def calc_policy(self, s_t):
    return self.policy.eval({self.s_t: s_t})

  def calc_value(self, s_t):
    return self.value.eval({self.s_t: s_t})

  def copy_w_from(self, target_model):
    for name in self.w.keys():
      self.w_assign_op[name].eval({self.w_input[name]: target_model.w[name].eval()})

  @property
  def variables(self):
    return self.w.items()

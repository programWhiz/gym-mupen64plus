import os
import yaml
import abc
import inspect

from gym import spaces

from gym_mupen64plus.envs.mupen64plus_env import Mupen64PlusEnv


class Mario64_Env(Mupen64PlusEnv):
    __metaclass__ = abc.ABCMeta

    def __init__(self, save_state=None):
        self.save_state = None
        if save_state:
            self.save_state = os.path.join(self._saves_dir(), save_state)

        super().__init__()

        self.action_space = spaces.MultiDiscrete([[-80, 80], # Joystick X-axis
                                                  [-80, 80], # Joystick Y-axis
                                                  [  0,  1], # A Button
                                                  [  0,  1], # B Button
                                                  [  0,  1], # RB Button
                                                  [  0,  1], # LB Button
                                                  [  0,  1], # Z Button
                                                  [  0,  1], # C Right Button
                                                  [  0,  1], # C Left Button
                                                  [  0,  1], # C Down Button
                                                  [  0,  1], # C Up Button
                                                  [  0,  0], # D-Pad Right Button
                                                  [  0,  0], # D-Pad Left Button
                                                  [  0,  0], # D-Pad Down Button
                                                  [  0,  0], # D-Pad Up Button
                                                  [  0,  0], # Start Button
                                                  ])

    def _get_save_state(self):
        return self.save_state

    def _load_config(self):
        dirname = os.path.dirname(inspect.stack()[0][1])
        config_path = os.path.join(dirname, "mario64_config.yml")
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)
        self.config.update(config)

    def _validate_config(self):
        pass

    def _navigate_menu(self):
        pass

    def _get_reward(self):
        return 0

    def _evaluate_end_state(self):
        return False

    def _reset(self):
        save_state = self._get_save_state()
        # self._load_save_state(save_state)

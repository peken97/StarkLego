import gym
from gym import spaces as _spaces
import numpy as _np
from StarkLego.lego_builders.model.blocks import TwoXTwoBlock
from StarkLego.lego_builders.service.builder import LegoWorld
from ldraw.pieces import Group, Piece
from StarkLego.analytics.tools import AgentPerformanceTracker

class LegoEnv(gym.Env):

	def __init__(self, x, y, z, noLegoPieces):
		super(LegoEnv, self).__init__()

		self.action_space = _spaces.Box(low=_np.array([0, 0]), high=_np.array([x,z], dtype=_np.int8))
		self.observation_space = _spaces.Box(
            low=0, high=1, shape=(x, y, z), dtype=_np.int8)
		
		self.current_step = 0
		self.reward = noLegoPieces
		self.cumulative_reward = 0;
		self.world = LegoWorld(x, y, z)
		self.number_of_lego_pieces = noLegoPieces
		self.consecutiveWrongChoices = 0
		self.steps_taken = 0
		self.previous_global_maximum = 0
		self.episode_number = 0
		self.episode_number_vs_performance = AgentPerformanceTracker()

		self.LDR_CONTENT = "ldr_content"
		self.CUMULATIVE_REWARD = "cumulative_reward"
		self.EPISODE_NUMBER = "episode_number"

	def _take_action(self, action):
		
		action_x = action[0]
		action_z = action[1]
		
		legoBlock = TwoXTwoBlock()
	
		self.world.add_part_to_world(legoBlock, action_x, action_z)
		return self.world.y_global_max
		

	def _next_observation(self):
		self.current_step += 1
		return self.world.content

	def step(self, action):
		done=False
		reward = 0
		
		try:
			global_maximum = self._take_action(action)
			if self.previous_global_maximum >= global_maximum:
				reward = 10
			else:
				self.previous_global_maximum = global_maximum
				reward = -10
		except:
			reward = -10

		self.steps_taken += 1
		self.cumulative_reward += reward
		
		if self.steps_taken >= self.number_of_lego_pieces:
			done = True
			done == True
			self.episode_number += 1
			self.episode_number_vs_performance.append(self.episode_number, self.cumulative_reward)

		obs = self._next_observation()
		return obs, reward, done, self.generate_info()

	def generate_info(self):
		return {
			self.LDR_CONTENT: self.world.ldraw_content,
			self.CUMULATIVE_REWARD: self.cumulative_reward,
			self.EPISODE_NUMBER: self.episode_number
		}

	def find_maximum_possible_reward(self):
		y = self.world.world_dimensions.y
		return y

	def reset(self):
		self.reward = 0
		self.world.reset()
		self.current_step = 0
		self.steps_taken = 0
		self.previous_global_maximum = 0
		self.cumulative_reward = 0


		return self.world.content

	def render(self, mode='human', close=False):
		print(self.world.ldraw_content)

	def plot_results(self):
		self.episode_number_vs_performance.plot()
		

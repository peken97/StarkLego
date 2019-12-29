from StarkLego.environments.env_low_height import LegoEnv
from stable_baselines.common.policies import MlpPolicy
from stable_baselines.common.vec_env import DummyVecEnv
from stable_baselines import PPO2
import numpy as np


env = DummyVecEnv([lambda: LegoEnv(4, 14, 4, 5)])

model = PPO2(MlpPolicy, env, verbose=1, learning_rate=0.0001, gamma=1)
#obs = env.reset()
#model.set_env(env)
#del model
#model = PPO2.load("training_model", env)
model.learn(total_timesteps=3000000)

#model.save("training_model")
obs = env.reset()

print("Done training")

for i in range(4):
    action, _states = model.predict(obs, deterministic=True)
    obs, rewards, done, info = env.step(action)
    print(rewards)
    env.render()
import gym
import numpy as np

import sys

sys.path.insert(0, "./")
import agents


def main():
    # env = gym.make('LunarLanderContinuous-v2')
    env = gym.make('LunarLander-v2')

    agent = agents.ActorAgent(env)
    # agent = agents.KeyboardAgent(env)
    i = 0
    while True:
    # while i < 1000:
        i += 1
        current_state = env.reset()
        done = False
        steps = 0
        while not done:
            steps += 1
            env.render()

            action = agent.get_action(current_state)
            observation, reward, done, info = env.step(action)

            agent.remember(current_state, action, observation, reward, done)

            current_state = observation

        agent.train()
        # print(observation, action, reward)
        print('end session {}, steps: {}, reward: {}, '.format(i, steps, reward))


if __name__ == '__main__':
    main()

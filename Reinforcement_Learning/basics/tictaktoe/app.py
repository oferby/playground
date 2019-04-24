import sys

sys.path.insert(0, "./")
import agents
import envs


def main():
    env = envs.make()

    agent1 = agents.RandomAgent(env.get_state_space(), env.get_action_space(), name='r1')
    agent2 = agents.RandomAgent(env.get_state_space(), env.get_action_space(), name='r2')
    is_agent1_player = True
    i = 0

    render = True

    while True:
        i += 1
        current_state = env.reset()
        reward = 0
        done = False
        steps = 0

        if render:
            env.render()

        agent = None
        while not done:
            steps += 1

            if is_agent1_player:
                agent = agent1
            else:
                agent = agent2



            is_valid = False
            while not is_valid:
                action = agent.get_action(current_state)
                observation, reward, done, info = env.step(action)
                is_valid = 'valid' in info

            if render:
                env.render()

            agent.observe(observation, reward, done)

            if done:
                if is_agent1_player:
                    agent2.observe(observation, -reward, done)
                else:
                    agent1.observe(observation, -reward, done)

            current_state = observation
            is_agent1_player = not is_agent1_player

        print('end session {}, steps: {}, reward: {}, '.format(i, steps, reward))


if __name__ == '__main__':
    main()

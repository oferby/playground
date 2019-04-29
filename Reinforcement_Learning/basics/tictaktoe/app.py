import sys

sys.path.insert(0, "./")
import agents
import envs


def main():
    env = envs.make()

    agent1 = agents.RandomAgent(env.get_state_space(), env.get_action_space(), name='r1')
    # agent1 = agents.MCTS(env.get_state_space(), env.get_action_space(), name='Agent1')
    agent2 = agents.MCTS(env.get_state_space(), env.get_action_space(), name='Agent2')
    i = 0
    agent1_wins = 0
    agent2_wins = 0
    render = True

    while True:
        is_agent1_player = True
        i += 1
        current_state = env.reset()
        reward = 0
        done = False
        steps = 0

        if render:
            env.render()

        agent = None
        other_agent = None

        while not done:
            steps += 1

            if is_agent1_player:
                agent = agent1
                other_agent = agent2
            else:
                agent = agent2
                other_agent = agent1

            is_valid = False
            while not is_valid:
                action = agent.get_action(current_state)
                observation, reward, done, info = env.step(action)
                is_valid = 'valid' in info
                if not is_valid:
                    pass

            if render:
                env.render()



            if done:
                agent.observe(observation, reward, done)
                other_agent.observe(observation, -reward, done)
                if reward != 0:
                    if agent == agent1:
                        agent1_wins += 1
                    else:
                        agent2_wins += 1
            else:
                other_agent.observe(observation, reward, done)

            current_state = observation
            is_agent1_player = not is_agent1_player

        print('end session {}, steps: {}, reward: {}, agent1 wins: {}, agent2 wins: {}'.format(i, steps, reward, agent1_wins, agent2_wins))


if __name__ == '__main__':
    main()

import abc
import sys
import numpy as np


class AbstractAgent:

    def __init__(self, state_space, action_space, name=None):
        self.state_space = state_space
        self.action_space = action_space
        self.name = name

    @abc.abstractmethod
    def get_action(self, state):
        pass

    @abc.abstractmethod
    def observe(self, observation, reward, done):
        pass


class RandomAgent(AbstractAgent):

    def get_action(self, state):
        return np.random.randint(0, self.action_space)

    def observe(self, observation, reward, done):
        if done:
            print('{} my reward: {}'.format(self.name, reward))


class Node:
    def __init__(self, state, is_terminal=False):
        self.state = state
        self.edges = []
        self.is_terminal = is_terminal
        self.visited = 0


class Edge:
    def __init__(self, parent, child):
        self.parent = parent
        self.child = child
        self.value = -sys.maxsize


class Action:
    def __init__(self, action):
        self.action = action
        self.edges = []
        self.selected = 1


class MCTS(AbstractAgent):

    def __init__(self, state_space, action_space, name=None):
        name = 'MCTS' if name is None else name
        super(MCTS, self).__init__(state_space, action_space, name=name)

        self.mc_tree = {}
        # UCT constant
        self.C = 0.1

        self.memory = []
        self.step = 0

        self.last_state = None
        self.last_action = None

    def get_action(self, state):
        self.step += 1

        self.last_state = self.decode(state)

        if self.last_state not in self.mc_tree:
            node = Node(self.last_state)
            self.mc_tree[self.last_state] = node
        else:
            node = self.mc_tree[self.last_state]

        self.last_action = self.select_action(node)
        return self.last_action

    def decode(self, state):
        return str(state)

    def select_action(self, node):

        # check if all actions visited
        if len(node.edges) != self.action_space:
            self.last_action = self._get_default_action(node)
        else:
            self.last_action = self._select_action(node)

        self._add_action_to_tree(node, self.last_action)
        return self.last_action

    def _select_action(self, node):
        # calculate UCB1
        actions = [None] * self.action_space
        for edge in node.edges:
            value = edge.value + np.sqrt((2 * np.log(node.visited)) / edge.child.selected)
            actions[edge.child.action] = value

        action =  np.argmax(actions)
        print('visited: {}, action: {}, actions: {}'.format(node.visited, action, actions))

        max_value = actions[action]

        indexes = [i for i, x in enumerate(actions) if x == max_value]

        if len(indexes) > 1:
            r = np.random.randint(0, len(indexes))
            return indexes[r]

        return action

    def _get_default_action(self, node):

        actions = []
        for edge in node.edges:
            actions.append(edge.child.action)

        #     remove
        if len(actions) == self.action_space:
            return np.random.randint(0, self.action_space)

        all_actions = range(self.action_space)
        not_visited = np.setdiff1d(all_actions, actions)

        random_action_index = np.random.randint(0, len(not_visited))
        action = not_visited[random_action_index]

        return action

    def _add_action_to_tree(self, node, action):

        self.last_action = action
        actions = {}
        for edge in node.edges:
            actions[edge.child.action] = edge.child

        if self.last_action not in actions:
            action_node = Action(self.last_action)
            edge = Edge(node, action_node)
            node.edges.append(edge)

    def observe(self, observation, reward, done):

        if self.last_state is None:
            return

        observation = self.decode(observation)

        self.memory.append([self.last_state, self.last_action, observation, reward, done])

        node = self.mc_tree[self.last_state]

        for edge in node.edges:
            if edge.value == -sys.maxsize and edge.child.action == self.last_action:
                edge.value = 0

        if observation not in self.mc_tree:
            new_node = Node(observation, done)
            self.mc_tree[observation] = new_node
            for edge in node.edges:
                action_node = edge.child
                if action_node.action == self.last_action:
                    e = Edge(action_node, new_node)
                    action_node.edges.append(e)
                    break

        if done:
            print('MCTS: my reward: {}'.format(reward))
            self.calc_values()

    def calc_values(self):

        i = 0
        state, action, observation, reward, done = self.memory[-1]
        for _ in range(len(self.memory)):
            i += 1
            state, action, observation, _, done = self.memory[-i]

            node = self.mc_tree[state]
            node.visited += 1
            for edge in node.edges:
                if edge.child.action == action:
                    if done:
                        edge.value = reward
                    else:
                        edge.child.selected += 1
                        edge.value = edge.value * (
                                edge.child.selected - 1) / edge.child.selected + reward * 1 / edge.child.selected

                    break

        self.memory.clear()

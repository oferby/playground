from gym import envs

envs = envs.registry.all()

for e in envs:
    print(e)

import dm_alchemy

LEVEL_NAME = ('alchemy/perceptual_mapping_'
              'randomized_with_rotation_and_random_bottleneck')
settings = dm_alchemy.EnvironmentSettings(seed=123, level_name=LEVEL_NAME)
env = dm_alchemy.load_from_docker(settings)
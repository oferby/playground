import tensorflow_datasets as tfds

ds = tfds.load('trivia_qa', split='train')
ds = ds.shuffle().batch(64)

import tensorflow as tf
import tensorflow_hub as hub

# elmo = hub.Module("https://tfhub.dev/google/elmo/2", trainable=True)
elmo = hub.Module("../../data/elmo", trainable=True)

# docs = ["the cat is on the mat", "dogs are in the fog"]

docs = ['Well done!',
        'Good work',
        'Great effort',
        'nice work',
        'Excellent!',
        'Weak',
        'Poor effort!',
        'not good',
        'poor work',
        'Could have done better.',
        'very good',
        'very bad',
        'very nice']

embeddings = elmo(
    docs,
    signature="default",
    as_dict=True)["elmo"]

with tf.Session() as sess:
    sess.run([tf.global_variables_initializer(), tf.tables_initializer()])
    message_embeddings = sess.run(embeddings)


print(message_embeddings)


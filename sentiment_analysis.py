import tensorflow_datasets as tfds
import tensorflow as tf

dataset, info = tfds.load('imdb_reviews/subwords8k', with_info=True, as_supervised=True)
encoder = info.features['text'].encoder  # encoder = reduced dimension representation of a set of words

def pad_to_size(vec, size):
  zeros = [0] * (size - len(vec))
  vec.extend(zeros)
  return vec


def sample_predict(sample_pred_text, pad, model_):
  encoded_sample_pred_text = encoder.encode(sample_pred_text) #from string reprezentation to multi dimensional rep

  if pad:
    encoded_sample_pred_text = pad_to_size(encoded_sample_pred_text, 64)
  encoded_sample_pred_text = tf.cast(encoded_sample_pred_text, tf.float32)
  predictions = model_.predict(tf.expand_dims(encoded_sample_pred_text, 0))

  return predictions


def load_model():
    model = tf.keras.models.load_model('modelSentimentAnalysis.h5')
    return model


def get_prediction(text, model):
    predictions = sample_predict(text, pad=True, model_=model)
    return predictions[0][0]


def main():
    train_dataset, test_dataset = dataset['train'], dataset['test']
    # prepare data for training
    BUFFER_SIZE = 10000
    BATCH_SIZE = 64

    padded_shapes = ([None], ())
    train_dataset = train_dataset.shuffle(BUFFER_SIZE).padded_batch(BATCH_SIZE, padded_shapes=padded_shapes)
    test_dataset = test_dataset.padded_batch(BATCH_SIZE, padded_shapes=padded_shapes)

    # recurrent neural network
    # create the model
    model = tf.keras.Sequential([
        tf.keras.layers.Embedding(encoder.vocab_size, 64),
        tf.keras.layers.Bidirectional(tf.keras.layers.LSTM(64)),
        tf.keras.layers.Dense(64, activation='relu'),
        tf.keras.layers.Dense(1, activation='sigmoid')])

    model.compile(loss='binary_crossentropy',
                  optimizer=tf.keras.optimizers.Adam(1e-4),
                  metrics=['accuracy'])

    history = model.fit(train_dataset, epochs=10, validation_data=test_dataset, validation_steps=30)

    sample_pred_text = ('I had a very good day')
    predictions = sample_predict(sample_pred_text, pad=True, model_=model)
    print(predictions)

    sample_pred_text = ('I had a bad day')
    predictions = sample_predict(sample_pred_text, pad=True, model_=model)
    print(predictions)

    model.save('modelSentimentAnalysis.h5')


if __name__ == '__main__':
    main()




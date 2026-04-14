import tensorflow as tf
import numpy as np
import json
import os

# Ultra lightweight NLP model for Hackathon MVP
# Predicts an overarching "Category ID" which maps to Type + Severity.

# Augmented data for better stability
texts = [
    "smoke fire burning flames", "there is a fire in the building", "it is burning here",
    "help injured person bleeding", "medical emergency heart attack", "someone fainted",
    "theft suspicious activity", "someone stole my bag", "intruder in the lobby"
] * 10
labels = [0, 0, 0, 1, 1, 1, 2, 2, 2] * 10

# Tokenizer setup
vocab_size = 100
max_length = 10

tokenizer = tf.keras.preprocessing.text.Tokenizer(num_words=vocab_size, oov_token="<OOV>")
tokenizer.fit_on_texts(texts)
sequences = tokenizer.texts_to_sequences(texts)
padded_sequences = tf.keras.preprocessing.sequence.pad_sequences(sequences, maxlen=max_length, padding='post')

# Build a Tiny Model
model = tf.keras.Sequential([
    tf.keras.layers.Embedding(vocab_size, 8, input_length=max_length),
    tf.keras.layers.GlobalAveragePooling1D(),
    tf.keras.layers.Dense(8, activation='relu'),
    tf.keras.layers.Dense(3, activation='softmax')
])

model.compile(loss='sparse_categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

print("Training model...")
model.fit(np.array(padded_sequences), np.array(labels), epochs=300, verbose=0)
print("Training complete.")

# Save model and tokenizer word index
model.save('nlp_model.keras')
with open('tokenizer.json', 'w') as f:
    json.dump(tokenizer.word_index, f)

print("Model saved to nlp_model.keras")

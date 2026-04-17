import os
import sys
import json
import numpy as np

# Force CPU usage
os.environ['CUDA_VISIBLE_DEVICES'] = '-1'
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

import tensorflow as tf

# Load generated dataset
with open("training_data.json", "r", encoding="utf-8") as f:
    raw_data = json.load(f)

texts = [item["text"].lower() for item in raw_data]
labels = [item["label"] for item in raw_data]

# Tokenizer setup
vocab_size = 5000
max_length = 50

tokenizer = tf.keras.preprocessing.text.Tokenizer(num_words=vocab_size, oov_token="<OOV>")
tokenizer.fit_on_texts(texts)
sequences = tokenizer.texts_to_sequences(texts)
padded_sequences = tf.keras.preprocessing.sequence.pad_sequences(sequences, maxlen=max_length, padding='post')

# Build a Robust multi-language model (Single Bi-LSTM for speed on CPU)
model = tf.keras.Sequential([
    tf.keras.layers.Embedding(vocab_size, 32, input_shape=(max_length,)),
    tf.keras.layers.Bidirectional(tf.keras.layers.LSTM(32)),
    tf.keras.layers.Dense(16, activation='relu'),
    tf.keras.layers.Dropout(0.2),
    tf.keras.layers.Dense(3, activation='softmax')
])

model.compile(loss='sparse_categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

print(f"Training voice-optimized model on CPU ({len(texts)} samples)...")
model.fit(np.array(padded_sequences), np.array(labels), epochs=40, batch_size=32, verbose=1)
print("Training complete.")

# Save model and tokenizer
model.save('nlp_model.keras')
with open('tokenizer.json', 'w') as f:
    json.dump(tokenizer.word_index, f)

print("Voice-optimized model saved to nlp_model.keras")

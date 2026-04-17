import os
import sys
import json
import numpy as np
import tensorflow as tf

# GPU Support: Link NVIDIA libraries installed in venv
VENV_PATH = os.path.join(os.getcwd(), "venv/lib/python3.12/site-packages/nvidia")
LIB_PATHS = [
    os.path.join(VENV_PATH, "cudnn/lib"),
    os.path.join(VENV_PATH, "cublas/lib"),
    os.path.join(VENV_PATH, "cuda_nvrtc/lib"),
    os.path.join(VENV_PATH, "cuda_runtime/lib")
]
os.environ['LD_LIBRARY_PATH'] = ":".join(LIB_PATHS) + ":" + os.environ.get('LD_LIBRARY_PATH', '')

# Link libdevice for the XLA/JIT compiler
NVCC_PATH = os.path.join(VENV_PATH, "cuda_nvcc")
os.environ['XLA_FLAGS'] = f"--xla_gpu_cuda_data_dir={NVCC_PATH}"
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

# Re-enable JIT for full GPU performance
tf.config.optimizer.set_jit(True)

# Verify GPU
print("Num GPUs Available: ", len(tf.config.list_physical_devices('GPU')))

# Load massive generated dataset
with open("training_data.json", "r", encoding="utf-8") as f:
    raw_data = json.load(f)

texts = [item["text"].lower() for item in raw_data]
labels = [item["label"] for item in raw_data]

# Tokenizer setup (Increased for Accuracy Overhaul)
vocab_size = 8000
max_length = 64

tokenizer = tf.keras.preprocessing.text.Tokenizer(num_words=vocab_size, oov_token="<OOV>")
tokenizer.fit_on_texts(texts)
sequences = tokenizer.texts_to_sequences(texts)
padded_sequences = tf.keras.preprocessing.sequence.pad_sequences(sequences, maxlen=max_length, padding='post')

# Build a Deeper robust model (Stacked Bidirectional LSTMs)
model = tf.keras.Sequential([
    tf.keras.layers.Embedding(vocab_size, 128, input_shape=(max_length,)),
    tf.keras.layers.Bidirectional(tf.keras.layers.LSTM(128, return_sequences=True)),
    tf.keras.layers.Bidirectional(tf.keras.layers.LSTM(64)),
    tf.keras.layers.Dense(64, activation='relu'),
    tf.keras.layers.Dropout(0.3),
    tf.keras.layers.Dense(3, activation='softmax')
])

model.compile(loss='sparse_categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

print(f"Training deep Accuracy Overhaul model on GPU ({len(texts)} samples)...")
model.fit(np.array(padded_sequences), np.array(labels), epochs=60, batch_size=32, verbose=1)
print("Training complete.")

# Save model and tokenizer word index
model.save('nlp_model.keras')
with open('tokenizer.json', 'w') as f:
    json.dump(tokenizer.word_index, f)

print("Accuracy Overhaul model saved to nlp_model.keras")

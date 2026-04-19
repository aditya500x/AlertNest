import os
import json
import numpy as np
import tensorflow as tf

# Standard hardware config from train_model.py
VENV_PATH = os.path.join(os.getcwd(), "venv/lib/python3.12/site-packages/nvidia")
LIB_PATHS = [
    os.path.join(VENV_PATH, "cudnn/lib"),
    os.path.join(VENV_PATH, "cublas/lib"),
    os.path.join(VENV_PATH, "cuda_nvrtc/lib"),
    os.path.join(VENV_PATH, "cuda_runtime/lib")
]
os.environ['LD_LIBRARY_PATH'] = ":".join(LIB_PATHS) + ":" + os.environ.get('LD_LIBRARY_PATH', '')
NVCC_PATH = os.path.join(VENV_PATH, "cuda_nvcc")
os.environ['XLA_FLAGS'] = f"--xla_gpu_cuda_data_dir={NVCC_PATH}"
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

tf.config.optimizer.set_jit(True)

def preprocess_and_build():
    print("Loading EPE dataset and Tokenizer...")
    with open("epe_training_data.json", "r", encoding="utf-8") as f:
        data = json.load(f)
        
    with open("tokenizer.json", "r", encoding="utf-8") as f:
        word_index = json.load(f)

    # PREPARE INPUTS
    texts = [item["text"].lower() for item in data]
    meta_features = [[
        item["nlp_category"],
        item["severity"],
        item["people_affected"],
        item["people_at_risk"],
        item["time_reported_mins"]
    ] for item in data]
    targets = [item["priority_score"] for item in data]

    # NLP preprocessing using existing vocabulary size (match train_model.py)
    vocab_size = 8000
    max_length = 64
    
    tokenizer = tf.keras.preprocessing.text.Tokenizer(num_words=vocab_size, oov_token="<OOV>")
    # Directly mapping the pre-trained word index
    tokenizer.word_index = word_index
    sequences = tokenizer.texts_to_sequences(texts)
    text_inputs = tf.keras.preprocessing.sequence.pad_sequences(sequences, maxlen=max_length, padding='post')

    meta_inputs = np.array(meta_features, dtype=np.float32)
    targets = np.array(targets, dtype=np.float32)

    # BUILDING THE DUAL-INPUT ARCHITECTURE
    text_in = tf.keras.layers.Input(shape=(max_length,), name="text_input")
    meta_in = tf.keras.layers.Input(shape=(5,), name="meta_input")
    
    # Branch 1: NLP
    x1 = tf.keras.layers.Embedding(vocab_size, 64)(text_in)
    x1 = tf.keras.layers.Bidirectional(tf.keras.layers.LSTM(32))(x1)
    x1 = tf.keras.layers.Dense(32, activation="relu")(x1)
    
    # Branch 2: Meta metrics (Severity, Category, People stats)
    x2 = tf.keras.layers.Dense(32, activation="relu")(meta_in)
    x2 = tf.keras.layers.BatchNormalization()(x2)
    
    # Merge streams
    combined = tf.keras.layers.concatenate([x1, x2])
    z = tf.keras.layers.Dense(64, activation="relu")(combined)
    z = tf.keras.layers.Dropout(0.3)(z)
    z = tf.keras.layers.Dense(32, activation="relu")(z)
    
    # Predict Priority Score across output dimension
    output = tf.keras.layers.Dense(1, activation="sigmoid", name="priority_output")(z)
    
    model = tf.keras.Model(inputs=[text_in, meta_in], outputs=output)
    model.compile(loss='mse', optimizer='adam', metrics=['mae'])
    
    print("\nEPE Core Model Architecture Created!")
    model.summary()
    
    return model, text_inputs, meta_inputs, targets

def main():
    model, text_inputs, meta_inputs, targets = preprocess_and_build()
    
    print("\n=== STARTING EPE TRAINING ON GPU ===")
    print("The model is ready to train on dual input vectors:")
    print(f"Text Input Layout: {text_inputs.shape}")
    print(f"Meta Input Layout: {meta_inputs.shape}")
    
    # Train the model
    model.fit(
        [text_inputs, meta_inputs], targets,
        epochs=30,
        batch_size=32,
        validation_split=0.1,
        verbose=1
    )
    
    # Save the output
    model.save("epe_model.keras")
    print("Saved dual-input ranking model to epe_model.keras")

if __name__ == "__main__":
    main()

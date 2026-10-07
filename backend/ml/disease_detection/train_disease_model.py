"""
Plant Disease Detection CNN Training Pipeline
Compatible with the PlantVillage Dataset (Tomato, Potato, Rice)

Target Disease Classes:
0: Healthy leaf
1: Potato Early Blight
2: Potato Late Blight
3: Rice Leaf Blast
4: Tomato Early Blight
5: Tomato Late Blight
6: Tomato Leaf Mold

Instructions:
1. Download PlantVillage dataset or place your plant disease images in:
   datasets/plant_village/<class_name>/
2. Run this script:
   python backend/ml/disease_detection/train_disease_model.py
"""

import os
import sys

# Disease Classes
DISEASE_CLASSES = [
    "Healthy leaf",
    "Potato Early Blight",
    "Potato Late Blight",
    "Rice Leaf Blast",
    "Tomato Early Blight",
    "Tomato Late Blight",
    "Tomato Leaf Mold"
]

def build_cnn_model(input_shape=(224, 224, 3), num_classes=len(DISEASE_CLASSES)):
    """Constructs a Convolutional Neural Network for plant disease classification."""
    try:
        import tensorflow as tf
        from tensorflow.keras import layers, models
    except ImportError:
        print("[ERROR] TensorFlow is required to train the CNN model. Install via: pip install tensorflow")
        sys.exit(1)

    model = models.Sequential([
        # Block 1
        layers.Input(shape=input_shape),
        layers.Conv2D(32, (3, 3), activation="relu", padding="same"),
        layers.BatchNormalization(),
        layers.MaxPooling2D((2, 2)),

        # Block 2
        layers.Conv2D(64, (3, 3), activation="relu", padding="same"),
        layers.BatchNormalization(),
        layers.MaxPooling2D((2, 2)),

        # Block 3
        layers.Conv2D(128, (3, 3), activation="relu", padding="same"),
        layers.BatchNormalization(),
        layers.MaxPooling2D((2, 2)),

        # Block 4
        layers.Conv2D(256, (3, 3), activation="relu", padding="same"),
        layers.BatchNormalization(),
        layers.MaxPooling2D((2, 2)),

        # Classification Head
        layers.GlobalAveragePooling2D(),
        layers.Dense(256, activation="relu"),
        layers.Dropout(0.5),
        layers.Dense(num_classes, activation="softmax")
    ])

    model.compile(
        optimizer=tf.keras.optimizers.Adam(learning_rate=1e-4),
        loss="sparse_categorical_crossentropy",
        metrics=["accuracy"]
    )

    return model

def train(data_dir=None, epochs=15, batch_size=32):
    """Executes dataset loading and CNN model training."""
    import tensorflow as tf
    from tensorflow.keras.callbacks import ModelCheckpoint, EarlyStopping

    current_dir = os.path.dirname(os.path.abspath(__file__))
    model_save_path = os.path.join(current_dir, "disease_model.keras")

    if not data_dir or not os.path.exists(data_dir):
        print(f"[INFO] Dataset directory '{data_dir}' not found.")
        print("[INFO] To train on your custom dataset, organize folders as:")
        print("       datasets/plant_village/<class_name>/*.jpg")
        print("[INFO] Example classes supported:")
        for c in DISEASE_CLASSES:
            print(f"       - {c}")
        return

    print(f"[TRAIN] Loading dataset from: {data_dir}")
    train_ds = tf.keras.utils.image_dataset_from_directory(
        data_dir,
        validation_split=0.2,
        subset="training",
        seed=42,
        image_size=(224, 224),
        batch_size=batch_size
    )

    val_ds = tf.keras.utils.image_dataset_from_directory(
        data_dir,
        validation_split=0.2,
        subset="validation",
        seed=42,
        image_size=(224, 224),
        batch_size=batch_size
    )

    # Normalize pixels to [0, 1]
    rescale_layer = tf.keras.layers.Rescaling(1./255)
    train_ds = train_ds.map(lambda x, y: (rescale_layer(x), y))
    val_ds = val_ds.map(lambda x, y: (rescale_layer(x), y))

    model = build_cnn_model()
    model.summary()

    callbacks = [
        ModelCheckpoint(model_save_path, save_best_only=True, monitor="val_accuracy"),
        EarlyStopping(patience=4, restore_best_weights=True)
    ]

    print("[TRAIN] Starting CNN model training...")
    history = model.fit(
        train_ds,
        validation_data=val_ds,
        epochs=epochs,
        callbacks=callbacks
    )

    print(f"[SUCCESS] Trained disease detection model saved to: {model_save_path}")

if __name__ == "__main__":
    current_dir = os.path.dirname(os.path.abspath(__file__))
    default_dataset = os.path.abspath(os.path.join(current_dir, "..", "..", "..", "datasets", "plant_village"))
    train(default_dataset)

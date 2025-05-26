from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D
from tensorflow.keras.optimizers import Adam
import os

# Paths
DATASET_DIR = "pokedex_dataset_ready"
MODEL_FILE = "pokedex_model.h5"
CLASS_FILE = "class_names.txt"

# Image settings
IMG_SIZE = (160, 160)
BATCH_SIZE = 32
EPOCHS = 10

# Data generator
datagen = ImageDataGenerator(
    rescale=1./255,
    validation_split=0.2
)

train_gen = datagen.flow_from_directory(
    DATASET_DIR,
    target_size=IMG_SIZE,
    batch_size=BATCH_SIZE,
    subset="training",
    class_mode="categorical"
)

val_gen = datagen.flow_from_directory(
    DATASET_DIR,
    target_size=IMG_SIZE,
    batch_size=BATCH_SIZE,
    subset="validation",
    class_mode="categorical"
)

# Save class names
class_names = list(train_gen.class_indices.keys())
with open(CLASS_FILE, "w") as f:
    for name in class_names:
        f.write(name + "\n")

# Build model
base_model = MobileNetV2(weights='imagenet', include_top=False, input_shape=(160, 160, 3))
base_model.trainable = False  # Transfer learning

model = Sequential([
    base_model,
    GlobalAveragePooling2D(),
    Dense(len(class_names), activation="softmax")
])

model.compile(optimizer=Adam(learning_rate=0.0005),
              loss="categorical_crossentropy",
              metrics=["accuracy"])

# Train
model.fit(train_gen, validation_data=val_gen, epochs=EPOCHS)

# Save
model.save(MODEL_FILE)
print("✅ Model saved as pokedex_model.h5")
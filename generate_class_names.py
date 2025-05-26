from tensorflow.keras.preprocessing.image import ImageDataGenerator

DATASET_DIR = "pokedex_dataset_ready"
CLASS_FILE = "class_names.txt"
IMG_SIZE = (160, 160)
BATCH_SIZE = 32

datagen = ImageDataGenerator(
    rescale=1./255,
    validation_split=0.2,
)

train_gen = datagen.flow_from_directory(
    DATASET_DIR,
    target_size=IMG_SIZE,
    batch_size=BATCH_SIZE,
    subset="training",
    class_mode="categorical"
)

# Print the class indices for verification
print("CLASS INDICES:", train_gen.class_indices)

class_names = list(train_gen.class_indices.keys())
with open(CLASS_FILE, "w") as f:
    for name in class_names:
        f.write(name + "\n")

print("✅ class_names.txt regenerated! Order matches model output indices.") 
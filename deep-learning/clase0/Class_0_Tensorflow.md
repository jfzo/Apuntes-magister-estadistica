---
title: EST-744
subtitle: Workshop Tensorflow
author: Juan Zamora O.
date: Deep Learning
fonttheme: "professionalfonts"
fontsize: 11pt
theme: default
innertheme: circles
urlcolor: blue
linkstyle: bold
aspectratio: 169
titlegraphic: logosAzul.png
logo: logoAzul.png
section-titles: false
toc: false
toc-depth: 1
toc-title: Estructura de la Presentación
---

# Introduction & Setup

## Workshop Objectives (90 minutes)

By the end of this workshop, you will:

- Build neural networks using **all three Keras APIs**
- Know when to use Sequential, Functional, or Model Subclassing
- Train models and interpret results
- Debug and improve model performance
- Deploy models for inference


\vspace{0.2cm}

**Three ways to build a model in Keras**:

```
Sequential    → simple, linear pipelines
Functional    → branching, multi-input/output architectures
Subclassing   → fully custom, research-grade control
```


## Environment Setup

### Check Your Installation

```python
import tensorflow as tf
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

print(f"TensorFlow version: {tf.__version__}")
print(f"Keras version: {tf.keras.__version__}")

# GPU check (optional)
print(f"GPU available: {len(tf.config.list_physical_devices('GPU')) > 0}")
```

**If missing packages:**
```bash
pip install tensorflow numpy pandas matplotlib scikit-learn
```


# Part 1: Keras Basics (0:00 - 0:15)

## Topic 1.1: Sequential API (The Simple Way)

**Concept**: Stack layers in order (input → hidden → output)

### Code Block 1.1a: Create a Simple Network

```python
from tensorflow import keras
from tensorflow.keras import layers

# Method 1: Sequential API (simplest)
model = keras.Sequential([
    layers.Dense(64, activation='relu', input_shape=(10,)),
    layers.Dense(32, activation='relu'),
    layers.Dense(1, activation='sigmoid')
])

# Method 2: Add layers incrementally
model = keras.Sequential()
model.add(layers.Dense(64, activation='relu', input_shape=(10,)))
model.add(layers.Dense(32, activation='relu'))
model.add(layers.Dense(1, activation='sigmoid'))

# Print network architecture
model.summary()
```

**Output shows:**
```
Model: "sequential"
_________________________________________________________________
Layer (type)                 Output Shape              Param #   
=================================================================
dense (Dense)               (None, 64)                704       
dense_1 (Dense)             (None, 32)                2080      
dense_2 (Dense)             (None, 1)                 33        
=================================================================
Total params: 2,817
Trainable params: 2,817
Non-trainable params: 0
```

**Interpretation**: 
- First layer: $10 \times 64 + 64 = 704$ parameters
- Second layer: $64 \times 32 + 32 = 2080$ parameters
- Output layer: $32 \times 1 + 1 = 33$ parameters


## Topic 1.2: Compile: Loss, Optimizer, Metrics

**Concept**: Tell the model how to learn and what to measure

### Code Block 1.2a: Compile a Network

```python
model.compile(
    loss='binary_crossentropy',      # What to minimize
    optimizer='adam',                # How to learn
    metrics=['accuracy']             # What to track
)
```

**Common Loss Functions:**
- `binary_crossentropy`: Binary classification (2 classes)
- `categorical_crossentropy`: Multi-class (3+ classes)
- `sparse_categorical_crossentropy`: Multi-class (integer labels)
- `mse`: Regression (continuous values)

**Common Optimizers:**
- `adam`: Adaptive, most popular
- `sgd`: Stochastic gradient descent
- `rmsprop`: Root mean square propagation

**Common Metrics:**
- `accuracy`: Classification accuracy
- `mse`: Mean squared error
- `mae`: Mean absolute error
- `auc`: Area under ROC curve



## Topic 1.3: Train: Fit the Model

**Concept**: Feed data to the model, let it learn

### Code Block 1.3a: Prepare Data

```python
# Generate dummy data for binary classification
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

X, y = make_classification(
    n_samples=1000,      # 1000 examples
    n_features=10,       # 10 input features
    n_classes=2,         # Binary classification
    random_state=42
)

# Split data
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Normalize features (important!)
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

print(f"Training set: {X_train.shape}")
print(f"Test set: {X_test.shape}")
```

### Code Block 1.3b: Train the Model

```python
# Train for 20 epochs, batch size 32
history = model.fit(
    X_train, y_train,
    epochs=20,
    batch_size=32,
    validation_split=0.2,  # Use 20% for validation
    verbose=1              # Show progress
)

# Output:
# Epoch 1/20
# 25/25 [==============================] - 0s 3ms/step
# loss: 0.6895 - accuracy: 0.5125 - val_loss: 0.6932 - val_accuracy: 0.5000
# ...
# Epoch 20/20
# loss: 0.1234 - accuracy: 0.9500 - val_loss: 0.1356 - val_accuracy: 0.9250
```

**Explanation**:
- `epochs=20`: Pass through data 20 times
- `batch_size=32`: Update weights after every 32 samples
- `validation_split=0.2`: Reserve 20% of training data for validation
- `verbose=1`: Print progress (0 = silent, 2 = one line per epoch)



## Topic 1.4: Evaluate: Test the Model

**Concept**: See how well it generalizes to unseen data

### Code Block 1.4a: Evaluate on Test Set

```python
# Get loss and metrics on test data
test_loss, test_accuracy = model.evaluate(X_test, y_test)
print(f"Test loss: {test_loss:.4f}")
print(f"Test accuracy: {test_accuracy:.4f}")

# Make predictions
y_pred_prob = model.predict(X_test[:5])  # Probabilities
y_pred = (y_pred_prob > 0.5).astype(int).flatten()  # Binary predictions

print(f"First 5 predictions: {y_pred}")
print(f"First 5 actual: {y_test[:5]}")
```



## Topic 1.5: Visualize Training

**Concept**: Understand what happened during training

### Code Block 1.5a: Plot Loss and Accuracy

```python
import matplotlib.pyplot as plt

plt.figure(figsize=(12, 4))

# Plot 1: Loss
plt.subplot(1, 2, 1)
plt.plot(history.history['loss'], label='Training Loss')
plt.plot(history.history['val_loss'], label='Validation Loss')
plt.xlabel('Epoch')
plt.ylabel('Loss')
plt.title('Model Loss Over Time')
plt.legend()
plt.grid(True)

# Plot 2: Accuracy
plt.subplot(1, 2, 2)
plt.plot(history.history['accuracy'], label='Training Accuracy')
plt.plot(history.history['val_accuracy'], label='Validation Accuracy')
plt.xlabel('Epoch')
plt.ylabel('Accuracy')
plt.title('Model Accuracy Over Time')
plt.legend()
plt.grid(True)

plt.tight_layout()
plt.show()

# Signs of good training:
# o Loss decreases over time
# o Training and validation curves track together
# x Large gap between training and validation = overfitting
```



# Part 2: Real Dataset Example (0:15 - 0:35)

## Topic 2.1: Iris Dataset (Classification)

**Concept**: Multi-class classification with real data

### Code Block 2.1a: Load and Explore Data

```python
from tensorflow.keras.datasets import fashion_mnist
import numpy as np

# Load Iris dataset
from sklearn.datasets import load_iris
iris = load_iris()

X = iris.data  # 150 samples, 4 features
y = iris.target  # 3 classes (0, 1, 2)

print(f"Features: {X.shape}")
print(f"Classes: {np.unique(y)}")
print(f"Class distribution: {np.bincount(y)}")

# Split and normalize
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# Convert labels to one-hot encoding
y_train_cat = keras.utils.to_categorical(y_train, 3)
y_test_cat = keras.utils.to_categorical(y_test, 3)

print(f"One-hot y_train shape: {y_train_cat.shape}")
```

### Code Block 2.1b: Build Multi-class Classifier

```python
model_iris = keras.Sequential([
    layers.Dense(16, activation='relu', input_shape=(4,)),
    layers.Dense(8, activation='relu'),
    layers.Dense(3, activation='softmax')  # softmax for multi-class
])

model_iris.compile(
    loss='categorical_crossentropy',  # For one-hot labels
    optimizer='adam',
    metrics=['accuracy']
)

# Train
history_iris = model_iris.fit(
    X_train, y_train_cat,
    epochs=50,
    batch_size=8,
    validation_split=0.2,
    verbose=0  # Silent
)

# Evaluate
test_loss, test_acc = model_iris.evaluate(X_test, y_test_cat, verbose=0)
print(f"Test Accuracy: {test_acc:.4f}")

# Predict on new data
predictions = model_iris.predict(X_test[:5])  # Probabilities for each class
predicted_classes = np.argmax(predictions, axis=1)  # Get class with highest prob
print(f"Predictions: {predicted_classes}")
print(f"True labels: {y_test[:5]}")
```



## Topic 2.2: MNIST Digits (Image Classification)

**Concept**: Neural networks on images (preprocessing included)

### Code Block 2.2a: Load and Preprocess MNIST

```python
from tensorflow.keras.datasets import mnist

# Load dataset (auto-downloads ~11 MB)
(X_train, y_train), (X_test, y_test) = mnist.load_data()

print(f"Training images: {X_train.shape}")  # (60000, 28, 28)
print(f"Training labels: {y_train.shape}")  # (60000,)

# Images are 28×28 pixels, flatten to 784
X_train_flat = X_train.reshape(-1, 784).astype('float32') / 255.0
X_test_flat = X_test.reshape(-1, 784).astype('float32') / 255.0

# One-hot encode labels
y_train_cat = keras.utils.to_categorical(y_train, 10)
y_test_cat = keras.utils.to_categorical(y_test, 10)

print(f"Flattened training: {X_train_flat.shape}")
print(f"One-hot labels: {y_train_cat.shape}")
```

### Code Block 2.2b: Build MNIST Classifier

```python
model_mnist = keras.Sequential([
    layers.Dense(128, activation='relu', input_shape=(784,)),
    layers.Dropout(0.2),  # Drop 20% of neurons (regularization)
    layers.Dense(64, activation='relu'),
    layers.Dropout(0.2),
    layers.Dense(10, activation='softmax')
])

model_mnist.compile(
    loss='categorical_crossentropy',
    optimizer='adam',
    metrics=['accuracy']
)

# Train (smaller subset for speed)
history_mnist = model_mnist.fit(
    X_train_flat[:10000], y_train_cat[:10000],
    epochs=10,
    batch_size=128,
    validation_split=0.2,
    verbose=1
)

# Test
test_loss, test_acc = model_mnist.evaluate(X_test_flat, y_test_cat, verbose=0)
print(f"\nTest Accuracy: {test_acc:.4f}")
```

**Expected performance**: ~97% accuracy with simple network



## Topic 2.3: Understand Dropout

**Concept**: Regularization technique to prevent overfitting

### Code Block 2.3a: With vs Without Dropout

```python
# Model WITHOUT dropout
model_no_dropout = keras.Sequential([
    layers.Dense(128, activation='relu', input_shape=(784,)),
    layers.Dense(64, activation='relu'),
    layers.Dense(10, activation='softmax')
])

model_no_dropout.compile(
    loss='categorical_crossentropy',
    optimizer='adam',
    metrics=['accuracy']
)

history_no_dropout = model_no_dropout.fit(
    X_train_flat[:5000], y_train_cat[:5000],
    epochs=10,
    batch_size=128,
    validation_split=0.2,
    verbose=0
)

# Model WITH dropout
model_with_dropout = keras.Sequential([
    layers.Dense(128, activation='relu', input_shape=(784,)),
    layers.Dropout(0.3),
    layers.Dense(64, activation='relu'),
    layers.Dropout(0.3),
    layers.Dense(10, activation='softmax')
])

model_with_dropout.compile(
    loss='categorical_crossentropy',
    optimizer='adam',
    metrics=['accuracy']
)

history_with_dropout = model_with_dropout.fit(
    X_train_flat[:5000], y_train_cat[:5000],
    epochs=10,
    batch_size=128,
    validation_split=0.2,
    verbose=0
)

# Compare
print("\nWithout dropout:")
print(f"Final train accuracy: {history_no_dropout.history['accuracy'][-1]:.4f}")
print(f"Final val accuracy: {history_no_dropout.history['val_accuracy'][-1]:.4f}")

print("\nWith dropout:")
print(f"Final train accuracy: {history_with_dropout.history['accuracy'][-1]:.4f}")
print(f"Final val accuracy: {history_with_dropout.history['val_accuracy'][-1]:.4f}")

# Plot comparison
fig, axes = plt.subplots(1, 2, figsize=(12, 4))

axes[0].plot(history_no_dropout.history['accuracy'], label='Train')
axes[0].plot(history_no_dropout.history['val_accuracy'], label='Val')
axes[0].set_title('Without Dropout')
axes[0].set_ylabel('Accuracy')
axes[0].set_xlabel('Epoch')
axes[0].legend()
axes[0].grid(True)

axes[1].plot(history_with_dropout.history['accuracy'], label='Train')
axes[1].plot(history_with_dropout.history['val_accuracy'], label='Val')
axes[1].set_title('With Dropout')
axes[1].set_ylabel('Accuracy')
axes[1].set_xlabel('Epoch')
axes[1].legend()
axes[1].grid(True)

plt.tight_layout()
plt.show()
```



# Part 3: The Three Keras APIs (0:35 - 1:10)

## The Three Keras APIs: When to Use Each

All three APIs produce fully compatible `keras.Model` objects — same `compile()`, `fit()`, `evaluate()`, `predict()`, `save()`.

| API | Control | Verbosity | Best For |
|---|---|---|---|
| **Sequential** | Low | Minimal | Linear stacks, quick prototyping |
| **Functional** | Medium | Moderate | Multi-input, skip connections, branching |
| **Subclassing** | Full | Verbose | Custom layers, research, dynamic graphs |

\vspace{0.2cm}

**Analogy**: Like Python classes vs functions vs scripts — each has its place.



## Topic 3.1: Functional API (Medium Control)

**Concept**: Build models as a directed graph of layers

### Code Block 3.1a: Functional API — Same Task, More Flexibility

```python
from tensorflow import keras
from tensorflow.keras import layers

# Sequential (familiar)
model_seq = keras.Sequential([
    layers.Dense(64, activation='relu', input_shape=(10,)),
    layers.Dense(32, activation='relu'),
    layers.Dense(1, activation='sigmoid')
])

# Functional (same architecture, explicit data flow)
inputs = keras.Input(shape=(10,))
x = layers.Dense(64, activation='relu')(inputs)
x = layers.Dense(32, activation='relu')(x)
outputs = layers.Dense(1, activation='sigmoid')(x)
model_func = keras.Model(inputs=inputs, outputs=outputs)

# Both compiled and trained identically
model_func.compile(loss='binary_crossentropy', optimizer='adam',
                   metrics=['accuracy'])
model_func.summary()
```

### Code Block 3.1b: Functional API — Multiple Inputs

```python
# Real use case: patient data (numerical) + diagnosis code (categorical)
numerical_input = keras.Input(shape=(5,), name='numerical')
x1 = layers.Dense(32, activation='relu')(numerical_input)

categorical_input = keras.Input(shape=(1,), name='categorical')
x2 = layers.Embedding(input_dim=6, output_dim=4)(categorical_input)
x2 = layers.Flatten()(x2)

merged = layers.Concatenate()([x1, x2])
output = layers.Dense(1, activation='sigmoid')(merged)

model_multi = keras.Model(inputs=[numerical_input, categorical_input],
                          outputs=output)
model_multi.compile(loss='binary_crossentropy', optimizer='adam')

# Feed a list of arrays, one per input
X1 = np.random.randn(200, 5)
X2 = np.random.randint(1, 6, (200, 1))
y  = np.random.randint(0, 2, 200)
model_multi.fit([X1, X2], y, epochs=5, verbose=0)
print('Multi-input model trained!')
```



## Topic 3.2: Model Subclassing (Full Control)

**Concept**: Define a model as a Python class — maximum flexibility for custom behaviour

**When to prefer it**:
- Layers whose behaviour changes between training and inference (e.g. custom dropout)
- Dynamic computation graphs (variable number of steps, loops, conditions)
- Research prototyping where every forward pass may differ

**Key rule**: Override `__init__` to *define* layers, `call` to *use* them.



## Topic 3.2 (cont.): Subclassing — Basic Pattern

### Code Block 3.2a: Minimum Working Example

```python
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers

class SimpleClassifier(keras.Model):
    """Equivalent to the Sequential model in Part 1."""

    def __init__(self):
        super().__init__()                        # ← always call super().__init__()
        self.dense1 = layers.Dense(64, activation='relu')
        self.dense2 = layers.Dense(32, activation='relu')
        self.out    = layers.Dense(1,  activation='sigmoid')

    def call(self, x, training=False):           # ← forward pass logic lives here
        x = self.dense1(x)
        x = self.dense2(x)
        return self.out(x)

# Instantiate, compile, train — identical interface to Sequential/Functional
model_sub = SimpleClassifier()
model_sub.compile(loss='binary_crossentropy',
                  optimizer='adam',
                  metrics=['accuracy'])

model_sub.fit(X_train, y_train, epochs=10,
              batch_size=32, validation_split=0.2, verbose=0)

test_loss, test_acc = model_sub.evaluate(X_test, y_test, verbose=0)
print(f'Subclassed model test accuracy: {test_acc:.4f}')
```



## Topic 3.2 (cont.): Subclassing — Adding Dropout Correctly

### Code Block 3.2b: `training` Flag Controls Behaviour

```python
class ClassifierWithDropout(keras.Model):
    """
    Dropout is ON during training, OFF during inference.
    The `training` argument in call() propagates this signal.
    """

    def __init__(self, dropout_rate=0.3):
        super().__init__()
        self.dense1   = layers.Dense(128, activation='relu')
        self.drop1    = layers.Dropout(dropout_rate)
        self.dense2   = layers.Dense(64,  activation='relu')
        self.drop2    = layers.Dropout(dropout_rate)
        self.out      = layers.Dense(10,  activation='softmax')

    def call(self, x, training=False):
        x = self.dense1(x)
        x = self.drop1(x, training=training)   # ← pass training flag!
        x = self.dense2(x)
        x = self.drop2(x, training=training)
        return self.out(x)

model_drop = ClassifierWithDropout(dropout_rate=0.3)
model_drop.compile(loss='categorical_crossentropy',
                   optimizer='adam',
                   metrics=['accuracy'])

# Reusing MNIST data from Part 2
model_drop.fit(X_mnist_train[:10000], y_mnist_train_cat[:10000],
               epochs=5, batch_size=128,
               validation_split=0.2, verbose=0)

_, acc = model_drop.evaluate(X_mnist_test, y_mnist_test_cat, verbose=0)
print(f'Subclassed MNIST accuracy: {acc:.4f}')
```



## Topic 3.2 (cont.): Subclassing — Custom Layer Inside a Model

### Code Block 3.2c: Reusable Custom Layer

```python
class ResidualBlock(keras.layers.Layer):
    """
    A simple residual (skip-connection) block.
    Adds the input directly to the output: out = F(x) + x.
    Used in ResNet-style architectures.
    """

    def __init__(self, units):
        super().__init__()
        self.dense1 = layers.Dense(units, activation='relu')
        self.dense2 = layers.Dense(units)          # no activation here
        self.add    = layers.Add()
        self.relu   = layers.Activation('relu')

    def call(self, x):
        residual = x                               # ← save original input
        x = self.dense1(x)
        x = self.dense2(x)
        x = self.add([x, residual])               # ← skip connection
        return self.relu(x)


class ResidualClassifier(keras.Model):
    """Model that stacks two ResidualBlocks."""

    def __init__(self):
        super().__init__()
        self.proj   = layers.Dense(64)            # project input to 64-d
        self.block1 = ResidualBlock(64)
        self.block2 = ResidualBlock(64)
        self.out    = layers.Dense(1, activation='sigmoid')

    def call(self, x, training=False):
        x = self.proj(x)
        x = self.block1(x)
        x = self.block2(x)
        return self.out(x)


model_res = ResidualClassifier()
model_res.compile(loss='binary_crossentropy',
                  optimizer='adam',
                  metrics=['accuracy'])
model_res.fit(X_train, y_train, epochs=10,
              batch_size=32, validation_split=0.2, verbose=0)

_, acc = model_res.evaluate(X_test, y_test, verbose=0)
print(f'ResidualClassifier accuracy: {acc:.4f}')
model_res.summary()
```



## Topic 3.2 (cont.): API Comparison Side-by-Side

### Code Block 3.2d: Same Network, Three Styles

```python
#  Sequential 
seq = keras.Sequential([
    layers.Dense(64, activation='relu', input_shape=(10,)),
    layers.Dense(32, activation='relu'),
    layers.Dense(1,  activation='sigmoid')
])

#  Functional 
inp  = keras.Input(shape=(10,))
x    = layers.Dense(64, activation='relu')(inp)
x    = layers.Dense(32, activation='relu')(x)
out  = layers.Dense(1,  activation='sigmoid')(x)
func = keras.Model(inp, out)

#  Subclassing 
class SubModel(keras.Model):
    def __init__(self):
        super().__init__()
        self.d1  = layers.Dense(64, activation='relu')
        self.d2  = layers.Dense(32, activation='relu')
        self.out = layers.Dense(1,  activation='sigmoid')

    def call(self, x, training=False):
        return self.out(self.d2(self.d1(x)))

sub = SubModel()

# All three compile, fit, and evaluate identically
for m, name in [(seq, 'Sequential'),
                (func, 'Functional'),
                (sub, 'Subclassing')]:
    m.compile(loss='binary_crossentropy',
              optimizer='adam', metrics=['accuracy'])
    m.fit(X_train, y_train, epochs=5,
          batch_size=32, validation_split=0.2, verbose=0)
    _, acc = m.evaluate(X_test, y_test, verbose=0)
    print(f'{name:12s}: test accuracy = {acc:.4f}')
```

**Expected**: all three converge to similar accuracy — the API choice is about *design*, not *performance*.



## Topic 3.3: Custom Training Loop (GradientTape)

**Concept**: Full control over the training process

### Code Block 3.3a: Gradient Tape (TensorFlow's Autograd)

```python
# Simple regression: y = 2x + noise
X = np.random.randn(100, 1).astype('float32')
y = 2 * X + np.random.randn(100, 1) * 0.1

# Build model
model = keras.Sequential([
    layers.Dense(16, activation='relu', input_shape=(1,)),
    layers.Dense(1)
])

# Loss function and optimizer
loss_fn = keras.losses.MeanSquaredError()
optimizer = keras.optimizers.Adam(learning_rate=0.01)

# Custom training step
@tf.function  # Compile to TensorFlow graph (faster)
def train_step(x, y):
    with tf.GradientTape() as tape:
        # Forward pass
        predictions = model(x, training=True)
        loss = loss_fn(y, predictions)
    
    # Backward pass (compute gradients)
    gradients = tape.gradient(loss, model.trainable_weights)
    
    # Update weights
    optimizer.apply_gradients(zip(gradients, model.trainable_weights))
    
    return loss

# Training loop
losses = []
for epoch in range(10):
    epoch_loss = 0
    for batch in range(0, len(X), 32):
        x_batch = X[batch:batch+32]
        y_batch = y[batch:batch+32]
        loss = train_step(x_batch, y_batch)
        epoch_loss += loss.numpy()
    
    losses.append(epoch_loss / (len(X) // 32))
    if (epoch + 1) % 2 == 0:
        print(f"Epoch {epoch+1}, Loss: {losses[-1]:.4f}")

# Plot
plt.plot(losses)
plt.xlabel('Epoch')
plt.ylabel('Loss')
plt.title('Custom Training Loop Loss')
plt.grid(True)
plt.show()
```



## Topic 3.4: Callbacks (Monitor & Control Training)

**Concept**: Stop training early, save best model, adjust learning rate

### Code Block 3.4a: Early Stopping and Model Checkpoint

```python
# Build model
model = keras.Sequential([
    layers.Dense(64, activation='relu', input_shape=(10,)),
    layers.Dense(32, activation='relu'),
    layers.Dense(1, activation='sigmoid')
])

model.compile(
    loss='binary_crossentropy',
    optimizer='adam',
    metrics=['accuracy']
)

# Create callbacks
early_stop = keras.callbacks.EarlyStopping(
    monitor='val_loss',        # Watch validation loss
    patience=5,                # Stop if no improvement for 5 epochs
    restore_best_weights=True  # Use best weights
)

model_checkpoint = keras.callbacks.ModelCheckpoint(
    'best_model.h5',           # Save to file
    monitor='val_accuracy',
    save_best_only=True,       # Only save if better
    mode='max'
)

reduce_lr = keras.callbacks.ReduceLROnPlateau(
    monitor='val_loss',
    factor=0.5,                # Multiply LR by 0.5
    patience=3,                # After 3 epochs without improvement
    min_lr=1e-7
)

# Generate dummy data
X, y = make_classification(n_samples=1000, n_features=10, random_state=42)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

# Train with callbacks
history = model.fit(
    X_train, y_train,
    epochs=100,  # Might stop early
    batch_size=32,
    validation_split=0.2,
    callbacks=[early_stop, model_checkpoint, reduce_lr],
    verbose=0
)

print(f"Stopped at epoch {len(history.history['loss'])}")
print(f"Best validation accuracy: {max(history.history['val_accuracy']):.4f}")

# Load best model
model_best = keras.models.load_model('best_model.h5')
test_loss, test_acc = model_best.evaluate(X_test, y_test, verbose=0)
print(f"Best model test accuracy: {test_acc:.4f}")
```



## Topic 3.5: Regularization Techniques

**Concept**: Prevent overfitting by constraining weights

### Code Block 3.5a: L1/L2 Regularization

```python
# Model WITHOUT regularization
model_no_reg = keras.Sequential([
    layers.Dense(128, activation='relu', input_shape=(10,)),
    layers.Dense(64, activation='relu'),
    layers.Dense(1, activation='sigmoid')
])

# Model WITH L2 regularization
model_l2 = keras.Sequential([
    layers.Dense(128, activation='relu', 
                 input_shape=(10,),
                 kernel_regularizer=keras.regularizers.l2(0.001)),
    layers.Dense(64, activation='relu',
                 kernel_regularizer=keras.regularizers.l2(0.001)),
    layers.Dense(1, activation='sigmoid')
])

# Model WITH L1 regularization
model_l1 = keras.Sequential([
    layers.Dense(128, activation='relu',
                 input_shape=(10,),
                 kernel_regularizer=keras.regularizers.l1(0.001)),
    layers.Dense(64, activation='relu',
                 kernel_regularizer=keras.regularizers.l1(0.001)),
    layers.Dense(1, activation='sigmoid')
])

# Compile and train all three
for model, name in [(model_no_reg, 'No Regularization'),
                     (model_l2, 'L2 Regularization'),
                     (model_l1, 'L1 Regularization')]:
    model.compile(loss='binary_crossentropy', optimizer='adam', 
                  metrics=['accuracy'])
    history = model.fit(X_train, y_train, epochs=20, 
                       batch_size=32, validation_split=0.2, verbose=0)
    
    test_loss, test_acc = model.evaluate(X_test, y_test, verbose=0)
    print(f"{name}: Test Acc = {test_acc:.4f}")

# L1 tends to produce sparse weights (useful for feature selection)
# L2 tends to distribute weights evenly
```



# Part 4: Debugging & Optimization (1:10 - 1:20)

## Topic 4.1: Identify and Fix Common Problems

**Concept**: Diagnose why models fail to learn

### Code Block 4.1a: Common Issues and Solutions

```python
# ISSUE 1: Loss is NaN or Inf
# Causes: exploding gradients, bad learning rate, invalid data

# Solution: Check data for NaN
print(f"NaN in X_train: {np.isnan(X_train).any()}")
print(f"NaN in y_train: {np.isnan(y_train).any()}")

# Solution: Normalize input
from sklearn.preprocessing import StandardScaler
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)

# Solution: Use gradient clipping
model = keras.Sequential([
    layers.Dense(64, activation='relu', input_shape=(10,)),
    layers.Dense(1, activation='sigmoid')
])

model.compile(
    loss='binary_crossentropy',
    optimizer=keras.optimizers.Adam(
        learning_rate=0.001,
        clipvalue=1.0  # Clip gradients to [-1, 1]
    ),
    metrics=['accuracy']
)

# ISSUE 2: Constant loss (not learning)
# Causes: learning rate too small, bad architecture, dead ReLU

# Solution: Check learning rate
print("Testing different learning rates:")
for lr in [0.0001, 0.001, 0.01, 0.1]:
    model = keras.Sequential([
        layers.Dense(64, activation='relu', input_shape=(10,)),
        layers.Dense(1, activation='sigmoid')
    ])
    model.compile(
        loss='binary_crossentropy',
        optimizer=keras.optimizers.Adam(learning_rate=lr)
    )
    history = model.fit(X_train, y_train, epochs=10, 
                       batch_size=32, validation_split=0.2, verbose=0)
    final_loss = history.history['loss'][-1]
    print(f"  LR={lr}: Final loss = {final_loss:.4f}")

# ISSUE 3: Overfitting (train acc high, val acc low)
# Causes: too large model, too many epochs, no regularization

# Solution: Add dropout
model = keras.Sequential([
    layers.Dense(64, activation='relu', input_shape=(10,)),
    layers.Dropout(0.3),
    layers.Dense(32, activation='relu'),
    layers.Dropout(0.3),
    layers.Dense(1, activation='sigmoid')
])

# Solution: Stop early
early_stop = keras.callbacks.EarlyStopping(
    monitor='val_loss', patience=5, restore_best_weights=True
)
model.compile(loss='binary_crossentropy', optimizer='adam')
model.fit(X_train, y_train, epochs=100, batch_size=32,
         validation_split=0.2, callbacks=[early_stop], verbose=0)
```



## Topic 4.2: Hyperparameter Tuning

**Concept**: Find good hyperparameters systematically

### Code Block 4.2a: Grid Search with Keras

```python
from sklearn.model_selection import GridSearchCV
from tensorflow.keras.wrappers.scikit_learn import KerasClassifier

# Define model builder function
def create_model(learning_rate=0.001, dropout_rate=0.2, 
                 hidden_units=64):
    model = keras.Sequential([
        layers.Dense(hidden_units, activation='relu', 
                    input_shape=(10,)),
        layers.Dropout(dropout_rate),
        layers.Dense(1, activation='sigmoid')
    ])
    
    model.compile(
        loss='binary_crossentropy',
        optimizer=keras.optimizers.Adam(learning_rate=learning_rate),
        metrics=['accuracy']
    )
    return model

# Wrap for sklearn
model = KerasClassifier(
    build_fn=create_model,
    epochs=10,
    batch_size=32,
    verbose=0
)

# Grid search
param_grid = {
    'learning_rate': [0.001, 0.01],
    'dropout_rate': [0.2, 0.5],
    'hidden_units': [32, 64]
}

grid = GridSearchCV(
    estimator=model,
    param_grid=param_grid,
    cv=3,  # 3-fold cross-validation
    verbose=1,
    n_jobs=-1  # Use all CPU cores
)

print("Starting grid search (this will take a minute)...")
grid.fit(X_train, y_train)

print(f"\nBest parameters: {grid.best_params_}")
print(f"Best cross-val accuracy: {grid.best_score_:.4f}")

# Evaluate best model
best_model = grid.best_estimator_.model
test_loss, test_acc = best_model.evaluate(X_test, y_test, verbose=0)
print(f"Test accuracy with best params: {test_acc:.4f}")
```



## Topic 4.3: Save and Load Models

**Concept**: Persist trained models for later use

### Code Block 4.3a: Model Persistence

```python
# Build and train a model
model = keras.Sequential([
    layers.Dense(64, activation='relu', input_shape=(10,)),
    layers.Dense(32, activation='relu'),
    layers.Dense(1, activation='sigmoid')
])

model.compile(loss='binary_crossentropy', optimizer='adam',
              metrics=['accuracy'])

history = model.fit(X_train, y_train, epochs=10, batch_size=32,
                   validation_split=0.2, verbose=0)

# Method 1: Save entire model (architecture + weights)
model.save('my_model.h5')
print("Model saved as 'my_model.h5'")

# Load entire model
loaded_model = keras.models.load_model('my_model.h5')
test_loss, test_acc = loaded_model.evaluate(X_test, y_test, verbose=0)
print(f"Loaded model test accuracy: {test_acc:.4f}")

# Method 2: Save only weights
model.save_weights('my_weights.h5')

# Rebuild architecture and load weights
new_model = keras.Sequential([
    layers.Dense(64, activation='relu', input_shape=(10,)),
    layers.Dense(32, activation='relu'),
    layers.Dense(1, activation='sigmoid')
])
new_model.load_weights('my_weights.h5')
print("Weights loaded into new model")

# Method 3: SavedModel format (TensorFlow format)
model.save('my_model_tf')  # Saves as directory
loaded_tf_model = keras.models.load_model('my_model_tf')
print("Model saved/loaded as TensorFlow SavedModel")

# Make predictions with loaded model
predictions = loaded_model.predict(X_test[:5])
print(f"Predictions from loaded model:\n{predictions}")
```



# Part 5: Hands-On Exercises (1:20 - 1:45)

## Exercise 1: Build and Train (Beginner — 5 min)

**Task**: Create a binary classifier for synthetic data using Sequential API

```python
# 1. Generate classification data
from sklearn.datasets import make_moons
X, y = make_moons(n_samples=500, noise=0.1, random_state=42)

# 2. Split and normalize
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
X_train = StandardScaler().fit_transform(X_train)
X_test  = StandardScaler().fit_transform(X_test)

# 3. Build model with:
#    - 2 inputs (from 2D data)
#    - One hidden layer with 16 neurons + ReLU
#    - Output layer with sigmoid
# 
# 4. Compile and train for 20 epochs
#
# 5. Print test accuracy
#
# EXPECTED: ~95% accuracy
```



## Exercise 2: Model Subclassing (Medium — 15 min)

**Task**: Recreate the same binary classifier using a subclassed model, then extend it

```python
# PART A: Basic subclassed model (5 min)
# Create a subclassed model equivalent to Exercise 1's Sequential model.
# Hint: define layers in __init__, use them in call().
# Compile, fit, and print test accuracy — should match Exercise 1.

# PART B: Add a configurable block (10 min)
# Extend your model with a configurable number of hidden layers.
# - __init__ should accept n_layers=2 and units=32 as arguments
# - Build that many Dense layers dynamically inside __init__
# - Apply them in sequence inside call()
# - Compare test accuracy for n_layers in [1, 2, 3]

class ConfigurableNet(keras.Model):
    def __init__(self, n_layers=2, units=32, dropout_rate=0.0):
        super().__init__()
        # TODO: create self.hidden = [Dense(units, activation='relu')
        #                             for _ in range(n_layers)]
        # TODO: create self.drop  = Dropout(dropout_rate)
        # TODO: create self.out   = Dense(1, activation='sigmoid')
        pass

    def call(self, x, training=False):
        # TODO: iterate through self.hidden, apply dropout, return output
        pass

# Train and compare:
for n in [1, 2, 3]:
    m = ConfigurableNet(n_layers=n, units=32, dropout_rate=0.2)
    m.compile(loss='binary_crossentropy', optimizer='adam',
              metrics=['accuracy'])
    m.fit(X_train, y_train, epochs=20, verbose=0)
    _, acc = m.evaluate(X_test, y_test, verbose=0)
    print(f'n_layers={n}: test accuracy = {acc:.4f}')
```



## Exercise 3: API Comparison (Medium — 5 min)

**Task**: Build the same 64-32-1 network in all three styles, confirm identical accuracy

```python
# 1. Build the SAME architecture three times:
#    Sequential, Functional, Subclassed
#
# 2. Train all three on make_moons data (same splits)
#
# 3. Create a summary table:
#    | API         | Test Accuracy | Trainable Params | Lines of Code |
#    |-------------|---------------|-----------------|---------------|
#    | Sequential  | ?             | ?               | ?             |
#    | Functional  | ?             | ?               | ?             |
#    | Subclassing | ?             | ?               | ?             |
#
# 4. Answer:
#    a) Does the API choice affect accuracy?
#    b) Which requires the most/least code?
#    c) When would you choose Subclassing over Functional?
```


# Part 6: Wrap-up and Q&A (1:45 - 1:50)

## Key Takeaways

1. **Sequential API**: Linear stacking — fast to write, limited flexibility
2. **Functional API**: Explicit graph — multi-input/output, skip connections
3. **Model Subclassing**: Full Python class — custom logic, dynamic graphs, research
4. **Training process**: `model.fit()` works identically across all three APIs
5. **Debugging**: Check data → learning rate → regularization
6. **Validation**: Always monitor training vs validation curves
7. **Persistence**: `model.save()` works for all three API styles



## Common Pitfalls to Avoid

```python
# x Don't forget to normalize data
model.fit(X_raw, y)  # Bad!

# o Always scale inputs
X_scaled = StandardScaler().fit_transform(X)
model.fit(X_scaled, y)  # Good!

# x Don't use validation_split AND separate validation set
model.fit(X, y, validation_data=(X_val, y_val), 
          validation_split=0.2)  # Confusing!

# o Use one or the other
model.fit(X, y, validation_split=0.2)  # Good!

# x Don't train on test set
history = model.fit(X_test, y_test, ...)  # Bad!

# o Use separate data for training and testing
model.fit(X_train, y_train, validation_data=(X_val, y_val))
model.evaluate(X_test, y_test)  # Good!

# x Don't ignore warning signs
# Constant loss → investigate
# NaN loss → check data and LR
# Large gap between train/val acc → add regularization

# o Monitor training curves
plt.plot(history.history['accuracy'])
plt.plot(history.history['val_accuracy'])
```



## Resources for Continued Learning

**Official Documentation:**
- TensorFlow: https://www.tensorflow.org/guide
- Keras: https://keras.io/
- API Reference: https://www.tensorflow.org/api_docs/python/keras

**Recommended Tutorials:**
- Keras sequential guide: https://keras.io/getting_started/sequential_model/
- Functional API: https://keras.io/getting_started/functional/
- Training from scratch: https://keras.io/getting_started/intro_to_keras_for_engineers/

**Practice Datasets:**
- MNIST, CIFAR-10: `tensorflow.keras.datasets`
- UCI Machine Learning: https://archive.ics.uci.edu/ml/
- Kaggle: https://www.kaggle.com/



## Questions & Discussion

**What we covered in 90 minutes:**

o Keras **Sequential** API (build, compile, train)

o Keras **Functional** API (multi-input, branching)

o Keras **Model Subclassing** (full Python class, custom layers, residual blocks)

o The three APIs compared side-by-side

o Real datasets (Iris, MNIST, synthetic data)

o Debugging and optimization techniques

o Custom training loop, callbacks, regularization

o Hands-on exercises (3 progressively difficult)

\vspace{0.5cm}

**What to practice:**

- Implement a model you read about in a paper using Subclassing
- Build the same architecture all three ways — spot the trade-offs
- Monitor training curves and identify problems
- Save and load models across all API styles

\vspace{0.5cm}

**Next steps:**

- Use Subclassing when writing custom LSTM cells or attention heads
- Combine Functional API for the outer scaffold + custom layers inside
- Fine-tune pre-trained models (Class 5 applies to all three APIs)



# Appendix: Cheat Sheet

## Quick Reference

### Sequential API
```python
model = keras.Sequential([
    layers.Dense(64, activation='relu', input_shape=(10,)),
    layers.Dropout(0.2),
    layers.Dense(1, activation='sigmoid')
])
```

### Functional API
```python
inputs  = keras.Input(shape=(10,))
x       = layers.Dense(64, activation='relu')(inputs)
x       = layers.Dropout(0.2)(x)
outputs = layers.Dense(1, activation='sigmoid')(x)
model   = keras.Model(inputs, outputs)
```

### Model Subclassing
```python
class MyModel(keras.Model):
    def __init__(self):
        super().__init__()
        self.d1  = layers.Dense(64, activation='relu')
        self.drop = layers.Dropout(0.2)
        self.out = layers.Dense(1, activation='sigmoid')

    def call(self, x, training=False):
        x = self.d1(x)
        x = self.drop(x, training=training)  # ← pass training flag!
        return self.out(x)

model = MyModel()
```


### Compilation (same for all three)
```python
model.compile(
    loss='binary_crossentropy',
    optimizer='adam',
    metrics=['accuracy']
)
```

### Training, Evaluation & Prediction (same for all three)
```python
history = model.fit(X_train, y_train, epochs=10,
                    batch_size=32, validation_split=0.2)
loss, acc = model.evaluate(X_test, y_test)
predictions = model.predict(X_new)
```

### Save & Load (same for all three)
```python
model.save('model.h5')
model = keras.models.load_model('model.h5')
```

### When to Use Each API

| Situation | API |
|---|---|
| Quick prototype, linear layers | Sequential |
| Multiple inputs/outputs, skip connections | Functional |
| Custom forward pass, research, loops/conditionals | Subclassing |


# End of Workshop

**Thank you for participating!**

All code is available in accompanying Jupyter notebook.

Remember: The best way to learn deep learning is by building models.

**Start coding! **

---
title: EST-744
subtitle: Fundamentos de Redes Neuronales
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

# Introduction

## What is a Neural Network?


\begin{tikzpicture}[
    scale=1.2,
    every node/.style={draw, circle, minimum size=0.7cm},
    input node/.style={fill=blue!30},
    hidden node/.style={fill=orange!30},
    output node/.style={fill=green!30},
    edge/.style={->, thick, gray},
    label/.style={draw=none},remember picture, overlay
]
\tikzset{shift={(current page.center)},yshift=-2.5cm, scale=0.8}
% Title
\node[label, font=\Large\bfseries] at (3,6.2) {Neural Network Architecture};

% Layer labels
\node[label, font=\textbf\small] at (0.5,5.6) {Input};
\node[label, font=\textbf\small] at (3,5.6) {Hidden};
\node[label, font=\textbf\small] at (5.5,5.6) {Output};

% Input layer
\node[input node] (i1) at (0.5,4.2) {$x_1$};
\node[input node] (i2) at (0.5,2.8) {$x_2$};
\node[input node] (i3) at (0.5,1.4) {$x_3$};

% Hidden layer
\node[hidden node] (h1) at (3,4.2) {$h_1$};
\node[hidden node] (h2) at (3,2.8) {$h_2$};
\node[hidden node] (h3) at (3,1.4) {$h_3$};

% Output layer
\node[output node] (o1) at (5.5,3.5) {$y_1$};
\node[output node] (o2) at (5.5,2.1) {$y_2$};

% All connections
\foreach \i in {1,2,3} {
  \foreach \j in {1,2,3} {
    \draw[edge] (i\i) -- (h\j);
  }
}

\foreach \i in {1,2,3} {
  \foreach \j in {1,2} {
    \draw[edge] (h\i) -- (o\j);
  }
}

% Forward pass arrow
\draw[->, very thick, blue!60, dashed] (-0.7,5) -- (6.7,5);
\node[label, font=\itshape\small, color=blue!60] at (3,5.25) {Forward Pass};

% Description below
\node[label, font=\footnotesize, anchor=north] at (3,-0.3) {
    Blue circles = inputs \quad Orange = hidden units \quad Green = predictions
};
\node[label, font=\footnotesize, anchor=north] at (3,-0.8) {
    Edges represent learnable weights; data flows left to right
};

\end{tikzpicture}

:::::: {.columns}
::: {.column width="50%"}
A neural network is a system of interconnected "neurons" that learns to map inputs to outputs

**Biological inspiration**: mimics how neurons in the brain process information

**Practical reality**: mathematical functions composed of simpler functions
:::

::: {.column width="50%"}

:::
::::::

## Why Neural Networks?

- Traditional ML: features carefully engineered by humans
- Neural Networks: **automatically learn** useful representations

\vspace{0.3cm}

**Analogy**: 
- A chef (human) vs. a kitchen robot (neural network)
- Chef: manually prepares ingredients
- Robot: learns what cuts and prep work matter


# The Building Blocks

## A Single Neuron

$$y = \sigma(w \cdot x + b)$$

\vspace{0.3cm}

- **Input** $x$: features (image pixels, word vectors, etc.)
- **Weights** $w$: learnable parameters (what matters)
- **Bias** $b$: threshold adjustment
- **Activation** $\sigma()$: non-linearity (ReLU, sigmoid, etc.)

\vspace{0.3cm}

**Key insight**: Without activation functions, stacking neurons = one linear transformation (useless for complex patterns)

## Activation Functions

| Function | Formula | When to use |
|---|---|---|
| ReLU | $\max(0, x)$ | Hidden layers (most common) |
| Sigmoid | $\frac{1}{1+e^{-x}}$ | Binary classification output |
| Tanh | $\frac{e^x - e^{-x}}{e^x + e^{-x}}$ | RNNs, hidden layers |

**Intuition**: Activation functions add non-linearity, allowing networks to learn curves and decision boundaries

# Neural Network Architecture

## Layers and Forward Pass

```
Input Layer → Hidden Layer 1 → Hidden Layer 2 → Output Layer
   [3 neurons]    [5 neurons]    [4 neurons]     [2 neurons]
```

\vspace{0.3cm}

Each layer:
1. Takes input from previous layer
2. Applies weights + bias
3. Applies activation function
4. Passes output to next layer

**Forward pass**: input flows through all layers to produce prediction

## Depth and Width

- **Depth**: number of layers (deep = many layers)
- **Width**: neurons per layer

\vspace{0.3cm}

**Trade-off**:
- More layers = can learn more complex patterns
- Too many layers = harder to train, risk of vanishing gradients

\vspace{0.2cm}

For this course: start with 2-3 hidden layers unless specific needs


# Training: The Learning Process

## Loss Function

A **loss function** measures how wrong the network is:

$$L = \text{mean}((y_{true} - y_{pred})^2)$$

\vspace{0.3cm}

- **MSE Loss**: regression problems (continuous output)
- **Cross-entropy Loss**: classification problems (probabilities)

\vspace{0.3cm}

**Goal during training**: minimize loss by adjusting weights

## Gradient Descent

\vspace{0.3cm}

**Intuition**: Imagine a ball rolling down a hill (loss surface)
- Calculate the slope (gradient)
- Roll down the steepest direction
- Repeat until you reach the valley

\vspace{0.3cm}

$$w_{new} = w_{old} - \alpha \cdot \frac{dL}{dw}$$

- $\alpha$ = learning rate (step size)
- $\frac{dL}{dw}$ = gradient (slope of loss w.r.t. weight)



# Backpropagation

## How Networks Learn

\vspace{0.2cm}

**Backpropagation**: Efficiently compute gradients for all weights

\vspace{0.2cm}

1. **Forward pass**: compute predictions and loss
2. **Backward pass**: compute gradients layer-by-layer (chain rule)
3. **Update**: adjust weights using gradients

\vspace{0.3cm}

**Why backward?**
- Start from loss (what we care about)
- Work backward to earlier layers
- Reuse intermediate calculations (efficient)

## Optimization: SGD to Adam

| Optimizer | Idea | Learning Rate |
|---|---|---|
| SGD | Simple gradient descent | Fixed (manual tuning) |
| Momentum | Accumulate direction | Fixed |
| Adam | Adaptive per-parameter | Auto-adjusting |

\vspace{0.2cm}

**For this course**: Use Adam (robust, requires less tuning)



# Practical Example: Setup

## A Simple Classification Task

**Goal**: Predict if a handwritten digit is 0-9

\vspace{0.3cm}

**Data**: MNIST (28×28 pixel images)

\vspace{0.3cm}

**Network**:
- Input: 784 pixels (28 × 28 flattened)
- Hidden 1: 128 neurons, ReLU
- Hidden 2: 64 neurons, ReLU
- Output: 10 neurons, softmax (probabilities for digits 0-9)


# Practical Example: Implementation

## Code with Keras/TensorFlow

```python
import tensorflow as tf
from tensorflow import keras

# Load MNIST dataset
(x_train, y_train), (x_test, y_test) = keras.datasets.mnist.load_data()
x_train = x_train.reshape(-1, 784).astype('float32') / 255.0
x_test = x_test.reshape(-1, 784).astype('float32') / 255.0

# Build network
model = keras.Sequential([
    keras.layers.Dense(128, activation='relu', input_shape=(784,)),
    keras.layers.Dense(64, activation='relu'),
    keras.layers.Dense(10, activation='softmax')
])

# Compile (loss + optimizer)
model.compile(
    loss='sparse_categorical_crossentropy',
    optimizer='adam',
    metrics=['accuracy']
)

# Train
model.fit(x_train, y_train, epochs=10, batch_size=32, 
          validation_split=0.1)
```



# Practical Example: Evaluation

## Monitoring Training

```python
# Evaluate on test set
test_loss, test_acc = model.evaluate(x_test, y_test)
print(f"Test accuracy: {test_acc:.4f}")

# Make predictions
predictions = model.predict(x_test[:5])
print(predictions)  # probabilities for each digit
```

\vspace{0.3cm}

**Typical results**: ~97-98% accuracy with this simple architecture

\vspace{0.3cm}

**What to visualize**:
- Training loss curve (should decrease)
- Accuracy improvement over epochs
- Predictions on a few test examples


# Key Concepts Summary

## What We've Covered

o Neurons as basic units (weights, bias, activation)

o Layers and forward passes

o Loss functions and gradient descent

o Backpropagation (the learning algorithm)

o Optimizers (Adam as default choice)

o Full training pipeline in code

## Common Pitfalls

- **Learning rate too high**: weights oscillate, don't converge
- **Too many layers**: vanishing gradients, hard to train
- **Imbalanced data**: accuracy misleading
- **Overfitting**: memorizes training data, fails on test data


# Exercises for Class 1

## Hands-On Tasks

1. **Modify architecture**: Try different numbers of layers/neurons. How does it affect accuracy and training speed?

2. **Change activation functions**: Replace ReLU with tanh. Compare results.

3. **Experiment with learning rates**: Train with lr=0.001 and lr=0.1. What happens?

4. **Regularization**: Add `keras.layers.Dropout(0.2)` between hidden layers. Does overfitting decrease?

5. **Visualize weights**: Print `model.get_weights()`. Do they look reasonable?



# Next Class Preview

## From Networks to Text

Neural networks work on **any numeric input**—but how do we feed text?

\vspace{0.3cm}

**Class 2: Embeddings**
- Convert words to vectors
- Learn meaning from context
- Visualize semantic relationships

\vspace{0.3cm}

"The quick brown fox" → Vector representations that capture "meaning"


# Questions & Discussion

Thank you!

**Key takeaway**: Neural networks are function approximators that learn through gradient-based optimization. Everything else is architecture and tricks.

\vspace{0.5cm}

Next: How do we feed text to these networks?

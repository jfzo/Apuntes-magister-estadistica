import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from gensim.models import KeyedVectors # Si falla, ejecutar !pip install gensim
from gensim.models import Word2Vec

# Descarga y carga de set de datos de reviews de películas.
VOCAB_SIZE = 10000
(x_train, y_train), (x_test, y_test) = keras.datasets.imdb.load_data(
    num_words=VOCAB_SIZE
)

# Mapa que permite obtener la palabra a partir de su indeice
inx_palabras = keras.datasets.imdb.get_word_index()


w2v = Word2Vec(x_train) # tarda algunos segundos


# Construir la matriz con un embedding por fila y tantas filas como palabras del voc.
embedding_matrix = np.zeros((VOCAB_SIZE, 100))

for w, idx in inx_palabras.items():
    if idx in w2v.wv:
        embedding_matrix[idx] = w2v.wv[idx]
    else:
        print(f"Palabra {w} no tiene vector denso")


# procesando secuencias para que tengan mismo largo
MAX_LEN = 0
for i in range(x_train.shape[0]):
    len_i = len(x_train[i])
    if len_i > MAX_LEN:
        MAX_LEN = len_i

padded_x_train = keras.preprocessing.sequence.pad_sequences(
    x_train, padding = "post", truncating="post", maxlen=MAX_LEN
    )

# La capa de embedding con los pesso del embedding ya incorporados
embedding_layer = layers.Embedding(
    input_dim = VOCAB_SIZE,
    output_dim = 100, # si tuvieramos embeddings con otro largo, usar ese valor.
    weights = [embedding_matrix], # esta matriz fue rellenada con vectores pre-aprendidos
    trainable = False,
    mask_zero = True,
    name = "w2v_embeddings"
)

# ahora construir modelo
modelo01 = keras.Sequential([
    embedding_layer,
    layers.GlobalAveragePooling1D(),
    layers.Dense(32, activation="relu"),
    layers.Dense(1, activation="sigmoid")],
    name = "clasificador_promedio"
)

modelo01.compile(
    optimizer = "adam",
    loss = "binary_crossentropy",
    metrics = ["accuracy", "auc"]
    )




modelo01.fit(padded_x_train, y_train, batch_size=32, epochs=5, validation_split = 0.2)
res = modelo01.evaluate(padded_x_test, y_test)



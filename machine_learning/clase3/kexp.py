import os; os.environ['TF_CPP_MIN_LOG_LEVEL']='3'
import numpy as np, keras, tensorflow as tf, json
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
from sklearn.datasets import load_digits
from sklearn.model_selection import train_test_split
keras.utils.set_random_seed(0)
d=load_digits(); X=d.data/16.0; y=d.target
Xtr,Xte,ytr,yte=train_test_split(X,y,test_size=.3,random_state=0,stratify=y)
model=keras.Sequential([keras.Input((64,)),keras.layers.Dense(64,activation='relu'),keras.layers.Dense(10,activation='softmax')])
model.compile(optimizer='adam',loss='sparse_categorical_crossentropy',metrics=['accuracy'])
h=model.fit(Xtr,ytr,epochs=100,batch_size=32,validation_split=.15,callbacks=[keras.callbacks.EarlyStopping(patience=5,restore_best_weights=True)],verbose=0)
loss,acc=model.evaluate(Xte,yte,verbose=0)
R=dict(epochs=len(h.history['loss']),best_val=max(h.history['val_accuracy']),test_acc=acc,test_loss=loss,params=model.count_params(),tf=tf.__version__,keras=keras.__version__)
fig,ax=plt.subplots(1,2,figsize=(9,3.2)); ax[0].plot(h.history['loss'],label='entrenamiento'); ax[0].plot(h.history['val_loss'],label='validación'); ax[0].set_xlabel('época'); ax[0].set_ylabel('entropía cruzada'); ax[0].legend()
ax[1].plot(h.history['accuracy'],label='entrenamiento'); ax[1].plot(h.history['val_accuracy'],label='validación'); ax[1].set_xlabel('época'); ax[1].set_ylabel('accuracy'); ax[1].legend(); plt.tight_layout(); plt.savefig('fig_keras.png',dpi=200)
print(R)

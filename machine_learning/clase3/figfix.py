import numpy as np, matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
from nnlib import *
from sklearn.datasets import make_moons
from sklearn.model_selection import train_test_split
# XOR
Xx=np.array([[0,0],[1,0],[0,1],[1,1]]); yx=np.array([0,1,1,0])
W1=np.array([[1,1],[1,1]]); b1=np.array([[0],[-1]]); A1=np.maximum(W1.T@Xx.T+b1,0)
cols=['tab:blue' if v==0 else 'tab:red' for v in yx]
fig,ax=plt.subplots(1,2,figsize=(8,3.3))
ax[0].scatter(Xx[:,0],Xx[:,1],c=cols,s=120); ax[0].set_title('Espacio de entrada $(x_1,x_2)$'); ax[0].set_xlabel('$x_1$'); ax[0].set_ylabel('$x_2$'); ax[0].set_xlim(-.3,1.4); ax[0].set_ylim(-.3,1.4)
for a_,b_ in Xx: ax[0].annotate(f'({a_},{b_})',(a_,b_),textcoords='offset points',xytext=(8,6),fontsize=8)
ax[1].scatter(A1[0],A1[1],c=cols,s=120); h=np.linspace(-.2,2.4,10); ax[1].plot(h,(h-.5)/2,'k--',lw=1,label='$h_1-2h_2=0{,}5$')
ax[1].annotate('(1,0): dos puntos\nrojos coinciden',(1,0),textcoords='offset points',xytext=(-10,22),fontsize=8)
ax[1].set_title('Espacio oculto $(h_1,h_2)$'); ax[1].set_xlabel('$h_1$'); ax[1].set_ylabel('$h_2$'); ax[1].set_xlim(-.3,2.4); ax[1].set_ylim(-.3,1.4); ax[1].legend(fontsize=8,loc='upper left')
plt.tight_layout(); plt.savefig('fig_xor.png',dpi=200); plt.close()
# lr/batch
X,y=make_moons(300,noise=.25,random_state=0)
Xtr,Xte,ytr,yte=train_test_split(X,y,test_size=.3,random_state=0,stratify=y); Xt,Yt=Xtr.T,ytr.reshape(1,-1)
fig,ax=plt.subplots(1,2,figsize=(9.5,3.3))
for lr in [0.01,0.1,1.0,5.0]:
    P,h,it=entrenar(Xt,Yt,4,lr,300); ax[0].plot(h,label=f'tasa={lr}')
ax[0].set_xlabel('época'); ax[0].set_ylabel('costo $J$ (entrenamiento)'); ax[0].set_yscale('log'); ax[0].legend(fontsize=8,loc='lower left'); ax[0].set_title('Tasa de aprendizaje (batch completo)',fontsize=10)
for b in [None,32,1]:
    P,h,it=entrenar(Xt,Yt,4,0.5,100,b); ax[1].plot(h,label=f'batch={b or "completo"} ({it} iter.)')
ax[1].set_xlabel('época'); ax[1].set_yscale('log'); ax[1].legend(fontsize=8,loc='upper right'); ax[1].set_title('Minibatch: épocas vs iteraciones (tasa 0,5)',fontsize=10)
plt.tight_layout(); plt.savefig('fig_lr_batch.png',dpi=200); plt.close()

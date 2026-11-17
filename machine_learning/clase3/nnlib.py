import numpy as np
sig=lambda z:1/(1+np.exp(-z))
def forward(X,P):
    Z1=P['W1'].T@X+P['b1']; A1=sig(Z1); Z2=P['W2'].T@A1+P['b2']; A2=sig(Z2)
    return dict(X=X,A1=A1,A2=A2)
def cost(A2,Y,eps=1e-12):
    A2=np.clip(A2,eps,1-eps); return -np.mean(Y*np.log(A2)+(1-Y)*np.log(1-A2))
def backward(c,P,Y):
    m=Y.shape[1]; A1,A2,X=c['A1'],c['A2'],c['X']
    dZ2=(A2-Y)/m; dW2=A1@dZ2.T; db2=dZ2.sum(1,keepdims=True)
    dA1=P['W2']@dZ2; dZ1=dA1*A1*(1-A1); dW1=X@dZ1.T; db1=dZ1.sum(1,keepdims=True)
    return dict(W1=dW1,b1=db1,W2=dW2,b2=db2)
def init(n_in,n_h,seed=0,modo='aleatoria'):
    r=np.random.default_rng(seed)
    if modo=='ceros': W1=np.zeros((n_in,n_h)); W2=np.zeros((n_h,1))
    else: W1=r.normal(0,.5,(n_in,n_h)); W2=r.normal(0,.5,(n_h,1))
    return dict(W1=W1,b1=np.zeros((n_h,1)),W2=W2,b2=np.zeros((1,1)))
def entrenar(X,Y,n_h=4,lr=1.0,epocas=300,batch=None,seed=0,modo='aleatoria'):
    m=X.shape[1]; batch=batch or m; P=init(X.shape[0],n_h,seed,modo); r=np.random.default_rng(seed+1); h=[]; it=0
    for ep in range(epocas):
        idx=r.permutation(m)
        for s in range(0,m,batch):
            b=idx[s:s+batch]; g=backward(forward(X[:,b],P),P,Y[:,b])
            for k in P: P[k]=P[k]-lr*g[k]
            it+=1
        h.append(cost(forward(X,P)['A2'],Y))
    return P,h,it
def acc(P,X,Y): return float(((forward(X,P)['A2']>.5)==Y).mean())

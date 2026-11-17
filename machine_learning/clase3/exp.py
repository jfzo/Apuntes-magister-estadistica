import numpy as np, warnings, json; warnings.filterwarnings('ignore')
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
from nnlib import *
from sklearn.datasets import make_moons, load_digits
from sklearn.model_selection import train_test_split, StratifiedKFold, GridSearchCV, cross_val_score
from sklearn.linear_model import LogisticRegression
from sklearn.neural_network import MLPClassifier
from sklearn.svm import SVC
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
R={}
# --- moons
X,y=make_moons(300,noise=.25,random_state=0)
Xtr,Xte,ytr,yte=train_test_split(X,y,test_size=.3,random_state=0,stratify=y)
Xt,Yt=Xtr.T,ytr.reshape(1,-1); Xe,Ye=Xte.T,yte.reshape(1,-1)
lr_=LogisticRegression().fit(Xtr,ytr); R['moons_logreg_test']=lr_.score(Xte,yte)
# gradient check
P=init(2,3,1); Xg=np.random.default_rng(3).normal(size=(2,8)); Yg=(np.random.default_rng(4).random((1,8))>.5).astype(float)
g=backward(forward(Xg,P),P,Yg); mx=0
for k in P:
    num=np.zeros_like(P[k])
    for idx in np.ndindex(*P[k].shape):
        o=P[k][idx]; P[k][idx]=o+1e-6; jp=cost(forward(Xg,P)['A2'],Yg); P[k][idx]=o-1e-6; jm=cost(forward(Xg,P)['A2'],Yg); P[k][idx]=o
        num[idx]=(jp-jm)/2e-6
    rel=np.linalg.norm(num-g[k])/(np.linalg.norm(num)+np.linalg.norm(g[k])); mx=max(mx,rel)
R['gradcheck_maxrel']=mx
# lr experiments
R['lr']={}
fig,ax=plt.subplots(1,2,figsize=(9,3.2))
for lr in [0.01,0.1,1.0,5.0]:
    Pn,h,it=entrenar(Xt,Yt,4,lr,300); R['lr'][lr]=(h[-1],acc(Pn,Xe,Ye)); ax[0].plot(h,label=f'lr={lr}')
ax[0].set_xlabel('época'); ax[0].set_ylabel('costo J (entrenamiento)'); ax[0].set_yscale('log'); ax[0].legend(); ax[0].set_title('Efecto de la tasa de aprendizaje')
R['batch']={}
for b in [None,32,1]:
    Pn,h,it=entrenar(Xt,Yt,4,0.5 if b else 0.5,100,b); R['batch'][str(b)]=(it,h[-1],acc(Pn,Xe,Ye)); ax[1].plot(h,label=f'batch={b or "completo"} ({it} it.)')
ax[1].set_xlabel('época'); ax[1].set_yscale('log'); ax[1].legend(); ax[1].set_title('Minibatch: épocas vs iteraciones')
plt.tight_layout(); plt.savefig('fig_lr_batch.png',dpi=200); plt.close()
# init zeros
Pz,hz,_=entrenar(Xt,Yt,4,1.0,300,modo='ceros'); Pr,hr,_=entrenar(Xt,Yt,4,1.0,300)
R['init']=dict(zeros_acc=acc(Pz,Xe,Ye),rand_acc=acc(Pr,Xe,Ye),zeros_cols_equal=bool(np.allclose(Pz['W1'][:,0],Pz['W1'][:,1])),zeros_final=hz[-1],rand_final=hr[-1])
# boundary figure (own net vs logreg vs hidden sizes)
xx,yy=np.meshgrid(np.linspace(-2,3,200),np.linspace(-1.5,2,200)); G=np.c_[xx.ravel(),yy.ravel()]
fig,ax=plt.subplots(1,4,figsize=(13,3.2))
R['moons_hidden']={}
for a,(name,pred) in zip(ax,[('Regresión logística',lambda G:lr_.predict(G))]+[(f'MLP {h} neuronas',None) for h in (1,3,20)]):
    if pred is None:
        h=int(name.split()[1]); m=MLPClassifier((h,),activation='logistic',solver='lbfgs',max_iter=5000,random_state=0).fit(Xtr,ytr)
        pred=m.predict; R['moons_hidden'][h]=m.score(Xte,yte)
    a.contourf(xx,yy,pred(G).reshape(xx.shape),alpha=.25,cmap='coolwarm'); a.scatter(Xtr[:,0],Xtr[:,1],c=ytr,cmap='coolwarm',s=12,edgecolor='k',lw=.3); a.set_title(name,fontsize=9); a.set_xticks([]); a.set_yticks([])
plt.tight_layout(); plt.savefig('fig_moons.png',dpi=200); plt.close()
# --- XOR
Xx=np.array([[0,0],[1,0],[0,1],[1,1]]); yx=np.array([0,1,1,0])
R['xor_logreg_acc']=LogisticRegression(C=1e6).fit(Xx,yx).score(Xx,yx)
W1=np.array([[1,1],[1,1]]); b1=np.array([[0],[-1]]); W2=np.array([[1],[-2]])
Z1=W1.T@Xx.T+b1; A1=np.maximum(Z1,0); out=(W2.T@A1)
R['xor_hidden']=A1.tolist(); R['xor_out']=out.tolist()
fig,ax=plt.subplots(1,2,figsize=(7.5,3.2))
cols=['tab:blue' if v==0 else 'tab:red' for v in yx]
ax[0].scatter(Xx[:,0],Xx[:,1],c=cols,s=120); ax[0].set_title('Espacio de entrada $(x_1,x_2)$'); ax[0].set_xlabel('$x_1$'); ax[0].set_ylabel('$x_2$'); ax[0].set_xlim(-.3,1.3); ax[0].set_ylim(-.3,1.3)
ax[1].scatter(A1[0],A1[1]+np.array([0,0,0,0]),c=cols,s=120); ax[1].plot([0,2],[0,1],'k--',lw=1); ax[1].set_title('Espacio oculto $(h_1,h_2)$'); ax[1].set_xlabel('$h_1$'); ax[1].set_ylabel('$h_2$'); ax[1].set_xlim(-.3,2.3); ax[1].set_ylim(-.3,1.3)
for i,(a_,b_) in enumerate(zip(Xx[:,0],Xx[:,1])): ax[0].annotate(f'({a_},{b_})',(a_,b_),textcoords='offset points',xytext=(8,6),fontsize=8)
plt.tight_layout(); plt.savefig('fig_xor.png',dpi=200); plt.close()
# --- sigmoid derivative
z=np.linspace(-8,8,400); s=sig(z)
fig,ax=plt.subplots(figsize=(4.8,3)); ax.plot(z,s*(1-s),label="$g'(z)=g(z)(1-g(z))$"); ax.axhline(.25,ls=':',c='k'); ax.text(-7.5,.26,'máximo 1/4 en $z=0$',fontsize=8); ax.set_xlabel('z'); ax.legend(); plt.tight_layout(); plt.savefig('fig_dsigmoid.png',dpi=200); plt.close()
# --- architecture figure
fig,ax=plt.subplots(figsize=(7.5,3.6)); ax.axis('off')
ins=[(0,.7),(0,.3)]; hid=[(1,.85),(1,.5),(1,.15)]; out_=[(2,.5)]
for (a_,b_) in ins:
    for (c_,d_) in hid: ax.plot([a_,c_],[b_,d_],c='gray',lw=1,zorder=1)
for (a_,b_) in hid: ax.plot([a_,2],[b_,.5],c='gray',lw=1,zorder=1)
for i,(a_,b_) in enumerate(ins): ax.scatter(a_,b_,s=1200,c='#f28b82',zorder=2,edgecolor='k'); ax.text(a_,b_,f'$x_{i+1}$',ha='center',va='center',fontsize=12)
for i,(a_,b_) in enumerate(hid): ax.scatter(a_,b_,s=1200,c='#81c995',zorder=2,edgecolor='k'); ax.text(a_,b_,f'$a_{i+1}^{{[1]}}$',ha='center',va='center',fontsize=11)
ax.scatter(2,.5,s=1200,c='#8ab4f8',zorder=2,edgecolor='k'); ax.text(2,.5,'$a^{[2]}$',ha='center',va='center',fontsize=11)
ax.text(0,1.0,'Entrada\n$n=2$',ha='center',fontsize=10); ax.text(1,1.05,'Capa oculta\n3 neuronas, sigmoide',ha='center',fontsize=10); ax.text(2,.78,'Salida\n1 neurona, sigmoide',ha='center',fontsize=10)
ax.text(.5,.02,'$W^{[1]}\\in\\mathbb{R}^{2\\times 3},\\ b^{[1]}\\in\\mathbb{R}^{3\\times 1}$',ha='center',fontsize=10); ax.text(1.5,.02,'$W^{[2]}\\in\\mathbb{R}^{3\\times 1},\\ b^{[2]}\\in\\mathbb{R}^{1\\times 1}$',ha='center',fontsize=10)
ax.set_xlim(-.3,2.4); ax.set_ylim(-.05,1.2); plt.tight_layout(); plt.savefig('fig_arch231.png',dpi=200); plt.close()
# --- digits
d=load_digits(); Xd,yd=d.data,d.target
Xdtr,Xdte,ydtr,ydte=train_test_split(Xd,yd,test_size=.3,random_state=0,stratify=yd)
cv=StratifiedKFold(5,shuffle=True,random_state=0)
R['digits']={}
svm=SVC(C=1,gamma=0.001); R['digits']['svm_cv']=cross_val_score(svm,Xdtr,ydtr,cv=cv).mean(); R['digits']['svm_test']=svm.fit(Xdtr,ydtr).score(Xdte,ydte)
pipe=make_pipeline(StandardScaler(),MLPClassifier(max_iter=1000,random_state=0))
gs=GridSearchCV(pipe,{'mlpclassifier__hidden_layer_sizes':[(16,),(64,),(128,)],'mlpclassifier__alpha':[1e-4,1e-2,1.0]},cv=cv,n_jobs=-1).fit(Xdtr,ydtr)
R['digits']['mlp_best']=gs.best_params_ and {k:str(v) for k,v in gs.best_params_.items()}; R['digits']['mlp_cv']=gs.best_score_; R['digits']['mlp_test']=gs.score(Xdte,ydte)
R['digits']['grid']={str(p):round(s,4) for p,s in zip(gs.cv_results_['params'],gs.cv_results_['mean_test_score'])}
R['digits']['has_class_weight']='class_weight' in MLPClassifier().get_params()
es=make_pipeline(StandardScaler(),MLPClassifier((64,),max_iter=500,early_stopping=True,validation_fraction=.15,n_iter_no_change=10,random_state=0)).fit(Xdtr,ydtr)
mm=es[-1]; R['digits']['es']=dict(n_iter=mm.n_iter_,best_val=mm.best_validation_score_,test=es.score(Xdte,ydte))
fig,ax=plt.subplots(1,2,figsize=(9,3.2)); ax[0].plot(mm.loss_curve_); ax[0].set_xlabel('época'); ax[0].set_ylabel('pérdida (entrenamiento)'); ax[1].plot(mm.validation_scores_); ax[1].set_xlabel('época'); ax[1].set_ylabel('accuracy (validación)'); ax[1].axvline(np.argmax(mm.validation_scores_),ls='--',c='k'); plt.tight_layout(); plt.savefig('fig_early.png',dpi=200); plt.close()
json.dump(R,open('results.json','w'),indent=1,default=str); print(json.dumps(R,indent=1,default=str))

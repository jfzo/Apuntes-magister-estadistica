import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
fig,ax=plt.subplots(figsize=(8,4.2)); ax.axis('off')
X=[(0,.72),(0,.28)]; H=[(1.6,.72),(1.6,.28)]; O=(3.2,.5)
lw=1.4; grey='#555555'
def edge(p,q,label,pos=.30,off=(0,0),color=grey):
    ax.annotate('',xy=q,xytext=p,arrowprops=dict(arrowstyle='-|>',color=color,lw=lw,shrinkA=22,shrinkB=22),zorder=1)
    x=p[0]+(q[0]-p[0])*pos+off[0]; y=p[1]+(q[1]-p[1])*pos+off[1]
    ax.text(x,y,label,fontsize=11,ha='center',va='center',bbox=dict(fc='white',ec='none',pad=1.2),zorder=3)
# capa 1: w^{[1]}_{jk}, de la entrada j a la neurona oculta k
edge(X[0],H[0],r'$w^{[1]}_{11}=1$',.62,(0,.045))
edge(X[0],H[1],r'$w^{[1]}_{12}=1$',.24,(0,-.012))
edge(X[1],H[0],r'$w^{[1]}_{21}=1$',.24,(0,.012))
edge(X[1],H[1],r'$w^{[1]}_{22}=1$',.62,(0,-.045))
# capa 2
edge(H[0],O,r'$w^{[2]}_{1}=1$',.45,(0,.055),'#1b6ca8')
edge(H[1],O,r'$w^{[2]}_{2}=-2$',.45,(0,-.055),'#1b6ca8')
for i,(x,y) in enumerate(X):
    ax.scatter(x,y,s=2300,c='#f9c9c5',ec='k',zorder=2); ax.text(x,y,f'$x_{i+1}$',ha='center',va='center',fontsize=15,zorder=4)
bias1=[0,-1]
for i,(x,y) in enumerate(H):
    ax.scatter(x,y,s=2300,c='#c5e8cd',ec='k',zorder=2); ax.text(x,y,f'$a^{{[1]}}_{i+1}$',ha='center',va='center',fontsize=14,zorder=4)
    ax.text(x,y-.178,f'$b^{{[1]}}_{i+1}={bias1[i]}$',ha='center',fontsize=10.5)
    ax.text(x,y+.145,'ReLU',ha='center',fontsize=10,color='#2e7d32')
ax.scatter(*O,s=2300,c='#c4d9fb',ec='k',zorder=2); ax.text(*O,r'$\hat y$',ha='center',va='center',fontsize=16,zorder=4)
ax.text(O[0],O[1]-.178,r'$b^{[2]}=0$',ha='center',fontsize=10.5); ax.text(O[0],O[1]+.145,'identidad',ha='center',fontsize=10,color='#1b6ca8')
for x,t in [(0,'Entrada\n$n_0=2$'),(1.6,'Capa oculta\n$n_1=2$'),(3.2,'Salida\n$n_2=1$')]: ax.text(x,1.0,t,ha='center',fontsize=11)
ax.text(.8,-.07,r'$W^{[1]}$ ($2\times2$): todos los pesos $=1$;  $b^{[1]}=(0,\,-1)^T$',ha='center',fontsize=10.5)
ax.text(2.45,-.07,r'$W^{[2]}=(1,\,-2)^T$ ($2\times1$);  $b^{[2]}=0$',ha='center',fontsize=10.5)
ax.set_xlim(-.45,3.65); ax.set_ylim(-.16,1.12); plt.tight_layout(); plt.savefig('fig_arch221.png',dpi=200); plt.close()

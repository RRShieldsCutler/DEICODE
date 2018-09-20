import pandas as pd
import numpy as np

from sklearn.metrics import mean_squared_error
from DEICODE.utils import mean_KL

#PCoA
from skbio import DistanceMatrix
from skbio.stats.ordination import pcoa
from scipy.spatial.distance import pdist, squareform

from DEICODE.utils import rclr
from DEICODE.opt_space import optspace
from fancyimpute import KNN, SoftImpute, IterativeSVD, BiScaler
from skbio.stats.composition import clr_inv
from skbio.stats.composition import closure
from skbio.stats.composition import clr
from numpy.linalg import matrix_rank

#import base truth data
base_truth=pd.read_csv('gradient_models/simulation_base_truth.csv', index_col=[0,1,2])
#import noisy and sparse data
subsampled=pd.read_csv('gradient_models/simulation_subsampled_noisy.csv', index_col=[0,1,2])

#intial dict to save results
results={}
for width_ in set(subsampled.index.get_level_values('band_width')): #iter by rank (only two)
    for depth_ in set(subsampled.index.get_level_values('sequence_depth')): #iter by overlap between clusters

        subtmp=subsampled.loc[(width_,depth_,),:].copy().T #get the data for that subset
        basetmp=base_truth.loc[(width_,depth_,),:].copy().T #get the base truth data for that subset
    
        X_sparse=rclr(subtmp.copy()) # take the robust clr transform
        U, s, V, _ =optspace(X_sparse.copy(),r=5
                             , niter=5, tol=1e-5) #fit opt-space to the r-clr data

        PCA_tmp = pcoa(DistanceMatrix(pdist(subtmp.as_matrix(), 'euclidean'),
                                    list(subtmp.index)))
        RPCA_tmp =pd.DataFrame(U,index=subtmp.index)
        RPCA_tmp = RPCA_tmp.rename(columns={0: 'PC1', 1: 'PC2'})
        PCA_tmp.samples[['PC1','PC2']].to_csv('gradient_models/ordination/'+str(width_)+'_'+str(depth_)+'_PCA.csv')
        RPCA_tmp.to_csv('gradient_models/ordination/'+str(width_)+'_'+str(depth_)+'_RPCA.csv')


        optcomp_rclr=clr_inv(U.dot(s).dot(V.T)) # recompose the completed matrix 
        X_filled_knn = clr_inv(KNN(verbose=False).fit_transform(X_sparse.copy())) # KNN fill 
        X_filled_softimpute = clr_inv(SoftImpute(verbose=False).fit_transform(X_sparse.copy())) #SoftImpute
        X_filled_iter=clr_inv(IterativeSVD(verbose=False).fit_transform(X_sparse.copy())) #Iter SVD        
        optcomp_rclr[np.isnan(optcomp_rclr)]=1 #replace any nans
        X_filled_knn[np.isnan(X_filled_knn)]=1 #replace any nans
        X_filled_softimpute[np.isnan(X_filled_softimpute)]=1 #replace any nans
        X_filled_iter[np.isnan(X_filled_iter)]=1 #replace any nans

        #calculate the KL-divergence and then fill the dict of results 
        results[(width_,depth_,'rclr-OptSpace','KL-Div')]=[mean_KL(optcomp_rclr
                                                            ,closure(basetmp))]

        results[(width_,depth_,'rclr-KNN','KL-Div')]=[mean_KL(X_filled_knn
                                                            ,closure(basetmp))]

        results[(width_,depth_,'rclr-SoftImpute','KL-Div')]=[mean_KL(X_filled_softimpute
                                                            ,closure(basetmp))]

        results[(width_,depth_,'rclr-IterativeSVD','KL-Div')]=[mean_KL(X_filled_iter
                                                            ,closure(basetmp))]             

        fancy_=np.array(subtmp.astype(float).copy())
        fancy_[fancy_==0]=np.nan
        U_, s_, V_, _ =optspace(fancy_.copy(),r=5, niter=5, tol=1e-5)
        opnew_=U_.dot(s_).dot(V_.T)
        opnew_[opnew_<1]=1
        X_filled_knn = KNN(verbose=False,min_value=1).fit_transform(fancy_.copy()) # KNN fill 
        X_filled_softimpute = SoftImpute(verbose=False,min_value=1).fit_transform(fancy_.copy()) #SoftImpute
        X_filled_iter=IterativeSVD(verbose=False,min_value=1).fit_transform(fancy_.copy()) #Iter SVD

        #calculate the KL-divergence and then fill the dict of results 
        results[(width_,depth_,'OptSpace','KL-Div')]=[mean_KL((opnew_)
                                                            ,(basetmp))]

        results[(width_,depth_,'KNN','KL-Div')]=[mean_KL((X_filled_knn)
                                                        ,(basetmp))]

        results[(width_,depth_,'SoftImpute','KL-Div')]=[mean_KL((X_filled_softimpute)
                                                                ,(basetmp))]

        results[(width_,depth_,'IterativeSVD','KL-Div')]=[mean_KL((X_filled_iter)
                                                                ,(basetmp))]

#convert the results to df to make it easier to read and plot       
results=pd.DataFrame(results).T
results.index.names = ['Band_Width','Sequence_Depth','Method','Metric']
results.columns=['value']
results.to_csv('gradient_models/results.csv')
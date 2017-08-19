from DEICODE.optspace import (G, F_t, gradF_t, Gp, getoptT, getoptS, optspace,
                              P_E)
import numpy as np
from numpy.random import randn, rand
from numpy.linalg import norm
import unittest
import numpy.testing as npt
from gneiss.util import block_diagonal
from scipy.io import loadmat
from skbio.util import get_data_path


class TestOptspace(unittest.TestCase):
    def setUp(self):
        pass

    def test_G(self):
        X = np.ones((10, 10))
        m0 = 2
        r = 2
        exp = G(X, m0, r)
        self.assertAlmostEqual(exp, 0.644944589179)

    def test_G_z_0(self):
        X = np.array([[0,.1],[4,1],[33,1]])
        m0 = 2
        r = 2
        exp = G(X, m0, r)
        self.assertAlmostEqual(exp, 2.54530786122)

    def test_F_t(self):
        X = np.ones((5, 5))
        Y = np.ones((5, 5))
        E = np.zeros((5, 5))
        E[0, 1] = 1
        E[1, 1] = 1
        S = np.eye(5)
        M_E = np.ones((5, 5)) * 6
        M_E[0, 0] = 1
        m0 = 2
        rho = 0.5
        res = F_t(X, Y, S, M_E, E, m0, rho)
        exp = 1
        self.assertAlmostEqual(res, exp)

    def test_F_t_random(self):
        #random ones and zeros
        np.random.seed(0)
        X = np.ones((5, 5))
        Y = np.ones((5, 5))
        E=np.random.choice([0, 1], size=(5,5))
        S = np.eye(5)
        M_E = np.ones((5, 5)) * 6
        M_E[0, 0] = 1
        m0 = 2
        rho = 0.5
        res = F_t(X, Y, S, M_E, E, m0, rho)
        self.assertAlmostEqual(res, 6.5)

    def test_gradF_t(self):
        X = np.ones((5, 5))
        Y = np.ones((5, 5))
        E = np.zeros((5, 5))
        E[0, 1] = 1
        E[1, 1] = 1
        S = np.eye(5)
        M_E = np.ones((5, 5)) * 6
        M_E[0, 0] = 1
        m0 = 2
        rho = 0.5

        res = gradF_t(X, Y, S, M_E, E, m0, rho)

    def test_Gp(self):
        X = np.ones((5, 5)) * 3
        X[0, 0] = 2
        m0 = 2
        r = 5
        res = Gp(X, m0, r)
        exp = np.array(
            [[1.08731273, 1.6309691, 1.6309691, 1.6309691, 1.6309691],
             [3.57804989, 3.57804989, 3.57804989, 3.57804989, 3.57804989],
             [3.57804989, 3.57804989, 3.57804989, 3.57804989, 3.57804989],
             [3.57804989, 3.57804989, 3.57804989, 3.57804989, 3.57804989],
             [3.57804989, 3.57804989, 3.57804989, 3.57804989, 3.57804989]]
            )

        npt.assert_allclose(exp, res)

    def test_getoptT(self):
        X = np.ones((5, 5))
        Y = np.ones((5, 5))
        E = np.zeros((5, 5))
        E[0, 1] = 1
        E[1, 1] = 1
        S = np.eye(5)
        M_E = np.ones((5, 5)) * 6
        M_E[0, 0] = 1
        m0 = 2
        rho = 0.5
        W, Z = gradF_t(X, Y, S, M_E, E, m0, rho)
        res = getoptT(X, W, Y, Z, S, M_E, E, m0, rho)
        exp = -0.0125
        npt.assert_allclose(exp, res)

    def test_getoptS(self):
        X = np.ones((5, 5))
        Y = np.ones((5, 5))
        E = np.zeros((5, 5))
        E[0, 1] = 1
        E[1, 1] = 1
        M_E = np.ones((5, 5)) * 6
        M_E[0, 0] = 1
        res = getoptS(X, Y, M_E, E)
        exp = np.array([[0.58, 0.58, 0.58, 0.58, 0.58],
                        [0.58, 0.58, 0.58, 0.58, 0.58],
                        [0.58, 0.58, 0.58, 0.58, 0.58],
                        [0.58, 0.58, 0.58, 0.58, 0.58],
                        [0.58, 0.58, 0.58, 0.58, 0.58]])
        npt.assert_allclose(res, exp)

    def test_getoptS_small(self):
        # warning : this test must ALWAYS pass
        data = loadmat(get_data_path('small_test.mat'))

        M_E = np.array(data['M_E'].todense())
        E = data['E']

        x = data['x']
        y = data['y']
        res = getoptS(x, y, M_E, E)
        exp = np.array([[ 0.93639499, 0.07644197, -0.02828782],
                        [-0.03960841, 0.60787383, 0.00521257],
                        [ 0.00729038, 0.00785834, 0.67853083]])
        npt.assert_allclose(res, exp, atol=1e-5)

    def test_getoptS_rect(self):
        X = np.ones((5, 5))
        Y = np.ones((10, 5))
        E = np.zeros((5, 10))
        E[0, 1] = 1
        E[1, 1] = 1
        M_E = np.ones((5, 10)) * 6
        M_E[0, 0] = 1
        res = getoptS(X, Y, M_E, E)
        exp = np.array([[ 1.18,  1.18,  1.18,  1.18,  1.18],
                        [ 1.18,  1.18,  1.18,  1.18,  1.18],
                        [ 1.18,  1.18,  1.18,  1.18,  1.18],
                        [ 1.18,  1.18,  1.18,  1.18,  1.18],
                        [ 1.18,  1.18,  1.18,  1.18,  1.18]])
        npt.assert_allclose(res, exp)

    def test_P_E(self):
        x = np.array([1., 2., 0., 4.])
        y = P_E(x)
        exp_y = np.array([1, 2, 1.5, 4])
        npt.assert_allclose(y, exp_y)

    def test_optspace_no_noise_small(self):
        np.random.seed(0)

        n = 10
        m = 10
        r = 3
        tol = 1e-8

        eps = r*np.log10(n);

        U = randn(n, r)
        V = randn(m, r)
        Sig = np.eye(r)
        M0 = U.dot(Sig).dot(V.T)

        E = 1 - np.ceil( rand(n, m) - eps/np.sqrt(m*n)  )

        M_E = np.multiply(M0, E)
        X, S, Y, dist = optspace(M_E, r=3, niter=10, tol=tol)

        exp_X = np.array([[-8.79865705e-01, 5.80137539e-01, -2.11945417e+00],
                          [2.41254717e+00, -4.15135158e-02, -8.08590887e-02],
                          [9.54706347e-01, 6.53315999e-01, -7.83143452e-01],
                          [-1.26239471e-01, -1.15034917e-01, -6.73104191e-02],
                          [-4.75788895e-04, -1.83763198e-03, 1.77844164e-03],
                          [9.86004154e-01, 1.38993763e+00, 3.02042515e-01],
                          [4.30368032e-03, 1.66220416e-02, -1.60866433e-02],
                          [8.92420611e-01, 3.16881628e-01, 2.81385102e-01],
                          [1.72236780e-01, 1.34451853e+00, -1.60799313e+00],
                          [-8.24468845e-01, 2.31976548e+00, 1.45849936e+00]])

        exp_S = np.array([[-0.026053,  0.017146, -0.000697],
                           [-0.325643, -0.027534, -0.174478],
                           [-0.030218,  0.062173,  0.025056]])

        exp_Y = np.array([[0.13823077, -0.02226359, 0.16660621],
                          [-0.16332081, -1.83297345, 2.44195478],
                          [0.48775225, 0.12243485, 0.09789257],
                          [0.77352332, -1.52764724, -0.86834177],
                          [1.10757851, 1.45958719, 1.71390276],
                          [-0.42845364, -0.85749063, -0.28152323],
                          [-2.41851741, -0.17623352, 0.19516526],
                          [1.360709, -1.1687075, -0.39642448],
                          [-0.03081843, -0.1683746, 0.18097424],
                          [-0.07726637, -0.00677196, 0.02805902]])

        exp_dist = np.array([1.04939, 1.04939, 1.04939, 1.04939,
                             1.04939, 1.04939, 1.04939, 1.04939,
                             1.04939, 1.04939, 1.04939])

        npt.assert_allclose(X, exp_X, atol=1e-5)
        npt.assert_allclose(S, exp_S, atol=1e-5)
        npt.assert_allclose(Y, exp_Y, atol=1e-5)
        npt.assert_allclose(dist, exp_dist, atol=1e-5)


    def test_optspace_noisy_small_noise(self):
        np.random.seed(0)

        n = 20
        m = 10
        r = 3
        tol = 1e-8

        eps = r*np.log10(n);
        U = randn(n, r)
        V = randn(m, r)
        Sig = np.eye(r)
        M0 = U.dot(Sig).dot(V.T)

        # add some noise (.001 is noise amplitude)
        err = .001 * np.ones_like(M0)
        i = np.random.randint(0, err.shape[0], 5000)
        j = np.random.randint(0, err.shape[1], 5000)
        err[i, j] = .0001
        M0 = abs(np.random.normal(M0, err))

        #sparcity
        E = 1 - np.ceil( rand(n, m) - eps/np.sqrt(m*n)  )
        M_E = np.multiply(M0, E)

        X, S, Y, dist = optspace(M_E, r=3, niter=10, tol=tol)

        exp_X=np.array([[-0.26134281, -0.41393434, 0.11403524],
                        [-0.36609965,  1.21811109, 2.95791077],
                        [-0.14474412, -0.67538941, 0.21050033],
                        [ 0.68803887,  0.42471769, 1.41160298],
                        [ 0.97182945, -0.1118488,  0.13085956],
                        [-0.17368144, -0.27508969, 0.07578477],
                        [-0.27047183, -0.43171811, 0.12821394],
                        [-0.1135297,  -0.17947632, 0.05574364],
                        [ 4.0901963,  -0.96071107, 0.74072681],
                        [-0.19701012,  0.48167355, 1.14591719],
                        [-0.25295422,  0.39408504, 1.18878877],
                        [-0.69441878, -2.62017853, 0.80837871],
                        [-0.26041274,  0.63668773, 1.51470101],
                        [-0.44400625,  0.12780867, 1.2857783 ],
                        [ 0.03207322, -0.02150631, 0.3029942 ],
                        [-0.04795981, -0.0146558,  0.06633133],
                        [-0.79011987, -2.90133905, 1.06238611],
                        [-0.11137632, -0.14576371, 0.11956169],
                        [-0.14626283, -0.60152865, 0.20338137],
                        [-0.03958251, -0.05197697, 0.04291738]])

        exp_S= np.array([[ 0.62433487,  1.48690764,  0.88114666],
                         [ 0.02594646,  0.01457821,  0.03445409],
                         [-0.07239248, -0.06171197, -0.02125931]])

        exp_Y=[[-0.39595047, -0.6587885,  0.57826609],
               [-0.02088513, -0.02779878, 0.0123531 ],
               [ 0.24141507, -0.02192573, 0.02413501],
               [-0.0798941,  -0.17471797, 0.09384464],
               [ 3.03947516, -0.46676993, 0.5861467 ],
               [-0.39323852, -0.7891716,  0.23111203],
               [-0.12375933,  0.02516122, 0.25897812],
               [-0.36754715,  1.13858948, 2.87973405],
               [-0.45989274, -2.71894255, 0.90093003],
               [ 0.15221148,  0.06232314, 0.29575815]]

        exp_dist=np.array([2.85982659, 2.85982646, 2.85982633, 2.8598262,
                           2.85982607, 2.85982593, 2.8598258,  2.85982567,
                           2.85982554, 2.85982541, 2.85982528])

        npt.assert_allclose(X, exp_X, atol=1e-5)
        npt.assert_allclose(S, exp_S, atol=1e-5)
        npt.assert_allclose(Y, exp_Y, atol=1e-5)
        npt.assert_allclose(dist, exp_dist, atol=1e-5)

    def test_optspace_rect(self):
        np.random.seed(0)

        n = 20
        m = 10
        r = 3
        tol = 1e-8

        eps = r*np.log10(n);

        U = randn(n, r)
        V = randn(m, r)
        Sig = np.eye(r)
        M0 = U.dot(Sig).dot(V.T)

        E = 1 - np.ceil( rand(n, m) - eps/np.sqrt(m*n)  )
        M_E = np.multiply(M0, E)
        X, S, Y, dist = optspace(M_E, r=3, niter=10, tol=tol)

        exp_X = np.array([[  0.00000000e+00,   0.00000000e+00,   0.00000000e+00],
                          [ -1.24892755e+00,   5.88144728e-01,   3.18387947e+00],
                          [  0.00000000e+00,   0.00000000e+00,   0.00000000e+00],
                          [ -7.63136433e-01,  -1.98094129e-01,   1.80647747e+00],
                          [  4.05329760e-02,   5.87627252e-02,   4.70863349e-02],
                          [  4.94528191e-01,   1.61195228e+00,   1.62518238e+00],
                          [  1.33212104e+00,   5.44980483e-01,  -1.95348224e-01],
                          [  9.49694012e-01,   8.22714305e-01,   1.02216976e+00],
                          [  1.61988963e+00,  -3.66564079e+00,   1.54640216e+00],
                          [ -8.94818034e-01,  -2.82148981e-01,  -1.45854340e-01],
                          [ -3.83365000e-02,  -3.75112372e-02,  -5.02019854e-02],
                          [ -1.81994286e+00,  -7.32909404e-01,  -2.53509729e-01],
                          [  2.25401679e+00,   9.89076672e-01,   2.70043810e-01],
                          [  1.71295204e-01,  -2.32540544e-01,   5.98892258e-02],
                          [  2.74366648e-01,   3.18456561e-01,   2.65223065e-01],
                          [  4.19583079e-01,  -5.15096351e-01,   1.49644625e-01],
                          [ -1.12150992e-01,   5.00684838e-02,  -4.28622725e-04],
                          [  1.51729245e+00,  5.82858430e-01,   1.95268698e-01],
                          [  1.03817652e-01,   1.69187705e-01,  -3.24675239e-02],
                          [  7.14100851e-01,  -4.62712815e-01,  -4.30432263e-01]])

        exp_S = np.array([[0.00000000e+00, 1.85550119e-01, 0.00000000e+00],
                         [-9.62508393e-48, 1.25410283e-01, 0.00000000e+00],
                         [0.00000000e+00, -1.34288448e+00, 0.00000000e+00]])

        exp_Y = np.array([[-0.47458205, -0.15117831, -0.03750719],
                          [ 0.08870875,  0.14503068,  0.08960488],
                          [-0.48638819,  1.71614626, -1.38156126],
                          [-0.20044288,  0.43704371, -0.10685386],
                          [ 1.09411935, -1.78957477,  0.62180472],
                          [ 0.3292932,  -0.15750601, -0.26225341],
                          [ 0.66740927,  0.21048231, -0.31906342],
                          [ 2.34342552,  0.96412366,  0.52283276],
                          [-0.93584522,  1.05607652,  2.68589675],
                          [-1.17121138, -1.2261424, -0.16068614]])


        exp_dist = np.array([2.017845, 2.017845, 2.017845, 2.017845, 2.017845,
                             2.017845, 2.017845, 2.017845, 2.017845, 2.017845,
                             2.017845])

        npt.assert_allclose(X, exp_X, atol=1e-5)
        npt.assert_allclose(S, exp_S, atol=1e-5)
        npt.assert_allclose(Y, exp_Y, atol=1e-5)
        npt.assert_allclose(dist, exp_dist, atol=1e-5)

    def test_optspace_original(self):
        M0 = loadmat(get_data_path('dense_opttest.mat'))['M0'].astype(np.float)
        M_E = loadmat(get_data_path('sparse_opttest.mat'))['M_E'].astype(np.float)

        M_E = np.array(M_E.todense())
        X, S, Y, dist = optspace(M_E, r=3, niter=1, tol=1e-8)
        err = X.dot(S).dot(Y.T) - M0
        n, m = M0.shape

        print(norm(err, 'fro') / np.sqrt(m*n))


if __name__ == "__main__":
    unittest.main()


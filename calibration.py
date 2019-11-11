import numpy as np
import math
from random import sample   

#Read the input first
#matrix_2D_a = read_matrix.matrix('input/pts2d-pic_a.txt')
#matrix_2D_b = read_matrix.matrix('input/pts2d-pic_b.txt')

def get_matrix(rand_list, matrix_3D, matrix_2D, matrix_3D_M, matrix_2D_M):
    for j in rand_list:
        matrix_3D_M = np.vstack((matrix_3D_M, matrix_3D[j]))
        matrix_2D_M = np.vstack((matrix_2D_M, matrix_2D[j]))
    matrix_3D_M = np.delete(matrix_3D_M , (0), axis=0)
    matrix_2D_M = np.delete(matrix_2D_M , (0), axis=0)
    return matrix_3D_M, matrix_2D_M

def A_matrix(u, v, u_1, v_1):
    #Define the A matrix
    A = [
         [u_1*u, u_1*v, u_1, v_1*u, v_1*v, v_1, u, v, 1]
        ]
    return A

def testing(matrix_2D_b, matrix_2D_a, f, row_count):
    #Add one to the matrix
    extra = [
             [1]
            ]
    for i in range(0, len(matrix_2D_a[:, 0])-1):
        extra = np.concatenate((extra, [[1]]), axis=0)

    matrix_2D_a = np.append(matrix_2D_a, extra, axis  = 1)
    matrix_2D_b = np.append(matrix_2D_b, extra, axis = 1)

    first_row_a = matrix_2D_a[row_count] #Change the row count if wantted to test other points
    first_row_b = matrix_2D_b[row_count]

    first_row_a.resize(3,1)

    matrix_1 = np.dot(first_row_b, f)
    result = np.dot(matrix_1, first_row_a)
    return result


def residual(matrix_2D_b, matrix_2D_a, f):
    residual = 0
    #Find the predicted points
    for i in range(0, len(matrix_2D_a[:, 0])):
        assumption = testing(matrix_2D_b, matrix_2D_a, f, i)
        real = 0
        residual += math.pow(real - assumption[0], 2)
        residual = math.sqrt(residual)

    return residual


def appending(matrix_2D_a, matrix_2D_b):
    #Define the zero matrix
    Z = [
         [0]
        ]
    current = None
    for i in range(0, len(matrix_2D_a[:, 0])):

        x_1 = matrix_2D_a[i, 0]
        y_1 = matrix_2D_a[i, 1]


        u_1 = matrix_2D_b[i, 0]
        v_1 = matrix_2D_b[i, 1]
        
        if i < 1:
            A = A_matrix(x_1, y_1, u_1, v_1)
        else:
            A_part = A_matrix(x_1, y_1, u_1, v_1)
            A = np.concatenate((A, A_part), axis=0)
            Z = np.concatenate((Z, [[0]]), axis=0)
    #Got SVD
    U, sigma, VT = np.linalg.svd(A)
    # print(VT)
    f = VT[8]
    f.resize(3,3)
    # print(f)
    return f

#f = appending(matrix_2D_a, matrix_2D_b)

#residual(matrix_2D_b, matrix_2D_a, f)
#print(residual(matrix_2D_b, matrix_2D_a, f))


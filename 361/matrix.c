#include <stdlib.h>
#include <stdio.h>
#include <time.h>

struct DenseMatrix {
    int num_rows;
    int num_cols;
    float **data;
};

void print_dense_matrix(struct DenseMatrix *matrix) {
    int i,j;
    for (i=0 ; i<matrix->num_rows ; i++) {
        for (j=0 ; j<matrix->num_cols ; j++) {
            printf("%f ",matrix->data[i][j]);
        }
        printf("\n");
    }
}

struct Coordinate {
    int row;
    int col;
    float value;
};

struct COOMatrix {
    /* Coordinate Matrix */
    int num_non_zero;
    struct Coordinate *coords;
};

/* coordinate matrix:
   79.000000 0.000000 
    0.000000 45.000000
    0.000000 0.000000 
    [ (0,0,79.0), (2,1,45) ]
   coordinate matrix is an array of element triples*/

void dense_matrix_to_coo(struct DenseMatrix *dense_matrix, struct COOMatrix *coo_matrix) {
    int num_non_zero = 0;
    int i, j;
    for (i=0 ; i<dense_matrix->num_rows ; i++) {
        for (j=0 ; j<dense_matrix->num_cols ; j++) {
            if (dense_matrix->data[i][j] == 0) {
                num_non_zero++;
            }
        }
    }
}

void init_dense_matrix_random(struct DenseMatrix *matrix) {
    /* populate existing matrix with values 0 to 99 
        want ratio of 0 to non-zero values to be 1:4*/
    int i, j;
    for (i=0 ; i<matrix->num_rows ; i++) {
        for (j=0 ; j<matrix->num_cols ; j++) {
            if (rand() % 4 != 0) {
                matrix->data[i][j] = 0;
            }
            else {
                matrix->data[i][j] = (float)(rand() % 100);
            }
        }
    }
}

int main(void) {
    srand(time(NULL));

    struct DenseMatrix matrix;
    matrix.num_rows = 3;
    matrix.num_cols = 2;

    matrix.data = malloc(matrix.num_rows * sizeof(float*));
    
    int i;
    for (i=0 ; i<matrix.num_rows ; i++) {
        matrix.data[i] = malloc(matrix.num_cols * sizeof(float));
    }

    int j;
    /*
    for (i=0 ; i<matrix.num_rows ; i++) {
        for (j=0 ; j<matrix.num_cols ; j++) {
            matrix.data[i][j] = i*matrix.num_cols + j + 1;
        }
    }
    */
    init_dense_matrix_random(&matrix);

    print_dense_matrix(&matrix);

    float sum = 0;
    for (i=0 ; i<matrix.num_rows ; i++) {
        for (j=0 ; j<matrix.num_cols ; j++) {
            sum += matrix.data[i][j];
        }
    }

    printf("\nsum = %f\n",sum);

    return 0;
}
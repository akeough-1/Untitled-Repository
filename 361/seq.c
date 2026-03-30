/* Requirements:
    accept -d for double precision, otherwise single
    generate the first n terms of given sequence and starting vals
    use n = 10 if single precision, n = 20 if double
    exact converges to 6
    print out the n terms, one per line

    x_{k+1} = 111 - (1130 - 3000/x_{k-1})/x_k
    x1 = 11/2
    x2 = 61/11
    
   Algorithm:
    check number of inputs, should be one (no flag) or two (flag)
    if second input, check that exactly "-d"
    if -d, everything is type double
    else, everything is type float
    basically have two different programs lol could put them in funcs?
    */

#include <stdio.h>

void fseq(void) {
    float x[10];
    x[0] = 11.0/2.0;
    x[1] = 61.0/11.0;

    int n;
    for (n = 1 ; n < 9 ; n++) {
        x[n+1] = 111 - (1130 - 3000/x[n-1])/x[n];
    }
   
    for (n=0 ; n<10 ; n++) {
        printf("%f\n",x[n]);
    }
}

void dseq(void) {
    double x[20];
    x[0] = 11.0/2;
    x[1] = 61.0/11.0;

    int n;
    for (n = 1; n < 19 ; n++) {
        x[n+1] = 111 - (1130 - 3000/x[n-1])/x[n];
    }

    for (n=0 ; n<20 ; n++) {
        printf("%lf\n",x[n]);
    }
}

int main(int argc, char **argv){
    if (argc > 2) {
        printf("INPUT ERROR (1): Too many command line inputs.\n");
        return 1;
    }

    if (argc == 1) {
        fseq();
    }
    /* literally strcmp */
    else if (argv[1][0] == '-' && argv[1][1] == 'd' && argv[1][2] == '\0') {
        dseq();
    }
    else {
        printf("INPUT ERROR (1): Invalid input.\n");
        return 1;
    }

    return 0;
}
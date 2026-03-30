/* Requirements:
    Solve a quadratic equation using standard formula and/or alternative
    input coefficients a, b, and c from command line
    output both roots
    detect when roots are imaginary, but don't need to do complex arithmatic
    guard against overflow, underflow, and cancellation
    make robust given unusual input values?
    compute any root within floating-point range, even if other is out of range
    
  Ideas:
    scale coefficients relative to largest where largest becomes 1
    create user-defined functions for each of the two formulas
    check what happens when atof is given non-double
    
  Algorithm:
    Input coefficients from the command line
    check that they can be converted to type double (64-bit)
      - output an error 1 describing which input failed
    determine which input is the largest
    divide all three inputs by the largest input
    call quadratic forumla function based on sign of b (?)
    return solved roots
    
    Normal quad:
        recieve three coeficients as doubles
        evaluate formula with + -> first root
        evaluate formula with - -> second root
        for now, just return the two roots
        
    Input check:
        recieve coefficient char array (string) and pointer to new double
        check if string is just '0' -> set double to 0.0
        ELSE: use atof -> double
          - now if this one == 0.0, then atof failed
        if success, set new pointer to atof double or 0.0
        return 0 for success and error value for error
*/

#include <stdio.h>
#include <stdlib.h>
#include <float.h>
#include <math.h>

int convert_input(char *input_str, double *out_ptr) {
    /* input char string and output address 
       return error status: 0 for success */
    double out;

    /* check if string is exactly "0": \0 signifies end */
    if (input_str[0] == '0' && input_str[1] == '\0') {
        out = 0.0;
    }

    else {
        out = atof(input_str);
        /* check if string is invalid, too large, or too small */
        if (out == 0.0 || fabs(out) > DBL_MAX || fabs(out) < DBL_MIN) {
            return 2;
        }
    }

    *out_ptr = out;
    return 0;
}

double plus_norm_quad(double a, double b, double c) {
    return (-b + sqrt(pow(b,2) - 4*a*c))/(2*a);
}

double minus_norm_quad(double a, double b, double c) {
    return (-b - sqrt(pow(b,2) - 4*a*c))/(2*a);
}

double plus_alt_quad(double a, double b, double c) {
    return (2*c)/(-b + sqrt(pow(b,2) - 4*a*c));
}

double minus_alt_quad(double a, double b, double c) {
    return (2*c)/(-b - sqrt(pow(b,2) - 4*a*c));
}

int main(int argc, char **argv) {
    if (argc != 4) {
        printf("INPUT ERROR (1): Incorrect number of inputs.\n");
        return 1;
    }
    
    double a,b,c;
    double *in_ptr;
    int err,i;
    /* run the input verification function for each coefficient*/
    for (i=1 ; i<=3 ; i++) {
        switch (i) {
            case 1: in_ptr = &a; break;
            case 2: in_ptr = &b; break;
            case 3: in_ptr = &c; break;
        }
        err = convert_input(argv[i],in_ptr);

        if (err != 0) {
            printf("VALUE ERROR (%d): Input %d could not be converted to double.\n",err,i);
            return err;
        }
    }

    /* check if system is first degree */
    if (a == 0) {
        printf("Root = %.20lf\n",-c/b);
        return 0; /* technically a success :) */
    }

    /* scale the inputs based on the largest */
    double scale;
    double Aa = fabs(a);
    double Ab = fabs(b);
    double Ac = fabs(c);
    if (Aa > Ab && Aa > Ac) {
        scale = Aa;
    }
    else if (Ab > Aa && Ab > Ac) {
        scale = Ab;
    }
    else if (Ac > Aa && Ac > Ab) {
        scale  = Ac;
    }
    /* use this if the magnitudes are all equal */
    else {
        scale = 1;
    }
    a /= scale;
    b /= scale;
    c /= scale;

    /* check if inside the sqrt will be negative */
    if (pow(b,2) - 4*a*c < 0) {
        printf("SOLVER ERROR (3): Imaginary roots.\n");
        return 3;
    }

    double Nroot1 = plus_norm_quad(a,b,c);
    double Nroot2 = minus_norm_quad(a,b,c);
    printf("Normal Roots = %.20lf, %.20lf\n",Nroot1,Nroot2);

    double Aroot1 = minus_alt_quad(a,b,c);
    double Aroot2 = plus_alt_quad(a,b,c);
    printf("Alt Roots = %.20lf, %.20lf\n",Aroot1,Aroot2);

    return 0;
}
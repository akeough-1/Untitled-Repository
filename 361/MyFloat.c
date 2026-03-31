/* Requirements:
    Implement my own floating point data-type, MyFloat
    declare struct for MyFloat with three data items:
      - variable sign-bit (always one bit)
      - dynamic exponent array
      - dynamic significand array
    accept number of exponent bits, significand bits, and decimal
      number to be stored
    program outputs the representation in the new format 
    
   Algorithm:
    accept exactly 3 (4 total) inputs from command line
    check that first two inputs are int
    check that third input is valid
      - zero or one decimal
      - zero or one minus sign
      - zero or one e
      - before and after decimal are type long int?
          (or at least only have type int inside)

    if minus sign at beginning, sign bit =1 otherwise =0
          
    needed exponent = log2(value * 10^(e...))
      - can be negative
    calculate max exponent:
      - unsigned int: 2^(exp bits) - 1
      - divide by 2 (round down) - this is reference exp
      - max exp = unsigned int val - ref
      - maximum value = (2 - 2^(-signifcand ary len)) * 2^(max exp)
      - IF above max, return err unrepresentable
    minimum exponent = 2 * (1 - ref_exp)
      - minimum value = 2^(min_exp)
      - if input is smaller, use denormalized form
      - minimum denorm = 2^(-signifcand array length) * 2^(min exp)
      - if input is smaller, return err unrepresentable
    
    if normalized, divide input by 2^(needed exp)
      - should be 1.something
      - convert "something" to binary using frac method
    if denormalized, set exp to all 00000
      - divide input by 2^(min exp (should be negative))
      - should be 0.something
      - convert "something to binary using frac method"

   Functions:
    
*/

#include <stdio.h>
#include <stdlib.h>
#include <limits.h>
#include <errno.h>
#include <math.h>

struct MyFloat {
    char sign;
    char *exponent;
    char *significand;
};

int str2int(char *input_str, int *out_ptr) {
    /* input char array and destination address 
        return error status: 0 for success 
        error map:
        1: negative sign
        2: not int
        3: too big
    */
    
    unsigned long out;
    char *endp;

    /* check if there's a cheeky negative sign (bad) */
    if (input_str[0] == '-') {
        return 1;
    }

    /* check if str is exactly 0 */
    if (input_str[0] == '0' && input_str[1] == '\0') {
        out = 0;
    }
    else {
        out = strtoul(input_str,&endp,10);
        
        /* this checks if there's non int at beginning || end */
        if (out == 0 || *endp != '\0') {
            return 2;
        }

        /* check if int is out of range (set by strtoul)*/
        if (errno == ERANGE) {
            return 3;
        }
    }

    *out_ptr = out;
    return 0;
}

int main(int argc, char **argv) {
    /* check that there are the exact number of inputs */
    if (argc != 4) {
        printf("INPUT ERROR (1): incorrect number of inputs.\n");
        return 1;
    }

    int exp_bits, sig_bits;
    int *in_ptr;
    int err, i;
    /* run int converter for first two inputs - stores values automatically */
    for (i=1 ; i<=2 ; i++) {
        switch (i) {
            case 1: in_ptr = &exp_bits; break;
            case 2: in_ptr = &sig_bits; break;
        }

        err = str2int(argv[i],in_ptr);

        switch (err) {
            case 1: 
            printf("ARGUMENT ERROR (2): arg %d must be positive.\n",i); return 2;
            case 2:
            printf("ARGUMENT ERROR (2): arg %d must be type int.\n",i); return 2;
            case 3:
            printf("ARGUMENT ERROR (2): arg %d is too large.\n",i); return 2;
        }
    }

    /* initialize MyFloat struct */
    struct MyFloat floaty;

    /* check if 3rd input is 0 */
    double value;
    char *endp;

    /* check if str is exactly 0 */
    if (argv[3][0] == '0' && argv[3][1] == '\0') {
        value = 0;
    }
    else {
        value = strtod(argv[3],&endp);
        
        /* this checks if there's non int at beginning || end */
        if (value == 0 || *endp != '\0') {
            printf("ARGUMENT ERROR (2): arg 3 must be type double.\n");
            return 2;
        }

        /* check if int is out of range (set by strtod)*/
        if (errno == ERANGE) {
            printf("ARGUMENT ERROR (3): arg 3 is outside of bounds.\n");
        }
    }
    printf("DEBUG: value = %lf\n",value);

    /* calculate the necesary exponent value to fit given
       always round down */
    int needed_exp = (int)log2(value);

    /* calculate the maximum available exponent */
    int max_bin = pow(2,exp_bits) - 1;
    int ref_exp = max_bin/2;
    int max_exp = max_bin - ref_exp;

    double max_val = (2 - pow(2,-sig_bits)) * pow(2,ref_exp);

    /* stop if the given value is greater than the maximum representable value */
    if (value > max_val) {
        printf("VALUE ERROR (3): value %lf is too big to fit in given structure.\n",value);
        return 3;
    }

    /* set the status of normalized to true*/
    int normalized = 0;

    int min_exp = 2 * (1 - ref_exp);
    double min_val = pow(2,min_exp);

    if (value < min_val) {
        normalized = 1;
        min_val = pow(2,-sig_bits) * pow(2,min_exp);

        if (value < min_val) {
            printf("VALUE ERROR (3): value %lf is too small to fit in given structure.\n",value);
            return 3;
        }
    }

    /*
    if normalized, divide input by 2^(needed exp)
      - should be 1.something
      - convert "something" to binary using frac method
    if denormalized, set exp to all 00000
      - divide input by 2^(min exp (should be negative))
      - should be 0.something
      - convert "something to binary using frac method"
    */

    return 0;
}
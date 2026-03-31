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

    /* set sign var in struct */
    int str_start;
    if (argv[3][0] == '-') {
        floaty.sign = '1';
        str_start = 1;
    }
    else {
        floaty.sign = '0';
        str_start = 0;
    }

    /* set up a for loop for each char in argv3 */

    int dec_ind = -1;
    int minus_ind = -1;
    int exp_ind = -1;

    /* start at the second index if there's a negative sign in front */
    i = str_start;
    while (argv[3][i] != '\0') {
        switch (argv[3][i]) {
            /* numbers are ok just pass */
            case '0': case '1': case '2': case '3': case '4':
            case '5': case '6': case '7': case '8': case '9':
            break;

            /* set location of decimal, or return err if more than one */
            case '.':
            if (dec_ind != -1) {
                printf("ARGUMENT ERROR (2): arg 3 has too many \'.\'\n");
                return 2;
            }
            else {
                dec_ind = i;
                break;
            }
            
            /* set location of exponent, or return err if more than one */
            case 'e':
            if (exp_ind != -1) {
                printf("ARGUMENT ERROR (2): arg 3 has too many \'e\'\n");
                return 2;
            }
            else {
                exp_ind = i;
                break;
            }

            /* any other char is invalid at this point (including -)*/
            default:
            printf("ARGUMENT ERROR (2): arg 3 has invalid character \'%c\'\n",argv[3][i]);
            return 2;
        }

        i++;
    }

    /* define the number of chars in input array */
    int str_len = i;

    printf("DEBUG: dec loc = %d\n",dec_ind);
    printf("DEBUG: exp loc = %d\n",exp_ind);
    printf("DEBUG: str len = %d\n",str_len);

    

    return 0;
}
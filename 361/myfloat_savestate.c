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
    int j = 0;
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
                dec_ind = j;
                break;
            }
            
            /* set location of exponent, or return err if more than one */
            case 'e':
            if (exp_ind != -1) {
                printf("ARGUMENT ERROR (2): arg 3 has too many \'e\'\n");
                return 2;
            }
            else {
                exp_ind = j;
                break;
            }

            /* any other char is invalid at this point (including -)*/
            default:
            printf("ARGUMENT ERROR (2): arg 3 has invalid character \'%c\'\n",argv[3][i]);
            return 2;
        }

        i++;
        j++;
    }

    /* define the number of chars in input array */
    int str_len = j;

    /*
    printf("DEBUG: dec loc = %d\n",dec_ind);
    printf("DEBUG: exp loc = %d\n",exp_ind);
    printf("DEBUG: str len = %d\n",str_len);
    */

    /* if exp_ind still -1, then there is none */
    int exp_val;
    if (exp_ind == -1) {
        /* set this to the string length for when it's compared to later */
        exp_ind = str_len;
        exp_val = 0;
    }

    /* otherwise convert the exp array to an int */
    else {
        int size = str_len - 1 - exp_ind;
        char *exp_str = malloc(size);
        for (i=0 ; i<size ; i++) {
            /* get the right index from the input str (account for - and e)*/
            j = exp_ind + 1 + i + str_start;
            exp_str[i] = argv[3][j];
        }
        exp_val = atoi(exp_str);
        free(exp_str);
    }
    printf("DEBUG: exp val = %d\n",exp_val);

    int int_val;
    double frac_val;

    /* if dec_ind still -1, then no fraction component */
    if (dec_ind == -1) {
        frac_val = 0;
        
        int size = exp_ind;
        char *int_str = malloc(size);
        for (i=0 ; i<size ; i++) {
            j = str_start + i;
            int_str[i] = argv[3][j];
        }
        int_val = atoi(int_str);
        free(int_str);
    }

    /* otherwise there definitely is a fraction component */
    else {
        int int_size = dec_ind;
        char *int_str = malloc(int_size);
        for (i=0 ; i<int_size ; i++) {
            j = str_start + i;
            int_str[i] = argv[3][j];
        }
        int_val = atoi(int_str);
        free(int_str);

        int frac_size = exp_ind - dec_ind - 1;
        char *frac_str = malloc(frac_size+2);
        frac_str[0] = '0';
        frac_str[1] = '.';
        for (i=0 ; i<frac_size ; i++) {
            j = str_start + dec_ind + 1 + i;
            frac_str[i+2] = argv[3][j];
            /* printf("DEBUG: crnt char = %c\n",frac_str[i+2]); */
        }
        frac_val = atof(frac_str);
        free(frac_str);
    }

    printf("DEBUG: int val = %d\n",int_val);
    printf("DEBUG: frac val = %lf\n",frac_val);

    double value = ((double)int_val + frac_val) * pow(10,exp_val);
    printf("DEBUG: value = %lf\n",value);
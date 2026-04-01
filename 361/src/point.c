#include <math.h>
#include "point.h"

double compute_distance(struct Point *p1, struct Point *p2) {
/* Return distance between two points 
    sqrt(difference in y squared plus difference in x squared) */
    return sqrt(pow(p2->y - p1->y,2) + pow(p2->x - p1->x,2));
}

void set_to_origin(struct Point *p) {
    /* sets point to origin (0,0) */
    p->x = 0;
    p->y = 0;
    /* needs to be pointer because otherwise the local copy of p will be thrown out */
}
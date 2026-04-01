#include <stdio.h>
#include <math.h>

/* define a point */
struct Point {
    double x;
    double y;
};

/* define a rectangle */
struct Rectangle {
    struct Point lwr_left;
    double height, width;
};

/* make function prototypes */

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

double compute_area(struct Rectangle *rect) {
    return rect->height * rect->width;
}

int main() {
    /* write test cases */
    struct Point p1 = {1,1};
    struct Point p2 = {3,3};

    double dist = compute_distance(&p1,&p2);
    printf("distance = %f\n",dist);

    set_to_origin(&p1);
    printf("x = %f, y = %f\n",p1.x,p1.y);

    struct Rectangle rect = {p1,5,5};
    double area = compute_area(&rect);
    printf("area = %f\n",area);

    return 0;
}
#ifndef POINT_H
#define POINT_H

struct Point {
    double x;
    double y;
};

double compute_distance(struct Point *p1, struct Point *p2);

void set_to_origin(struct Point *p);

#endif
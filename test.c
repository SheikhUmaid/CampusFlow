// swap two variables withut using 3rd variable


#include <stdio.h>



void main()
{
    int a = 10, b = 20;
    printf("Before swapping: a = %d, b = %d\n", a, b);
    a = a + b;
    b = a - b;
    a = a - b;
    printf("After swapping: a = %d, b = %d\n", a, b);
}



#include <stdio.h>
#include <string.h>


    void fkthis(int *v){
        int i;
        for (i= 0; i<4; ++i){
            printf("v[%d] = %d\n", i, v[i]);
        }
    }

int main() {
    int data[4]; 
    data[0] = 1;
    data[1] = 3;
    data[2] = 5;
    data[3] = 7;

    fkthis(data); 

    char *new = (char*)data;
    new++; 
    int *newnew = (int*)new;
    
    fkthis(newnew);
    return 0;
}

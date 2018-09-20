// Linked list interface ... COMP9024 18s2
#include <stdbool.h>

typedef struct Node *List;

List insertLL(List, int);
List deleteLL(List, int);
bool inLL(List, int);
void freeLL(List);
void showLL(List);
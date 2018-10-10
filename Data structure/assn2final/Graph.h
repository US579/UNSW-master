// Graph ADT interface ... COMP9024 18s2
#include <stdbool.h>
#define WHITE   0
#define GREY    1
#define BLACK   2

typedef struct GraphRep *Graph;

// vertices are ints
typedef int Vertex;

// edges are pairs of vertices (end-points)
typedef struct Edge {
   Vertex v;
   Vertex w;
} Edge;


typedef struct Path{
    int len;
    int nNext;
    int *next;
}Path;

typedef struct Node{
    int *next;
    int outdegree;
}Node;

Graph newGraph(int);
void  insertEdge(Graph, Edge);
void  freeGraph(Graph);
void findPath(Graph g, Path *paths);
void printG(Graph g,int *divisor,int len);
int numOfVertices(Graph g);
bool adjacent(Graph g, Vertex v, Vertex w);

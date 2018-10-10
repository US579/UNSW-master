#include<stdio.h>
#include<stdlib.h>
#include<math.h>
#include"queue.h"
#include"Graph.h"
#include "stack.h"
#define MAX_NODES  1000
#define initial_number 0

/*
* for Task A, in the worst case,it will have O(n^2) connections ,and examine every connections will cost O(m^2),
* hence the time complexity is O((nm)^2).
* for TaskB, the time complexity is O(n^2) in the worst case,which means each divisors related to the others,and also it will takes O(E)
* to examines each edge,and there are O(n^2) edges in total in the worst case;
*/
int visited[MAX_NODES][MAX_NODES];
int pathss[MAX_NODES][MAX_NODES];
int LLpathss[MAX_NODES][MAX_NODES];
int n = initial_number;



//funtion to find all divisor and store all in a queue
int *find_divisor(int v, int *len){
    queue q = newQueue();
    QueueEnqueue(q,1);
    int i;
    for (i = 2; i <= v;i++){
        if (v % i == 0){
            QueueEnqueue(q,i);
        }
    }
    *len = QueueLen(q);
    int *divisor = malloc(sizeof(int) * (*len));
    int k = 0;
    while(!QueueIsEmpty(q)){
        divisor[k] = QueueDequeue(q);
        k++;
    }
    dropQueue(q);
    return divisor;
}

//funtion to split a number
int *split(int a, int *len){
    int n = a;
    while (a != 0){
        a = a / 10;
        (*len)++;
    }
    int *num = malloc(sizeof(int) * (*len));
    int i;
    for (i =0; i <= (*len)-1 ; i++){
        num[(*len)-i-1] = n % 10;
        n = n / 10;
    }
    return num;
}

//function to find wether the all digits in x is appear in y, all in true otherwise false
bool isIn(int x, int y){
    int i,j;
    int len1 = 0;
    int *split1 = split(x,&len1);
    int len2 = 0;
    int *split2 = split(y,&len2);

    for (i = 0; i < len1; i++){
        int buff = 0;
        for(j = 0; j < len2; j++){
            if (split2[j] == split1[i]){
                buff = 1;
            }
        }
        if (buff == 0){
            free(split1);
            free(split2);
            return false;
        }

    }
    free(split1);
    free(split2);
    return true;
}

//print partial order 
void PrintConnection(Graph g,int *divisor, int len){
    int i,j;
    for(i = 0; i < len; i++){
        printf("%d: ",divisor[i]);
        for(j = i + 1; j < len; j ++){
            if (divisor[j] % divisor[i] == 0 && isIn(divisor[i],divisor[j])){
                printf("%d ",divisor[j] );
                Edge e = {i,j};
                insertEdge(g,e);
            }
        }
        printf("\n");
    }
}


bool isVisit(Vertex v,Vertex w){
    if (visited[v][w] == -1){
        return true;
    }
    return false;
}

bool isConnect(Graph g,Vertex v){
    int i;
    for (i =0; i< numOfVertices(g);i++){
        if (adjacent(g, v, i)){
            return true;
        }
    }
    return false;
}

/************************************************************(*******************/

void dfsPathSerach(Graph g,Vertex v,Vertex dest,stack s,stack p,stack flag,int n) {
    Vertex w;

    //if vertex v equal to destination pop path from stack and store it in the pathss list and pop 
    //the first element from stack keep going to recursive for the top element in stack to find anoter path.
    if (v == dest) {
        int count=1;
        /*************************************************************/

        while (StackHeight(s)) {

            int t = StackPop(s);

            StackPush(p,t);
        }
        pathss[n][0] = StackHeight(p);
        while (!StackIsEmpty(p)){
            int temp1 = StackPop(p);
            pathss[n][count] = temp1;
            count++;
            StackPush(s,temp1);
        }
        n++;
        /*************************************************************/


        if (StackIsEmpty(s)) {
            return;}
        int x = StackPop(s);
        StackPush(flag, x);
        if (StackHeight(flag) == 2) {
            int a1 = StackPop(flag);
            int a2 = StackPop(flag);
            visited[a1][a2] = 0;
        }
        if (StackIsEmpty(s)) {
            return;}

        int y = StackTop(s);
        visited[y][x] = -1;

        return dfsPathSerach(g,y,dest,s,p,flag,n);

    } else {
    	//if v not equal to destion vertex than search all the vertex to find another vertex that can go, 
    	//and than recursive
        for (w = v; w < numOfVertices(g); w++) {
            if (adjacent(g, v, w) && !isVisit(v, w)) {
                if (StackHeight(flag) > 0) {
                    while (StackHeight(flag)){
                        StackPop(flag);
                    }
                }
                StackPush(s, w);
                return dfsPathSerach(g, w, dest, s,p,flag,n);

            }
        }
        /*************************************************************/
        //if there is no way to go and all the edge has been visited than store this path in the 
        //pathess list 

        int count1=1;
        while (StackHeight(s)) {
            int t1 = StackPop(s);
            StackPush(p,t1);
        }
        pathss[n][0] = StackHeight(p);
        while (!StackIsEmpty(p)){
            int temp = StackPop(p);
            pathss[n][count1] = temp;
            count1++;
            StackPush(s,temp);
        }
        n++;
        /*************************************************************/

        if (StackIsEmpty(s)) {
            return;}
        int a = StackPop(s);
        StackPush(flag,a);
        if (StackHeight(flag) == 2) {
            int a11 = StackPop(flag);
            int a22 = StackPop(flag);
            visited[a11][a22] = 0;
        }
        if (StackIsEmpty(s)) {
            return;}
        int b = StackTop(s);

        visited[b][a] = -1;
        return dfsPathSerach(g,b,dest,s,p,flag,n);
    }
    // if all the elements pop from the stack ,all the paths has been searched 
}
/*************************************************************/

int main(int argc,char* argv[])
{
	//initial the path list to -2 in case conflict with the index number
    int i,j,k;
    for(i= 0;i<MAX_NODES;i++){
        for(j = 0; j < MAX_NODES;j++){
            pathss[i][j] = -2;
            LLpathss[i][j] = -2;
        }
    }
    int v = 0;
    int max = -1;
    int path_num = 0;
    v = atoi(argv[1]);
    int len = 0;
    int ct = 0;


    int *divisor = find_divisor(v,&len);
    Graph g = newGraph(len);
    printf("Partial order: \n");
    PrintConnection(g,divisor,len);
    stack s = newStack();
    stack p = newStack();
    stack flag = newStack();




    printf("\nLongest monotonically increasing sequences:\n");
    //traverse every vertex as the start vertex to search path

    for (k =0;k <len; k++){
        StackPush(s,k);
        dfsPathSerach(g, k, numOfVertices(g), s, p, flag,n);
        //get the path and find the max length path in different start vertex
        for (i = 0; i < MAX_NODES; i++) {
            if (pathss[i][0] != -2) {
                path_num++;
                for (j = 0; j < MAX_NODES; j++) {
                    if (pathss[i][j] == -2) {
                        if (j > max)
                            max = j;
                        break;
                    }
                }
            } else
                break;
        }
        //copy all the longest path in the LLpathss 
        for (i = 0; i < path_num; i++) {
            if (pathss[i][0] == max - 1) {
                for (j = 0; j < max; j++) {
                    if (pathss[i][j] != -2 && pathss[i][0] == max - 1) {
                        LLpathss[ct][j] = pathss[i][j];
                    }
                }ct++;
            }
        }

        int i2;
        int j2;
        // re-initinal the path list to store the path for the next start vertex

        for(i2= 0;i2<MAX_NODES;i2++){
            for(j2 = 0; j2 < MAX_NODES;j2++){
                pathss[i2][j2] = -2;
            }
        }
        int i3,j3;
        for(i3= 0;i3<MAX_NODES;i3++){
            for(j3 = 0; j3 < MAX_NODES;j3++){
                visited[i3][j3] = 0;
            }
        }

    }
    //traverse to find the longest path number in the whole pathes

    int max1 = 0 ;
    int path_num1 = 0;
    for (i = 0; i < MAX_NODES; i++) {
        if (LLpathss[i][0] != -2) {
            path_num1++;
            if(LLpathss[i][0] > max1){
                max1 = LLpathss[i][0];
            }
        } else
            break;
    }
   //print all the longest pathes

   int ha =0;
   int i2;
   int j2;
    for (i2 = 0; i2 < path_num1;i2++) {
        for (j2 = 1; j2 < max-1; j2++) {
            if (LLpathss[i2][j2] != -2 && LLpathss[i2][0] == max-1) {
                printf("%d < ", divisor[LLpathss[i2][j2]]);
                ha++;
            }

        }
        if (ha == max -2) {
            printf("%d\n", divisor[LLpathss[i2][max - 1]]);
        }
        ha = 0;
    }
    //free the memory
    freeGraph(g);
    free(flag);
    free(p);
    free(s);
    free(divisor);
    return 0;


}




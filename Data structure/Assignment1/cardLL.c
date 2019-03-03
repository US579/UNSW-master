// Linked list of transport card records implementation ... Assignment 1 COMP9024 18s2
#include <stdio.h>
#include <stdlib.h>
#include <assert.h>
#include "cardLL.h"
#include "cardRecord.h"

// linked list node type
// DO NOT CHANGE
typedef struct node {
    cardRecordT data;
    struct node *next;
} NodeT;

// linked list type
typedef struct ListRep {
   NodeT *head;

/* Add more fields if you wish */

} ListRep;

/*** Your code for stages 2 & 3 starts here ***/

// Time complexity: O(1)
// Explanation: take constant time and variety with the input size
List newLL() {
   ListRep *LL = malloc(sizeof(ListRep));
   assert(LL != NULL);
   LL -> head = NULL;
   return LL;  /* needs to be replaced */
}

// Time complexity: O(N)
// Explanation: this function will automatically iterate through linked list from the start to the end, hence,
//              time complexity increased linearly in related to parameters.
void dropLL(List listp) {
    NodeT *curr = listp->head;
    while (curr != NULL)
    {
        NodeT *new;
        new = curr->next;
        free(curr);
        curr = new;
    }
    free(listp);
}

// Time complexity: O(N)
// Explanation: this function will automatically iterate through linked list from the start to the end, hence,
//              time complexity increased linearly in related to parameters.
void removeLL(List listp, int cardID) {
    //Creating Pointer
    NodeT *pos;
    NodeT *p;
    pos = listp->head;
    p  = listp->head;
    int flag = 0;
    //find the positation where the node.cardID equal to the cardID
    while(cardID != pos->data.cardID && pos->next != NULL)
    {
        p = pos;
        pos = pos->next;
        flag = 1;
    }

    if (flag == 0 && cardID == p->data.cardID){
        listp->head = p->next;
        printf("Card removed.\n");
    }else {

        if (cardID == pos->data.cardID) {

            if (p == listp->head && p->next == NULL) {
                listp->head = p->next;
            } else {
                p->next = p->next->next;
                printf("Card removed.\n");
            }

        } else {
            printf("Card not found.\n");
        }
    }
}


// Time complexity: O(N)when inserting new node in the head of the linked list.
//                  O(1)when inserting new node in the ascending order
// Explanation: O(1) take constant time and variety with the input size
//              O(N)this will automatically iterate through linked list from the start to the end, hence,
//              time complexity increased linearly in related to parameters.
void insertLL(List listp, int cardID, float amount) {
    //Creating Pointer
    NodeT *node = malloc(sizeof(NodeT));
    NodeT *buff;
    assert(node != NULL);
    //Assign values to the new node
    node->data.cardID = cardID;
    node->data.balance = amount;
    node->next = NULL;
    buff = listp->head;
    while (buff != NULL) {
        if (buff->data.cardID == cardID) {
            buff->data.cardID = cardID;
            buff->data.balance = amount + buff->data.balance;
            printCardData(buff->data);
            free(node);
            return;
        } else {
            buff = buff->next;
        }
    }
    //
    if (listp->head == NULL || listp->head->data.cardID >= node->data.cardID) {
        node->next = listp->head;
        listp->head = node;
    } else {
        buff = listp->head;
        while (buff->next != NULL && buff->next->data.cardID < node->data.cardID) {
            buff = buff->next;
        }
        node->next = buff->next;
        buff->next = node;

    }
    printf("Card added.\n");
}

// Time complexity: O(N)
// Explanation: this function will automatically iterate through linked list from the start to the end, hence,
//              time complexity increased linearly in related to parameters.
void getAverageLL(List listp, int *n, float *balance) {
    int nn = 0;
    float avg_balance;
    float total_balance = 0;
    NodeT *Node = malloc(sizeof(NodeT));
    assert(Node != NULL);
    Node = listp->head;
    while (Node != NULL)
    {
        nn++;
        total_balance += Node->data.balance;
        Node = Node->next;
    }
    n = &nn;
    printf("Number of cards on file: %d\n",*n);
    if (*n != 0)
    {
        avg_balance = total_balance / nn;
        balance = &avg_balance;
        if (*balance < 0 )
        {
            printf("Average balance: -$%.2f\n",-*balance);
        } else {
            printf("Average balance: $%.2f\n", *balance);
        }
    }
}

// Time complexity: O(N)
// Explanation: this function will automatically iterate through linked list from the start to the end, hence,
//              time complexity increased linearly in related to parameters.
void showLL(List listp) {
    //Creating Pointer
    NodeT *ps = malloc(sizeof(NodeT));
    assert(ps != NULL);
    for (ps = listp->head;ps != NULL;ps = ps->next)
    {
        printCardData(ps->data);
    }
    free(ps);
}

// Queue ADT header file ... COMP9024 18s2

typedef struct QueueRep *queue;

queue newQueue();               // set up empty queue
void  dropQueue(queue);         // remove unwanted queue
int   QueueIsEmpty(queue);      // check whether queue is empty
void  QueueEnqueue(queue, int); // insert an int at end of queue
int   QueueDequeue(queue);      // remove int from front of queue
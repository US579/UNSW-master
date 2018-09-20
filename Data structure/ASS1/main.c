/**
     main.c

     Program supplied as a starting point for
     Assignment 1: Transport card manager

     COMP9024 18s2
**/
#include <stdio.h>
#include <stdlib.h>
#include <assert.h>
#include <ctype.h>

#include "cardRecord.h"
#include "cardLL.h"

void printHelp();
void CardLinkedListProcessing();

int main(int argc, char *argv[]) {
   if (argc == 2) {
       int n;
       n = atoi(argv[1]);
       cardRecordT *records = malloc(n * sizeof(cardRecordT));
       for(int i=0;i<n;i++)
       {
           int card_id=readValidID();
           records[i].cardID=card_id;
           float balance_amount =readValidAmount();
           records[i].balance = balance_amount;
       }

       float averge_balance;
       float cal_average = 0.00;
       for(int i = 0;i <n ; i++)
       {
           printCardData(records[i]);
           cal_average += records[i].balance;
       }
       printf("Number of cards on file: %d\n",n);
       if (n != 0)
       {
           averge_balance = cal_average / n;
           if (averge_balance <0) {
               printf("Average balance: -$%.2f\n", -averge_balance);
           } else{
               printf("Average balance: $%.2f\n", averge_balance);
           }
       }
      
   } else {
      CardLinkedListProcessing();
   }
   return 0;
}

/* Code for Stages 2 and 3 starts here */

void CardLinkedListProcessing() {
   int op, ch;

   List list = newLL();   // create a new linked list
   
   while (1) {
      printf("Enter command (a,g,p,q,r, h for Help)> ");

      do {
	 ch = getchar();
      } while (!isalpha(ch) && ch != '\n');  // isalpha() defined in ctype.h
      op = ch;
      // skip the rest of the line until newline is encountered
      while (ch != '\n') {
	 ch = getchar();
      }

      switch (op) {

          case 'a':
          case 'A': {
              int cardID = readValidID();
              float balance = readValidAmount();
              insertLL(list, cardID, balance);
              break;
          }

          case 'g':
          case 'G':
          {
              int *n = malloc(sizeof(int));
              float *average = malloc(sizeof(float));
              getAverageLL(list, n, average);
              free(n);
              free(average);
              break;
          }


          case 'h':
          case 'H': {
              printHelp();
              break;
          }

          case 'p':
          case 'P': {
              showLL(list);
              break;
          }


          case 'r':
          case 'R': {
              int cardid = readValidID();
              removeLL(list, cardid);
              /*** Insert your code for removing a card record ***/
              break;
           }

	 case 'q':
         case 'Q':{
             dropLL(list);       // destroy linked list before returning
             printf("Bye.\n");
             return;
         }
      }
   }
}

void printHelp() {
   printf("\n");
   printf(" a - Add card record\n" );
   printf(" g - Get average balance\n" );
   printf(" h - Help\n");
   printf(" p - Print all records\n" );
   printf(" r - Remove card\n");
   printf(" q - Quit\n");
   printf("\n");
}

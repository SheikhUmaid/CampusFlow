#include <stdio.h>
#include <stdlib.h>
struct node{
        int info;
        struct node *next;
};


void displayList(struct node*);

struct node *insertAtBeginning(struct node *list, int el){
        struct node *node;
        node = (struct node *)malloc(sizeof(struct node));
        node->info = el;

        if(list==NULL){
                node->next = NULL;
                list = node;
        }
        else{
                node->next = list;
                list = node;
        }

        return list;


}
struct node *deleteAtEnd(struct node *list){
        struct node *node, *temp;
        node = list;
        temp = node;

        if (node == NULL){
                printf("The list is empty");
                return NULL;
        }

        while(node->next != NULL){
                temp = node;
                node = node->next;

        }
        free(node);
        temp->next = NULL;

        return list;
}


struct node *deleteAtBeginning(struct node *head){
        struct node *temp;
        temp = head;
        if(head == NULL){
                printf("the list is empty");
                return NULL;
        }
        else{
                        head = head->next;
                        free(temp);

        }
        return head;
}

void main(){
        int ch, n;
        struct node *list;
        while(1){
                printf("\n-----------------menu-------------------\n1. add at begining\n2. delete element at end\n3. display list\n4. to delete at beginning\n5. exit\n");
                scanf("%d",&ch);
                switch(ch){
                        case 1:
                                printf("Enter the element to be added: \n");
                                scanf("%d",&n);
                                list = insertAtBeginning(list, n);
                                printf("added");
                                break;
                        case 2:
                                list = deleteAtEnd(list);
                                break;
                        case 3:
                                displayList(list);
                                break;
                        case 4:
                                list = deleteAtBeginning(list);
                                break;
                        case 5:
                                exit(0);
                        default:
                                printf("Enter valid option");
                }
        }
}


void displayList(struct node *list){
        struct node *ptr;
        if(list==NULL){
                printf("list is empty");
                return;
        }
        ptr = list;
        printf("---------------------------------displaying list-------------------\n");
        while(ptr != NULL){
                printf("%d->",ptr->info);
                ptr = ptr->next;
        }

        return;
}


                                     
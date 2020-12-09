#include <stdio.h>
#include <stdlib.h>

struct Node {
    int data;
    struct Node* next;
};

struct Node* CreateList()
{
    struct Node* head = (struct Node *)malloc(sizeof(struct Node));
    head->next = NULL;
    return head;
}

struct Node* CreateNode(int data)
{
    struct Node* new_node = (struct Node *)malloc(sizeof(struct Node));
    new_node->data = data;
    new_node->next = NULL;
    return new_node;
}

void InsertNode(struct Node* head, int data)
{
    struct Node* new_node = CreateNode(data);
    new_node->next = head->next;
    head->next = new_node;
}

void Swap(int *x, int *y)
{
    int tmp = *x;
    *x = *y;
    *y = tmp;
}

void BubbleSortArr(int arr[], int sz)
{
    for (int i = 0; i < sz -1; i++)
    {
        for (int j = 0; j< sz-1-i; j++)
        {
            if (arr[j] > arr[j+1])
            {
                Swap(&arr[j], &arr[j+1]);
            }
        }
    }
}

void InsertSortArr(int arr[], int sz)
{
    int key = arr[1];
    int i = 0;
    int j = 0;
    for (i = 1; i < sz; i++)
    {
        key = arr[i];
        for(j = i; j >= 0; j--)
        {
            if(key < arr[j-1])
                arr[j] = arr[j-1];
            else
                break;
        }
        arr[j] = key;
    }
}

int QuickOneSortArr(int arr[], int start, int end)
{
    int key = start;
    while(start < end)
    {
        while(start < end && arr[end] >= arr[key])
            end--;
        while(start < end && arr[start] <= arr[key])
            start++;
        Swap(&arr[start],&arr[end]);
    }
    Swap(&arr[key],&arr[end]);
    return start;
}

void QuickSortArr(int arr[], int start, int end)
{
    if(start >= end)
        return;
    int index = QuickOneSortArr(arr,start,end);
    QuickSortArr(arr,start,index-1);
    QuickSortArr(arr,index+1,end);
}

void PrintArr(int arr[], int sz)
{
    for (int i = 0; i < sz; i++)
        printf("%d ", arr[i]);
    printf("\n");
}

void BubbleSortList(struct Node* head)
{
    for(struct Node* p = head->next; p != NULL; p=p->next)
    {
        for(struct Node* q = p->next; q != NULL; q=q->next)
        {
            if(p->data > q->data)
            {
                int tmp = p->data;
                p->data = q->data;
                q->data = tmp;
            }
        }
    }
}

void InsertSortList(struct Node* head)
{
    struct Node* p = head->next->next;
    struct Node* q = p->next;
    head->next->next = NULL;
    while(p != NULL)
    {
        q = p->next;
        struct Node* cur = head;
        while(cur->next != NULL && cur->next->data < p->data)
        {
            cur = cur->next;
        }
        p->next = cur->next;
        cur->next = p;
        p = q;
    }
}

void PrintList(struct Node* head)
{
    struct Node* cur = head->next;
    while(cur)
    {
        printf("%d -> ", cur->data);
        cur = cur->next;
    }
    printf("NULL \n");
}

struct Node* MerList(struct Node* list1, struct Node* list2)
{
    struct Node* newhead = (struct Node*)malloc(sizeof(struct Node));
    //head没有值
    struct Node* cur1 = list1->next;
    struct Node* cur2 = list2->next;
    struct Node* head = newhead;
    while(cur1 && cur2)
    {
        if(cur1->data < cur2->data)
        {
            head->next = cur1;
            cur1 = cur1->next;
        }
        else
        {
            head->next = cur2;
            cur2 = cur2->next;
        }
        head = head->next;
    }
    if(cur1)
    {
        head->next = cur1;
    }
    if(cur2)
    {
        head->next = cur2;
    }
    return newhead;
}

int main()
{
    int arr[10] = {10, 2, 30, 4, 56, 6, 7, 89, 9, 10};
    int size = sizeof(arr) / sizeof(arr[0]);
    PrintArr(arr, size);
    //BubbleSortArr(arr, size);
    //InsertSortArr(arr, size);
    QuickSortArr(arr,0, size-1);
    PrintArr(arr, size);

    struct Node* list = CreateList();
    InsertNode(list, 50);
    InsertNode(list, 25);
    InsertNode(list, 79);
    InsertNode(list, 3);
    InsertNode(list, 16);
    InsertNode(list, 1);
    InsertNode(list, 42);
    PrintList(list);
    //BubbleSortList(list);
    InsertSortList(list);
    PrintList(list);

    struct Node* list_mer = CreateList();
    InsertNode(list_mer, 5);
    InsertNode(list_mer, 29);
    InsertNode(list_mer, 7);
    InsertNode(list_mer, 38);
    InsertNode(list_mer, 65);
    InsertNode(list_mer, 2);
    InsertNode(list_mer, 45);
    PrintList(list_mer);
    //BubbleSortList(list);
    InsertSortList(list_mer);
    PrintList(list_mer);

    struct Node* res = MerList(list,list_mer);
    PrintList(res);

    return 0;
}
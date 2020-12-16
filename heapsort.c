#include <stdio.h>
#include <stdlib.h>

void swap(int* a, int* b)
{
    int tmp = *a;
    *a = *b;
    *b = tmp;
}

//向下调整算法，root是下标
void AdjustDown(int arr[], int sz, int root)
{
    int parent = root;
    int child = parent * 2 + 1;//默认指向左孩子
    while(child < sz)
    {
        //选左右孩子中大的那一个
        //child + 1 < sz表示右孩子也在，右孩子也在并且右孩子大于左孩子就让指向右孩子
        if(child + 1 < sz && arr[child]<arr[child+1])
        {
            child++;
        }
        //如果左右孩子中的任何一个大于父亲节点就就交换孩子和父亲
        if(arr[child]>arr[parent])
        {
            swap(&arr[child], &arr[parent]);
            //让父亲往下走，变到原先孩子的位置，再往下遍历
            parent = child;
            child = parent * 2 + 1;
        }
        //如果左右孩子中的任何一个都不大于父亲，那就跳出循环
        else
        {
            break;
        }
    }
}

void HeapSort(int arr[], int sz)
{
    //建大堆
    //(n-1)/2是找到该节点的父亲
    //调到根，也就是>=0就终止，向下调整
    for(int i = (sz-2)/2; i>=0; i--)
    {
        AdjustDown(arr,sz,i);
    }
    //选数排序
    //交换大顶堆的顶和最后一个数
    int end = sz-1;
    while(end>0)
    {
        swap(&arr[0], &arr[end]);
        AdjustDown(arr, end,0); //0是下标，每次从根开始向下调整
        end--;
    }
}

int main()
{
    int arr[10] = {12, 1, 36, 98, 5, 76, 52, 2, 84, 6};
    int sz = sizeof(arr)/sizeof(arr[0]);
    HeapSort(arr, sz);
    for(int i = 0; i<sz; i++)
    {
        printf("%d, ", arr[i]);
    }
    return 0;
}


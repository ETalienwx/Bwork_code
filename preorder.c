#include <stdio.h>
#include <stdlib.h>

typedef struct node
{
    int data;
    struct node *left;
    struct node *right;
}Node;

typedef struct tree
{
    Node* root;
}Tree;

void InsertNode(Tree* tree, int val)
{
    Node* node = (Node*)malloc(sizeof(Node));
    node->data = val;
    node->left = NULL;
    node->right = NULL;

    if(tree->root == NULL)
    {
        tree->root = node;
    }
    else
    {
        Node* tmp = tree->root;
        while(tmp)
        {
            if(tmp->data > node->data)
            {
                if(tmp->left == NULL)
                {
                    tmp->left = node;
                    return;
                }
                else
                {
                    tmp = tmp->left;
                }
            }
            else
            {
                if(tmp->data < node->data)
                {
                    if(tmp->right == NULL)
                    {
                        tmp->right = node;
                        return;
                    }
                    else
                    {
                        tmp = tmp->right;
                    }
                }
            }
        }
    }
}

void InitTree(Tree* tree)
{
    tree->root = NULL;
    int arr[10] = {5, 2, 8, 4, 10, 6, 7, 3, 1, 9};
    for(int i = 0; i<sizeof(arr)/sizeof(arr[0]); i++)
    {
        InsertNode(tree, arr[i]);
    }
}

void PreorderTree(Node* node)
{
    if(node) {
        printf("%d, ", node->data);
        PreorderTree(node->left);
        PreorderTree(node->right);
    }
}

Node* arr[10];
int Index = 0;

void Push(Node *cur)
{
    arr[Index] = cur;
    Index++;
}

Node* Top()
{
    return arr[Index-1];
}

void Pop()
{
    if(Index > 0)
        Index--;
}

int Empty()
{
    return Top() == 0 ? 0 : 1;
}

void PreorderTree_no_recursive(Node* node)
{
    while(node || Empty()==1)
    {
        while(node)
        {
            Push(node);
            printf("%d, ", node->data);
            node = node->left;
        }
        Node* top = Top();
        Pop();
        node = top->right;
    }
}

void DestoryTree(Node* node)
{
    if(node)
    {
        DestoryTree(node->left);
        DestoryTree(node->right);
        printf("free node : %d\n", node->data);
        free(node);
        node = NULL;
    }
}

int main()
{
    Tree tree;
    InitTree(&tree);
    PreorderTree(tree.root);
    printf("\n");
    PreorderTree_no_recursive(tree.root);
    printf("\n");
    DestoryTree(tree.root);
    return 0;
}

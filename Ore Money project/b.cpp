#include<iostream>
#include <list>

using namespace std;


class Graph {
    int V;
    list<int> *adj;
    bool *visited;

  public:
    Graph(int V);
    void addEdge(int v, int w);
    void getBFS();
    void bfs(int s);
};

Graph::Graph(int v) {
    V = v;
    adj = new list<int>[V + 1];
}

void Graph::addEdge(int a, int b) {
    //Creating an edge between a and b
    adj[a].push_back(b);
    //Creating an edge between b and a
    adj[b].push_back(a);
}
void Graph::getBFS() {
    visited = new bool[V + 1];

    //Marking all the vertices as unvisited
    for(int i = 1; i <= V; i++)
      visited[i] = false;

    for(int i = 1; i <= V; i++) {
      //Call bfs for the unvisited nodes
      if(visited[i] == false) {
        bfs(i);
      }
    }
}
void Graph::bfs(int start) {
    list<int> queue;
    //mark the start node as visited
    visited[start] = true;
    //Enqueue the start node
    queue.push_back(start);
    list<int>::iterator i;

    while(!queue.empty()) {
      //Dequeue the oldest vertex from queue
      start = queue.front();
      //Printing the dequeued vertex
      cout << start << " ";
      queue.pop_front();

      //Get all the adjacent vertices of the dequeued vertex
      for(i = adj[start].begin(); i != adj[start].end(); ++i) {
        //Enqueue the vertex if unvisited and mark as visited
        if(!visited[*i]) {
          visited[*i] = true;
          queue.push_back(*i);
        }
      }
    }
}

int main() {
    Graph g(7);
    g.addEdge(1, 2);
    g.addEdge(1, 3);
    g.addEdge(1, 5);
    g.addEdge(4, 2);
    g.addEdge(6, 4);
    g.addEdge(6, 5);
    g.addEdge(2, 5);
    g.getBFS() ;
    return 0;
}

#include <iostream>
#include "TXLib.h"
#include <vector>
#include <cmath>
using namespace std;
class Graph{
public:
    int k = 2;
    Graph(){
    }
    void draw(){
        txSetFillColor(TX_BLACK);
        txSetColor(TX_BLACK);
        for(int i = -500; i < 500; i+= 5){
            txCircle(i + 500 , (500-pow(i, k)), 2);
        }
    }
};
class BackGround{
public:
    int x,y;
    BackGround(int x, int y){
        this->x = x;
        this->y = y;
    }
    void draw(){
        txSetFillColor(TX_WHITE);
        txSetColor(TX_WHITE);
        txRectangle(0,0,x,y);
        txSetFillColor(TX_BLACK);
        txSetColor(TX_BLACK, 5);
        /*ось обцисс*/
        txLine(0,y/2,x,y/2);
        /*ось ординат*/
        txLine(x/2,y,x/2,0);
        txSetColor(TX_BLACK, 1);
        for(int i = 0; i < 50; i++){
            txLine(i*20, 0, i*20, 1000);
            txLine(0, i*20, 1000, i*20);
        }
    }
};
class Window{
public:
    int winX = 1000;
    int winY = 1000;
    BackGround bg = BackGround(winX, winY);
    Graph graph = Graph();
    void run(){
        txCreateWindow(winX, winY);
        while(true){
            txClear();
            bg.draw();
            graph.draw();
            txSleep(1);
        }
    }
};
int main(){
    Window window;
    window.run();
}

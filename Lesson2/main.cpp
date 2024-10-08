#include <iostream>
#include "TxLib.h"
using namespace std;

class Hero{
public:
    int x;
    int y;
    Hero(int x1, int y1){
        x = x1;
        y = y1;
    }
    void draw(){
        txSetFillColour(TX_BLACK);
        txCircle(x,y,40);
    }
    void hero_move(){
        if(GetAsyncKeyState(VK_RIGHT)){
            x += 5;
        }
        if(GetAsyncKeyState(VK_LEFT)){
            x -= 5;
        }
        if(GetAsyncKeyState(VK_DOWN)){
            y += 5;
        }
        if(GetAsyncKeyState(VK_UP)){
            y -= 5;
        }
    }
};
class Enemy{
public:
    int x;
    int y;
    Enemy(int x1, int y1){
        x = x1;
        y = y1;
    }
    void draw(){
        txSetFillColour(TX_RED);
        txCircle(x,y,40);
    }
};
class Background{
public:
    int x;
    int y;
    int xStar[1000];
    int yStar[1000];
    int sizeStar[1000];
    int stars_quan;
    bool flag = true;
    Background(int x1, int y1){
        x = x1;
        y = y1;
    }
    void draw(){
        txSetFillColour(TX_GREY);
        txRectangle(0,0,x,y);
        if(flag == true){
            for (stars_quan = 0; stars_quan < 1000; stars_quan ++ ){

                xStar[stars_quan] = rand() % 1000;
                yStar[stars_quan] = rand() % 800;
                sizeStar[stars_quan] = rand() % 4;
            }
            flag = false;
        }
        for(stars_quan = 0; stars_quan < 1000; stars_quan++){
            txSetFillColour(TX_WHITE);
            txCircle(xStar[stars_quan], yStar[stars_quan], sizeStar[stars_quan]);
        }
    }
};
int main()
{
    txCreateWindow(1000,800);
    Background bg = Background(1000,800);
    Hero hero = Hero(500, 400);
    Enemy * enemy = new Enemy(300, 600);
    while(true){
        txClear();
        bg.draw();
        hero.draw();
        hero.hero_move();
        if(((hero.x-enemy.x)*(hero.x-enemy.x))+((hero.y-enemy.y)*(hero.y-enemy.y)) >= 6400){
            delete aa;
        }
        txSleep(10);

    }
    return 0;
}

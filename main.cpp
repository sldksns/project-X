#include <iostream>
#include"TXLib.h"
#include <string>
#include <sstream>
using namespace std;
class Background{
public:
    HDC image = txLoadImage("img/bg.bmp");
    void draw(){
        txBitBlt(txDC(), 0, 0, 0, 0, image, 0, 0);
    }
};
class Menu{
public:
    HDC image = txLoadImage("img/menu_bg.bmp");
    void draw(){
        txBitBlt(txDC(), 0, 0, 0, 0, image, 0, 0);
        txSetFillColor(TX_WHITE);
        txRectangle(450, 640, 750, 715);
        txSetColor(TX_BLACK);
        txTextOut(550, 650, "PLAY");
        txSelectFont("Comic Sans MS", 58);
    }
    bool check(){
        if (txMouseX() >= 450 && txMouseX() <= 750 && txMouseY() >= 640 && txMouseY() <= 715 && txMouseButtons()==1 ){
                return true;
        }
    }
};
class Enemy{
public:
    int x, y;
    HDC image = txLoadImage("img/enemy.bmp");
    Enemy (int x,int y){
    this ->x=x;
    this ->y =y;
    }
    void draw(){
        txTransparentBlt(txDC(),x,y,0,0, image ,0,0, TX_WHITE);
    }
    void moved(){
        y += 3;
    }
};
class Bullet{
public:
    int x, y;
    HDC image = txLoadImage("img/bullet.bmp");
    Bullet (int x,int y){
    this ->x=x;
    this ->y =y;
    }
    void draw(){
        txTransparentBlt(txDC(),x,y,0,0, image ,0,0, TX_WHITE);
    }
    void moved(){
        y -= 10;
    }
};
class EBullet{
public:
    int x, y;
    HDC image = txLoadImage("img/ebullet.bmp");
    EBullet (int x,int y){
    this ->x=x;
    this ->y =y;
    }
    void draw(){
        txTransparentBlt(txDC(),x,y,0,0, image ,0,0, TX_WHITE);
    }
    void moved(){
        y += 10;
    }
};
class Pers{
public:
    int x, y;
    int hp = 100;
    HDC image = txLoadImage("img/pers.bmp");
    Pers (int x,int y){
    this ->x=x;
    this ->y =y;
    }
    void draw(){
        txTransparentBlt(txDC(),x,y,0,0, image ,0,0, TX_WHITE);
    }
    void moved(){
        if(GetAsyncKeyState('A')){
            x -= 6;
        }
        if (x < 0) {
                x = 0;
            }
        if(GetAsyncKeyState('D')){
            x += 6;
        }
        if (x > 1100) {
                x = 1100;
            }

    }
    void death(){
        if (hp <= 0){
            y = 1100;
        }
    }
};
class Game {
public:
    Background bg;
    Menu menu;
    int scene = 0;
    Pers pers = Pers(600, 800);
    Enemy *enemy[5];
    Bullet *bull[20];
    EBullet *ebull[20];
    int shoot_number[20];
    bool is_fire[20];
    bool is_efire[20];
    int fire_timer = 15;
    int efire_timer = 50;
    void run(){
        txCreateWindow(1200, 1000);
        for(int i = 0; i < 5; i++){
            enemy[i] = new Enemy(rand() % 1100 - 1 + i *10, -(rand() % 700-100) + i*10);
        }
        for(int i = 0; i < 20; i++){
            bull[i] = new Bullet(0, 0);
            is_fire[i] = false;
        }
        for(int i = 0; i < 20; i++){
            ebull[i] = new EBullet(0, 0);
        }
        while(true){
            if (scene == 0){
                txClear();
                menu.draw();
                menu.check();
                if(menu.check() == true){
                    scene = 1;
                }
                txSleep(1);
            }
            if (scene == 1){
                txClear();
                bg.draw();
                txSetFillColor(TX_RED);
                txRectangle(50, 25, 250, 65);
                txSetFillColor(TX_GREEN);
                txRectangle(50,25,pers.hp*2+50, 65);
                pers.draw();
                pers.death();
                pers.moved();
                for(int i = 0; i < 5; i++){
                    enemy[i]->draw();
                    enemy[i]->moved();
                    if (enemy[i]->y >= 1000){
                        enemy[i]->y = -(rand() % 700-100) + i*10;
                        enemy[i]->x = rand() % 1100 - 1 + i *10;
                    }
                    if (pers.x >= enemy[i]->x - 70 && pers.x <= enemy[i]->x + 70 && pers.y <= enemy[i]->y + 90 && pers.y >= enemy[i]->y - 90){
                        enemy[i]->y = -(rand() % 700-100) + i*10;
                        enemy[i]->x = rand() % 1100 - 1 + i *10;
                    }
                }
                for(int i = 0; i < 20; i++){
                    shoot_number[i] = rand() % 4 - 0;
                    if(enemy[shoot_number[i]]->y > 0){
                        if (efire_timer >= 50){
                            if (is_efire[i] != true){
                                is_efire[i] = true;
                                ebull[i]->x = enemy[shoot_number[i]]->x + 60;
                                ebull[i]->y = enemy[shoot_number[i]]->y + 95;
                                efire_timer = 0;
                            }
                        }
                    }
                }
                for(int i = 0; i < 20; i++){
                    //cout << is_fire[i] << " ";
                    if (is_efire[i]){
                        ebull[i]->draw();
                        ebull[i]->moved();
                        if(ebull[i]->y >= pers.y - 50 && ebull[i]->x >= pers.x && ebull[i]->x <= pers.x + 80){
                            pers.hp -= 20;
                            is_efire[i] = false;
                        }
                    }
                    if (ebull[i]->y >= 1000){
                        is_efire[i] = false;
                    }

                }
                for(int i = 0; i < 20; i++){
                    if(GetAsyncKeyState('S')){
                        if (fire_timer >= 15){
                            if (is_fire[i] != true){
                                is_fire[i] = true;
                                bull[i]->x = pers.x + 60;
                                bull[i]->y = pers.y;
                                fire_timer = 0;
                            }
                        }
                    }
                    if (is_fire[i] != true){
                        bull[i]->x = pers.x;
                        bull[i]->y = pers.y;
                    }
                }
                for(int i = 0; i < 20; i++){
                    //cout << is_fire[i] << " ";
                    if (is_fire[i]){
                        bull[i]->draw();
                        bull[i]->moved();
                        for(int j = 0; j < 5; j++){
                            if(bull[i]->y <= enemy[j]->y + 78 && bull[i]->x >= enemy[j]->x && bull[i]->x <= enemy[j]->x + 97){
                                is_fire[i] = false;
                                enemy[j]->y = -(rand() % 700-100) + j*10;
                                enemy[j]->x = rand() % 1100 - 1 + j *10;
                            }
                        }
                    }
                    if (pers.y - bull[i]->y >= 600){
                        is_fire[i] = false;
                    }

                }

                fire_timer++;
                efire_timer++;
                txSleep(1);
            }
        }
    }
} ;
int main(){
    Game game;
    game.run();
}

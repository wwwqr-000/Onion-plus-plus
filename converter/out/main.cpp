#include <iostream>
#define root main
void say(std::string txt) { std::cout << txt; }


void test() {
say("Hello! from test!\n");
return;
}

int root() {
if (true) { test(); }
say("Hello world!\n");
if (1 == 1) { say("Marfkas!\n");say("Test!@#\n"); }
return 0;
}
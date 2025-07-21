#include <iostream>
#define root main
void say(std::string txt) { std::cout << txt; }


void test() {
say("Hello!");
return;
}

int root() {
if (1 == 1 || 2 == 2 && 2 >= 4) { say("test"); }
say("Hello world!");
test();
return 0;
}
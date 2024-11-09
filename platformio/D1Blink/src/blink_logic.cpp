#include "blink_logic.h"

void sweepDelayLoop(int *led, void (*switchOn)(int, int), void (*switchOff)(int, int)) {
  int delay_base = 20;
  int delay_step = 10;
  int delay = delay_base;
  while (true) {

    switchOn(*led, delay);
    switchOff(*led, delay);

    delay += delay_step;
    if (delay < delay_base || delay > 10 * delay_base) {
      delay_step = -delay_step;
    }
  }
}
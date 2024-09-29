#include "fwwasm.h"

#define MAX_LOOPS 20
#define NUM_LEDS 7
#define DELAY_MS 50
#define LED_FADE_DURATION 0

//different color RGB values
#define RED 0xFF0000
#define PINK 0xFFC6FF
#define ORANGE 0xFF7F00
#define YELLOW 0xFFFF00
#define GREEN 0x00FF00
#define LIGHT_GREEN 0xCAFFBF
#define BLUE 0x0000FF
#define LIGHT_BLUE 0x9BF6FF
#define INDIGO 0x4B0082
#define VIOLET 0x9400D3
#define MAX_COLORS 10
#define WHITE 0x000000

//some macros to get color RGB components
#define GET_RED(x) ((x >> 16) & 0xFF)
#define GET_GREEN(x) ((x >> 8) & 0xFF)
#define GET_BLUE(x) (x & 0xFF)

int main()
{
    int color = WHITE;

    for (int i = 0; i < 7; i++) {
        setBoardLED(i, GET_RED(color), GET_GREEN(color), GET_BLUE(color), LED_FADE_DURATION, LEDManagerLEDMode::ledflash);
    }

    return 0;
}
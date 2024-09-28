#include "fwwasm.h"
// Send IR Data
int main()
{
    unsigned int unlock_door = 2;
    sendIRData(unlock_door);

    return 0;
}
#include "fwwasm.h"
// Send IR Data
int main()
{
    unsigned int lock_door = 1;
    sendIRData(lock_door);

    return 0;
}
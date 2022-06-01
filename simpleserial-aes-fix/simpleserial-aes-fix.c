/*
    This file is based on ChipWhisperer Example Targets
    Copyright (C) 2012-2017 NewAE Technology Inc.
    Copyright (C) 2022 Stian Husum

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
*/

#include "hal.h"
#include <stdint.h>
#include <stdlib.h>
#include <string.h>

#include "stm32f303x8.h"
#include "core_cm4.h"

#include "simpleserial.h"
#include "aes.h"

uint32_t rk[88];

uint8_t get_key(uint8_t* k, uint8_t len)
{
    aes128_keyschedule_ffs_lut(rk, k);
    // Load key here
    return 0x00;
}

#if SS_VER == SS_VER_2_0
uint8_t get_pt(uint8_t cmd, uint8_t scmd, uint8_t len, uint8_t* pt)
#else
uint8_t get_pt(uint8_t* pt, uint8_t len)
#endif

{
    /**********************************
    * Start user-specific code here. */
    trigger_high();

    //16 hex bytes held in 'pt' were sent
    //from the computer. Store your response
    //back into 'pt', which will send 16 bytes
    //back to computer. Can ignore of course if
    //not needed

    aes128_encrypt_ffs(pt, pt + 16, pt, pt + 16, rk);

    trigger_low();
    /* End user-specific code here. *
    ********************************/
    simpleserial_put('r', 32, pt);
    return 0x00;
}

#if SS_VER == SS_VER_2_0
uint8_t get_count(uint8_t cmd, uint8_t scmd, uint8_t len, uint8_t* pt)
#else
uint8_t get_count(uint8_t* pt, uint8_t len)
#endif

{
    CoreDebug->DEMCR |= CoreDebug_DEMCR_TRCENA_Msk;
    DWT->CYCCNT = 0;
    DWT->CTRL |= DWT_CTRL_CYCCNTENA_Msk;
    /**********************************
    * Start user-specific code here. */
    unsigned int oldcount = DWT->CYCCNT;

    aes128_encrypt_ffs(pt, pt, pt, pt, rk);
    
    unsigned int cyclecount = DWT->CYCCNT-oldcount;
    /* End user-specific code here. *
    ********************************/
    uint8_t out[4];
    memcpy(out, &cyclecount, 4);
    simpleserial_put('r', 4, out);
    return 0x00;
}

uint8_t reset(uint8_t* x, uint8_t len)
{
    // Reset key here if needed
    return 0x00;
}


int main(void)
{
    platform_init();
    init_uart();
    trigger_setup();

    simpleserial_init();
    simpleserial_addcmd('p', 32, get_pt);
#if SS_VER != SS_VER_2_0
    simpleserial_addcmd('k', 16, get_key);
    simpleserial_addcmd('x', 0, reset);
    simpleserial_addcmd('c', 16, get_count);
#endif
    while(1)
        simpleserial_get();
}

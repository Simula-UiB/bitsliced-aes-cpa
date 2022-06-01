/******************************************************************************
* MIT License
* 
* Copyright (c) 2020 Alexandre Adomnicai
* 
* Permission is hereby granted, free of charge, to any person obtaining a copy
* of this software and associated documentation files (the "Software"), to deal
* in the Software without restriction, including without limitation the rights
* to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
* copies of the Software, and to permit persons to whom the Software is
* furnished to do so, subject to the following conditions:
* 
* The above copyright notice and this permission notice shall be included in all
* copies or substantial portions of the Software.
* 
* THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
* IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
* FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
* AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
* LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
* OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
* SOFTWARE.
******************************************************************************/
#ifndef AES_H_
#define AES_H_

#include <stdint.h>

/* Fully-fixsliced encryption functions */
void aes128_encrypt_ffs(unsigned char ctext0[16], unsigned char ctext1[16],
				const unsigned char ptext0[16], const unsigned char ptext1[16],
				const uint32_t rkeys[88]);
void aes256_encrypt_ffs(unsigned char ctext0[16], unsigned char ctext1[16],
				const unsigned char ptext0[16], const unsigned char ptext1[16],
				const uint32_t rkeys[120]);

/* Semi-fixsliced encryption functions */
void aes128_encrypt_sfs(unsigned char ctext0[16], unsigned char ctext1[16],
				const unsigned char ptext0[16], const unsigned char ptext1[16],
				const uint32_t rkeys[88]);
void aes256_encrypt_sfs(unsigned char ctext0[16], unsigned char ctext1[16],
				const unsigned char ptext0[16], const unsigned char ptext1[16],
				const uint32_t rkeys[120]);

/* Fully-fixsliced key schedule functions */
void aes128_keyschedule_ffs(uint32_t rkeys[88], const unsigned char key0[16],
				const unsigned char key1[16]);
void aes256_keyschedule_ffs(uint32_t rkeys[120], const unsigned char key0[32],
				const unsigned char key1[32]);

/* Semi-fixsliced key schedule functions */
void aes128_keyschedule_sfs(uint32_t rkeys[88], const unsigned char key0[16],
				const unsigned char key1[16]);
void aes256_keyschedule_sfs(uint32_t rkeys[120], const unsigned char key0[32],
				const unsigned char key1[32]);

/* Fully-fixsliced key schedule functions (LUT-based) */
void aes128_keyschedule_ffs_lut(uint32_t rkeys[88],const unsigned char key[16]);
void aes256_keyschedule_ffs_lut(uint32_t rkeys[120], const unsigned char key[32]);

/* Semi-fixsliced key schedule functions (LUT-based) */
void aes128_keyschedule_sfs_lut(uint32_t rkeys[88], const unsigned char key[16]);
void aes256_keyschedule_sfs_lut(uint32_t rkeys[120], const unsigned char key[32]);

#endif 	// AES_H_

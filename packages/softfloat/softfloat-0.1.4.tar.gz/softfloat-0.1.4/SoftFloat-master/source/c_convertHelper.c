#include <stdio.h> 
#include <inttypes.h> 

#include "platform.h"
#include "internals.h"


/* This method is faster than the OpenEXR implementation (very often
 * used, eg. in Ogre), with the additional benefit of rounding, inspired
 * by James Tursa’s half-precision code. */
static inline uint16_t float_to_half_branch(uint32_t x)
{
    uint16_t bits = (x >> 16) & 0x8000; /* Get the sign */
    uint16_t m = (x >> 12) & 0x07ff; /* Keep one extra bit for rounding */
    unsigned int e = (x >> 23) & 0xff; /* Using int is faster here */

    /* If zero, or denormal, or exponent underflows too much for a denormal
     * half, return signed zero. */
    if (e < 103)
        return bits;

    /* If NaN, return NaN. If Inf or exponent overflow, return Inf. */
    if (e > 142)
    {
        bits |= 0x7c00u;
        /* If exponent was 0xff and one mantissa bit was set, it means NaN,
         * not Inf, so make sure we set one mantissa bit too. */
        bits |= e == 255 && (x & 0x007fffffu);
        return bits;
    }

    /* If exponent underflows but not too much, return a denormal */
    if (e < 113)
    {
        m |= 0x0800u;
        /* Extra rounding may overflow and set mantissa to 0 and exponent
         * to 1, which is OK. */
        bits |= (m >> (114 - e)) + ((m >> (113 - e)) & 1);
        return bits;
    }

    bits |= ((e - 112) << 10) | (m >> 1);
    /* Extra rounding. An overflow will set mantissa to 0 and increment
     * the exponent, which is OK. */
    bits += m & 1;
    return bits;
}


uint32_t static halfToFloatI(uint16_t y);
union ui32_f32_convert  {
    uint32_t ui; // here_write_bits
    float    f; // here_read_float
};

union ui64_f64_convert  {
    uint64_t ui; // here_write_bits
    double    f; // here_read_float
};

float64_t convertDoubleToF64(double a){
	union ui64_f64 uTmp;
	union ui64_f64_convert uA;

	uA.f = a;
	uTmp.ui = uA.ui;
	return uTmp.f;
}

float32_t convertDoubleToF32(float a){
	union ui32_f32 uTmp;
	union ui32_f32_convert uA;

	uA.f = a;
	uTmp.ui = uA.ui;
	return uTmp.f;
}

float16_t convertDoubleToF16(float a){
	union ui32_f32_convert uA;
	union ui16_f16 uTmp;
	uA.f = a;
	uTmp.ui = float_to_half_branch(uA.ui);
	return uTmp.f;
}

double convertF64ToDouble(float64_t y){
	union ui64_f64 uTmp;
	union ui64_f64_convert uA;
	uTmp.f = y;
	uA.ui = uTmp.ui;
	return uA.f;

}
float convertF32ToDouble(float32_t y){
	union ui32_f32 uTmp;
	union ui32_f32_convert uA;
	uTmp.f = y;
	uA.ui = uTmp.ui;
	return uA.f;
}

float convertF16ToDouble(float16_t y) {
	union {
		float f; uint32_t i;
	} v;

	union ui16_f16 uA;
	uA.f = y;
	v.i = halfToFloatI(uA.ui);
	return v.f;
}

uint32_t halfToFloatI(uint16_t y) {
	int s = (y >> 15) & 0x00000001; // sign
	int e = (y >> 10) & 0x0000001f; // exponent
	int f = y & 0x000003ff; // fraction

	// need to handle 7c00 INF and fc00 -INF?
	if (e == 0) {
		// need to handle +-0 case f==0 or f=0x8000?
		if (f == 0) // Plus or minus zero
			return s << 31;
		else { // Denormalized number -- renormalize it
			while (!(f & 0x00000400)) {
				f <<= 1;
				e -= 1;
			}
			e += 1;
			f &= ~0x00000400;
		}
	}
	else if (e == 31) {
		if (f == 0) // Inf
			return (s << 31) | 0x7f800000;
		else // NaN
			return (s << 31) | 0x7f800000 | (f << 13);
	}
	e = e + (127 - 15);
	f = f << 13;

	return ((s << 31) | (e << 23) | f);

}

void printHex(uint64_t s) {
	printf("0x%llx\n", s);

}

void printBinary(uint64_t * s, int size) {
	int i;
	uint64_t number = *s;
	int bitSize = size -1;
	for(i = 0; i < size; ++i) {
		if(i%8 == 0)
			putchar(' ');
		printf("%llu", (number >> (bitSize-i))&1);
	}
	printf("\n");

}

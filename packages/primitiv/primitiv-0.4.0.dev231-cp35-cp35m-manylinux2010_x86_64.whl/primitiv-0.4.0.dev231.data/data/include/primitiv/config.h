#ifndef PRIMITIV_CONFIG_H_
#define PRIMITIV_CONFIG_H_

/* #undef PRIMITIV_BUILD_TESTS_PROBABILISTIC */
#define PRIMITIV_BUILD_STATIC_LIBRARY
/* #undef PRIMITIV_USE_CACHE */
#define PRIMITIV_USE_EIGEN
/* #undef PRIMITIV_USE_CUDA */
/* #undef PRIMITIV_USE_CUDNN */
/* #undef PRIMITIV_USE_OPENCL */

#if defined(__x86_64__) || defined(__ppc64__)
#define PRIMITIV_WORDSIZE_64
#endif  // defined(__x86_64__) || defined(__ppc64__)

#ifdef __i386
#define PRIMITIV_MAYBE_FPMATH_X87
#endif // __i386

#endif  // PRIMITIV_CONFIG_H_

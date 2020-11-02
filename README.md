# SimpleProfiler


Simple profiling tool for measuring run-time performance of batch jobs.

Contains implementations in **Kotlin** and **Python 3.6+**.

Read my [blog post](https://medium.com/@davidoha/simple-runtime-profiling-of-batch-jobs-in-production-ddd59e192924) about it. 


### Example: Measureing performance of various hashing algorithms

In Kotlin: 

```kotlin
package davidoh.sample

import davidoh.profiling.SimpleProfiler
import java.security.MessageDigest
import kotlin.math.sqrt

fun main() {
    val profiler = SimpleProfiler(
        enclosingSectionName = "total",
        resetAfterSampleCount = 500000
    )

    println("app started")

    profiler.startSection("init")
    val md5 = MessageDigest.getInstance("MD5")
    val sha1 = MessageDigest.getInstance("SHA-1")
    val sha256 = MessageDigest.getInstance("SHA-256")
    val r = java.util.Random()
    val bytes = ByteArray(10000)
    r.nextBytes(bytes)
    profiler.endSection()

    while (true) {
        profiler.startSection("total")

        profiler.startSection("hashing")

        profiler.startSection("md5")
        md5.digest(bytes)
        profiler.endSection()

        profiler.startSection("sha256")
        sha256.digest(bytes)
        profiler.endSection()

        profiler.startSection("sha1")
        sha1.digest(bytes)
        profiler.endSection()

        profiler.endSection("hashing")

        profiler.startSection("random")
        val randNum = r.nextDouble() * 1000000 + 1
        profiler.endSection()

        profiler.startSection("sqrt")
        sqrt(randNum)
        profiler.endSection()

        profiler.endSection("total")
        if (profiler.report())
            println("-----")
    }
}
```

In Python: 

```python
import hashlib
import math
import os
import random

from simple_profiler import SimpleProfiler

print("app started")

profiler = SimpleProfiler(enclosing_section_name="total", 
                          reset_after_sample_count=500000)

profiler.start_section("init")
payload = os.urandom(10000)
r = random.random()
profiler.end_section()

while True:
    profiler.start_section("total")

    profiler.start_section("hashing")

    profiler.start_section("md5")
    hashlib.md5(payload)
    profiler.end_section()

    profiler.start_section("sha1")
    hashlib.sha1(payload)
    profiler.end_section()

    profiler.start_section("sha256")
    hashlib.sha256(payload)
    profiler.end_section()

    profiler.end_section("hashing")

    profiler.start_section("random")
    rand_number = random.random() * 1000000 + 1
    profiler.end_section("random")

    profiler.start_section("sqrt")
    math.sqrt(rand_number)
    profiler.end_section()

    profiler.end_section("total")

    if profiler.report():
        print("-------")
```

Sample output:
```
total          : took      9.87 s (100.00%),     86,889 samples,    113.58 (   113.58) ms / 1000 samples,      8,804.39 (     8,804.39) hz
hashing        : took      9.76 s ( 98.89%),     86,889 samples,    112.32 (   112.32) ms / 1000 samples,      8,903.15 (     8,903.15) hz
sha1           : took      3.89 s ( 39.37%),     86,889 samples,     44.72 (    44.72) ms / 1000 samples,     22,362.05 (    22,362.05) hz
sha256         : took      3.07 s ( 31.13%),     86,889 samples,     35.36 (    35.36) ms / 1000 samples,     28,283.50 (    28,283.50) hz
md5            : took      2.72 s ( 27.54%),     86,889 samples,     31.28 (    31.28) ms / 1000 samples,     31,970.85 (    31,970.85) hz
init           : took      0.06 s (  0.57%),          1 samples, 56,346.55 (56,346.55) ms / 1000 samples,         17.75 (        17.75) hz
random         : took      0.03 s (  0.29%),     86,889 samples,      0.33 (     0.33) ms / 1000 samples,  3,023,135.87 ( 3,023,135.87) hz
sqrt           : took      0.01 s (  0.13%),     86,889 samples,      0.15 (     0.15) ms / 1000 samples,  6,703,392.64 ( 6,703,392.64) hz
-----
```

## Comments

* The profiler is not (yet) thread-safe. 

## License

Apache-2.0


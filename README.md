# SimpleProfiler

![Sample Output](docs/output_sample.png)

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
    val profiler = SimpleProfiler(resetAfterSampleCount = 500000)

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

profiler = SimpleProfiler(reset_after_sample_count=500000)

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
total               : took      9.94 s (100.00%),       96,776 samples,    102.69 (   102.69) ms / 1000 samples,      9,738.11 (     9,738.11) hz
 hashing            : took      9.87 s ( 99.33%),       96,776 samples,    102.00 (   102.00) ms / 1000 samples,      9,803.81 (     9,803.81) hz
  sha1              : took      3.98 s ( 40.01%),       96,776 samples,     41.09 (    41.09) ms / 1000 samples,     24,339.19 (    24,339.19) hz
  sha256            : took      3.04 s ( 30.58%),       96,776 samples,     31.40 (    31.40) ms / 1000 samples,     31,842.21 (    31,842.21) hz
  md5               : took      2.80 s ( 28.16%),       96,776 samples,     28.91 (    28.91) ms / 1000 samples,     34,585.10 (    34,585.10) hz
init                : took      0.01 s (  0.14%),            1 samples, 14,022.17 (14,022.17) ms / 1000 samples,         71.32 (        71.32) hz
 random             : took      0.01 s (  0.12%),       96,776 samples,      0.13 (     0.13) ms / 1000 samples,  7,946,587.01 ( 7,946,587.01) hz
 sqrt               : took      0.01 s (  0.07%),       96,776 samples,      0.08 (     0.08) ms / 1000 samples, 13,209,724.44 (13,209,724.44) hz
-----
```

## Comments

* The profiler is not (yet) thread-safe. 

## License

Apache-2.0


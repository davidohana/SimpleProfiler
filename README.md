# SimpleProfiler


Simple profiling tool for measuring run-time performance of batch jobs (wip).

Contains implementations in Kotlin and Python.

```kotlin
import davidoh.profiling.SimpleProfiler
import java.math.BigInteger
import java.security.MessageDigest
import kotlin.math.sqrt

fun main(args: Array<String>) {
    val profiler = SimpleProfiler(reportSec = 10, enclosingSectionName = "--total--", resetAfterSampleCount = 500000)

    profiler.startSection("init")
    val md5 = MessageDigest.getInstance("MD5")
    val sha1 = MessageDigest.getInstance("SHA-1")
    val sha256 = MessageDigest.getInstance("SHA-256")
    val r = java.util.Random()
    profiler.endSection()

    println("app started")
    for (i in 0..999999999) {
        profiler.startSection("--total--")

        profiler.startSection("create_payload")
        val bytes = ByteArray(1000)
        r.nextBytes(bytes)
        profiler.endSection()

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

        profiler.startSection("sqrt")
        sqrt(r.nextDouble() * 1000)
        profiler.endSection()

        profiler.startSection("probablePrime")
        BigInteger.probablePrime(32, r)
        profiler.endSection()

        profiler.endSection("--total--")
        profiler.periodicReport()
    }
    println("app ended")
}
```

Sample Output:
```
--total--      : took      9.95 s (100.00)%,     97,136 samples,    102.39 (   102.39) ms per 1K samples,      9,766.85 (     9,766.85) samples/s
probablePrime  : took      8.34 s ( 83.81)%,     97,136 samples,     85.81 (    85.81) ms per 1K samples,     11,653.93 (    11,653.93) samples/s
hashing        : took      1.21 s ( 12.15)%,     97,136 samples,     12.44 (    12.44) ms per 1K samples,     80,371.76 (    80,371.76) samples/s
sha1           : took      0.45 s (  4.48)%,     97,136 samples,      4.59 (     4.59) ms per 1K samples,    217,955.26 (   217,955.26) samples/s
sha256         : took      0.41 s (  4.12)%,     97,136 samples,      4.22 (     4.22) ms per 1K samples,    236,998.52 (   236,998.52) samples/s
create_payload : took      0.32 s (  3.25)%,     97,136 samples,      3.33 (     3.33) ms per 1K samples,    300,425.37 (   300,425.37) samples/s
md5            : took      0.31 s (  3.07)%,     97,136 samples,      3.15 (     3.15) ms per 1K samples,    317,933.78 (   317,933.78) samples/s
init           : took      0.01 s (  0.13)%,          1 samples, 12,440.59 (12,440.59) ms per 1K samples,         80.38 (        80.38) samples/s
sqrt           : took      0.01 s (  0.12)%,     97,136 samples,      0.12 (     0.12) ms per 1K samples,  8,084,393.42 ( 8,084,393.42) samples/s
```
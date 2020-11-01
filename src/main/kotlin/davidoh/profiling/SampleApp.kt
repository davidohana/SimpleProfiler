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

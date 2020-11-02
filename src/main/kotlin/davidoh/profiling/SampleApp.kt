import davidoh.profiling.SimpleProfiler
import java.security.MessageDigest
import kotlin.math.sqrt

fun main(args: Array<String>) {
    val profiler = SimpleProfiler(reportSec = 10, enclosingSectionName = "total", resetAfterSampleCount = 500000)

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

//        profiler.startSection("probablePrime")
//        BigInteger.probablePrime(32, r)
//        profiler.endSection()

        profiler.endSection("total")
        if (profiler.periodicReport())
            println("-----")
    }
}

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
    profiler.end_section()

    profiler.start_section("sqrt")
    math.sqrt(rand_number)
    profiler.end_section()

    profiler.end_section("total")

    if profiler.report(10):
        print("-------")

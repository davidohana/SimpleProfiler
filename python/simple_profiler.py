"""
Description : A simple section-based performance profiler
Author      : David Ohana
Author_email: david.ohana@ibm.com
License     : MIT
"""
import os
import time

from abc import ABC, abstractmethod


class Profiler(ABC):

    @abstractmethod
    def start_section(self, section_name: str):
        pass

    @abstractmethod
    def end_section(self, section_name=""):
        pass

    @abstractmethod
    def periodic_report(self):
        pass

    @abstractmethod
    def print_results(self):
        pass


class NullProfiler(Profiler):
    def start_section(self, section_name: str):
        pass

    def end_section(self, section_name=""):
        pass

    def periodic_report(self):
        pass

    def print_results(self):
        pass


class SimpleProfiler(Profiler):
    def __init__(self, reset_after_sample_count=0, enclosing_section_name="", printer=print, report_sec=30):
        self.printer = printer
        self.enclosing_section_name = enclosing_section_name
        self.reset_after_sample_count = reset_after_sample_count
        self.report_sec = report_sec

        self.section_to_stats = {}
        self.last_report_timestamp_sec = time.time()
        self.last_started_section_name = ""

    def start_section(self, section_name: str):
        if not section_name:
            raise ValueError("Section name is empty")
        self.last_started_section_name = section_name

        section = self.section_to_stats.get(section_name, None)
        if section is None:
            section = ProfiledSectionStats(section_name)
            self.section_to_stats[section_name] = section

        if section.start_time_sec != 0:
            raise ValueError(f"Section {section_name} is already started")

        section.start_time_sec = time.time()

    def end_section(self, name=""):
        now = time.time()

        section_name = name
        if not name:
            section_name = self.last_started_section_name

        if not section_name:
            raise ValueError("Neither section name is specified nor a section is started")

        section: ProfiledSectionStats = self.section_to_stats.get(section_name, None)
        if section is None:
            raise ValueError(f"Section {section_name} does not exist")

        if section.start_time_sec == 0:
            raise ValueError(f"Section {section_name} was not started")

        took_sec = now - section.start_time_sec
        if self.reset_after_sample_count > 0 and section.sample_count == self.reset_after_sample_count:
            section.sample_count_batch = 0
            section.total_time_sec_batch = 0

        section.sample_count += 1
        section.total_time_sec += took_sec
        section.sample_count_batch += 1
        section.total_time_sec_batch += took_sec
        section.start_time_sec = 0

    def print_results(self):
        enclosing_time_sec = 0
        if self.enclosing_section_name:
            enclosing_section: ProfiledSectionStats = self.section_to_stats.get(self.enclosing_section_name, None)
            if enclosing_section:
                enclosing_time_sec = enclosing_section.total_time_sec

        include_batch_rates = self.reset_after_sample_count > 0
        text = ""

        sections = self.section_to_stats.values()
        sorted_sections = sorted(sections, key=lambda it: it.total_time_sec, reverse=True)
        for section in sorted_sections:
            text += section.to_string(enclosing_time_sec, include_batch_rates) + os.linesep
        self.printer(text)

    def periodic_report(self):
        if time.time() - self.last_report_timestamp_sec < self.report_sec:
            return
        self.print_results()
        self.last_report_timestamp_sec = time.time()


class ProfiledSectionStats:
    def __init__(self, section_name, start_time_sec=0, sample_count=0, total_time_sec=0,
                 sample_count_batch=0, total_time_sec_batch=0):
        self.section_name = section_name
        self.start_time_sec = start_time_sec
        self.sample_count = sample_count
        self.total_time_sec = total_time_sec
        self.sample_count_batch = sample_count_batch
        self.total_time_sec_batch = total_time_sec_batch

    def to_string(self, enclosing_time_sec: int, include_batch_rates: bool):
        took_sec_text = f"{self.total_time_sec:>8.2f} s"
        if enclosing_time_sec > 0:
            took_sec_text += f" ({100 * self.total_time_sec / enclosing_time_sec:>6.2f})%"

        ms_per_k_samples = f"{1000000 * self.total_time_sec / self.sample_count: 7.2f}"
        samples_per_sec = f"{self.sample_count / self.total_time_sec: 15,.2f}"

        if include_batch_rates:
            ms_per_k_samples += f" ({1000000 * self.total_time_sec_batch / self.sample_count_batch: 7.2f})"
            samples_per_sec += f" ({self.sample_count_batch / self.total_time_sec_batch: 15,.2f})"

        return f"{self.section_name: <15}: took {took_sec_text}, " \
               f"{self.sample_count: >10,} samples, " \
               f"{ms_per_k_samples} ms per 1K samples, " \
               f"{samples_per_sec} hz"
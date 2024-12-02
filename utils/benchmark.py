"""
Утилиты для тестирования производительности
"""
import time

class Benchmark:
    @staticmethod
    def measure_time(func, iterations=100):
        """Измеряет среднее время выполнения функции"""
        total_time = 0
        for _ in range(iterations):
            start_time = time.time()
            func()
            total_time += time.time() - start_time
        return total_time / iterations 
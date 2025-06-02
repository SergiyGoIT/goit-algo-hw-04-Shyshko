import random
import timeit
import statistics
import sys
from typing import List
import matplotlib.pyplot as plt

def insertion_sort(arr: List[int]) -> List[int]:
    # Сортування вставками
    arr = arr.copy()
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and arr[j] > key:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key
    return arr

def merge(left: List[int], right: List[int]) -> List[int]:
    # Об'єднання двох відсортованих масивів для сортування злиттям
    result = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    result.extend(left[i:])
    result.extend(right[j:])
    return result

def merge_sort(arr: List[int]) -> List[int]:
    # Сортування злиттям
    if len(arr) <= 1:
        return arr
    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])
    return merge(left, right)

def generate_datasets(size: int):
    # Генерація наборів даних
    random_data = [random.randint(0, 10000) for _ in range(size)]
    sorted_data = sorted(random_data)
    reverse_sorted_data = sorted_data[::-1]
    duplicated_data = [random.randint(0, 100) for _ in range(size)]  # Менший діапазон для дублікатів
    return {
        "random": random_data,
        "sorted": sorted_data,
        "reverse_sorted": reverse_sorted_data,
        "duplicated": duplicated_data
    }

def measure_time(algorithm, data: List[int], number: int = 10) -> float:
    # Вимірювання часу виконання за допомогою timeit
    setup_code = f'''
from sorting_comparison import {algorithm.__name__}
data = {data}
'''
    stmt = f"{algorithm.__name__}(data)"
    times = timeit.repeat(stmt, setup=setup_code, number=number, globals=globals())
    return statistics.mean(times) / number  # Середній час на одну ітерацію

def run_benchmarks(sizes: List[int]):
    # Виконання бенчмарків для різних розмірів даних
    algorithms = [
        ("Insertion Sort", insertion_sort),
        ("Merge Sort", merge_sort),
        ("Timsort", sorted)
    ]
    results = {alg_name: {size: {} for size in sizes} for alg_name, _ in algorithms}
    
    for size in sizes:
        datasets = generate_datasets(size)
        for dataset_name, data in datasets.items():
            for alg_name, alg_func in algorithms:
                time = measure_time(alg_func, data)
                results[alg_name][size][dataset_name] = time
                print(f"{alg_name}, Size: {size}, Dataset: {dataset_name}, Time: {time:.6f} seconds")
    
    return results

def save_results(results, filename="sorting_results.txt"):
    # Збереження результатів у файл
    with open(filename, "w") as f:
        f.write("Результати порівняння алгоритмів сортування\n\n")
        for alg_name in results:
            f.write(f"Алгоритм: {alg_name}\n")
            for size in results[alg_name]:
                f.write(f"  Розмір: {size}\n")
                for dataset_name, time in results[alg_name][size].items():
                    f.write(f"    Набір даних: {dataset_name}, Час: {time:.6f} секунд\n")
            f.write("\n")

def plot_results(results, sizes):
    # Побудова графіків для порівняння
    dataset_types = ["random", "sorted", "reverse_sorted", "duplicated"]
    
    for dataset in dataset_types:
        plt.figure(figsize=(10, 6))
        for alg_name in results:
            times = [results[alg_name][size][dataset] for size in sizes]
            plt.plot(sizes, times, marker='o', label=alg_name)
        
        plt.title(f"Порівняння часу виконання ({dataset} дані)")
        plt.xlabel("Розмір масиву")
        plt.ylabel("Час виконання (секунди)")
        plt.legend()
        plt.grid(True)
        plt.savefig(f"sorting_comparison_{dataset}.png")
        plt.close()
        print(f"Графік збережено у sorting_comparison_{dataset}.png")

def main():
    # Основна функція
    sizes = [100, 1000, 5000, 10000]  # Розміри наборів даних
    results = run_benchmarks(sizes)
    save_results(results)
    plot_results(results, sizes)
    
    # Аналіз та висновки
    print("\nВисновки:")
    print("1. Сортування вставками (Insertion Sort):")
    print("   - Теоретична складність: O(n²) у середньому та в найгіршому випадку.")
    print("   - Добре працює на малих і майже відсортованих масивах.")
    print("   - Значно повільніше на великих масивах.")
    print("2. Сортування злиттям (Merge Sort):")
    print("   - Теоретична складність: O(n log n) у всіх випадках.")
    print("   - Стабільна продуктивність незалежно від типу даних.")
    print("   - Потребує додаткової пам’яті.")
    print("3. Timsort (вбудований sorted):")
    print("   - Теоретична складність: O(n log n) у середньому, O(n) для майже відсортованих.")
    print("   - Оптимізований гібрид сортування злиттям і вставками.")
    print("   - Найшвидший у всіх тестах завдяки адаптивності до структури даних.")
    print("\nTimsort ефективніший, оскільки поєднує переваги сортування вставками (швидкість на малих і майже відсортованих масивах) та сортування злиттям (стабільність на великих масивах). Це пояснює, чому програмісти віддають перевагу вбудованим функціям Python.")

if __name__ == "__main__":
    main()

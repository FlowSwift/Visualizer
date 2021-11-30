


# Algorithms Visualizer

A program to visualize sorting algorithms and pathfinder algorithms(FUTURE FEATURE)

## Development

```python
python3 -m venv venv
. venv/bin/activate
pip install -r requirements.txt
```

## Running

```python
python3 visualizer_main.py
```

Press the spacebar to begin the sorting visualizer

# Sorting Visualizer

## Controls:
left-right arrow keys: Change sorting speed.
up-down arrow keys: Change array length
Spacebar: Start a new sort and generate a new array
Use the mouse to choose between different options and modes in the overlay

### Delay: 
Use the left and right arrow keys to change the amount of delay between animations. 
Has a maximum vlalue of 150.

### Length:
Use the up and down arrow keys to change the amount of numbers or bars in the array.  
Has a maximum vlalue of 250.

### Array Modes: 
Change the way an array generates when a new sort starts using 2 options.
1. Random: Generate a random array with duplicates or no duplicates depending on user selection.
2. Nearly Sorted: Generate a sorted array with duplicates or no duplicates depending on user selection then swap `unsorted_amount` elements to make a nearly sorted array. Change unsorted_amount by using the + and - option on the overlay.

### Duplicates: 
Choose True or False to generate an array with or without duplicates on a new sort

## Sort Modes: 
### Curretnly Available Sort Modes:
#### 1. Bubble Sort: 

Bubble Sort is a sorting algorithm that works by looping over an array `n` times, looping over the array `n - i - 1` times each time where `i` is our main loop current iterator. To find the smallest number, on each inner loop, compare pairs of numbers from left to right and swap them if the left number is bigger than the right number.
`i` can be used to loop 1 less time on every main loop to maximize efficiency since the highest number will always be on the right side of the array and sorted once a main loop is done. If a main loop has finished without any swaps during it, the array is sorted and the sort is finished.

**Worst and Average Case Time Complexity:** `O(n^2)`. Worst case occurs when array is reverse sorted.  
**Best Case Time Complexity:** `O(n)` Best case occurs when array is already sorted.  
**Boundary Cases:** Bubble sort takes minimum time (Order of n) when elements are already sorted.  
**Stable:** Yes

#### 2. Selection Sort: 

Selection Sort algorithm works by loop over an array `n` times. On every loop, iterate over the array `n - i` times, where `i` is the current main loop iterator, starting from `i` on every main loop. When iterating over the array, find the smallest number after the index `i` that is smaller `i`th number, then swap it with the index `i`.
Selection Sort has no boundary cases and will take almost as much time for a nearly sorted array.

**Time Complexity:** `O(n^2)`. Worst case occurs when array is reverse sorted.  
**Stable**: No (in this implementation)

#### 3. Merge Sort: 

Merge Sort sorting alogrithm works on the Divide and Conquer principle. Recursively call itself and split the array in halfs until you reach 1 elements sub arrays(which are sorted) and merge it with the other half sub arrays in a way that it is a sorted array after by adding numbers to a new array in an incrementing order.

**Average Time Complexity:**  `O(n log n)`
**Algorithmic Paradigm:** Divide and Conquer  
**Stable:**  Yes
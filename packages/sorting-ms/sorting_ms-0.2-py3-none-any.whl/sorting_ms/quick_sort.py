# quick sort
def partition(myList, start, end):
    pivot = myList[start]
    left = start + 1
    # Start outside the area to be partitioned
    right = end
    done = False
    while not done:
        while left <= right and myList[left] <= pivot:
            left = left + 1
        while myList[right] >= pivot and right >= left:
            right = right - 1
        if right < left:
            done = True
        else:
            # swap places
            temp = myList[left]
            myList[left] = myList[right]
            myList[right] = temp
    # swap start with myList[right]
    temp = myList[start]
    myList[start] = myList[right]
    myList[right] = temp
    return right


def quick_sort(myList, start, end):
    if start < end:
        # partition the list
        split = partition(myList, start, end)
        # sort both halves
        quick_sort(myList, start, split - 1)
        quick_sort(myList, split + 1, end)
    return myList


def main():
    myList = [54, 26, 93, 17, 77, 31, 44, 55, 20]
    sortedList = quick_sort(myList, 0, len(myList) - 1)
    print(sortedList)

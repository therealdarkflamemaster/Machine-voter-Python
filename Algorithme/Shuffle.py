# customized Shuffle realisation
import random


def shuffle(target):
    for change in range(len(target) - 1, 0, -1):
        lower = random.randint(0, change)
        # in place action, don't need to return the target one more time
        target[lower], target[change] = target[change], target[lower]

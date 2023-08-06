import math


def distribute(whole, cnt):
    remains = whole
    progress = 0

    if whole >= cnt:
        while remains > 0:
            current_portion = math.ceil(remains / cnt)
            progress += current_portion
            remains -= current_portion

            cnt -= 1
            yield (progress, current_portion, remains, cnt)

    else:
        while cnt > 0:
            repeat = math.floor(cnt / remains)

            current_portion = 1
            progress += current_portion
            remains -= current_portion

            while repeat > 0:
                repeat -= 1
                cnt -= 1
                yield (progress, current_portion, remains, cnt)

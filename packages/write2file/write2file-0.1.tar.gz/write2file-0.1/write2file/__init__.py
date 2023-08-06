def write2file(fp, lyst, new=False):
    if new:
        with open(fp, 'w') as f:
            f.write(','.join(lyst))
            f.write('\n')
    else:
        with open(fp, 'a') as f:
            f.write(','.join(list(map(str, lyst))))
            f.write('\n')

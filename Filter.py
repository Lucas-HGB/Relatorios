def math_size(B):
    B = float(B)
    KB = float(1024)
    MB = float(KB ** 2) # 1,048,576
    GB = float(KB ** 3) # 1,073,741,824
    TB = float(KB ** 4) # 1,099,511,627,776

    if B < KB:
        return '{0} {1}'.format(B,'Bytes' if 0 == B > 1 else 'Byte')
    elif KB <= B < MB:
        return '{0:.2f} KB'.format(B/KB)
    elif MB <= B < GB:
        return '{0:.2f} MB'.format(B/MB)
    elif GB <= B < TB:
        return '{0:.2f} GB'.format(B/GB)
    elif TB <= B:
        return '{0:.2f} TB'.format(B/TB)


def math_network(B):
    B = float(B)
    KB = float(1000)
    MB = float(KB ** 2) # 1,048,576
    GB = float(KB ** 3) # 1,073,741,824
    TB = float(KB ** 4) # 1,099,511,627,776

    if B < KB:
        return '{0} {1}'.format(B,'Bytes' if 0 == B > 1 else 'Byte')
    elif KB <= B < MB:
        return '{0:.2f} Kbps'.format(B/KB)
    elif MB <= B < GB:
        return '{0:.2f} Mbps'.format(B/MB)
    elif GB <= B < TB:
        return '{0:.2f} GB'.format(B/GB)
    elif TB <= B:
        return '{0:.2f} TB'.format(B/TB)


def Convert(name, last, max, med, min):
    a = True
    if "TAMANHO TOTAL USADO" in name.upper():
        last_convert = math_size(last)
        max_convert = math_size(max)
        med_convert = math_size(med)
        min_convert = math_size(min)
    elif "MONITORAMENTO DO TAMANHO DA INSTANCE" in name.upper():
        last_convert = math_size(last)
        max_convert = math_size(max)
        med_convert = math_size(med)
        min_convert = math_size(min)
    elif "SPACE" in name.upper() and "PERCENTAGE" not in name.upper():
        last_convert = math_size(last)
        max_convert = math_size(max)
        med_convert = math_size(med)
        min_convert = math_size(min)
    elif "MEMORY" in name.upper():
        last_convert = math_size(last)
        max_convert = math_size(max)
        med_convert = math_size(med)
        min_convert = math_size(min)
    elif "TRAFFIC" in name.upper():
        if last != 0:
            last_convert = math_network(last)
            max_convert = math_network(max)
            med_convert = math_network(med)
            min_convert = math_network(min)
    else:
        a = False
    if a:
        return last_convert, max_convert, med_convert, min_convert
    else:
        return last, max, med, min

    
if __name__ == "__main__":
    pass

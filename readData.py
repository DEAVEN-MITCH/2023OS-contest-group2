def read_hit_rates(file_path, file_name, method_name):
    '''
    file_path: 文件路径
    file_name: 数据集的名称
    method_name: 方法名称
    '''
    hit_rates = []

    with open(file_path, 'r') as file:
        lines = file.readlines()

    i = 0
    while i < len(lines):
        line = lines[i].strip()
        if line.startswith("traceFile:"):
            if line == f"traceFile:{file_name}":
                flag = True
            else:
                flag = False
        if line.startswith(method_name) and flag:
            hit_rate_line = lines[i].strip().split('\t')
            hit_rates.append(float(hit_rate_line[-1]))
        i += 1
        
    return hit_rates

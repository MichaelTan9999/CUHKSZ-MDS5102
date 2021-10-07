from math import sin, cos, tan

try:
    func_type = input('Enter function type (sin, cos, tan): ')
    if func_type not in ['sin', 'cos', 'tan']:
        raise TypeError
    
    interval_a = eval(input('Enter interval start point: '))
    interval_b = eval(input('Enter interval end point: '))
    if type(interval_a) not in [int, float] or type(interval_b) not in [int, float]:
        raise TypeError
    
    num_intervals = int(eval(input('Enter number of sub-intervals: ')))
    if type(num_intervals) != int:
        raise TypeError
    if num_intervals < 1:
        raise ValueError
    
except(TypeError, NameError, SyntaxError, ValueError):
    print('Something you entered is not valid, please check.')

else:
    if func_type == 'sin':
        f = sin
    elif func_type == 'cos':
        f = cos
    else:
        f = tan

    sum = 0
    for i in range(1, num_intervals + 1):
        sum += (interval_b - interval_a) / num_intervals * f(interval_a + (interval_b - interval_a) / num_intervals * (i - 0.5))
    print('Integral from {} to {} on {} is {:.3f}'.format(interval_a, interval_b, func_type, sum))
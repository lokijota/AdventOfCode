### the following block of code was an attempt at narrowing down which bits are wrong based on
### the trying different calculations and seeing which positions are wrong. But the results of bit N+1
### are affected potentially by the "carry" of bit N, so this ends up identifying as wrong, structures
### that are right. Discarding.

def set_inputs(circuit: dict, x: str, y:str):
    """Sets an x and y (binary strings) as inputs to the circuit"""
    for gate_name, gate_def in circuit.items():

        if gate_def[1] == "input":
            pos = int(gate_name[1:])

            if gate_name.startswith("x"):
                gate_def[0] = int(x[44-pos])
            elif gate_name.startswith("y"):
                gate_def[0] = int(y[44-pos])
        else:
            gate_def[0] = None

def calculate_all_outputs(circuit):
    """ Calculate all the output z variables and return result """
    result = []

    for bit_pos in range(0, 46):
        current_var = f'z{bit_pos:02}'
        result.insert(0, calculate(current_var, circuit))

    return "".join([str(dig) for dig in result])

def find_bad_bits(x, y, z):
    bad_bits = set()
    
    right_answer = bin(int(x,2) + int(y,2))[2:].zfill(46) # [2:] because bin adds 0b as prefix
    
    for pos in range(0, len(z)):
        if right_answer[45-pos] != z[45-pos]:
            bad_bits.add(pos)
        
    return bad_bits

def find_wrong_bits(circuit):

    wrong_bits = set()

    all_zeros =   "000000000000000000000000000000000000000000000"
    all_ones =    "111111111111111111111111111111111111111111111"
    alternating = "101010101010101010101010101010101010101010101"

    set_inputs(circuit, all_zeros, all_zeros)
    result = calculate_all_outputs(circuit)
    wrong_bits.update(find_bad_bits(all_zeros, all_zeros, result))

    set_inputs(circuit, all_ones, all_ones)
    result = calculate_all_outputs(circuit)
    wrong_bits.update(find_bad_bits(all_ones, all_ones, result))

    set_inputs(circuit, all_ones, all_zeros)
    result = calculate_all_outputs(circuit)
    wrong_bits.update(find_bad_bits(all_ones, all_zeros, result))

    set_inputs(circuit, all_zeros, all_ones)
    result = calculate_all_outputs(circuit)
    wrong_bits.update(find_bad_bits(all_zeros, all_ones, result))

    set_inputs(circuit, alternating, alternating)
    result = calculate_all_outputs(circuit)
    wrong_bits.update(find_bad_bits(alternating, alternating, result))

    set_inputs(circuit, all_ones, alternating)
    result = calculate_all_outputs(circuit)
    wrong_bits.update(find_bad_bits(all_ones, alternating, result))

    return wrong_bits

# find the bad bits
bb = find_wrong_bits(circuit)

### This is an older version of the code above, that just looks at the provided input
### Discarding

# find "suspicious bits": as their results are wrong
suspicious_bits = []
error_sequence = False
for bits in range(0, output_bits+1):
    current_var = f'z{bits:02}'
    values[bits] = calculate(current_var, circuit)

    if values[bits] != int(desired_z_bin[output_bits-bits]):
        if error_sequence == False:
            suspicious_bits.append(current_var)
        error_sequence = True
    else:
        error_sequence = False

print(suspicious_bits)

for suspicious_bit in suspicious_bits:
    print("Suspicious bit: ", suspicious_bit, "has deps: ", trace_dependencies_variable(circuit, suspicious_bit, False))


### This is code that tries all the combinations of gate swaps. It WAY TOO SLOW
### Discarding.

values = np.zeros(output_bits+1, dtype=int)

for s0 in tqdm(range(0, len(variables))):
    print("s0", s0)
    for s1 in range(s0+1, len(variables)):
        print("s1", s1)
        for s2 in range(s1+1, len(variables)):
            print("s2", s2)
            for s3 in range(s2+1, len(variables)):
                for s4 in range(s3+1, len(variables)):
                    for s5 in range(s4+1, len(variables)):
                        for s6 in range(s5+1, len(variables)):
                            for s7 in range(s6+1, len(variables)):

                                nreps += 1
                                # not needed as I'm now testing bit by bit as it is output'ed


                                # for j in range(0,output_bits+1):
                                #     values[j] = 0
                                for var in variables:
                                    circuit[var][0] = None

                                # swap
                                circuit[variables[s0]], circuit[variables[s1]] = circuit[variables[s1]], circuit[variables[s0]]
                                circuit[variables[s2]], circuit[variables[s3]] = circuit[variables[s3]], circuit[variables[s2]]
                                circuit[variables[s4]], circuit[variables[s5]] = circuit[variables[s5]], circuit[variables[s4]]
                                circuit[variables[s6]], circuit[variables[s7]] = circuit[variables[s7]], circuit[variables[s6]]

                                # calculate

                                for bits in range(output_bits, -1, -1):
                                    current_var = f'z{bits:02}' # posso ter isto num diccionário e trocar o string build por um lookup, mas será mais rápido?
                                    values[bits] = calculate(current_var, circuit)
                                    # loop_detector.clear()

                                    if values[bits] != int(desired_z_bin[output_bits-bits]) or calculation_loop_error == True: 
                                        # restore
                                        circuit[variables[s0]], circuit[variables[s1]] = circuit[variables[s1]], circuit[variables[s0]]
                                        circuit[variables[s2]], circuit[variables[s3]] = circuit[variables[s3]], circuit[variables[s2]]
                                        circuit[variables[s4]], circuit[variables[s5]] = circuit[variables[s5]], circuit[variables[s4]]
                                        circuit[variables[s6]], circuit[variables[s7]] = circuit[variables[s7]], circuit[variables[s6]]

                                        if max_bit_matched < bits:
                                            max_bit_matched = bits
                                            print("new max bit: ", max_bit_matched, "nreps: ", nreps, "swaps:", s0, s1, s2, s3, s4, s5, s6, s7, "at", (time.time() - start_time))
                                        
                                        calculation_loop_error = True
                                        break

                                if calculation_loop_error == True:
                                    calculation_loop_error = False
                                    break


                                # restore
                                circuit[variables[s0]], circuit[variables[s1]] = circuit[variables[s1]], circuit[variables[s0]]
                                circuit[variables[s2]], circuit[variables[s3]] = circuit[variables[s3]], circuit[variables[s2]]
                                circuit[variables[s4]], circuit[variables[s5]] = circuit[variables[s5]], circuit[variables[s4]]
                                circuit[variables[s6]], circuit[variables[s7]] = circuit[variables[s7]], circuit[variables[s6]]

                                result = "".join([str(x) for x in values])
                                result = int(result, 2)

                                if result == desired_z:
                                    result_list = list(unique_ops)
                                    result_list.sort()
                                    result = "".join(result_list)
                                    print("Found!", result )
                                    input("press any key")
                                    input("press any key again")
                                    break

## try to use networkx to find the error visually
                                
nx_edges = []
for k,v in circuit.items():
    if k.startswith("x") or k.startswith("y"):
        continue

    nx_edges.append((v[2], k))
    nx_edges.append((v[3], k))

Gfull = nx.DiGraph()
Gfull.add_edges_from(nx_edges)

for n in range(0, 46):
    GforZ = nx.DiGraph()

    output_node_name = f'z{n:02}'

    for edge in Gfull.edges():
        if nx.has_path(Gfull, edge[1], output_node_name):
            GforZ.add_edges_from([edge]) 
        
    options = {
        'node_color': 'red',
        'node_size': 5,
        'width': 2,
        'edge_color': 'green',
        'font_size': 11
    }

    subax1 = plt.subplot(111) # the figure has 1 row, 1 columns, and this plot is the first plot.
    fig = plt.figure(1, figsize=(1000, 500), dpi=60)
    nx.draw_spectral(GforZ, with_labels=True, font_weight='normal', **options)
    plt.show()
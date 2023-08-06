#!/usr/bin/python
from cis_interface.interface.CisInterface import CisInput, CisOutput


if __name__ == '__main__':

    # Get input and output channels matching yaml
    in1 = CisInput('input1_python')
    in2 = CisInput('static_python')
    out1 = CisOutput('output_python')
    print('SaM(P): Set up I/O channels')

    # Get input from input1 channel
    ret, adata = in1.recv()
    if not ret:
        raise RuntimeError('SaM(P): ERROR RECV from input1')
    a = int(adata)
    print('SaM(P): Received %d from input1' % a)

    # Get input from static channel
    ret, bdata = in2.recv()
    if not ret:
        raise RuntimeError('SaM(P): ERROR RECV from static')
    b = int(bdata)
    print('SaM(P): Received %d from static' % b)

    # Compute sum and send message to output channel
    sum = a + b
    outdata = '%d' % sum
    ret = out1.send(outdata)
    if not ret:
        raise RuntimeError('SaM(P): ERROR SEND to output')
    print('SaM(P): Sent to output')

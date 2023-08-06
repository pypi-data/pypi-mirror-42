# Import classes for input/output channels
from cis_interface.interface.CisInterface import (
    CisAsciiTableInput, CisAsciiTableOutput)

# Initialize input/output channels
in_channel = CisAsciiTableInput('inputB')
out_channel = CisAsciiTableOutput('outputB', '%6s\t%d\t%f\n')

# Loop until there is no longer input or the queues are closed
while True:

    # Receive input from input channel
    # If there is an error, the flag will be False
    flag, msg = in_channel.recv()
    if not flag:
        print("Model B: No more input.")
        break
    name, count, size = msg

    # Print received message
    print('Model B: %s, %d, %f' % (name, count, size))

    # Send output to output channel
    # If there is an error, the flag will be False
    flag = out_channel.send(name, count, size)
    if not flag:
        raise RuntimeError("Model B: Error sending output.")

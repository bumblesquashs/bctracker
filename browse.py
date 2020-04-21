import datastructure as ds

ds.start()
while(True):
    tid = input('Find block: enter tripid or type q to quit... ')
    if tid == 'q':
        break
    ds.blockdict[ds.tripdict[tid].blockid].pretty_print()

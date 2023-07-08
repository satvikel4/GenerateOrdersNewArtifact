## To get the percentage of tests potentially being detected for four algorithms, we need to get the simulation results firstly.
### Because this script will output some overall results for each module, you still need to decompress data.tar.gz and orders.tar.gz.
`python3 parse-class-results.py ../simulation/only\_class\_simulation\_results.csv only`
`python3 parse-class-results.py ../simulation/intra\_class\_simulation\_results.csv intra`
`python3 parse-class-results.py ../simulation/inter\_class\_simulation\_results.csv inter`
`python3 parse-class-results.py ../simulation/static\_fields\_analysis\_simulation\_results.csv static`

### You can also do a simple check to only run the simulation results for a single module.
`python3 parse-class-results.py marine_intra_class_simulation_results.csv intra`
It will output something like below. It needs to go to the original order file to get the number of test in this module 926. The first 71 means the number of test classes after parsing the test in the original order. The first 12 means the number of OD tests in this module. The second 71 means the number of orders for intra-class algorithm. The second 12 means the number of OD tests detected. 100.0 means this algorithm can detect 100% of the OD tests in this module.

slug,sha,module,num\_of\_tests,num\_of\_test\_classes,num\_of\_OD\_tests,num\_of\_orders,num\_of\_orders\_detected,percentage\_of\_OD\_tests\_detected
ktuukkan/marine-api,af00038,.,926,71,12,71,12,100.0

## We also provide the final results for each module and algorithms.
only\_class\_results.csv
intra\_class\_results.csv
inter\_class\_results.csv
static\_analysis\_results.csv

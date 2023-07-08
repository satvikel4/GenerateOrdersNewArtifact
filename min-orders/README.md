## To get the minimal orders and the corresponding index, you need to follow the instructions below.
### decompress data.tar.gz and orders.tar.gz because data.tar.gz contains the file all-polluter-cleaner-info-combined.csv
all-polluter-cleaner-info-combined.csv contains all polluters and corresponding cleaners for all victims in our dataset
orders contains all the generated orders for four techniques
You need to apply the info from all-polluter-cleaner-info-combined.csv to simulate on orders.
all-polluter-cleaner-info-combined.csv is a huge file, but you can choose the lines related to one single module to simulate simply. We put a marine-polluter-cleaner-info-combined.csv under this directory.

The location to download data.tar.gz are on our website. The link is https://drive.google.com/file/d/1UYiJ2Ki2-oppV9VvRrmnOPEm5O6I2IL_ .
The location to download orders.tar.gz are also on out website. The link is https://drive.google.com/file/d/1DkjhitKbRK6X9iBvDh7ubLeWITi-Ybty .

### Then, you can run the following 
`python3 get-minimal-orders.py ../../data/all-polluter-cleaner-info-combined.csv only`
`python3 get-minimal-orders.py ../../data/all-polluter-cleaner-info-combined.csv intra`
`python3 get-minimal-orders.py ../../data/all-polluter-cleaner-info-combined.csv inter`
`python3 get-minimal-orders.py ../../data/all-polluter-cleaner-info-combined.csv static`

`python3 get-minimal-orders.py ../../data/all-polluter-cleaner-info-combined.csv <name of method>`

### These scripts will automatically output to the screen to show for each module, what is the minimal orders to cover the passing/failing orders for all the ODs in this module and the corresponding order index in the orders/ directory.
For example, if you want to get the minimal orders for intra-class on module marine-api. It will output like below.
`python3 get-minimal-orders.py marine-polluter-cleaner-info-combined.csv intra`

slug,sha,module,num\_of\_minimal\_orders,minimal\_passing\_orders,minimal\_failing\_orders,num\_of\_tests\_which\_have\_passing\_orders,num\_of\_tests\_which\_have\_failing\_orders,num\_of\_OD\_tests
ktuukkan/marine-api,af00038,.,2,{'0'},{'9'},12,12,12

The format looks like "ktuukkan/marine-api,af00038,.,2,{'0'},{'9'},12,12,12". It means, two orders can cover all the passing/ failing orders for 12 order-dependent flaky tests in this module. {'0'} means the order-0 in the orders directory (orders/intra-orders/ktuukkan\_marine-api-.-af00038-intra-orders/order-0) can make all the 12 OD tests pass. {'9'} means the order-9 in the orders directory (orders/intra-orders/ktuukkan\_marine-api-.-af00038-intra-orders/order-9) can make all the 12 OD tests fail. The first 12 means these two orders can make all the 12 OD tests pass. The second 12 means these two orders can make all the 12 OD tests fail. The third 12 means there are 12 OD tests in this module.

Note that get minimal orders for inter-class and Target Pairs algorithms requires a lot of time, we can only approximate on some orders like choose 1000 orders for Target Pairs algorithm.

## We put the final results for minimal orders in the following files
minimal-only.csv which contains all the minimal orders information for all the modules in our experiments using only-class algorithm.
minimal-intra.csv which contains all the minimal orders information for all the modules in our experiments using intra-class algorithm.
minimal-inter.csv which contains all the minimal orders information for all the modules in our experiments using inter-class algorithm.
minimal-sta.csv which contains all the minimal orders information for all the modules in our experiments using Target Pairs algorithm.

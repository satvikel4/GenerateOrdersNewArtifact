## We record the time during execution. And here we put a time.csv file here.

slug,sha,module,time\_to\_compute\_TuscanIntra\_orders,time\_to\_compute\_TuscanOnly\_orders,time\_to\_compute\_TuscanInter\_orders,time\_to\_process\_for\_static\_orders,time\_to\_compute\_static\_order
ktuukkan/marine-api,af00038,.,0.587,0.608,3066.705,3.330006162,2.269

Here, 0.587 (the first number) is the time to compute the orders for only-class algorithm.
0.608 (The second number) is the time to compute the orders for intra-class algorithm.
3066.705 (The third number) is the time to compute the orders for inter-class algorithm.
3.330006162 (The fourth number) is the time to get the pairs shared the same static fields for Target Pairs algorithm.
2.269 (The fifth number) is the time to compute the orders for Target Pairs algorithm.
3.330006162 + 2.269 = 5.6 is the time we report in the paper to compute the orders for Target Pairs algorithm.

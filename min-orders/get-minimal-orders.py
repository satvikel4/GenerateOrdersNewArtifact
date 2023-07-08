import sys
import os
import string
from collections import OrderedDict

def main(args):
    csvfile = args[1]
    option = args[2]
    if option != "intra" or option != "only" or option != "inter" or option != "static":
        exit
    victim_to_polluter = {}
    vic_pol_to_cleaner = {}
    victim_to_info = {}
    module_info = {}
    with open(csvfile) as f:
        for line in f:
            slug = line.split(',')[0] # .split("https://github.com/")[1]
            sha = line.split(',')[1] # [0-7]
            module = line.split(',')[2]
            victim = line.split(',')[3]
            polluter = line.split(',')[4]
            cleaner = line.split(',')[5]
            test_type = line.split(',')[6].strip()

            # skip the first line with # 
            if victim == 'victim/brittle':
                continue
            
            slug = slug[19:]
            sha = sha[0:7]
            if not victim in victim_to_info:
                victim_to_info[victim] = [slug, sha, module, test_type]
            
            module_key = slug + "_" + sha + "_" + module
            if not module_key in module_info:
                module_info[module_key] = {}
                module_info[module_key]["slug"] = slug
                module_info[module_key]["sha"] = sha
                module_info[module_key]["module"] = module
                module_info[module_key]["victim"] = []
            if not victim in module_info[module_key]["victim"]:
                module_info[module_key]["victim"].append(victim)
            

            polluters_for_this_vic = set()
            if victim in victim_to_polluter:
                polluters_for_this_vic = victim_to_polluter[victim]
            if not polluter == "":
                polluters_for_this_vic.add(polluter)
            victim_to_polluter[victim] = polluters_for_this_vic
            
            cleaners_for_this_vp = set()
            if (victim, polluter) in vic_pol_to_cleaner:
                cleaners_for_this_vp = vic_pol_to_cleaner[(victim, polluter)]
            if "|" in cleaner:
                cleaner_for_this_victim = cleaner.split("|")
                for cftv in cleaner_for_this_victim:
                    if not cftv == "":
                        cleaners_for_this_vp.add(cftv)
            else:
                if not cleaner == "":
                    cleaners_for_this_vp.add(cleaner)
            vic_pol_to_cleaner[(victim, polluter)] = cleaners_for_this_vp

    
    for mk in module_info:
        cur_slug = module_info[mk]["slug"]
        cur_sha = module_info[mk]["sha"]
        cur_mod = module_info[mk]["module"]
        victims_list = module_info[mk]["victim"]

        cur_slug = cur_slug.replace("/", "_")
        cur_mod = cur_mod.replace("./", "").replace("/", "_")
        if option == "intra":
            dirname = sys.path[0] + "/../../orders/intra-orders/" + cur_slug + "-" + cur_mod + "-" + cur_sha + "-intra-orders/"
        elif option == "only":
            dirname = sys.path[0] + "/../../orders/only-orders/" + cur_slug + "-" + cur_mod + "-" + cur_sha + "-only-orders/"
        elif option == "inter":
            dirname = sys.path[0] + "/../../orders/inter-orders/" + cur_slug + "-" + cur_mod + "-" + cur_sha + "-inter-orders/"
        elif option == "static":
            dirname = sys.path[0] + "/../../orders/static-orders/" + cur_slug + "-" + cur_mod + "-" + cur_sha + "-static-orders/"
        
        if not os.path.exists(dirname):
            continue
        num_of_orders = len([name for name in os.listdir(dirname) if os.path.isfile(os.path.join(dirname, name))])

        # get the original order
        original_order = []
        oo_file = sys.path[0] + "/../../data/original-orders/" + cur_slug + "-" + cur_mod + "-" + cur_sha + "-original_order"
        foo = open(oo_file, "r")
        loo = foo.readline()
        while loo:
            original_order.append(loo.strip())
            loo = foo.readline()
        foo.close()

        orders = []
        orders_pass_info = {}
        orders_fail_info = {}
        orders_all_info = {}
        # print(num_of_orders)
        if int(num_of_orders) > 0:
            orders_dir = dirname
            for i in range(num_of_orders):  
                order_file = orders_dir + "order-" + str(i)
                order = []
                if not os.path.exists(order_file):
                    continue
                
                if not str(i) in orders_pass_info:
                    orders_pass_info[str(i)] = set()
                if not str(i) in orders_fail_info:
                    orders_fail_info[str(i)] = set()
                if not str(i) in orders_all_info:
                    orders_all_info[str(i)] = set()
                
                # obtain the order
                fi = open(order_file, "r")
                li = fi.readline()
                while li:
                    if li.strip().isdigit():
                        c = int(li)
                        order.append(original_order[c])
                    else:
                        order.append(li.strip())
                    li = fi.readline()
                fi.close()
                orders.append(order)

                victims_in_this_module = [] 
                for v in victims_list:
                    if v in order:
                        victims_in_this_module.append(v)
                
                for v in victims_in_this_module:
                    index_v = order.index(v)
                    # only need to process the polluters in this order
                    polluters = victim_to_polluter[v]
                    polluters_in_order = set()
                    for polluter_item in polluters:
                        if polluter_item in order:
                            polluters_in_order.add(polluter_item)
                    
                    polluter_indice = []
                    for p in polluters_in_order:
                        index_p = order.index(p)
                        polluter_indice.append(index_p)
                    
                    before_polluter_indice = []
                    largest_index_p = -1
                    for ip in polluter_indice:
                        if ip >= index_v:
                            continue
                        else:
                            before_polluter_indice.append(ip)
                            if ip > largest_index_p:
                                largest_index_p = ip
                    
                    if len(before_polluter_indice) > 0:
                        if victim_to_info[v][3] == "brittle":
                            orders_pass_info[str(i)].add(v)
                            orders_all_info[str(i)].add(v)
                            continue
                        count = 0
                        for index_po in before_polluter_indice:
                            this_p = order[index_po]
                            cleaners_for_this_vp = vic_pol_to_cleaner[(v, this_p)]
                            cleaners_in_this_order = []
                            for c in cleaners_for_this_vp:
                                if c in order:
                                    cleaners_in_this_order.append(c)
                            
                            cleaner_indice = []
                            for c in cleaners_in_this_order:
                                index_c = order.index(c)
                                cleaner_indice.append(index_c)
                            
                            largest_index_c = -1
                            for ic in cleaner_indice:
                                if ic >= index_v:
                                    continue
                                else:
                                    if ic > largest_index_c:
                                        largest_index_c = ic
                        
                            if largest_index_c >= 0:
                                if largest_index_c > index_po:
                                    count += 1
                                    if count == len(before_polluter_indice):
                                        orders_pass_info[str(i)].add(v)
                                        orders_all_info[str(i)].add(v)
                                        break
                                else:
                                    orders_fail_info[str(i)].add(v)
                                    orders_all_info[str(i)].add(v)
                                    break
                            else:
                                orders_fail_info[str(i)].add(v)
                                orders_all_info[str(i)].add(v)
                                break
                    else:
                        if victim_to_info[v][3] == "brittle":
                            orders_fail_info[str(i)].add(v)
                            orders_all_info[str(i)].add(v)
                            continue
                        else: 
                            orders_pass_info[str(i)].add(v)
                            orders_all_info[str(i)].add(v)
                            continue
        
        minimal_passing_order_indice = set()
        minimal_failing_order_indice = set()
        num = int(num_of_orders)
        index = 0
        passing_nums = 0
        failing_nums = 0
        passing_items = set()
        failing_items = set()
        while len(victims_list) > passing_nums or len(victims_list) > failing_nums:
            if index == num:
                break
            index += 1
            all_order_key = max(orders_all_info, key=lambda k: len(orders_all_info[k]))
            all_order_values = orders_all_info[all_order_key]
            orders_all_info.pop(all_order_key)

            passing_order_values = orders_pass_info[all_order_key]
            if len(passing_order_values) > 0:
                minimal_passing_order_indice.add(all_order_key)
            for value in passing_order_values:
                passing_items.add(value)
            orders_pass_info.pop(all_order_key)

            for k in orders_pass_info:
                orders_pass_info[k].difference_update(passing_order_values)
                
            failing_order_values = orders_fail_info[all_order_key]
            if len(failing_order_values) > 0:
                minimal_failing_order_indice.add(all_order_key)
            for value in failing_order_values:
                failing_items.add(value)
            orders_fail_info.pop(all_order_key)

            for k in orders_fail_info:
                orders_fail_info[k].difference_update(failing_order_values)
            
            for k in orders_all_info:
                orders_all_info[k] = orders_fail_info[k]
                orders_all_info[k] = orders_all_info[k].union(orders_pass_info)

        passing_nums = len(passing_items)
        failing_nums = len(failing_items)
        
        if len(victims_list) > passing_nums or len(victims_list) > failing_nums:
            a = passing_items & failing_items
            if len(a) > 0:
                z = minimal_passing_order_indice.union(minimal_failing_order_indice)
                print(cur_slug + "," + cur_sha + "," + cur_mod + "," + str(len(z)) + "," + str(minimal_passing_order_indice) + "," + str(minimal_failing_order_indice) + "," + str(passing_nums) + "," + str(failing_nums) + "," + str(len(victims_list)))
            else:
                print(cur_slug + "," + cur_sha + "," + cur_mod + ",False" + "," + str(minimal_passing_order_indice) + "," + str(minimal_failing_order_indice) + "," + str(passing_nums) + "," + str(failing_nums) + "," + str(len(victims_list)))
        else:
            z = minimal_passing_order_indice.union(minimal_failing_order_indice)
            print(cur_slug + "," + cur_sha + "," + cur_mod + "," + str(len(z)) + "," + str(minimal_passing_order_indice) + "," + str(minimal_failing_order_indice) + "," + str(passing_nums) + "," + str(failing_nums) + "," + str(len(victims_list)))

if __name__ == '__main__':
    main(sys.argv)

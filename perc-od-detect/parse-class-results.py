import sys
import os

def main(args):
    csvfile = args[1]
    option = args[2]
    if option != "intra" or option != "only" or option != "inter" or option != "static":
        exit
    module_info = {}

    with open(csvfile) as f:
        for line in f:
            slug = line.split(',')[0]
            sha = line.split(',')[1][0:7]
            module = line.split(',')[2]
            victim = line.split(',')[3]
            can_fail = line.split(',')[4]
            can_pass = line.split(',')[6].strip()

            # print(can_fail)
            detected = False
            if can_fail == "True" and can_pass == "True":
                detected = True

            module_key = slug + "_" + sha + "_" + module
            cur_slug = slug.replace("/", "_")
            cur_mod = module.replace("./", "").replace("/", "_")
            if option == "intra":
                dirname = sys.path[0] + "/../../orders/intra-orders/" + cur_slug + "-" + cur_mod + "-" + sha + "-intra-orders/"
            elif option == "only":
                dirname = sys.path[0] + "/../../orders/only-orders/" + cur_slug + "-" + cur_mod + "-" + sha + "-only-orders/"
            elif option == "inter":
                dirname = sys.path[0] + "/../../orders/inter-orders/" + cur_slug + "-" + cur_mod + "-" + sha + "-inter-orders/"
            elif option == "static":
                dirname = sys.path[0] + "/../../orders/static-orders/" + cur_slug + "-" + cur_mod + "-" + sha + "-static-orders/"

            if not os.path.exists(dirname):
                continue
            num_of_orders = len([name for name in os.listdir(dirname) if os.path.isfile(os.path.join(dirname, name))])

            # get the original order
            original_order = []
            oo_file = sys.path[0] + "/../../data/original-orders/" + cur_slug + "-" + cur_mod + "-" + sha + "-original_order"
            
            if module_key not in module_info:
                module_info[module_key] = {}
                # module slug
                module_info[module_key]["slug"] = slug

                # module sha
                module_info[module_key]["sha"] = sha

                # module module
                module_info[module_key]["module"] = module

                # total num of tests
                module_num_of_tests = 0
                test_classes = set()
                original_order_filename = sys.path[0] + "/../../data/original-orders/" + cur_slug + "-" + cur_mod + "-" + sha + "-original_order"
                if os.path.exists(original_order_filename):
                    fo = open(original_order_filename, "r")
                    line = fo.readline()
                    while line:
                        module_num_of_tests += 1
                        last_index = line.rindex(".")
                        test_class = line[0:last_index]
                        test_classes.add(test_class)
                        line = fo.readline()
                    fo.close()
                module_info[module_key]["num_of_tests"] = module_num_of_tests

                # total num of test classes
                module_num_of_test_classes = len(test_classes)
                module_info[module_key]["num_of_test_classes"] = module_num_of_test_classes

                # total num of OD tests
                module_info[module_key]["num_of_OD_tests"] = 0

                # num of orders
                module_info[module_key]["num_of_orders"] = len([name for name in os.listdir(dirname) if os.path.isfile(os.path.join(dirname, name))])

                module_info[module_key]["num_of_detected_OD_tests"] = 0

            # total num of OD tests
            module_info[module_key]["num_of_OD_tests"] += 1

            # num of detected OD tests
            if detected:
                module_info[module_key]["num_of_detected_OD_tests"] += 1
            
            # percentage of detected OD tests
            module_info[module_key]["percent_of_detected_OD_tests"] = float(module_info[module_key]["num_of_detected_OD_tests"]) * 100 / float(module_info[module_key]["num_of_OD_tests"])

    print("# slug,sha,module,num_of_tests,num_of_test_classes,num_of_OD_tests,num_of_orders,num_of_detected_OD_tests,percent_of_detected_OD_tests")    
    for key in module_info:
        print(str(module_info[key]["slug"]) + "," + str(module_info[key]["sha"]) + "," + str(module_info[key]["module"]) + "," +
            str(module_info[key]["num_of_tests"]) + "," + str(module_info[key]["num_of_test_classes"]) + "," + str(module_info[key]["num_of_OD_tests"]) + "," + 
            str(module_info[key]["num_of_orders"]) + "," + str(module_info[key]["num_of_detected_OD_tests"]) + "," + str(module_info[key]["percent_of_detected_OD_tests"]))

if __name__ == '__main__':
    main(sys.argv)

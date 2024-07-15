from presenter import JsoneFormater

link_list = ['1','2','3']


for data in range(len(link_list)):

    json_dict = JsoneFormater().get_format()
    print(json_dict)



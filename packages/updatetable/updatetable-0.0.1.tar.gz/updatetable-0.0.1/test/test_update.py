#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''                                                          
Copyright (C)2018 SenseDeal AI, Inc. All Rights Reserved                                                      
File: {name}.py
Author: xuwei                                        
Email: weix@sensedeal.ai                                 
Last modified: 2018.12.23
Description:                                            
'''

from updatetable.updatetable import *


#从160服务器db_company数据库中的表更新193服务器basic_db数据库中的部分表
def update_stock_info():
    read_data = ReplaceTableData('160','db_company')
    write_data = ReplaceTableData('193','basic_db')

    list_dict = read_data.fetchall_data("""select stock_code,company_name,market_status,company_code,record_date,
total_market_value,industry,area,concept,market from stock_info""")

    write_data.replace_table_data(list_dict,'stock_info_xw','stock_code','id')

def update_stock_codes():
    read_data = ReplaceTableData('160', 'db_company')
    write_data = ReplaceTableData('193', 'basic_db')
    list_dict = read_data.fetchall_data("""select stock_code,company_name,market_status,company_code,
industry,record_date from stock_codes""")

    write_data.replace_table_data(list_dict, 'stock_codes', 'stock_code', 'id')


def update_category_stocks():
    read_data = ReplaceTableData('160', 'db_company')
    write_data = ReplaceTableData('193', 'basic_db')
    list_dict = read_data.fetchall_data("""select parent_id,category_name,choice_id,parent_choice_id,
category_level from category_stocks""")

    write_data.replace_table_data(list_dict, 'category_stocks', 'choice_id', 'id')

def update_company_infos():
    read_data = ReplaceTableData('160', 'db_company')
    write_data = ReplaceTableData('193', 'basic_db')

    columns = pd.read_sql("""select * from company_infos limit 1""",read_data.engine_db())
    # print(columns)
    columns_list = columns.columns.tolist()
    # print(len(columns_list))
    columns_list.remove('id')
    # print(columns_list)
    columns_str = ','.join(columns_list)
    # print(columns_str)

    list_dict = read_data.fetchall_data("select " +  columns_str + " from company_infos")
    #
    write_data.replace_table_data(list_dict, 'company_infos', 'stock_code', 'id')





if __name__ == '__main__':
    pass
    # update_stock_info()
    # update_stock_codes()
    # update_category_stocks()
    # update_company_infos()
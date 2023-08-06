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

import sense_core as sd
import pymysql
import pandas as pd
from sqlalchemy import create_engine
from multiprocessing import Pool
import datetime
import warnings
warnings.filterwarnings("ignore")

_ProcessNum = 4

class ReplaceTableData(object):
    def __init__(self,label,db):
        self.host=sd.config(label, 'host')
        self.port=int(sd.config(label, 'port'))
        self.user=sd.config(label, 'user')
        self.passwd=sd.config(label, 'passwd')
        self.db=db

    def operate_exist_db(self,sql):
        con = pymysql.connect(
            host = self.host,
            port = self.port,
            user = self.user,
            passwd = self.passwd,
            db = self.db,
            charset = 'utf8',
            # use_unicode=True
        )
        cursor = con.cursor()
        # 执行SQL语句
        cursor.execute(sql)
        con.commit()
        con.close()

    # pymysql读取已有数据库的数据，数据形式为列表字典
    def fetchall_data(self, sql):
        con = pymysql.connect(
            host=self.host,
            port=self.port,
            user=self.user,
            passwd=self.passwd,
            db=self.db,
            charset='utf8',
            cursorclass=pymysql.cursors.DictCursor
        )
        cursor = con.cursor()
        try:
            # 执行SQL语句
            cursor.execute(sql)
            # 获取所有记录列表
            results = cursor.fetchall()
            return results
        except Exception as error:
            print(error)

    def engine_db(self):
        # 用sqlalchemy连接需要读取数据的数据库
        engine = create_engine("mysql+pymysql://{user}:{passwd}@{host}:{port}/{db}".format(
            host=self.host,
            port=self.port,
            user=self.user,
            passwd=self.passwd,
            db=self.db,
        ), connect_args={'charset': 'utf8'})
        return engine


    def get_update_key(self,update_df,old_df,unique_key):
        key_list = []
        try:
            for i in range(len(update_df)):
                row_dict = update_df.iloc[i].dropna().to_dict()
                # print(row_dict)
                key = row_dict[unique_key]
                # print(old_df)
                old_data = old_df[old_df[unique_key] == key].iloc[0].dropna().to_dict()
                # print('比较开始：',datetime.datetime.now())
                if set(row_dict.values()) != set(old_data.values()):
                    print(set(row_dict.values()))
                    print(set(old_data.values()))
                    key_list.append(key)
            return key_list
        except Exception as e:
            print(e)
            return key_list

    def replace_table_data(self,list_dict,table_name,unique_key,primary_key):

        unique_key_df = pd.read_sql("""select {0} from {1}""".format(unique_key,table_name),self.engine_db()).dropna()
        origin_df = pd.DataFrame(list_dict)

        if len(unique_key_df) != 0:
            unique_key_list = unique_key_df[unique_key].tolist()
            append_id_list = list(set(origin_df[unique_key].tolist()) - set(unique_key_list))
            if len(append_id_list) != 0:
                append_df = origin_df[origin_df[unique_key].isin(append_id_list)]
                append_df = append_df.drop_duplicates(unique_key)
                # print(origin_df)
                append_df.to_sql(table_name, self.engine_db(), if_exists='append', index=False, chunksize=5000)
                print(table_name + '表中添加了{}条新记录。'.format(len(append_df)))
            else:
                print(table_name + '表中没有新数据添加。')
            # print(append_id_list)
            update_id_list = list(set(origin_df[unique_key].tolist()) - set(append_id_list))
            # print(update_id_list)
            # print(','.join(origin_df.columns.tolist()))
            if update_id_list:
                if len(update_id_list) != 1:
                    old_data = self.fetchall_data("select " +  ','.join(origin_df.columns.tolist())
                                         + " from {0} where {1} in {2}""".format(table_name,unique_key,tuple(update_id_list)))
                    old_df = pd.DataFrame(old_data)
                    # old_df = pd.read_sql_query("select " +  ','.join(origin_df.columns.tolist())
                    #                      + " from {0} where {1} in {2}""".format(table_name,unique_key,tuple(update_id_list)),
                    #                      self.engine_db())
                else:
                    old_data = self.fetchall_data("select " + ','.join(origin_df.columns.tolist())
                                         + " from {0} where {1}='{2}'""".format(table_name, unique_key,update_id_list[0]))
                    old_df = pd.DataFrame(old_data)

                    # old_df = pd.read_sql_query("select " + ','.join(origin_df.columns.tolist())
                    #                      + " from {0} where {1}='{2}'""".format(table_name, unique_key,update_id_list[0]),
                    #                      self.engine_db())

                update_df = origin_df[origin_df[unique_key].isin(update_id_list)]
                update_df = update_df.drop_duplicates(unique_key)

                loop_num = int(len(update_df) / _ProcessNum)
                pool = Pool(processes=_ProcessNum)
                jobs = []
                for i in range(0, len(update_df), loop_num):
                    p = pool.apply_async(self.get_update_key, (update_df.iloc[i:i + loop_num], old_df, unique_key,))
                    jobs.append(p)
                pool.close()  # 关闭进程池，表示不能在往进程池中添加进程
                pool.join()  # 等待进程池中的所有进程执行完毕，必须在close()之后调用

                update_key_list = []
                for j in jobs:
                    update_key_list = update_key_list + j.get()

                # print(update_key_list)

                update_df = update_df[update_df[unique_key].isin(update_key_list)]
                if len(update_key_list) == 0:
                    print(table_name + '表中数据无更新。')
                    return
                if len(update_key_list) > 1:
                    self.operate_exist_db("delete from {0} where {1} in {2}".format(table_name, unique_key,tuple(update_key_list)))
                else:
                    self.operate_exist_db("delete from {0} where {1}='{2}'".format(table_name, unique_key, update_key_list[0]))
                update_df.to_sql(table_name, self.engine_db(), if_exists='append', index=False, chunksize=5000)
                # print(update_df)
                print(table_name + '更新了{0}条记录。'.format(len(update_key_list)))
                try:
                    self.operate_exist_db("alter table {0} drop column {1}".format(table_name,primary_key))
                    self.operate_exist_db("alter table {0} add {1} int unsigned not Null auto_increment primary key".format(table_name,primary_key))
                except Exception as e:
                    print(e)
        else:
            write_df = origin_df.drop_duplicates(unique_key)
            write_df.to_sql(table_name, self.engine_db(), if_exists='append', index=False, chunksize=5000)
            try:
                self.operate_exist_db("alter table {0} drop column {1}".format(table_name, primary_key))
                self.operate_exist_db(
                    "alter table {0} add {1} int unsigned not Null auto_increment primary key".format(table_name, primary_key))
            except Exception as e:
                print(e)


    def write_new_table(self,list_dict,table_name,unique_key,primary_key):
        pass

if __name__ == '__main__':
    print(datetime.datetime.now())
    rd = ReplaceTableData('160','db_dct')
    # list_data = rd.fetchall_data("""select stock_code,company_code,company_name,company_name_full,market_status,`type` from test_xw""")
    list_data = rd.fetchall_data(
        """select stock_code,company_code,company_name,company_name_full,market_status from test_xw""")
    # print(list_data[0])
    xd = rd.replace_table_data(list_data,'test_xw_2','stock_code','id')

    print(datetime.datetime.now())




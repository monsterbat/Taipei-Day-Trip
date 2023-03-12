"""
WeHelp BootCamp Assignemt - Stage 2 taipei_day_trip -*-data insert to MySQL-*-
Update date: 2022/11/17
Authored by SC Siao
"""
import json
from MySQL_con import *

with open("/Users/sc/Documents/100_Work/140_WeHelp/WeHelp_Stage2/taipei-day-trip/data/taipei-attractions.json",mode="r") as file:
    data=json.load(file)
data=data["result"]["results"]
data_length=len(data)

count=0
while count<data_length:
    # INSERT to SQL information
    data_name=data[count]["name"]
    data_category=data[count]["CAT"]
    data_description=data[count]["description"]
    data_address=data[count]["address"]
    data_transport=data[count]["direction"]
    data_mrt=data[count]["MRT"]
    data_lat=data[count]["latitude"]
    data_lng=data[count]["longitude"]
    sql_command_attraction="""
    INSERT INTO attraction (name,category,description,address,transport,mrt,lat,lng) 
    VALUES (%s,%s,%s,%s,%s,%s,%s,%s);
    """
    value_input_attraction=(data_name,data_category,data_description,data_address,data_transport,data_mrt,data_lat,data_lng)
    insert_or_update_data(sql_command_attraction,value_input_attraction)

    # id find for INSERT img(attraction_id)
    sql_command_idfind="""
    SELECT id FROM attraction WHERE name=%s
    """
    value_input_idfind=(data_name,)
    data_idfind=query_data(sql_command_idfind,value_input_idfind)
    data_idfind=data_idfind[0]["id"]

    # INSERT images to SQL attraction_image table
    data_muti_images=data[count]["file"]
    image_url=""
    filter_word1=".jpg"
    filter_word2=".JPG"
    filter_word3=".png"
    filter_word4=".PNG"
    data_images=[]
    for data_muti_images_ls in data_muti_images:
        image_url=image_url+data_muti_images_ls
        filter1=image_url.find(filter_word1)
        filter2=image_url.find(filter_word2)
        filter3=image_url.find(filter_word3)
        filter4=image_url.find(filter_word4)
        if filter1!=-1 or filter2!=-1 or filter3!=-1 or filter4!=-1:
            sql_command_image="""
            INSERT INTO attraction_image (attraction_id,images) 
            VALUES (%s,%s);
            """
            value_input_image=(data_idfind,image_url)
            insert_or_update_data(sql_command_image,value_input_image)

            image_url=[image_url]
            data_images=data_images+image_url
            image_url=""

    count+=1







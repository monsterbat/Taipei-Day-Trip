# model.py
import sys
sys.path.append('api/function')
from MySQL_con import *
from flask import *
 
def get_attractions(page, keyword=None):
	one_page_quanity=12
	data_start=int(page*one_page_quanity)
	if keyword!=False:
		# attraction information With keyword
		sql_command="""
		SELECT * FROM attraction
		WHERE category like %s OR name like %s
		LIMIT %s, %s;
		"""
		sql_input=(keyword,"%"+keyword+"%",data_start,one_page_quanity)
		attraction_info=query_data(sql_command,sql_input)
	else:
		# attraction information WithOut keyword
		sql_command="""
		SELECT * FROM attraction
		LIMIT %s, %s;
		"""
		sql_input=(data_start,one_page_quanity)
		attraction_info=query_data(sql_command,sql_input)
	
	data_result=[]
	count=0
	
	while count<len(attraction_info):
			data={}
			data["id"] = attraction_info[count]["id"]
			data["name"] = attraction_info[count]["name"]
			data["category"] = attraction_info[count]["category"]
			data["description"] = attraction_info[count]["description"]
			data["address"] = attraction_info[count]["address"]
			data["transport"] = attraction_info[count]["transport"]
			data["mrt"] = attraction_info[count]["mrt"]
			data["lat"] = attraction_info[count]["lat"]
			data["lng"] = attraction_info[count]["lng"]

			# attraction image
			data_image_ls=[]
			data_image=[]
			id_check=data["id"]

			# With keyword 
			if keyword!=False:
				sql_command="""
				SELECT attraction_id,images FROM attraction
				INNER JOIN attraction_image ON attraction.id=attraction_image.attraction_id
				WHERE category LIKE %s AND attraction_id LIKE %s OR name LIKE %s AND attraction_id LIKE %s;
				"""	
				sql_input=(keyword,id_check,"%"+keyword+"%",id_check)
				attraction_img=query_data(sql_command,sql_input)
				
			# WithOut keyword
			else:
				sql_command="""
				SELECT attraction_id,images FROM attraction
				INNER JOIN attraction_image ON attraction.id=attraction_image.attraction_id
				WHERE attraction_id = %s;
				"""
				sql_input=(id_check,)
				attraction_img=query_data(sql_command,sql_input)
			
			count_image=0
			while count_image<len(attraction_img):
				data_image_ls=[attraction_img[count_image]["images"]]
				data_image.extend(data_image_ls)
				count_image+=1
			data["images"]=data_image
			# Merge all data
			data_result.append(data)
			# next one
			count+=1
	
	# page judge
	if len(attraction_info)==one_page_quanity:
		next_page=page+1
	else:
		next_page=None

	# Combine
	print(next_page)
	data_main=jsonify({
		"nextPage":next_page,
		"data":data_result
		})
	return data_main

def get_attractionId(attractionId):
	# attraction information
	sql_command=f"""
	SELECT * FROM attraction
	WHERE id={attractionId};
	"""
	attraction_info=query_data_read(sql_command)
	# With data situation
	if attraction_info!=[]:
		data_result=[]
		count=0
		data={}
		data["id"] = attraction_info[count]["id"]
		data["name"] = attraction_info[count]["name"]
		data["category"] = attraction_info[count]["category"]
		data["description"] = attraction_info[count]["description"]
		data["address"] = attraction_info[count]["address"]
		data["transport"] = attraction_info[count]["transport"]
		data["mrt"] = attraction_info[count]["mrt"]
		data["lat"] = attraction_info[count]["lat"]
		data["lng"] = attraction_info[count]["lng"]
		# attraction image
		data_image_ls=[]
		data_image=[]
		sql_command="""
		SELECT attraction_id,images FROM attraction
		INNER JOIN attraction_image ON attraction.id=attraction_image.attraction_id
		WHERE attraction_id=%s;
		"""
		sql_input=(attractionId,)
		attraction_img=query_data(sql_command,sql_input)
		count_image=0
		while count_image<len(attraction_img):
			data_image_ls=[attraction_img[count_image]["images"]]
			data_image.extend(data_image_ls)
			count_image+=1
		data["images"]=data_image
		data_result=data
		
		data_main={
			"data":data_result
			}

		return data_main
	# No data situation
	else:
		errorr_message = jsonify({
		"error": True,
		"message": "景點編號不正確"
	})
	return errorr_message,400

def get_categories():
	sql_command="""
	SELECT DISTINCT category FROM attraction;
	"""
	categories_raw_data=query_data_read(sql_command)
	data={}
	data_categories_ls=[]
	categories_data=[]
	count_categories=0
	while count_categories<len(categories_raw_data):
		data_categories_ls=[categories_raw_data[count_categories]["category"]]
		categories_data.extend(data_categories_ls)
		count_categories+=1
	data["data"]=categories_data
	return data
#!/usr/bin/python
# encoding:UTF-8
from django.http import HttpResponse
import MySQLdb
import json

def get_json(request):
	conn = MySQLdb.connect(host='mysql',
						user='nagios',
						passwd='nagios',
						port=3309,
						db='nagios')
	cursor = conn.cursor()
	query = "SELECT statehistory_id '通知ID',state_time '开始时间',(CASE WHEN a.state = 0 AND b.name2 IS NULL THEN '正常' WHEN a.state = 1 AND b.name2 IS NULL THEN '宕机' WHEN a.state = 1 AND b.name2 IS NOT NULL THEN '告警' WHEN a.state = 2 AND b.name2 IS NULL THEN '未知' WHEN a.state = 2 AND b.name2 IS NOT NULL THEN '紧急' WHEN a.state = 3 THEN '未知' END) AS '状态',	( CASE a.state_type WHEN 0 THEN '软' WHEN 1 THEN '硬' END )AS '通知类型', b.name1 '主机', b.name2 '服务', a.output '检查结果' FROM nagios_statehistory a, nagios_objects b WHERE a.object_id = b.object_id limit 100;"
	cursor.execute(query)
	#row = cursor.fetchone()
	row = cursor.fetchall()

	templist = []
	dic = dict()
	result = []
	dic['statehistory_id'] = row[0]
	for each in row:
		dic['statehistory_id'] = each[0]
		dic['state'] = each[2]
		dic['state_type'] = each[3]
		dic['name1'] = each[4]
		dic['name2'] = each[5]
		dic['output'] = each[6]
		result.append(dic)
	RESULT = json.dumps(result, ensure_ascii=False, encoding="utf-8")
	return HttpResponse(RESULT, mimetype="application/json")

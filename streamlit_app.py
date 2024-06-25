import streamlit as st
import pandas as pd
from io import BytesIO


# 创建 Streamlit 应用
	st.title("婉如启航 Sku 合并")
	st.write("上传一个 Excel 文件进行处理")

	# 文件上传
	uploaded_file = st.file_uploader("选择一个 Excel 文件", type=["xlsx", "xls"])
	
	if uploaded_file is not None:
		# 显示上传的文件名
		st.write(f"你上传的文件名: {uploaded_file.name}")

		# 读取上传的 Excel 文件
		df = pd.read_excel(uploaded_file, sheet_name='Sheet1')
		
		# 转换 '时间' 列为日期类型
		df['时间'] = pd.to_datetime(df['时间'])
		
		# 按 SKU 分组，统计数量，并计算开始和结束时间
		df_grouped = df.groupby('SKU').agg(
			开始时间=('时间', 'min'),
			结束时间=('时间', 'max'),
			总数量=('数量', 'sum')
		).reset_index()
		
		# 显示处理后的数据
		st.write("处理后的数据:")
		st.write(df_grouped)
		
		# 创建一个 BytesIO 对象以保存新的 Excel 文件
		output = BytesIO()
		
		# 使用原始文件创建一个新的 ExcelWriter 对象
		with pd.ExcelWriter(output, engine='openpyxl') as writer:
			# 将原始的 Sheet1 写入
			df.to_excel(writer, sheet_name='Sheet1', index=False)
			# 将处理后的数据写入新的 Sheet 页
			df_grouped.to_excel(writer, sheet_name='SKU_Statistics', index=False)
		
		# 将指针移到开头以便于下载
		output.seek(0)
		
		# 提供下载处理后的数据的功能
		st.download_button(
			label="下载处理后的 Excel 文件",
			data=output,
			file_name='processed_data.xlsx',
			mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
		)
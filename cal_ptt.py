# coding=utf-8
import sys
import pandas as pd
import numpy as np
import time
recent_ptt = 11.13  # 输入您的ptt
file_name  = "Arcaea.csv"  # 这里改文件名
unit_int = True  # Ture - y轴用整数； False - y轴用Million表示
save_html = False  # True - 存档到 [文件名][日期].html；Flase - 不存档

# 改用参数输入文件名
# file_name = sys.argv[1]

localtime = time.asctime(time.localtime(time.time()))
html_name = "{}_{}.html".format(file_name.replace(".csv", ""), time.strftime("%Y%m%d_%H_%M", time.localtime()))

def cal_ptt(row):
	score = row["分数"]
	stage = row["定数"]
	if score >= 10000000:
		ptt = stage + 2.000
	elif score >= 9800000:
		ptt = stage + 1 + (score - 9800000)/200000.
	elif score:
		ptt = stage + (score - 9500000)/300000.
		if ptt < 0:
			ptt = 0
	ptt = round(ptt, 2)
	return ptt

def cal_rank(row):
	score = row["分数"]
	if score >= 10000000:
		return "PM"
	elif score >= 9900000:
		return "EX+"
	elif score >= 9800000:
		return "EX"
	elif score >= 9500000:
		return "AA"
	elif score >= 9200000:
		return "A"
	elif score >= 8900000:
		return "B"
	elif score >= 8600000:
		return "C"
	else:
		return "D"

# df = pd.read_csv(sys.argv[1], header=0, index_col=0)
df = pd.read_csv(file_name, header=0, index_col=0)
# df.to_csv(sys.argv[1].replace(".csv", ".old.csv"))
df.to_csv(file_name.replace(".csv", ".old.csv"), encoding="utf-8-sig")
df["ptt"] = df.apply(cal_ptt, axis=1)
df = df.sort_values(by="ptt", ascending=False)
df.index = np.arange(1, len(df) + 1)
df["评级"] = df.apply(cal_rank, axis=1)
# df = df.reset_index()
df.to_csv(file_name, encoding="utf-8-sig")
# print(df.iloc[0:30])


B30 = round(df.iloc[0:30]["ptt"].sum()/30.0, 2)
R10 = round((recent_ptt*40 - df.iloc[0:30]["ptt"].sum())/10., 2)
B10 = round(df.iloc[0:10]["ptt"].sum()/10., 2)
print("PTT  : {}".format(recent_ptt))
print("B30  : {}".format(B30))
print("R10  : {}".format(R10))
print("B10  : {}".format(B10))
highest_score = round((df.iloc[0:30]["ptt"].sum() + df.iloc[0:10]["ptt"].sum())/40., 2)
print("Bw\\oU: {}".format(highest_score))

# import matplotlib as mpl
# import matplotlib.pyplot as plt
import plotly.graph_objects as go
import plotly.express as px

# mpl.rcParams['font.sans-serif']=['SimHei'] 
# mpl.rcParams['axes.unicode_minus']=False 

# fig, ax = plt.subplots()
# ax.scatter(df["定数"], df["分数"])
# ax.set_xlabel("定数")
# ax.set_ylabel("分数")
# ax.set_ylim(bottom=9200000)
# plt.tight_layout()
# plt.show()

df["排序"] = df.index
df = df.sort_values(by=["难度", "定数" ], ascending=[True, True])

fig = px.scatter(df,
                 title="您 ptt={}, B30={}, R10={}<br>日期：{}".format(recent_ptt, B30, R10, localtime),
                 x="定数", y="分数",  color="难度", hover_data=["曲目", "曲师", "评级", "ptt", "排序"], # symbol="评级",
				 color_discrete_map={"BYD":"maroon", "FTR": "dodgerblue", "PRS": "limegreen"},
				 template="simple_white",
				 )
fig.update_layout(
    hoverlabel=dict(
        bgcolor="white",
        font_size=12,
        font_family="Rockwell",
    )
)

fig.update_layout(
		xaxis={"autorange": False, "range":[df["定数"].min()-0.05, df["定数"].max()+0.05]},

)

if unit_int == True:
	fig.update_layout(yaxis=dict(tickformat="int"))


# fig.add_shape( # add a horizontal "target" line
#     type="line", line_color="black", line_width=2, opacity=1,
#     x0=0, x1=1, xref="paper", y0=10000000, y1=10000000, yref="y"
# )

# EX+
fig.add_shape( # add a horizontal "target" line
    type="line", line_color="tomato", line_width=2, opacity=1, line_dash="dot",
    x0=0, x1=1, xref="paper", y0=9900000, y1=9900000, yref="y"
)
# fig.add_annotation( # add a text callout with arrow
#     text="EX+", x=7.95, y=9925000, showarrow=False, align='left'
# )

# EX
fig.add_shape( # add a horizontal "target" line
    type="line", line_color="salmon", line_width=2, opacity=1, line_dash="dot",
    x0=0, x1=1, xref="paper", y0=9800000, y1=9800000, yref="y"
)
# fig.add_annotation( # add a text callout with arrow
#     text="EX", x=7.95, y=9825000, showarrow=False, align='left'
# )

fig.show()

if save_html == True:
	fig.write_html(html_name)

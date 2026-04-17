import pandas as pd
from pyecharts.charts import Bar, Pie, Grid
from pyecharts import options as opts
from pyecharts.globals import ThemeType


class Charts(object):
    def __init__(self):
        self.pd = pd
        self.pd.set_option('max_colwidth', 100)

    def Chart_City_Work_Proportion(self, sql, conn):
        df = self.pd.read_sql(sql, conn)
        pie = self.City_Pie(df)
        pie.render("./UI/公司.html")

    def Chart_EXP(self, sql, conn):
        df = self.pd.read_sql(sql, conn)
        pie = self.EXP_Pie(df)

        bar = self.EXP_Bar(df)

        bar.overlap(pie)
        bar.render("./UI/经验.html")

    def Chart_Degree(self, sql, conn):
        df = self.pd.read_sql(sql, conn)
        pie = self.Degree_Pie(df)

        bar = self.Degree_Bar(df)

        bar.overlap(pie)
        bar.render("./UI/学历.html")

    def City_Pie(self, df):
        df_city = df['区域'].str.split('.', expand=True)[1]
        df.insert(6, '所在区', df_city)

        experience_count = df.groupby('所在区')['区域'].count()  # 平均工资
        attr = experience_count.reset_index()['所在区'].tolist()
        value = experience_count.reset_index()['区域'].tolist()
        pie = Pie(init_opts=opts.InitOpts(width='1600px', height='600px', theme=ThemeType.MACARONS))
        pie.add(series_name='', data_pair=[(i, j) for i, j in zip(attr, value)])
        pie.set_global_opts(
            legend_opts=opts.LegendOpts(is_show=True, type_='scroll', orient='vertical', pos_left='left'),
            title_opts=opts.TitleOpts(title="招聘公司在武汉占比", pos_left="center",
                                      title_textstyle_opts=opts.TextStyleOpts(font_size=45)))
        pie.set_series_opts(label_opts=opts.LabelOpts(formatter='{b}:{d}%'))
        return pie

    def EXP_Pie(self, df):
        experience_count = df.groupby('经验要求')['平均薪资'].count()  # 平均工资
        attr = experience_count.reset_index()['经验要求'].tolist()
        value = experience_count.reset_index()['平均薪资'].tolist()
        pie = Pie(init_opts=opts.InitOpts(width='1600px', height='600px', theme=ThemeType.MACARONS))
        pie.add(series_name='', data_pair=[(i, j) for i, j in zip(attr, value)], center=["80%", "30%"],
                radius=["0%", "40%"])
        pie.set_global_opts(title_opts=opts.TitleOpts(title="经验要求占比"),
                            legend_opts=opts.LegendOpts(is_show=True))
        pie.set_series_opts(label_opts=opts.LabelOpts(formatter='{b}:{d}%'))
        return pie

    def EXP_Bar(self, df):
        ave_salary = df.groupby('经验要求')['平均薪资'].mean()  # 平均工资
        ave_min_salary = df.groupby('经验要求')['最低薪资'].mean()  # 最低平均工资
        ave_max_salary = df.groupby('经验要求')['最高薪资'].mean()  # 最高平均工资
        x, y1, y2, y3 = self.Set_X_EXP(ave_salary.reset_index()['经验要求'], ave_salary, ave_min_salary, ave_max_salary)
        bar = Bar(init_opts=opts.InitOpts(width='1600px', height='900px', theme=ThemeType.MACARONS))
        bar.add_xaxis(x)
        bar.add_yaxis("各经验要求平均工资", y1, )  # itemstyle_opts=opts.ItemStyleOpts(color="black")
        bar.add_yaxis("各经验要求最低平均工资", y2)
        bar.add_yaxis("各经验要求最高平均工资", y3)
        bar.set_series_opts(label_opts=opts.LabelOpts(is_show=False))
        bar.set_global_opts(title_opts=opts.TitleOpts(title="各经验等级工资"),
                            yaxis_opts=opts.AxisOpts(name="薪资"),
                            xaxis_opts=opts.AxisOpts(name="经验"))
        return bar

    def Degree_Pie(self,df):
        experience_count = df.groupby('学历要求')['平均薪资'].count()  # 平均工资
        attr = experience_count.reset_index()['学历要求'].tolist()
        value = experience_count.reset_index()['平均薪资'].tolist()
        pie = Pie(init_opts=opts.InitOpts(width='1600px', height='600px', theme=ThemeType.MACARONS))
        pie.add(series_name='', data_pair=[(i, j) for i, j in zip(attr, value)], center=["65%", "25%"],radius=["0%", "40%"])
        pie.set_global_opts(title_opts=opts.TitleOpts(title="学历要求占比"))
        pie.set_series_opts(label_opts=opts.LabelOpts(formatter='{b}:{d}%'))
        return pie

    def Degree_Bar(self,df):
        average_salary = df.groupby('学历要求')['平均薪资'].mean()  # 平均工资
        average_low_salary = df.groupby('学历要求')['最低薪资'].mean()  # 最低平均工资
        average_high_salary = df.groupby('学历要求')['最高薪资'].mean()  # 最高平均工资
        x, y1, y2, y3 = self.Set_X_Degree(average_salary.reset_index()['学历要求'], average_salary, average_low_salary, average_high_salary)
        bar = Bar(init_opts=opts.InitOpts(width='1600px', height='900px', theme=ThemeType.MACARONS))
        bar.add_xaxis(x)
        bar.add_yaxis("各学历要求平均工资", y1)
        bar.add_yaxis("各学历要求最低平均工资", y2)
        bar.add_yaxis("各学历要求最高平均工资", y3)
        bar.set_series_opts(label_opts=opts.LabelOpts(is_show=False))  # 不显示数字
        bar.set_global_opts(title_opts=opts.TitleOpts(title="各学历要求"),
                            yaxis_opts=opts.AxisOpts(name="薪资"),
                            xaxis_opts=opts.AxisOpts(name="学历", axislabel_opts=opts.LabelOpts(rotate=-50))  # 旋转x轴内容
                            )
        return bar

    def Set_X_Degree(self, old_x, average_salary, average_low_salary, average_high_salary):
        x = ['硕士', '博士', '本科', '大专', '高中', '中专/中技', '初中及以下', '不限']
        y1 = [0, 0, 0, 0, 0, 0, 0, 0]
        y2 = [0, 0, 0, 0, 0, 0, 0, 0]
        y3 = [0, 0, 0, 0, 0, 0, 0, 0]
        step = 0
        for vis in old_x:
            IndexOfX = x.index(vis)
            y1[IndexOfX] = average_salary.reset_index()['平均薪资'][step]
            y2[IndexOfX] = average_low_salary.reset_index()['最低薪资'][step]
            y3[IndexOfX] = average_high_salary.reset_index()['最高薪资'][step]
            step += 1
        return x, y1, y2, y3

    def Set_X_EXP(self, old_x, average_salary, average_low_salary, average_high_salary):
        x = ['10年以上', '5-10年', '3-5年', '1-3年', '1年以下', '不限']
        y1 = [0, 0, 0, 0, 0, 0]
        y2 = [0, 0, 0, 0, 0, 0]
        y3 = [0, 0, 0, 0, 0, 0]
        step = 0
        for vis in old_x:
            IndexOfX = x.index(vis)
            y1[IndexOfX] = average_salary.reset_index()['平均薪资'][step]
            y2[IndexOfX] = average_low_salary.reset_index()['最低薪资'][step]
            y3[IndexOfX] = average_high_salary.reset_index()['最高薪资'][step]
            step += 1
        return x, y1, y2, y3

import pandas as pd
from prophet import Prophet

#tạo dataframe của ngày nghỉ, ngày lễ
tet = pd.DataFrame({
  'holiday': 'tet',
  'ds': pd.to_datetime(['2019-02-02', '2019-02-03', '2019-02-04', '2019-02-05', '2019-02-06', '2019-02-07', '2019-02-08', '2019-02-09',
                        '2019-02-10', '2020-01-23', '2020-01-24', '2020-01-25', '2020-01-26', '2020-01-27', '2020-01-28', '2020-01-29',
                        '2020-01-30', '2020-01-31', '2020-02-01', '2020-02-02', '2021-02-10', '2021-02-11', '2021-02-12', '2021-02-13',
                        '2021-02-14', '2021-02-15', '2021-02-16', '2021-02-17', '2021-02-18', '2021-02-19', '2021-02-20', '2021-02-21',
                        '2022-01-29', '2022-01-30', '2022-01-31', '2022-02-01', '2022-02-02', '2022-02-03', '2022-02-04', '2022-02-05',
                        '2022-02-06', '2023-01-20', '2023-01-21', '2023-01-22', '2023-01-23', '2023-01-24', '2023-01-25', '2023-01-26',
                        '2023-01-27', '2023-01-28', '2023-01-29', '2024-02-08', '2024-02-09', '2024-02-10', '2024-02-11', '2024-02-12',
                        '2024-02-13', '2024-02-14', '2024-02-15', '2024-02-16', '2024-02-17', '2024-02-18', '2025-01-25', '2025-01-26',
                        '2025-01-27', '2025-01-28', '2025-01-29', '2025-01-30', '2025-01-31', '2025-02-01', '2025-02-02']),
  'lower_window': -5,
  'upper_window': 14,
})
GPMNQTLĐ = pd.DataFrame({
  'holiday': 'GPMNQTLĐ',
  'ds': pd.to_datetime(['2019-04-27', '2019-04-28', '2019-04-29', '2019-04-30', '2019-05-01',
                        '2020-04-30', '2020-05-01', '2020-05-02', '2020-05-03', '2021-04-29',
                        '2021-04-30', '2021-05-01', '2021-05-02', '2022-04-30', '2022-05-01',
                        '2022-05-02', '2022-05-03', '2023-04-29', '2023-04-30', '2023-05-01',
                        '2023-05-02', '2023-05-03', '2024-04-27', '2024-04-28', '2024-04-29',
                        '2024-04-30', '2024-05-01']),
  'lower_window': -10,
  'upper_window': 10,
})
holidays = pd.concat((tet, GPMNQTLĐ))
holidays_1 = tet 

#nhập data từ Excel
from pandas import ExcelFile
import matplotlib.pyplot as plt
from prophet.plot import plot_yearly
path = 'C:\\Users\\M3514278\\OneDrive - Saint-Gobain\\2.Price&BLK\\Source Data\\Python.xlsx'
df = pd.read_excel(path, sheet_name = 'Raw data adjusted')
df['DATE'] = pd.to_datetime(df['DATE'])
df_sales_perc = {cid:
                   df[(df['CUSTOMER_ID'] == cid) & (df['DATE'] < '2024-01-01')]
                   [['CUSTOMER_NAME','CUSTOMER_ID','DATE', 'SALES']] for cid in df['CUSTOMER_ID'].unique()
}

'''# khách trường phát
df_truongphat1 = df_sales_perc[11000912].rename(columns={'DATE': 'ds', 'SALES': 'y'})
df_truongphat = df_sales_perc[11000912].rename(columns={'DATE': 'ds', 'SALES': 'y'})
df_truongphat['cap'] = df_truongphat['y'].max()
df_truongphat['floor'] = 0
df_truongphat['growth_rate'] = df_truongphat['ds'].apply(lambda x: 60 if x < pd.Timestamp('2020-01-01') else (100 if x < pd.Timestamp('2021-01-01') else (133 if x < pd.Timestamp('2022-01-01') else (182 if x < pd.Timestamp('2023-01-01') else (184 if x < pd.Timestamp ('2024-01-01') else 161)))))
df_truongphat['fluctuation'] = df_truongphat['ds'].apply(lambda x: 1 if x < pd.Timestamp('2020-01-01') else (2 if x < pd.Timestamp('2021-01-01') else (4 if x < pd.Timestamp('2022-01-01') else (4 if x < pd.Timestamp('2023-01-01') else (2 if x < pd.Timestamp ('2024-01-01') else 2)))))
model_truongphat = Prophet(growth='logistic', changepoint_range=0.95, yearly_seasonality=6,
            weekly_seasonality=False, daily_seasonality=False, holidays=holidays,
            seasonality_mode='additive', seasonality_prior_scale=5,
            holidays_prior_scale=5, changepoint_prior_scale=0.1 ,interval_width=0.95)
model_truongphat.add_regressor('growth_rate', mode='additive')
model_truongphat.add_regressor('fluctuation', mode='additive')
model_truongphat.fit(df_truongphat)
#a = plot_yearly(model_truongphat)
future_truongphat = model_truongphat.make_future_dataframe(periods=12, freq='MS', include_history=True)
future_truongphat['cap'] = df_truongphat['y'].max()
future_truongphat['floor'] = 0
future_truongphat['growth_rate'] = future_truongphat['ds'].apply(lambda x: 60 if x < pd.Timestamp('2020-01-01') else (100 if x < pd.Timestamp('2021-01-01') else (133 if x < pd.Timestamp('2022-01-01') else (182 if x < pd.Timestamp('2023-01-01') else (184 if x < pd.Timestamp ('2024-01-01') else 161)))))
future_truongphat['fluctuation'] = future_truongphat['ds'].apply(lambda x: 1 if x < pd.Timestamp('2020-01-01') else (2 if x < pd.Timestamp('2021-01-01') else (4 if x < pd.Timestamp('2022-01-01') else (4 if x < pd.Timestamp('2023-01-01') else (2 if x < pd.Timestamp ('2024-01-01') else 2)))))
forecast_truongphat = model_truongphat.predict(future_truongphat)
result_truongphat = forecast_truongphat[['ds', 'yhat']]

# khách phú hà
df_phuha1 = df_sales_perc[11000614].rename(columns={'DATE': 'ds', 'SALES': 'y'})
df_phuha = df_sales_perc[11000614].rename(columns={'DATE': 'ds', 'SALES': 'y'})
df_phuha['cap'] = df_phuha['y'].max()
df_phuha['floor'] = 0
#df_phuha['T2'] = df_phuha['ds'].apply(lambda x: 1 if x < pd.Timestamp('2024-07-01') else 1.5)
df_phuha['growth_rate'] = df_phuha['ds'].apply(lambda x: 151 if x < pd.Timestamp('2020-01-01') else (135 if x < pd.Timestamp('2021-01-01') else (120 if x < pd.Timestamp('2022-01-01') else (187 if x < pd.Timestamp('2023-01-01') else (122 if x < pd.Timestamp ('2024-01-01') else 182)))))
df_phuha['quarter'] = df_phuha['ds'].dt.quarter
df_phuha['quarter_seasonality'] = df_phuha['quarter'].apply(lambda x: -1 if x in [1, 2] else 1)
model_phuha = Prophet(growth='logistic', changepoint_range=0.95, yearly_seasonality=5,
            weekly_seasonality=False, daily_seasonality=False, holidays=holidays,
            seasonality_mode='additive', seasonality_prior_scale=3,
            holidays_prior_scale=3, changepoint_prior_scale=0.2 ,interval_width=0.8)
model_phuha.add_regressor('growth_rate', mode='additive')
model_phuha.add_regressor('quarter_seasonality', mode='additive')
model_phuha.fit(df_phuha)
#a = plot_yearly(model_phuha)
future_phuha = model_phuha.make_future_dataframe(periods=12, freq='MS', include_history=True)
future_phuha['cap'] = df_phuha['y'].max()
future_phuha['floor'] = 0
#future_phuha['T2'] = future_phuha['ds'].apply(lambda x: 1 if x < pd.Timestamp('2021-07-01') else (0.5 if x < pd.Timestamp('2022-07-01') else (1.5 if x < pd.Timestamp('2023-01-01') else (1 if x < pd.Timestamp('2024-07-01') else 2))))
future_phuha['growth_rate'] = future_phuha['ds'].apply(lambda x: 151 if x < pd.Timestamp('2020-01-01') else (135 if x < pd.Timestamp('2021-01-01') else (120 if x < pd.Timestamp('2022-01-01') else (187 if x < pd.Timestamp('2023-01-01') else (122 if x < pd.Timestamp ('2024-01-01') else 182)))))
future_phuha['quarter'] = future_phuha['ds'].dt.quarter
future_phuha['year'] = future_phuha['ds'].dt.year
future_phuha['quarter_seasonality'] = future_phuha.apply(
  lambda row: -1.1 if row['year'] == 2024 and row['quarter'] == 1 else
              -1.2 if row['year'] == 2024 and row['quarter'] == 2 else
               1.2 if row['year'] == 2024 and row['quarter'] in [3, 4] else
              -1 if row['quarter'] in [1, 2] else
               1,
  axis = 1
)
forecast_phuha = model_phuha.predict(future_phuha)
result_phuha = forecast_phuha[['ds', 'yhat']]

# khách dũng yên
df_dungyen1 = df_sales_perc[11000872].rename(columns={'DATE': 'ds', 'SALES': 'y'})
df_dungyen = df_sales_perc[11000872].rename(columns={'DATE': 'ds', 'SALES': 'y'})
df_dungyen['cap'] = df_dungyen['y'].max() * 1.2
df_dungyen['floor'] = 0
#df_dungyen['T2'] = df_dungyen['ds'].apply(lambda x: 0 if x < pd.Timestamp('2023-02-01') else (2 if x < pd.Timestamp('2024-01-01') else 0))
df_dungyen['growth_rate'] = df_dungyen['ds'].apply(lambda x: 27 if x < pd.Timestamp('2020-01-01') else (27 if x < pd.Timestamp('2021-01-01') else (39 if x < pd.Timestamp('2022-01-01') else (55 if x < pd.Timestamp('2023-01-01') else (222 if x < pd.Timestamp ('2024-01-01') else 157)))))
df_dungyen['quarter'] = df_dungyen['ds'].dt.quarter
df_dungyen['year'] = df_dungyen['ds'].dt.year
df_dungyen['quarter_seasonality'] = df_dungyen.apply(
  lambda row: -2 if row['year'] == 2023 and row['quarter'] in [1, 2] else
               2 if row['year'] == 2023 and row['quarter'] in [3, 4] else
              -1 if row['quarter'] in [1, 2] else
               1,
  axis = 1
  )
model_dungyen = Prophet(growth='logistic', changepoint_range=0.9, yearly_seasonality=5,
            weekly_seasonality=False, daily_seasonality=False, holidays=holidays,
            seasonality_mode='additive', seasonality_prior_scale=3,
            holidays_prior_scale=3, changepoint_prior_scale=0.1 ,interval_width=0.95)
#model_dungyen.add_regressor('T2',prior_scale=3, mode='additive')
model_dungyen.add_regressor('growth_rate', mode='additive')
model_dungyen.add_regressor('quarter_seasonality', mode='additive')
model_dungyen.fit(df_dungyen)
#a = plot_yearly(model_dungyen)
future_dungyen = model_dungyen.make_future_dataframe(periods=12, freq='MS', include_history=True)
future_dungyen['cap'] = df_dungyen['y'].max() * 1.2
future_dungyen['floor'] = 0
#future_dungyen['T2'] = future_dungyen['ds'].apply(lambda x: 0 if x < pd.Timestamp('2023-02-01') else (2 if x < pd.Timestamp('2024-01-01') else 0))
future_dungyen['growth_rate'] = future_dungyen['ds'].apply(lambda x: 27 if x < pd.Timestamp('2020-01-01') else (27 if x < pd.Timestamp('2021-01-01') else (39 if x < pd.Timestamp('2022-01-01') else (55 if x < pd.Timestamp('2023-01-01') else (222 if x < pd.Timestamp ('2024-01-01') else 157)))))
future_dungyen['quarter'] = future_dungyen['ds'].dt.quarter
future_dungyen['year'] = future_dungyen['ds'].dt.year
future_dungyen['quarter_seasonality'] = future_dungyen.apply(
  lambda row: -2 if row['year'] == 2023 and row['quarter'] in [1, 2] else
               2 if row['year'] == 2023 and row['quarter'] in [3, 4] else
              -0.7 if row['year'] == 2024 and row['quarter'] in [1, 2] else
               0.7 if row['year'] == 2024 and row['quarter'] in [3, 4] else
              -1 if row['quarter'] in [1, 2] else
               1,
  axis = 1
  )
forecast_dungyen = model_dungyen.predict(future_dungyen)
result_dungyen = forecast_dungyen[['ds', 'yhat']]'''

# khách an phát
df_anphat1 = df_sales_perc[11001112].rename(columns={'DATE': 'ds', 'SALES': 'y'})
df_anphat = df_sales_perc[11001112].rename(columns={'DATE': 'ds', 'SALES': 'y'})
df_anphat['cap'] = df_anphat['y'].max()
df_anphat['floor'] = 0
df_anphat['growth_rate'] = df_anphat['ds'].apply(lambda x: 27 if x < pd.Timestamp('2021-01-01') else (88 if x < pd.Timestamp('2022-01-01') else (126 if x < pd.Timestamp('2023-01-01') else (112 if x < pd.Timestamp('2024-01-01') else 122))))
#df_anphat['fluctuation'] = df_anphat['ds'].apply(lambda x: 0 if x < pd.Timestamp('2021-01-01') else (4 if x < pd.Timestamp('2022-01-01') else (3 if x < pd.Timestamp('2023-01-01') else (4 if x < pd.Timestamp('2024-01-01') else 3))))
model_anphat = Prophet(growth='logistic', changepoint_range=0.9, yearly_seasonality=5,
            weekly_seasonality=False, daily_seasonality=False, holidays=holidays,
            seasonality_mode='multiplicative', seasonality_prior_scale=3,
            holidays_prior_scale=3, changepoint_prior_scale=0.1 ,interval_width=0.95)
model_anphat.add_regressor('growth_rate', mode='additive')
model_anphat.fit(df_anphat)
a = plot_yearly(model_anphat)
plt.show()
future_anphat = model_anphat.make_future_dataframe(periods=12, freq='MS', include_history=True)
future_anphat['cap'] = df_anphat['y'].max()
future_anphat['floor'] = 0
future_anphat['growth_rate'] = future_anphat['ds'].apply(lambda x: 27 if x < pd.Timestamp('2021-01-01') else (88 if x < pd.Timestamp('2022-01-01') else (126 if x < pd.Timestamp('2023-01-01') else (112 if x < pd.Timestamp('2024-01-01') else 122))))
#future_anphat['fluctuation'] = future_anphat['ds'].apply(lambda x: 0 if x < pd.Timestamp('2021-01-01') else (4 if x < pd.Timestamp('2022-01-01') else (3 if x < pd.Timestamp('2023-01-01') else (4 if x < pd.Timestamp('2024-01-01') else 3))))
forecast_anphat = model_anphat.predict(future_anphat)
result_anphat = forecast_anphat[['ds', 'yhat']]

'''# khách gia bảo
df_giabao1 = df_sales_perc[11000596].rename(columns={'DATE': 'ds', 'SALES': 'y'})
df_giabao = df_sales_perc[11000596].rename(columns={'DATE': 'ds', 'SALES': 'y'})
df_giabao['cap'] = df_giabao['y'].max() 
df_giabao['floor'] = 0
df_giabao['growth_rate'] = df_giabao['ds'].apply(lambda x: 63 if x < pd.Timestamp('2020-01-01') else (63 if x < pd.Timestamp('2021-01-01') else (94 if x < pd.Timestamp('2022-01-01') else (120 if x < pd.Timestamp('2023-01-01') else (109 if x < pd.Timestamp('2024-01-01') else 107)))))
df_giabao['year'] = df_giabao['ds'].dt.year
df_giabao['quarter'] = df_giabao['ds'].dt.quarter
df_giabao['quarter_seasonality'] = df_giabao.apply(
    lambda row: 1 if row['year'] == 2019 and row['quarter'] == 1 else
                2 if row['year'] == 2019 and row['quarter'] == 2 else
                3 if row['year'] == 2019 and row['quarter'] == 3 else
                4 if row['year'] == 2019 and row['quarter'] == 4 else
                1 if row['year'] == 2020 and row['quarter'] == 1 else
                2 if row['year'] == 2020 and row['quarter'] == 2 else
                3 if row['year'] == 2020 and row['quarter'] == 3 else
                4 if row['year'] == 2020 and row['quarter'] == 4 else
                1 if row['year'] == 2021 and row['quarter'] == 1 else
                2 if row['year'] == 2021 and row['quarter'] == 2 else
                4 if row['year'] == 2021 and row['quarter'] == 3 else
                4 if row['year'] == 2021 and row['quarter'] == 4 else
                2 if row['year'] == 2022 and row['quarter'] == 1 else
                2 if row['year'] == 2022 and row['quarter'] == 2 else
                3 if row['year'] == 2022 and row['quarter'] == 3 else
                4 if row['year'] == 2022 and row['quarter'] == 4 else
                2 if row['year'] == 2023 and row['quarter'] == 1 else
                2 if row['year'] == 2023 and row['quarter'] == 2 else
                3 if row['year'] == 2023 and row['quarter'] == 3 else
                3,        
  axis = 1
)
#df_giabao['DISCOUNT_RATE'] = df_giabao['ds'].apply(lambda x: 1 if x < pd.Timestamp('2024-04-01') else (0.97 if x < pd.Timestamp('2025-01-01') else 0.99))
model_giabao = Prophet(growth='logistic', changepoint_range=0.9, yearly_seasonality=5,
            weekly_seasonality=False, daily_seasonality=False, holidays=holidays,
            seasonality_mode='additive', seasonality_prior_scale=5,
            holidays_prior_scale=5, changepoint_prior_scale=0.1 ,interval_width=0.95)
model_giabao.add_regressor('growth_rate', mode='additive')
model_giabao.add_regressor('quarter_seasonality', mode='additive')
#model_giabao.add_seasonality(name='quarter', period=91.25, fourier_order=5)
#model_giabao.add_regressor('DISCOUNT_RATE',prior_scale=3, mode='additive')
model_giabao.fit(df_giabao)
#a = plot_yearly(model_giabao)
future_giabao = model_giabao.make_future_dataframe(periods=12, freq='MS', include_history=True)
future_giabao['cap'] = df_giabao['y'].max()
future_giabao['floor'] = 0
future_giabao['growth_rate'] = future_giabao['ds'].apply(lambda x: 63 if x < pd.Timestamp('2020-01-01') else (63 if x < pd.Timestamp('2021-01-01') else (94 if x < pd.Timestamp('2022-01-01') else (120 if x < pd.Timestamp('2023-01-01') else (109 if x < pd.Timestamp('2024-01-01') else 107)))))
future_giabao['year'] = future_giabao['ds'].dt.year
future_giabao['quarter'] = future_giabao['ds'].dt.quarter
future_giabao['quarter_seasonality'] = future_giabao.apply(
    lambda row: 1 if row['year'] == 2019 and row['quarter'] == 1 else
                2 if row['year'] == 2019 and row['quarter'] == 2 else
                3 if row['year'] == 2019 and row['quarter'] == 3 else
                4 if row['year'] == 2019 and row['quarter'] == 4 else
                1 if row['year'] == 2020 and row['quarter'] == 1 else
                2 if row['year'] == 2020 and row['quarter'] == 2 else
                3 if row['year'] == 2020 and row['quarter'] == 3 else
                4 if row['year'] == 2020 and row['quarter'] == 4 else
                1 if row['year'] == 2021 and row['quarter'] == 1 else
                2 if row['year'] == 2021 and row['quarter'] == 2 else
                4 if row['year'] == 2021 and row['quarter'] == 3 else
                4 if row['year'] == 2021 and row['quarter'] == 4 else
                2 if row['year'] == 2022 and row['quarter'] == 1 else
                2 if row['year'] == 2022 and row['quarter'] == 2 else
                3 if row['year'] == 2022 and row['quarter'] == 3 else
                4 if row['year'] == 2022 and row['quarter'] == 4 else
                2 if row['year'] == 2023 and row['quarter'] == 1 else
                2 if row['year'] == 2023 and row['quarter'] == 2 else
                3 if row['year'] == 2023 and row['quarter'] == 3 else
                3 if row['year'] == 2023 and row['quarter'] == 4 else
                3 if row['year'] == 2024 and row['quarter'] == 1 else
                2 if row['year'] == 2024 and row['quarter'] == 2 else
                3 if row['year'] == 2024 and row['quarter'] == 3 else
                4,
  axis = 1
)
#future_giabao['DISCOUNT_RATE'] = future_giabao['ds'].apply(lambda x: 1 if x < pd.Timestamp('2024-04-01') else (0.97 if x < pd.Timestamp('2025-01-01') else 0.99))
forecast_giabao = model_giabao.predict(future_giabao)
result_giabao = forecast_giabao[['ds', 'yhat']]

# khách ngọc dung
df_ngocdung1 = df_sales_perc[11000620].rename(columns={'DATE': 'ds', 'SALES': 'y'})
df_ngocdung = df_sales_perc[11000620].rename(columns={'DATE': 'ds', 'SALES': 'y'})
df_ngocdung['cap'] = df_ngocdung['y'].max()  * 1.2
df_ngocdung['floor'] = 0
df_ngocdung['growth_rate'] = df_ngocdung['ds'].apply(lambda x: 78 if x < pd.Timestamp('2020-01-01') else (100 if x < pd.Timestamp('2021-01-01') else (93 if x < pd.Timestamp('2022-01-01') else (101 if x < pd.Timestamp('2023-01-01') else (87 if x < pd.Timestamp('2024-01-01') else 103)))))
model_ngocdung = Prophet(growth='logistic', changepoint_range=0.9, yearly_seasonality=5,
            weekly_seasonality=False, daily_seasonality=False, holidays=holidays,
            seasonality_mode='multiplicative', seasonality_prior_scale=5,
            holidays_prior_scale=5, changepoint_prior_scale=0.1 ,interval_width=0.95)
model_ngocdung.add_regressor('growth_rate', mode='additive')
model_ngocdung.fit(df_ngocdung)
#a = plot_yearly(model_ngocdung)
future_ngocdung = model_ngocdung.make_future_dataframe(periods=12, freq='MS', include_history=True)
future_ngocdung['cap'] = df_ngocdung['y'].max() * 1.2
future_ngocdung['floor'] = 0
future_ngocdung['growth_rate'] = future_ngocdung['ds'].apply(lambda x: 78 if x < pd.Timestamp('2020-01-01') else (100 if x < pd.Timestamp('2021-01-01') else (93 if x < pd.Timestamp('2022-01-01') else (101 if x < pd.Timestamp('2023-01-01') else (87 if x < pd.Timestamp('2024-01-01') else 103)))))
forecast_ngocdung = model_ngocdung.predict(future_ngocdung)
result_ngocdung = forecast_ngocdung[['ds', 'yhat']]

# khách xuân thường
df_xuanthuong1 = df_sales_perc[11000624].rename(columns={'DATE': 'ds', 'SALES': 'y'})
df_xuanthuong = df_sales_perc[11000624].rename(columns={'DATE': 'ds', 'SALES': 'y'})
df_xuanthuong['cap'] = df_xuanthuong['y'].max() * 2
df_xuanthuong['floor'] = 0
df_xuanthuong['growth_rate'] = df_xuanthuong['ds'].apply(lambda x: 20 if x < pd.Timestamp('2020-01-01') else (26 if x < pd.Timestamp('2021-01-01') else (48 if x < pd.Timestamp('2022-01-01') else (51 if x < pd.Timestamp('2023-01-01') else (52 if x < pd.Timestamp('2024-01-01') else 100)))))
df_xuanthuong['quarter'] = df_xuanthuong['ds'].dt.quarter
df_xuanthuong['quarter_seasonality'] = df_xuanthuong['quarter'].apply(lambda x: -1 if x in [1,2] else 1)
model_xuanthuong = Prophet(growth='logistic', changepoints = None, changepoint_range=0.1, yearly_seasonality=5,
            weekly_seasonality=False, daily_seasonality=False, holidays=holidays,
            seasonality_mode='multiplicative', seasonality_prior_scale=10,
            holidays_prior_scale=10, changepoint_prior_scale=0.01 ,interval_width=0.95)
model_xuanthuong.add_regressor('growth_rate', mode='additive')
model_xuanthuong.add_regressor('quarter_seasonality', mode='additive')
model_xuanthuong.fit(df_xuanthuong)
#a = plot_yearly(model_xuanthuong)
future_xuanthuong = model_xuanthuong.make_future_dataframe(periods=12, freq='MS', include_history=True)
future_xuanthuong['cap'] = df_xuanthuong['y'].max() * 2
future_xuanthuong['floor'] = 0
future_xuanthuong['growth_rate'] = future_xuanthuong['ds'].apply(lambda x: 20 if x < pd.Timestamp('2020-01-01') else (26 if x < pd.Timestamp('2021-01-01') else (48 if x < pd.Timestamp('2022-01-01') else (51 if x < pd.Timestamp('2023-01-01') else (52 if x < pd.Timestamp('2024-01-01') else 100)))))
future_xuanthuong['quarter'] = future_xuanthuong['ds'].dt.quarter
future_xuanthuong['year'] = future_xuanthuong['ds'].dt.year
future_xuanthuong['quarter_seasonality'] = future_xuanthuong.apply(
  lambda row: -1.6 if row['year'] == 2024 and row['quarter'] == 1 else
              -1 if row['year'] == 2024 and row['quarter'] == 2 else
               1.5 if row['year'] == 2024 and row['quarter'] == 3 else
               2.7 if row['year'] == 2024 and row['quarter'] == 4 else
              -1 if row['quarter'] in [1,2] else
               1,
  axis = 1
)
forecast_xuanthuong = model_xuanthuong.predict(future_xuanthuong)
result_xuanthuong = forecast_xuanthuong[['ds', 'yhat']]

# khách toàn lộc
df_toanloc1 = df_sales_perc[11000602].rename(columns={'DATE': 'ds', 'SALES': 'y'})
df_toanloc = df_sales_perc[11000602].rename(columns={'DATE': 'ds', 'SALES': 'y'})
df_toanloc['cap'] = df_toanloc['y'].max() * 1.2
df_toanloc['floor'] = 0
df_toanloc['growth_rate'] = df_toanloc['ds'].apply(lambda x: 89 if x < pd.Timestamp('2020-01-01') else (94 if x < pd.Timestamp('2021-01-01') else (128 if x < pd.Timestamp('2022-01-01') else (147 if x < pd.Timestamp('2023-01-01') else (110 if x < pd.Timestamp('2024-01-01') else 93)))))
model_toanloc = Prophet(growth='logistic', changepoint_range=0.9, yearly_seasonality=5,
            weekly_seasonality=False, daily_seasonality=False, holidays=holidays,
            seasonality_mode='multiplicative', seasonality_prior_scale=0.1,
            holidays_prior_scale=0.1, changepoint_prior_scale=0.001 ,interval_width=0.95)
model_toanloc.add_regressor('growth_rate', mode='additive')
model_toanloc.fit(df_toanloc)
#a = plot_yearly(model_toanloc)
future_toanloc = model_toanloc.make_future_dataframe(periods=12, freq='MS', include_history=True)
future_toanloc['cap'] = df_toanloc['y'].max() * 1.2
future_toanloc['floor'] = 0
future_toanloc['growth_rate'] = future_toanloc['ds'].apply(lambda x: 89 if x < pd.Timestamp('2020-01-01') else (94 if x < pd.Timestamp('2021-01-01') else (128 if x < pd.Timestamp('2022-01-01') else (147 if x < pd.Timestamp('2023-01-01') else (110 if x < pd.Timestamp('2024-01-01') else 93)))))
forecast_toanloc = model_toanloc.predict(future_toanloc)
result_toanloc = forecast_toanloc[['ds', 'yhat']]
print(forecast_toanloc[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail(12))
fig, ax = plt.subplots(figsize=(10, 6))
model_toanloc.plot(forecast_toanloc, ax=ax)
plt.title('Dự báo với Prophet')
plt.xlabel('Ngày')
plt.ylabel('Giá trị')
plt.show()

# khách cao gia phát
df_caogiaphat1 = df_sales_perc[11001415].rename(columns={'DATE': 'ds', 'SALES': 'y'})
df_caogiaphat = df_sales_perc[11001415].rename(columns={'DATE': 'ds', 'SALES': 'y'})
df_caogiaphat['cap'] = df_caogiaphat['y'].max() * 1.2
df_caogiaphat['floor'] = 0
df_caogiaphat['growth_rate'] = df_caogiaphat['ds'].apply(lambda x: 52 if x < pd.Timestamp('2024-01-01') else 71)
model_caogiaphat = Prophet(growth='logistic', changepoint_range=0.9, yearly_seasonality=5,
            weekly_seasonality=False, daily_seasonality=False, holidays=holidays,
            seasonality_mode='additive', seasonality_prior_scale=3,
            holidays_prior_scale=3, changepoint_prior_scale=0.05 ,interval_width=0.95)
#model_caogiaphat.add_regressor('growth_rate', mode='additive')
model_caogiaphat.fit(df_caogiaphat)
#a = plot_yearly(model_caogiaphat)
future_caogiaphat = model_caogiaphat.make_future_dataframe(periods=12, freq='MS', include_history=True)
future_caogiaphat['cap'] = df_caogiaphat['y'].max() * 1.2
future_caogiaphat['floor'] = 0
future_caogiaphat['growth_rate'] = future_caogiaphat['ds'].apply(lambda x: 52 if x < pd.Timestamp('2024-01-01') else 71)
forecast_caogiaphat = model_caogiaphat.predict(future_caogiaphat)
result_caogiaphat = forecast_caogiaphat[['ds', 'yhat']]

# khách huy hùng
df_huyhung1 = df_sales_perc[11001324].rename(columns={'DATE': 'ds', 'SALES': 'y'})
df_huyhung = df_sales_perc[11001324].rename(columns={'DATE': 'ds', 'SALES': 'y'})
df_huyhung['cap'] = df_huyhung['y'].max() * 1.2
df_huyhung['floor'] = 0
df_huyhung['growth_rate'] = df_huyhung['ds'].apply(lambda x: 7 if x < pd.Timestamp('2022-01-01') else (50 if x < pd.Timestamp('2023-01-01') else (50 if x < pd.Timestamp('2024-01-01') else 68)))
df_huyhung['year'] = df_huyhung['ds'].dt.year
df_huyhung['quarter'] = df_huyhung['ds'].dt.quarter
df_huyhung['quarter_seasonality'] = df_huyhung.apply(
  lambda row: #-1 if row['year'] == 2021 and row['quarter'] == 4 else
              -1 if row['year'] == 2022 and row['quarter'] in [1, 2] else
               1 if row['year'] == 2022 and row['quarter'] in [3, 4] else
              -1 if row['year'] == 2023 and row['quarter'] in [1, 2] else
               1 if row['year'] == 2023 and row['quarter'] == 3 else
               0.5 if row['year'] == 2023 and row['quarter'] == 4 else
              -1 if row['quarter'] in [1, 2] else
               1,
  axis = 1
  )
#df_huyhung['DISCOUNT_RATE'] = df_huyhung['ds'].apply(lambda x: 1 if x < pd.Timestamp('2024-04-01') else (0.97 if x < pd.Timestamp('2025-01-01') else 0.99))
model_huyhung = Prophet(growth='logistic', changepoint_range=0.9, yearly_seasonality=5,
            weekly_seasonality=False, daily_seasonality=False, holidays=holidays,
            seasonality_mode='multiplicative', seasonality_prior_scale=3,
            holidays_prior_scale=3, changepoint_prior_scale=0.1 ,interval_width=0.95)
model_huyhung.add_regressor('growth_rate', mode='additive')
model_huyhung.add_regressor('quarter_seasonality', mode='additive')
#model_huyhung.add_regressor('DISCOUNT_RATE',prior_scale=3, mode='additive')
model_huyhung.fit(df_huyhung)
#a = plot_yearly(model_huyhung)
future_huyhung = model_huyhung.make_future_dataframe(periods=12, freq='MS', include_history=True)
future_huyhung['cap'] = df_huyhung['y'].max() * 1.2
future_huyhung['floor'] = 0
future_huyhung['growth_rate'] = future_huyhung['ds'].apply(lambda x: 7 if x < pd.Timestamp('2022-01-01') else (50 if x < pd.Timestamp('2023-01-01') else (50 if x < pd.Timestamp('2024-01-01') else 68)))
future_huyhung['year'] = future_huyhung['ds'].dt.year
future_huyhung['quarter'] = future_huyhung['ds'].dt.quarter
future_huyhung['quarter_seasonality'] = future_huyhung.apply(
  lambda row: #-1 if row['year'] == 2021 and row['quarter'] == 4 else
              -1 if row['year'] == 2022 and row['quarter'] in [1, 2] else
               1 if row['year'] == 2022 and row['quarter'] in [3, 4] else
              -1 if row['year'] == 2023 and row['quarter'] in [1, 2] else
               1 if row['year'] == 2023 and row['quarter'] == 3 else
               0.5 if row['year'] == 2023 and row['quarter'] == 4 else
              -1.3 if row['year'] == 2024 and row['quarter'] == 1 else
              -1.3 if row['year'] == 2024 and row['quarter'] == 2 else
               0.8 if row['year'] == 2024 and row['quarter'] == 3 else
               1.2 if row['year'] == 2024 and row['quarter'] == 4 else
               1,
  axis = 1
  )
#future_huyhung['DISCOUNT_RATE'] = future_huyhung['ds'].apply(lambda x: 1 if x < pd.Timestamp('2024-04-01') else (0.97 if x < pd.Timestamp('2025-01-01') else 0.99))
forecast_huyhung = model_huyhung.predict(future_huyhung)
result_huyhung = forecast_huyhung[['ds', 'yhat']]

# khách gyvina
df_givina1 = df_sales_perc[11001043].rename(columns={'DATE': 'ds', 'SALES': 'y'})
df_givina = df_sales_perc[11001043].rename(columns={'DATE': 'ds', 'SALES': 'y'})
df_givina['cap'] = df_givina['y'].max() * 1.2
df_givina['floor'] = 0
df_givina['growth_rate'] = df_givina['ds'].apply(lambda x: 38 if x < pd.Timestamp('2021-01-01') else (53 if x < pd.Timestamp('2022-01-01') else (65 if x < pd.Timestamp('2023-01-01') else (59 if x < pd.Timestamp('2024-01-01') else 67))))
df_givina['quarter'] = df_givina['ds'].dt.quarter
df_givina['quarter_seasonality'] = df_givina['quarter'].apply(lambda x: -1 if x in [1, 2] else 1)
model_givina = Prophet(growth='logistic', changepoint_range=0.9, yearly_seasonality=5,
            weekly_seasonality=False, daily_seasonality=False, holidays=holidays,
            seasonality_mode='multiplicative', seasonality_prior_scale=1,
            holidays_prior_scale=1, changepoint_prior_scale=0.1 ,interval_width=0.95)
model_givina.add_regressor('growth_rate', mode='additive')
model_givina.add_regressor('quarter_seasonality', mode='additive')
model_givina.fit(df_givina)
#a = plot_yearly(model_givina)
future_givina = model_givina.make_future_dataframe(periods=12, freq='MS', include_history=True)
future_givina['cap'] = df_givina['y'].max() * 1.2
future_givina['floor'] = 0
future_givina['growth_rate'] = future_givina['ds'].apply(lambda x: 38 if x < pd.Timestamp('2021-01-01') else (53 if x < pd.Timestamp('2022-01-01') else (65 if x < pd.Timestamp('2023-01-01') else (59 if x < pd.Timestamp('2024-01-01') else 67))))
future_givina['year'] = future_givina['ds'].dt.year
future_givina['quarter'] = future_givina['ds'].dt.quarter
future_givina['quarter_seasonality'] = future_givina.apply(
  lambda row: -1 if row['year'] == 2024 and row['quarter'] == 1 else
              -1 if row['year'] == 2024 and row['quarter'] == 2 else
               0.9 if row['year'] == 2024 and row['quarter'] == 3 else
               2 if row['year'] == 2024 and row['quarter'] == 4 else
              -1 if row['quarter'] in [1,2] else
               1,
  axis = 1
  )
forecast_givina = model_givina.predict(future_givina)
result_givina = forecast_givina[['ds', 'yhat']]

# khách hải dương nghệ an
df_haiduongnghean1 = df_sales_perc[11001241].rename(columns={'DATE': 'ds', 'SALES': 'y'})
df_haiduongnghean = df_sales_perc[11001241].rename(columns={'DATE': 'ds', 'SALES': 'y'})
df_haiduongnghean['cap'] = df_haiduongnghean['y'].max() * 1.2
df_haiduongnghean['floor'] = 0
df_haiduongnghean['growth_rate'] = df_haiduongnghean['ds'].apply(lambda x: 18 if x < pd.Timestamp('2022-01-01') else (42 if x < pd.Timestamp('2023-01-01') else (58 if x < pd.Timestamp('2024-01-01') else 51)))
model_haiduongnghean = Prophet(growth='logistic', changepoint_range=0.9, yearly_seasonality=6,
            weekly_seasonality=False, daily_seasonality=False,
            seasonality_mode='additive', seasonality_prior_scale=3,
            holidays_prior_scale=3, changepoint_prior_scale=0.1 ,interval_width=0.95)
model_haiduongnghean.add_regressor('growth_rate', mode='additive')
model_haiduongnghean.fit(df_haiduongnghean)
#a = plot_yearly(model_haiduongnghean)
future_haiduongnghean = model_haiduongnghean.make_future_dataframe(periods=12, freq='MS', include_history=True)
future_haiduongnghean['cap'] = df_haiduongnghean['y'].max() * 1.2
future_haiduongnghean['floor'] = 0
future_haiduongnghean['growth_rate'] = future_haiduongnghean['ds'].apply(lambda x: 18 if x < pd.Timestamp('2022-01-01') else (42 if x < pd.Timestamp('2023-01-01') else (58 if x < pd.Timestamp('2024-01-01') else 51)))
forecast_haiduongnghean = model_haiduongnghean.predict(future_haiduongnghean)
result_haiduongnghean = forecast_haiduongnghean[['ds', 'yhat']]

# khách hiền châu
df_hienchau1 = df_sales_perc[11001073].rename(columns={'DATE': 'ds', 'SALES': 'y'})
df_hienchau = df_sales_perc[11001073].rename(columns={'DATE': 'ds', 'SALES': 'y'})
df_hienchau['cap'] = df_hienchau['y'].max() * 1.2
df_hienchau['floor'] = 0
df_hienchau['growth_rate'] = df_hienchau['ds'].apply(lambda x: 14 if x < pd.Timestamp('2021-01-01') else (35 if x < pd.Timestamp('2022-01-01') else (40 if x < pd.Timestamp('2023-01-01') else (44 if x < pd.Timestamp('2024-01-01') else 48))))
df_hienchau['year'] = df_hienchau['ds'].dt.year
df_hienchau['quarter'] = df_hienchau['ds'].dt.quarter
df_hienchau['quarter_seasonality'] = df_hienchau.apply(
  lambda row: -1 if row['year'] == 2023 and row['quarter'] in [1,2] else
               1 if row['year'] == 2023 and row['quarter'] == 3 else
               1.2 if row['year'] == 2023 and row['quarter'] == 4 else
              -1 if row['quarter'] in [1,2] else
               1,
  axis = 1
  )
model_hienchau = Prophet(growth='logistic', changepoint_range=0.9, yearly_seasonality=5,
            weekly_seasonality=False, daily_seasonality=False, holidays=holidays,
            seasonality_mode='additive', seasonality_prior_scale=3,
            holidays_prior_scale=3, changepoint_prior_scale=0.1 ,interval_width=0.95)
model_hienchau.add_regressor('growth_rate', mode='additive')
model_hienchau.add_regressor('quarter_seasonality', mode='additive')
model_hienchau.fit(df_hienchau)
#a = plot_yearly(model_hienchau)
future_hienchau = model_hienchau.make_future_dataframe(periods=12, freq='MS', include_history=True)
future_hienchau['cap'] = df_hienchau['y'].max() * 1.2
future_hienchau['floor'] = 0
future_hienchau['growth_rate'] = future_hienchau['ds'].apply(lambda x: 14 if x < pd.Timestamp('2021-01-01') else (35 if x < pd.Timestamp('2022-01-01') else (40 if x < pd.Timestamp('2023-01-01') else (44 if x < pd.Timestamp('2024-01-01') else 48))))
future_hienchau['year'] = future_hienchau['ds'].dt.year
future_hienchau['quarter'] = future_hienchau['ds'].dt.quarter
future_hienchau['quarter_seasonality'] = future_hienchau.apply(
  lambda row: -1 if row['year'] == 2023 and row['quarter'] in [1,2] else
               1 if row['year'] == 2023 and row['quarter'] == 3 else
               1.2 if row['year'] == 2023 and row['quarter'] == 4 else
              -0.8 if row['year'] == 2024 and row['quarter'] == 1 else
              -1 if row['year'] == 2024 and row['quarter'] == 2 else
               1 if row['year'] == 2024 and row['quarter'] == 3 else
               1.2 if row['year'] == 2024 and row['quarter'] == 4 else
              -1 if row['quarter'] in [1,2] else
               1,
  axis = 1
  )
forecast_hienchau = model_hienchau.predict(future_hienchau)
result_hienchau = forecast_hienchau[['ds', 'yhat']]

# khách tiến thành
df_tienthanh1 = df_sales_perc[11000608].rename(columns={'DATE': 'ds', 'SALES': 'y'})
df_tienthanh = df_sales_perc[11000608].rename(columns={'DATE': 'ds', 'SALES': 'y'})
df_tienthanh['cap'] = df_tienthanh['y'].max() * 1.2
df_tienthanh['floor'] = 0
df_tienthanh['growth_rate'] = df_tienthanh['ds'].apply(lambda x: 22 if x < pd.Timestamp('2020-01-01') else (26 if x < pd.Timestamp('2021-01-01') else (32 if x < pd.Timestamp('2022-01-01') else (36 if x < pd.Timestamp('2023-01-01') else (34 if x < pd.Timestamp ('2024-01-01') else 45)))))
model_tienthanh = Prophet(growth='logistic', changepoint_range=0.9, yearly_seasonality=5,
            weekly_seasonality=False, daily_seasonality=False, holidays=holidays,
            seasonality_mode='additive', seasonality_prior_scale=3,
            holidays_prior_scale=3, changepoint_prior_scale=0.1 ,interval_width=0.95)
model_tienthanh.add_regressor('growth_rate', mode='additive')
model_tienthanh.fit(df_tienthanh)
#a = plot_yearly(model_tienthanh)
future_tienthanh = model_tienthanh.make_future_dataframe(periods=12, freq='MS', include_history=True)
future_tienthanh['cap'] = df_tienthanh['y'].max() * 1.2
future_tienthanh['floor'] = 0
future_tienthanh['growth_rate'] = future_tienthanh['ds'].apply(lambda x: 22 if x < pd.Timestamp('2020-01-01') else (26 if x < pd.Timestamp('2021-01-01') else (32 if x < pd.Timestamp('2022-01-01') else (36 if x < pd.Timestamp('2023-01-01') else (34 if x < pd.Timestamp ('2024-01-01') else 45)))))
forecast_tienthanh = model_tienthanh.predict(future_tienthanh)
result_tienthanh = forecast_tienthanh[['ds', 'yhat']]

# khách đại an (lê hiếu)
df_lehieu1 = df_sales_perc[11001709].rename(columns={'DATE': 'ds', 'SALES': 'y'})
df_lehieu = df_sales_perc[11001709].rename(columns={'DATE': 'ds', 'SALES': 'y'})
df_lehieu['cap'] = df_lehieu['y'].max() * 1.2
df_lehieu['floor'] = 0
df_lehieu['growth_rate'] = df_lehieu['ds'].apply(lambda x: 98 if x < pd.Timestamp('2020-01-01') else (129 if x < pd.Timestamp('2021-01-01') else (113 if x < pd.Timestamp('2022-01-01') else (118 if x < pd.Timestamp('2023-01-01') else (121 if x < pd.Timestamp ('2024-01-01') else 112)))))
#df_lehieu['DISCOUNT_RATE'] = df_lehieu['ds'].apply(lambda x: 1 if x < pd.Timestamp('2024-04-01') else 0.97)
model_lehieu = Prophet(growth='logistic', changepoint_range=0.9, yearly_seasonality=5,
            weekly_seasonality=False, daily_seasonality=False, holidays=holidays,
            seasonality_mode='additive', seasonality_prior_scale=3,
            holidays_prior_scale=3, changepoint_prior_scale=0.01 ,interval_width=0.95)
model_lehieu.add_regressor('growth_rate', mode='additive')
#model_lehieu.add_regressor('DISCOUNT_RATE',prior_scale=3, mode='additive')
model_lehieu.fit(df_lehieu)
#a = plot_yearly(model_lehieu)
future_lehieu = model_lehieu.make_future_dataframe(periods=12, freq='MS', include_history=True)
future_lehieu['cap'] = df_lehieu['y'].max() * 1.2
future_lehieu['floor'] = 0
future_lehieu['growth_rate'] = future_lehieu['ds'].apply(lambda x: 98 if x < pd.Timestamp('2020-01-01') else (129 if x < pd.Timestamp('2021-01-01') else (113 if x < pd.Timestamp('2022-01-01') else (118 if x < pd.Timestamp('2023-01-01') else (121 if x < pd.Timestamp ('2024-01-01') else 112)))))
#future_lehieu['DISCOUNT_RATE'] = future_lehieu['ds'].apply(lambda x: 1 if x < pd.Timestamp('2024-04-01') else 0.97)
forecast_lehieu = model_lehieu.predict(future_lehieu)
result_lehieu = forecast_lehieu[['ds', 'yhat']]

# khách trường nguyên
df_truongnguyen1 = df_sales_perc[11000597].rename(columns={'DATE': 'ds', 'SALES': 'y'})
df_truongnguyen = df_sales_perc[11000597].rename(columns={'DATE': 'ds', 'SALES': 'y'})
df_truongnguyen['cap'] = df_truongnguyen['y'].max() * 1.2
df_truongnguyen['floor'] = 0
df_truongnguyen['DISCOUNT_RATE'] = df_truongnguyen['ds'].apply(lambda x: 1 if x < pd.Timestamp('2024-04-01') else (0.97 if x < pd.Timestamp('2025-02-01') else 0.99))
model_truongnguyen = Prophet(growth='logistic', changepoint_range=0.9, yearly_seasonality=5,
            weekly_seasonality=False, daily_seasonality=False, holidays=holidays,
            seasonality_mode='multiplicative', seasonality_prior_scale=5,
            holidays_prior_scale=5, changepoint_prior_scale=0.1 ,interval_width=0.95)
model_truongnguyen.add_regressor('DISCOUNT_RATE',prior_scale=3, mode='additive')
model_truongnguyen.fit(df_truongnguyen)
#a = plot_yearly(model_truongnguyen)
future_truongnguyen = model_truongnguyen.make_future_dataframe(periods=12, freq='MS', include_history=True)
future_truongnguyen['cap'] = df_truongnguyen['y'].max() * 1.2
future_truongnguyen['floor'] = 0
future_truongnguyen['DISCOUNT_RATE'] = future_truongnguyen['ds'].apply(lambda x: 1 if x < pd.Timestamp('2024-04-01') else (0.97 if x < pd.Timestamp('2025-02-01') else 0.99))
forecast_truongnguyen = model_truongnguyen.predict(future_truongnguyen)
result_truongnguyen = forecast_truongnguyen[['ds', 'yhat']]

# khách thanh danh
df_thanhdanh1 = df_sales_perc[11000618].rename(columns={'DATE': 'ds', 'SALES': 'y'})
df_thanhdanh = df_sales_perc[11000618].rename(columns={'DATE': 'ds', 'SALES': 'y'})
df_thanhdanh['cap'] = df_thanhdanh['y'].max() * 1.2
df_thanhdanh['floor'] = 0
#df_thanhdanh["growth_rate"] = df_thanhdanh['ds'].apply(lambda x: 0 if x < pd.Timestamp('2021-01-01') else (0.1 if x < pd.Timestamp('2022-01-01') else (1.16 if x < pd.Timestamp('2023-01-01') else (0.24 if x < pd.Timestamp('2024-01-01') else (0.22 if x < pd.Timestamp ('2025-01-01') else 0.1)))))
#df_thanhdanh['DISCOUNT_RATE'] = df_thanhdanh['ds'].apply(lambda x: 1 if x < pd.Timestamp('2024-04-01') else (0.97 if x < pd.Timestamp('2025-02-01') else 0.99))
model_thanhdanh = Prophet(growth='logistic', changepoint_range=0.9, yearly_seasonality=6,
            weekly_seasonality=False, daily_seasonality=False, holidays=holidays,
            seasonality_mode='multiplicative', seasonality_prior_scale=5,
            holidays_prior_scale=5, changepoint_prior_scale=0.1 ,interval_width=0.95)
#model_thanhdanh.add_regressor('growth_rate', mode='additive')
#model_thanhdanh.add_regressor('DISCOUNT_RATE',prior_scale=0.5, mode='additive')
model_thanhdanh.fit(df_thanhdanh)
#a = plot_yearly(model_thanhdanh)
future_thanhdanh = model_thanhdanh.make_future_dataframe(periods=12, freq='MS', include_history=True)
future_thanhdanh['cap'] = df_thanhdanh['y'].max() * 1.2
future_thanhdanh['floor'] = 0
#future_thanhdanh["growth_rate"] = future_thanhdanh['ds'].apply(lambda x: 0 if x < pd.Timestamp('2021-01-01') else (0.1 if x < pd.Timestamp('2022-01-01') else (1.16 if x < pd.Timestamp('2023-01-01') else (0.24 if x < pd.Timestamp('2024-01-01') else (0.22 if x < pd.Timestamp ('2025-01-01') else 0.1)))))
#future_thanhdanh['DISCOUNT_RATE'] = future_thanhdanh['ds'].apply(lambda x: 1 if x < pd.Timestamp('2024-04-01') else (0.97 if x < pd.Timestamp('2025-02-01') else 0.99))
forecast_thanhdanh = model_thanhdanh.predict(future_thanhdanh)
result_thanhdanh = forecast_thanhdanh[['ds', 'yhat']]

# khách đông hàn
df_donghan1 = df_sales_perc[11000633].rename(columns={'DATE': 'ds', 'SALES': 'y'})
df_donghan = df_sales_perc[11000633].rename(columns={'DATE': 'ds', 'SALES': 'y'})
df_donghan['cap'] = df_donghan['y'].max() * 1.3
df_donghan['floor'] = 0
df_donghan['growth_rate'] = df_donghan['ds'].apply(lambda x: 7 if x < pd.Timestamp('2020-01-01') else (5 if x < pd.Timestamp('2021-01-01') else (6 if x < pd.Timestamp('2022-01-01') else (13 if x < pd.Timestamp('2023-01-01') else (21 if x < pd.Timestamp ('2024-01-01') else 50)))))
df_donghan['year'] = df_donghan['ds'].dt.year
df_donghan['quarter'] = df_donghan['ds'].dt.quarter
df_donghan['quarter_seasonality'] = df_donghan['quarter'].apply(lambda x: -1 if x in [1,2] else 1)
#df_donghan['DISCOUNT_RATE'] = df_donghan['ds'].apply(lambda x: 1 if x < pd.Timestamp('2024-04-01') else 0.97)
model_donghan = Prophet(growth='logistic', changepoint_range=0.9, yearly_seasonality=5,
            weekly_seasonality=False, daily_seasonality=False, holidays=holidays,
            seasonality_mode='multiplicative', seasonality_prior_scale=6,
            holidays_prior_scale=6, changepoint_prior_scale=0.001 ,interval_width=0.95)
model_donghan.add_regressor('growth_rate', mode='additive')
#model_donghan.add_regressor('quarter_seasonality',mode = 'additive')
#model_donghan.add_regressor('DISCOUNT_RATE',prior_scale=3, mode='additive')
model_donghan.fit(df_donghan)
#a = plot_yearly(model_donghan)
future_donghan = model_donghan.make_future_dataframe(periods=12, freq='MS', include_history=True)
future_donghan['cap'] = df_donghan['y'].max() * 1.3
future_donghan['floor'] = 0
future_donghan['growth_rate'] = future_donghan['ds'].apply(lambda x: 7 if x < pd.Timestamp('2020-01-01') else (5 if x < pd.Timestamp('2021-01-01') else (6 if x < pd.Timestamp('2022-01-01') else (13 if x < pd.Timestamp('2023-01-01') else (21 if x < pd.Timestamp ('2024-01-01') else 50)))))
future_donghan['year'] = future_donghan['ds'].dt.year
future_donghan['quarter'] = future_donghan['ds'].dt.quarter
future_donghan['quarter_seasonality'] = future_donghan.apply(
  lambda row: -1.2 if row['year'] == 2024 and row['quarter'] == 1 else
              -1 if row['year'] == 2024 and row['quarter'] == 2 else
               1 if row['year'] == 2024 and row['quarter'] == 3 else
               1.2 if row['year'] == 2024 and row['quarter'] == 4 else
               -1 if row['quarter'] in [1,2] else
               1,
  axis = 1
)
#future_donghan['DISCOUNT_RATE'] = future_donghan['ds'].apply(lambda x: 1 if x < pd.Timestamp('2024-04-01') else 0.97)
forecast_donghan = model_donghan.predict(future_donghan)
result_donghan = forecast_donghan[['ds', 'yhat']]
result_donghan.loc[result_donghan['ds'] == '2024-01-01', 'yhat'] -= 1000000000
result_donghan.loc[result_donghan['ds'] == '2024-02-01', 'yhat'] -= 1000000000
result_donghan.loc[result_donghan['ds'] == '2024-03-01', 'yhat'] -= 1000000000
result_donghan.loc[result_donghan['ds'] == '2024-10-01', 'yhat'] += 1000000000
result_donghan.loc[result_donghan['ds'] == '2024-11-01', 'yhat'] += 1000000000
result_donghan.loc[result_donghan['ds'] == '2024-12-01', 'yhat'] += 1000000000

# khách tín phát
df_tinphat1 = df_sales_perc[11001044].rename(columns={'DATE': 'ds', 'SALES': 'y'})
df_tinphat = df_sales_perc[11001044].rename(columns={'DATE': 'ds', 'SALES': 'y'})
df_tinphat['cap'] = df_tinphat['y'].max() * 1.2
df_tinphat['floor'] = 0
#df_tinphat['growth_rate'] = df_tinphat['ds'].apply(lambda x: 0 if x < pd.Timestamp('2021-01-01') else (0.1 if x < pd.Timestamp('2022-01-01')else (1.16 if x < pd.Timestamp('2023-01-01') else (0.24 if x < pd.Timestamp('2024-01-01') else (0.22 if x < pd.Timestamp ('2025-01-01') else 0.1)))))
#df_tinphat['DISCOUNT_RATE'] = df_tinphat['ds'].apply(lambda x: 1 if x < pd.Timestamp('2024-04-01') else (0.97 if x < pd.Timestamp('2025-02-01') else 0.99))
model_tinphat = Prophet(growth='logistic', changepoint_range=0.9, yearly_seasonality=6,
            weekly_seasonality=False, daily_seasonality=False, holidays=holidays,
            seasonality_mode='multiplicative', seasonality_prior_scale=5,
            holidays_prior_scale=5, changepoint_prior_scale=0.1 ,interval_width=0.95)
#model_tinphat.add_regressor('growth_rate', mode='additive')
#model_tinphat.add_regressor('DISCOUNT_RATE',prior_scale=3, mode='additive')
model_tinphat.fit(df_tinphat)
#a = plot_yearly(model_tinphat)
future_tinphat = model_tinphat.make_future_dataframe(periods=12, freq='MS', include_history=True)
future_tinphat['cap'] = df_tinphat['y'].max() * 1.2
future_tinphat['floor'] = 0
#future_tinphat['growth_rate'] = future_tinphat['ds'].apply(lambda x: 0 if x < pd.Timestamp('2021-01-01') else (0.1 if x < pd.Timestamp('2022-01-01') else (1.16 if x < pd.Timestamp('2023-01-01') else (0.24 if x < pd.Timestamp('2024-01-01') else (0.22 if x < pd.Timestamp ('2025-01-01') else 0.1)))))
#future_tinphat['DISCOUNT_RATE'] = future_tinphat['ds'].apply(lambda x: 1 if x < pd.Timestamp('2024-04-01') else (0.97 if x < pd.Timestamp('2025-02-01') else 0.99))
forecast_tinphat = model_tinphat.predict(future_tinphat)
result_tinphat = forecast_tinphat[['ds', 'yhat']]

listname_kh = ['truongphat', 'phuha', 'dungyen', 'anphat', 'giabao', 'ngocdung', 'xuanthuong', 'lehieu', 'toanloc', 'caogiaphat',
               'huyhung', 'givina', 'haiduongnghean', 'hienchau', 'tienthanh', 'truongnguyen', 'thanhdanh', 'donghan', 'tinphat']
all_results2 = []
for id in listname_kh:
    df_name = f'df_{id}1'
    result_name = f'result_{id}'
    if df_name in globals() and result_name in globals():
        df_id1 = globals()[df_name]
        result_id = globals()[result_name]
        excel_id = pd.merge(df_id1, result_id, on='ds', how='outer').rename(columns={'ds': 'DATE', 'y': 'SALES', 'yhat': 'SALES_PREDICTION'})
        excel_id['DIFFERENT'] = excel_id['SALES'] / excel_id['SALES_PREDICTION']
        excel_id['80%_TARGET'] = excel_id['SALES_PREDICTION'] * 0.8
        excel_id['120%_TARGET'] = excel_id['SALES_PREDICTION'] * 1.1
        all_results2.append(excel_id)

#final_df1 = pd.concat(all_results1, ignore_index=True)
#final_df1 = pd.concat(all_results1, ignore_index=True)
final_df = pd.concat(all_results2, ignore_index=True)
#final_df = pd.concat([final_df1, final_df2], ignore_index=True)
#final_df = pd.concat([final_df1, final_df2], ignore_index=True)
final_df['CUSTOMER_NAME'].fillna(method='ffill', inplace=True)
final_df['CUSTOMER_ID'].fillna(method='ffill', inplace=True)
path_save = 'C:\\Users\\M3514278\\OneDrive - Saint-Gobain\\Mạnh\\Code\\Result\\SALES_PREDICTION.xlsx'
final_df.to_excel(path_save, index=False)'''
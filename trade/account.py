def status():
  status_code = client.get_system_status()['status']
  if(status_code!=0):
     print("Exiting")
     sys.exit(1)

def permissions():
  return client.get_account_api_permissions()


def my_trades():
  df = pd.DataFrame(client.futures_account_trades())
  df['time'] = to_date(df['time'])
  return df



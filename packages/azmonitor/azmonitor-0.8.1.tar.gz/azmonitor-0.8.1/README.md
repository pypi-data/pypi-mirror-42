It is a helper tool for Azure Monitor. It is not official.
Recently it is used the term Azure Monitor logs instead of Log Analytics. Log data is still stored in a Log Analytics workspace and is still collected and analyzed by the same Log Analytics service.
https://docs.microsoft.com/en-us/azure/azure-monitor/

Install
```sh
pip install azmonitor
```

Example
```python
import azmonitor

log_type = 'AzMonitor'
customer_id = 'xxxxx-xxxx-xxxx-xxxx-xxxxx'
shared_key = 'xxxxxxxxxxxxxxxxxxxxxxxxxx'

applog = azmonitor.LogAnalytics(log_type, customer_id, shared_key)

# Single Data
data = {'status': 'starting', 'value': 50}
applog.log(data)

# Multi Data
list_data = []
for i in range(3):
    list_data.append({'status': 'starting', 'value': i})
applog.logs(list_data)
```

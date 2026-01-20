Approach 

## **Step first**
**Data Cleaning And Preprocessing**

#### **Data integrity and quality**
* Data size : 1,006,029 rows
* exact duplicates detected: 23,030 rows( ~ 2.2%)
* final cleaned dataset : 982,999 rows
* duplicates removed to avoid overestimation in aggregated results 

## **Data Cleaning and Processing**
### removed invalid / Junk records 
1) **Removed missing values** from critical identifiers:
<code>date</code>, <code>State</code>, <code>district</code>,<code>pincode</code>

reason:
Rows missing these fields cannot be reliably aggregated or analyzed geographically or temporally

2) **Validated and filtered pincodes**
* kept only pincodes in range 100_000 - 999_999

reason: Ensures the data represents valid Indian postal codes and prevents location-level analysis errors

3) **Created a unified total enviroment metric**
* Added a new column <code>enrol_total</code>:
enrol_total=age_0_5+age_5_17+age_18_greater

Reason: Enables consistent trend analysis, hotspot detection, anomaly detection, and forecasting using a single KPI.
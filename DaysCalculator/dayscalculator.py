from datetime import date,datetime


def date_fin(d):
    input_date = d
    format = "%Y-%m-%d"
    str2date=datetime.strptime(input_date,format)
    fin_date=str2date.date()
    return fin_date



def res_days(date1 , date2):
    diff = date1 - date2
    return(diff.days)

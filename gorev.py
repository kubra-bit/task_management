from pymongo  import MongoClient
from prettytable import PrettyTable
from datetime import datetime
from bson.objectid import ObjectId

client=MongoClient("mongodb://localhost:27017")
db=client["tasks_management"]
tasks=db["tasks"]

def add_task(title,description,due_date):
    result=tasks.insert_one({"title":title,"description":description,"due_date":due_date,"created_at":datetime.now(),"status":"pending"})
    print(f"yeni gorev eklendi ID: {result.inserted_id}")
def list_tasks():
    print("tüm görevler")
    table=PrettyTable(["ID","BASLİK","ACİKLAMA","SON TARİH","DURUM"])
    for task in tasks.find():
        table.add_row([str(task["_id"]),str(task["title"]),str(task["description"]),str(task["due_date"]),str(task["status"])])
    print(table)
def update_task(task_id,degisen,value):
    tasks.update_one({"_id":ObjectId(task_id)},{"$set":{degisen:value}})
    print(f"{degisen}  ,{value} ile guncellendi" )

def delete_task(task_id):
    tasks.delete_one({"_id":ObjectId(task_id)})
    print(f"{task_id}'li gorev silindi")
def  list_tasks_by(tarih,durum):
    if durum=="before":
        for task in tasks.find({"due_date":{"$lt":tarih}}):
            print(task["title"],task["description"])
    elif durum=="after":
        for task in tasks.find({"due_date":{"$gt":tarih}}):
            print(task["title"], task["description"])

icerik="""
--------GOREV YONETIM SISTEMI--------
 1. GOREV EKLE
2. GOREV LİSTELE
3. GOREV GUNCELLE
4. GOREV SİL
5. TARİHE GORE GOREV LİSTELE
6. CİKİS
"""
def main():
    while True:
        print(icerik)
        choice=int(input("seceginizi giriniz:"))
        if choice==1:
            title=input("görevi giriniz:")
            description=input("açiklamayi giriniz:")
            due_date=input("tarihi giriniz (YYYY-MM-DD)")
            add_task(title,description,due_date)
        elif choice==2:
            list_tasks()
        elif choice==3:
            task_id=input("guncellenecek gorevin IDsini giriniz:")
            degisen=input("degistirmek istediginizi giriniz (title,description,due_date,status)")
            value=input(f"yeni {degisen} i giriniz:")
            update_task(task_id,degisen,value)
        elif choice==4:
            task_id=input("silinecek gorevin idisini giriniz :")
            delete_task(task_id)
        elif choice==5:
            tarih=input("incelediginiz tarihi giriniz (YYYY-MM-DD)")
            durum=input("before or after")
            list_tasks_by(tarih,durum)
        elif choice==6:
            break
        else:
            print("yanlis deger girdiniz")

if __name__=="__main__":
    main()



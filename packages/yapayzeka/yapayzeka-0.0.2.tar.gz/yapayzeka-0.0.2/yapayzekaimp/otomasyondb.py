from pymongo import MongoClient
from pymongo.collection import Collection


# import pickle
class Veritabani():
    def __init__(self):
        client = MongoClient("mongodb://localhost:27017/")
        self.db = client["Veritabanı0"]
        super(Veritabani, self).__init__()

    @staticmethod
    def veritabani():
        client = MongoClient("mongodb://localhost:27017/")
        db = client["Veritabanı0"]
        return db

    def kullaniciEkle(self, *arg1):

        for i, j in arg1:
            self.db.create_collection(i)
            self.db.Kullanıcılar.insert_one({"kullanıcı_adı": i, "şifre": j})

    def kontrolEt(self, *args):
        for i, j in args:
            sorgu = {"kullanıcı_adı": i, "şifre": j}
            sdb = self.db.Kullanıcılar.find_one(sorgu)
            return sdb

    def ekle(self, *args):

        for i, j in args:
            coll = self.db.get_collection(i)

            return coll.insert({"girdiler": j})

    def getir(self, *args):
        try:
            list2 = []
            list3 = []
            list4 = []
            for i in args:
                coll = self.db.get_collection(i)
                listw = coll.find({})
                for i in listw:
                    z = i["_id"]
                    y = i["girdiler"]
                    list2.append(y)
                    list3.append(z)
                    list4.append(i)

            yield list2, list3, list4
        except(GeneratorExit):
            print("generator exit")

    def sayfa_ekle(self, *args):
        for i, j in args:
            self.db.sayfalar.insert_one({"sayfa_adı": i, "sayfa_gövdesi": j})

    def sayfa_getir(self, args):
        orn = Veritabani()
        sayfacoll = orn.veritabani()
        if isinstance(args, str):
            sorgu = sayfacoll.get_collection("sayfalar").find_one({"sayfa_adı": args})
            return sorgu
        elif isinstance(args, tuple) and len(args) == 2:
            sorgu = sayfacoll.get_collection("sayfalar").find_one({args[0]: args[1]})
            return sorgu
        else:
            print("geçerli bir argüman giriniz")


if __name__ == "__main__":
    orn = Veritabani()

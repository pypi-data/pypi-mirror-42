import os
import time
import timeit
import sys
import joblib
import numpy as np
import pandas as pd
# from matplotlib.colors import ListedColormap
# from sklearn.discriminant_analysis import QuadraticDiscriminantAnalysis
# from scipy.sparse import csr_matrix,csc_matrix
# from sklearn.linear_model import LassoLars
# from sklearn.neighbors import RadiusNeighborsClassifier
# from sklearn.neighbors import KNeighborsClassifier
from TurkishStemmer import TurkishStemmer as tust
# from sklearn import preprocessing
# from sklearn.multiclass import OneVsRestClassifier
# from sklearn.multiclass import OneVsOneClassifier
from joblib import Parallel, delayed
# from sklearn.linear_model import SGDClassifier
# from sklearn.feature_selection import f_classif
from sklearn import svm
from sklearn.feature_extraction.text import HashingVectorizer
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline

from yapayzekainterface.otomasyondb import Veritabani

# from joblib import dump, load
# from sklearn.naive_bayes import GaussianNB
# from sklearn.neural_network import MLPClassifier
# from sklearn.preprocessing import FunctionTransformer
# from mlxtend.preprocessing import DenseTransformer
# from sklearn import tree
class Yapayzeka():

    def veritabanigetir(self):
        DATABASE = Veritabani().db["sayfalars"]
        # DATABASE.create_index([("target","text")])
        # coll=DATABASE.aggregate([{"$group":{"_id":"$target"}}])
        # for i in coll:
        #     print(i)

        yasam = DATABASE.find({"$and": [
            {"target": {"$nin": ["turkiye", "dunya", "gundem","magazin","spor","cevre","medya","egitim", "ekonomi",
                                "bilim-teknoloji",
                                "kultur-sanat",
                                "saglik"]}},
            {"data": {"$gt": []}},
            {"target": {"$in": ["yasam"],
                        }},

        ]}, {"_id": 0, "url": 0})
        ekonomi = DATABASE.find({"$and": [
            {"target": {"$nin": ["turkiye", "dunya", "gundem", "magazin", "spor", "cevre", "medya", "egitim","bilim-teknoloji",
                                "kultur-sanat",
                                "saglik","yasam",]}},
            {"data": {"$gt": []}},
            {"target": {"$in": [ "ekonomi",
                                ],
                        }},

        ]}, {"_id": 0, "url": 0})
        bilim = DATABASE.find({"$and": [
            {"target": {"$nin": ["turkiye", "dunya", "gundem", "magazin", "spor", "cevre", "medya", "egitim","kultur-sanat",
                                "saglik","yasam", "ekonomi",]}},
            {"data": {"$gt": []}},
            {"target": {"$in": [
                                "bilim-teknoloji",
                                ],
                        }},

        ]}, {"_id": 0, "url": 0})
        kultur = DATABASE.find({"$and": [
            {"target": {"$nin": ["turkiye", "dunya", "gundem", "magazin", "spor", "cevre", "medya", "egitim","saglik","yasam", "ekonomi",
                                "bilim-teknoloji",]}},
            {"data": {"$gt": []}},
            {"target": {"$in": [
                                "kultur-sanat",
                                ],
                        }},

        ]}, {"_id": 0, "url": 0})
        saglik = DATABASE.find({"$and": [
            {"target": {"$nin": ["turkiye", "dunya", "gundem", "magazin", "spor", "cevre", "medya", "egitim","yasam", "ekonomi",
                                "bilim-teknoloji",
                                "kultur-sanat",]}},
            {"data": {"$gt": []}},
            {"target": {"$in": [
                                "saglik"],
                        }},

        ]}, {"_id": 0, "url": 0})



        # print(type(coll),coll.count())
        # coll = DATABASE.find({"target":{"$nin":["turkiye","dunya","gundem"]}}, {"_id": 0, "url": 0})

        return yasam,kultur,bilim,ekonomi,saglik

    def split_model(self):
        # df = pd.DataFrame(list(self.veritabanigetir()))
        # print(df)
        lf=list()
        yasam,_,_,_,_=self.veritabanigetir()
        _,kultur,_,_,_=self.veritabanigetir()
        _,_,bilim,_,_=self.veritabanigetir()
        _,_,_,ekonomi,_=self.veritabanigetir()
        _,_,_,_,saglik=self.veritabanigetir()
        lf.extend(yasam)
        lf.extend(kultur)
        lf.extend(bilim)
        lf.extend(ekonomi)
        lf.extend(saglik)
        df = pd.DataFrame(lf)
        print(df)
        data = df['data'] = [" ".join(data) for data in df['data'].values]
        df["target"] = [" ".join(target) for target in df['target'].values]
        target = np.array(df["target"])
        X_train,X_test, y_train, y_test = train_test_split(data, target, test_size=0.21, random_state=46)



        return X_train, X_test, y_train, y_test

    def plot_model(self):
        pass

    def save_model(self):
        X_train1, X_test, y_train, y_test = self.split_model()
        stemmed = []
        ps = tust()
        for i in X_train1:
            stem = ps.stem(i)
            stemmed.append(stem)
        X_train = stemmed
        pipeline = Pipeline(steps=[
            # ("Count",CountVectorizer()),
            ('tfidf', HashingVectorizer()),
            ('clf', svm.LinearSVC(verbose=3,),)])


        predicted = pipeline.fit(X_train, y_train)
        pcdump = joblib.dump(predicted, "svchash3.pkl")
        return pcdump

    def start_model(self):
        Parallel(n_jobs=3, verbose=1)(delayed(self.test_model()))

    def predict_from_model(self, args):
        docs_new3 = []
        docs_new3.append(args)
        docs_new = ['beslenme c vitamininin önemi', 'tarım ve köy işleri başkanlığı altın faiz',
                    "Münbiç şehir merkezinde bugün (16 Ocak) vuku bulan bombalı saldırıda ABD askeri personeli ve sivil can kaybı meydana geldiği üzüntüyle öğrenilmiştir. Bu menfur terör eylemini şiddetle kınıyoruz. ",
                    "Hazine ve Maliye Bakanı Berat Albayrak'ın imzasıyla yayımlanan genelge ile kamu idarelerinin kiraladığı taşınmazlarının kira artış oranlarının belirlenmesinde ve yeni yapacağı taşınmaz kiralamalarında uyacağı esaslar yer aldı. Genelgeye göre; kamu idarelerinin kiraladığı taşınmazların kira artışları, artışın yapılacağı ayda yayımlanan Tüketici Fiyatları Endeksi'nin(TÜFE) 12 aylık ortalamasına göre yüzde değişim oranını geçmeyecek şekilde yapılacak. Söz konusu yüzde değişim oranının negatif çıkması halinde kira bedelinde bir değişiklik yapılmayacak ",
                    "kanser hastlarında yeni laç üretimi ", "sabit transfer yörüngesine gitmek", "spacex",
                    "recep tayyip erdoğan", "orkun uçar", "ibm", "necip fazıl kısakürek kitapları",
                    "diyet kitapları ve faizle ilgili elifle konuşuyordum", "faiz",
                    "domates fiyatları son on yılın en yüksek rakamını gördü",
                    "kış aylarında gribe yakalanma olasılığı artıyor",
                    "irtifa ayarları,ve bilgisayar",
                    "Antalya Valisi Münir Karaloğlu, 2019 yılında turizmde yeni rekorların yaşanacağı bir yıl olmasını beklediklerini belirterek, Antalya  turizminin inşallah bu yıl yüzde 20-25 bandında büyüyeceğini varsayıyoruz. ded",
                    "Çevre Koruma Kanunu kapsamında bazı işletmelerde poşet kullanımının ücretlendirilmesinin ardından poşet beyannamesi süreci başladı. Peki, poşet beyannamesi için 15 Şubat olarak belirlenen süre uzatıldı mı? İşte, poşet beyannamesi hakkında merak edilen bazı bilgiler",
                    "Sanayi sektöründe ciro %17 arttıTakvim etkilerinden arındırılmış sanayi ciro endeksi, 2018 yılı Aralık ayında bir önceki yılın aynı ayına göre %17 arttı. Mevsim ve takvim etkilerinden arındırılmış sanayi ciro endeksi ise bir önceki aya göre %1 azaldı.İnşaat sektöründe ciro %3 arttıTakvim etkilerinden arındırılmış inşaat ciro endeksi, 2018 yılı Aralık ayında bir önceki yılın aynı ayına göre %3 arttı. Mevsim ve takvim etkilerinden arındırılmış inşaat ciro endeksi ise bir önceki aya göre %0,9 azaldı.Ticaret sektöründe ciro %8 arttıTakvim etkilerinden arındırılmış ticaret ciro endeksi, 2018 yılı Aralık ayında bir önceki yılın aynı ayına göre %8 arttı. Mevsim ve takvim etkilerinden arındırılmış ticaret ciro endeksi ise bir önceki aya göre %1,5 azaldı.",
                    "Antik bulgulara göre, Harran'ın, tarih boyunca önemli bir tıp merkezi olarak kabul edildiğine dikkati çeken Önal, geçen yıl bin yıllık miskçi dükkanı bulunan bölgede, bu yıl da tıp bilimini ilgilendiren çok önemli bir bulguya rastladıklarını kaydetti. Önal, kazılarda Orta Çağ döneminden kalma 9 asırlık bir ilaç şişesi çıkarıldığını ifade ederek, Şişenin bulunduğu tabaka, milattan sonra 12. yüzyıla aittir. O da Zengiler dönemine rast geliyor. Bu eser, günümüzden yaklaşık 9 asır öncesine dayanıyor. Dolayısıyla burada ilaç üretildiği ve bu şişelere konularak oradan satıldığı sonucuna ulaştık. Hem imalathanesi hem de satış yeri olması açısından oldukça önemlidir. diye konuştu",
                    "domates fiyatları",
                    " Bir dizi ziyaret için Düzce'ye gelen Enerji ve Tabii Kaynaklar Bakanı Fatih Dönmez, Vali Zülkif Dağlı ile görüştü. Daha sonra Belediye Başkanı Dursun Ay'ı ziyaret eden Dönmez, çıkışta gazetecilere yaptığı açıklamada, Bakanlık bünyesinde geliştirdikleri borlu gübre için mart ayında pilot üretime geçeceklerini söyledi. Eti Maden'deki Ar-Ge biriminde çalışan mühendislerin uzunca bir süredir borlu gübre üzerinde çalışma yaptığını aktaran Dönmez, şöyle devam etti:O çalışmaların artık netice alma aşamasına geldik. Zaten Cumhurbaşkanlığımızın ikinci 100 günlük programında hedeflerimiz arasında yer almaktaydı. İnşallah mart ayı içerisinde belki ilk pilot üretimleri gerçekleştirmiş olacağız. Bu, toprağın yapısına göre, ürünün çeşidine göre ve yağış alma durumuna göre değişecek şekilde 3 farklı borlu gübre geliştirmiş olduk. Eti Maden, Sabancı Üniversitesi iş birliğiyle bunu yaptık. Sadece Türkiye'de değil, yurt dışında da ciddi bir pazar potansiyelimiz var. Bildiğiniz gibi biz borda dünyadaki rezervlerin yaklaşık yüzde 73'üne sahibiz. Dünyadaki bor satış pazarının da yüzde 59'u bizde",
                    " Ozan Arif, Giresun'un Alucra ilçesine bağlı şimdiki ismi ile Yükselen eski adı ile Hapu köyünde 1949'da doğdu.Babasının memuriyeti dolayısıyla, ilk ve ortaokulu Samsun`da bitirdi. 1970'de başladığı öğretmenlik mesleğinde Samsun'un Devgeriş köyünde beş yıl öğretmenlik, dört yıl ise okul müdürlüğü görevi olmak üzere üzere dokuz yıl hizmet verdi. 24 Eylül 1980 ve 5 Kasım 1991 tarihleri arasında Almanya'da yaşadı.Güzel sanatlara yeteneği, şiire ilgisi ve özellikle şairliğe olan kabiliyetinden dolayı okul çağlarında şiir ve resim dallarında birincilikler ve ödüller almaya başlayan Ozan Arif`in başarıları hayatının ileriki yıllarında yöresel sınırları aşıp Türkiye genelinde de devam etti.Birçok şiir ve Halk Edebiyatı yarışmalarında üstün başarı gösteren Ozan Arif`in Türk Halk Edebiyatı`nın şiir, atışma, muamma, irticalen şiir söyleme, lebdeğmez (dudakdeğmez), güzelleme ve diğer dallarında çeşitli tarihlerde aldığı Türkiye birincilikleri, sertifikalar ve ödüller vardır.",
                     ]
        docs_new2 = ["beslenme c vitamininin önemir", ]

        path = os.getcwd()
        files = os.listdir(path)
        model = "svchash3.pkl"
        if len(docs_new3)!=0:
            if model in files:


                timestart = timeit.default_timer()
                loaded_model = joblib.load(model)
                # predicted3 = loaded_model.predict(docs_new)
                #
                # for i in enumerate(zip(predicted3, docs_new), 1):
                #     print("tahmin   ", i)
                # timeend = time.time()
                # print("Toplam öğrenme süresi:  ", timeit.default_timer() - timestart, " saniye.")
                # ttf=zip(predicted3,docs_new)
                # ttf2=pd.DataFrame(ttf)
                # print(ttf2)
                # return ttf2

                predicted3 = loaded_model.predict(list(docs_new3))
                tff = pd.DataFrame(predicted3)
                print(tff)
                return tff
            else:
                print("{0} öğrenim modeli bilinmiyor.eğitim başlatıldı...".format(model))
                timestart = timeit.default_timer()
                saved_model = self.save_model()
                loaded_model = joblib.load(model)
                predicted2 = loaded_model.predict(docs_new)

                for i in enumerate(zip(predicted2, docs_new), 1):
                    print("tahmin:  ", i)
                timeend = time.time()
                print("geçen süre:  ", timeit.default_timer() - timestart, "  saniye.")
        else:
            print("işlenecek veri bulunamadı.")

    def test_model(self):

        X_train, X_test, y_train, y_test = self.split_model()
        # y_test = self.split_model()[3]

        path = os.getcwd()
        files = os.listdir(path)
        model = "svchash3.pkl"
        if model in files:
            timestart = timeit.default_timer()
            loaded_model = joblib.load(model)
            predicted2 = loaded_model.predict(X_test)
            for i in enumerate(zip(predicted2[-40:], X_test[-40:]), 1):
                print("tahmin:  ", i)
            timeend = time.time()
            print("Tahmin skoru :         %", 100 * accuracy_score(y_test, predicted2),
                  "  doğruluk oranına ulaşılmıştır...")
            print("Toplam öğrenme süresi:  ", timeit.default_timer() - timestart, " saniye.")
        else:
            print("{0} öğrenim modeli bilinmiyor.eğitim başlatıldı...".format(model))
            timestart = timeit.default_timer()
            saved_model = self.save_model()
            loaded_model = joblib.load(model)
            predicted2 = loaded_model.predict(X_test)

            for i in enumerate(zip(predicted2[-20:], X_test[-20:]), 1):
                print("tahmin:  ", i)
            timeend = time.time()
            print("Tahmin skoru : %", 100 * accuracy_score(y_test, predicted2), " doğruluk oranına ulaşılmıştır.")
            print("geçen süre:  ", timeit.default_timer() - timestart,"  saniye.")
        # plt.xlabel('tahminler')
        # plt.ylabel('etiketler')
        # plt.title('Tahmin ortalaması')
        # plt.text(60, .025, r'$\mu=100,\ \sigma=15$')
        # plt.grid(True)
        # plt.plot(np.arange(0, 16), predicted2)
        # plt.show()
        # [1's a g l i k' 2'e k o n o m i' 3'b i l i m - 4t e k n o l o j i'
        #  5'e k o n o m i' 6's a g l i k' 7'b i l i m - t e k n o l o j i'
        #  8'b i l i m - t e k n o l o j i' 9'e k o n o m i' 10'y a s a m'
        #  11'b i l i m - t e k n o l o j i' 12'k u l t u r - s a n a t' 13's a g l i k'
        #  14'e k o n o m i']
        # [1'y a s a m' 2'e k o n o m i' 3'b i l i m - t e k n o l o j i'
        #  4'e k o n o m i' 5's a g l i k' 6'b i l i m - t e k n o l o j i'
        #  7'b i l i m - t e k n o l o j i' 8'e k o n o m i' 9'y a s a m' 10'y a s a m'
        #  11'y a s a m' 12'y a s a m' 13'e k o n o m i']


if __name__ == "__main__":
    orn = Yapayzeka()
    docs_new2 = ["beslenme c vitamininin önemir", ]

    orn.predict_from_model(*docs_new2)


# __version__ = '0.1'
from kivy.app import App
from kivy.graphics import Mesh, Color
from kivy.graphics.tesselator import Tesselator, WINDING_ODD, TYPE_POLYGONS
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.logger import Logger
from kivy.uix.textinput import TextInput
from kivy.config import Config
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget
from kivy.core.window import Window
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from urllib.error import URLError, HTTPError
from kivy.network.urlrequest import UrlRequest
import tempfile
import asyncio
import pickle
import urllib
from bs4 import BeautifulSoup as bs
from kivy.core.clipboard import Clipboard
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.bubble import Bubble
from kivy.properties import ObjectProperty, StringProperty
from urllib.request import Request
from otomasyondb import Veritabani
from kivy.config import Config
import urllib
from kivy.lang.builder import Builder
import threading
import time
import pathlib
from kivy.app import App
from kivy.lang import Builder
from kivy.factory import Factory
from kivy.animation import Animation
from kivy.clock import Clock, mainthread
from kivy.uix.gridlayout import GridLayout

# Config.set('input', 'mouse', 'mouse,disable_multitouch')
Config.set('input', 'mouse', 'mouse,multitouch_on_demand')


class GirisEkrani(Screen):
    pass


class KullaniciEkle(Screen):
    def yazdır(self):
        vtb = Veritabani()
        if not self.ids.metin.text == "" and self.ids.sifre.text == "":
            self.kullanici = self.ids.metin.text
            self.sifre = self.ids.sifre.text
            vtb.kullaniciEkle((self.kullanici, self.sifre))
            self.sifre = []
            self.kullanici = []
        else:
            print("kullanıcı ismi ve parola gerekli")

    def on_leave(self):
        self.ids.sifre.text = ""
        self.ids.metin.text = ""


class GirisYap(Screen):
    prob = ObjectProperty()

    def kontrol(self):
        vtb = Veritabani()
        kullanici = self.ids.metin.text
        sifre = self.ids.sifre.text
        try:
            ne = vtb.kontrolEt((kullanici, sifre))
            kullanıcıvari = ne["kullanıcı_adı"]
            sifrevari = ne["şifre"]
            self.prob = kullanıcıvari

            if kullanıcıvari == kullanici and sifrevari == sifre:
                print("geçiş izni verildi")
                return True
            else:
                return False
        except:
            print("doğru şifre gir")


class Anasayfa(Screen):
    vtb = Veritabani()

    def getir(self):
        kullanici = self.manager.girisyap_screen.prob
        try:
            for i, j, y in self.vtb.getir((kullanici)):
                yield i, j, y
        except(GeneratorExit):
            print("generator exit")

    def listele(self, args):
        if args == 1:
            for i, j, y in self.getir():
                liste2 = '\n'.join(map(str, i))
                self.ids.verilistesi.text = liste2
        elif args == 2:
            for i, j, y in self.getir():
                liste2 = '\n'.join(map(str, j))
                self.ids.verilistesi.text = liste2
        elif args == 3:
            for i, j, y in self.getir():
                liste2 = '\n'.join(map(str, y))
                self.ids.verilistesi.text = liste2
        else:
            print("aralık dışı bilgi")

    def girdiEkle(self):
        kullanici = self.manager.girisyap_screen.prob
        girdi = self.ids.metind.text
        self.vtb.ekle((kullanici, girdi))

    def tusserbest(self, args):
        if args == "metind":
            self.ids.metind.text = ""
        elif args == "verilistesi":
            self.ids.verilistesi.text = ""
        else:
            print("geçersiz veri metni")


class WebSayfa(Screen):
    def __init__(self, **kwargs):
        super(WebSayfa, self).__init__(**kwargs)
        self.temp = ObjectProperty(None)

    def clipboardGetir(self):
        self.text4 = Clipboard.paste()
        return self.text4

    def sayfaKontrol(self):
        kopya = self.clipboardGetir()
        from django.core.validators import URLValidator
        from django.core.exceptions import ValidationError
        import os
        os.environ['http_proxy'] = ''
        val = URLValidator(schemes=['http', 'https', 'ftp', 'ftps'])
        try:
            val(kopya)
            self.text = kopya
            self.ids.url.text = self.text
            self.temp = str(self.ids.url.text)
            return str(self.ids.url.text)
        except ValidationError:
            self.text = "url gerekli"
            self.ids.url.text = self.text
            print("url gerekli")

    def tusserbest(self, instance):
        instance.cursor = (0, 0)
        instance.focus = True
        Clock.schedule_once(lambda dt: instance.select_all(), 0)

    # def sayfa_get_asenkron(self,*args):
    #     # arglist=list(args)
    #     # futures=[self.sayfa_asenkron(url) for url in arglist]
    #     # sayfa=asyncio.run_(asyncio.wait(futures))
    #     loop=asyncio.get_event_loop()
    #     sayfa=loop.run_until_complete(self.sayfa_asenkron(args[0]))
    #
    #     return sayfa
    def sayfa_asenkron(self, page):
        orn = SayfaGetir()
        sayfa = orn.read_page(page)
        return sayfa

    def sayfalama(self):
        orn = Veritabani()
        url = self.sayfaKontrol()
        self.sayfa_asenkron(str(url))
        yazdıralacak = orn.sayfa_getir(url)
        self.ids.sayfa.text = str(yazdıralacak)
        print(self.ids.sayfa.text)


class SayfaGetir:
    def get_page(self, *args):
        paths = args[0]
        try:
            req = Request(paths, headers={'User-Agent': 'Mozilla/5.0'})
            resp = urllib.request.urlopen(req)
            return resp
        except HTTPError as e:
            print('Sunucu isteği getiremiyor.')
            print('Hata Kodu: ', e.code)
            raise ValueError("HTTP HATASI")
        except URLError as e:
            print("Sunucuya ulaşılamıyor.")
            print('Sebep: ', e.reason)
            raise ValueError("URL HATASI")
        except Exception:
            print("Geçerli bir URL giriniz.")

    def read_check_page(self, page):
        try:

            sayfa = self.get_page(page)
            soup = bs(sayfa, "html.parser")
            if len(list(soup)) != 0:
                return True
            else:
                raise ValueError("sayfa yok")
        except Exception:
            print("urlyi doğrulayın")

    def read_page(self, page):
        sayfa = self.get_page(page)
        check = self.read_check_page(page)
        orn = Veritabani()
        try:
            if check == True:
                soup = bs(sayfa, "html.parser")
                soup2 = soup.prettify()
                orn.sayfa_ekle((page, soup2))
                return soup2
            else:
                raise ValueError("sayfa okunmadı")
        except Exception as e:
            print("urlyi kontrol edin.  ")

    # async def sayfaGetir(self,path):
    #     try:
    #
    #         req = Request(path, headers={'User-Agent': 'Mozilla/5.0'})
    #         web_byte = urllib.request.urlopen(req).read()
    #         print(web_byte)
    #         pickle.dump(web_byte,self.pix)
    #         return web_byte
    #     except ():
    #         self.ids.sayfa.text = "Sayfa çok büyük"
    #
    # def sayfalama(self):
    #     path = self.temp
    #     sa=urllib.parse.quote_plus(path)
    #     loop = asyncio.get_event_loop()
    #     loop.run_until_complete(self.sayfaGetir(sa))
    #     if self.sayfaKontrol() == True:
    #         self.sayfaGetir()
    #     print(path)
    #
    # def pickling(self):
    #     pixx = pickle.load(self.pix)
    #     web_byte=self.ids.sayfa.text
    #     soup = bs(web_byte, "lxml")
    #     self.ids.sayfa.text = str(soup)


class Screen_Management(ScreenManager):
    girisekrani_screen = ObjectProperty(None)
    kullaniciekle_screen = ObjectProperty(None)
    girisyap_screen = ObjectProperty(None)
    anasayfa_screen = ObjectProperty(None)
    websayfa_screen = ObjectProperty(None)


class MainApp(App):
    def __init__(self, **kwargs):
        super(MainApp, self).__init__(**kwargs)
        self.title = "Veritabanı Kayıtları"

    def build(self):
        self.sm = Screen_Management()
        return self.sm


if __name__ == '__main__':
    open = MainApp()
    open.run()

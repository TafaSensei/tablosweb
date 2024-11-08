import streamlit as st
import pandas as pd
import datetime
from datetime import date
import requests
from bs4 import BeautifulSoup
from requests_html import HTMLSession
import numpy as np
import json
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from streamlit_option_menu import option_menu
from PIL import Image

st.set_page_config(page_title=" 🎯 Stock Analytics", layout="wide")

gelir_DESC = """

        ---------------------------------------------------------------------
        
        *Gelir Tablosu; bir şirketin belirli bir dönemdeki (genellikle bir çeyrek veya bir yıl) mali performansının anlık görüntüsünü sağlayan  
        çok önemli bir mali tablodur. Bir şirketin finansal sağlığını, kârlılığını ve operasyonel verimliliğini değerlendirmek için çok önemlidir.  
        Finansal analiz, karar alma ve paydaşlarla iletişimde hayati bir rol oynar.*   

        ---------------------------------------------------------------------
        
        """

ceyrek_DESC = """

        ---------------------------------------------------------------------
        
        *Çeyreklik güncellemelerin sıklığı, yatırımcıların bir şirketteki gelişmelerden haberdar olmalarını, yönetim stratejilerini  
        değerlendirmelerini ve yatırım stratejilerini buna göre ayarlamalarını sağlayarak daha dinamik ve bilgili bir yatırım yaklaşımını  
        teşvik eder.*   

        ---------------------------------------------------------------------
        
        """

yillik_DESC = """

        ---------------------------------------------------------------------
        
        *Gelir tablolarının yıllık hale getirilmesi, bir şirketin tüm yıl boyunca gösterdiği mali performansın konsolide ve kapsamlı bir  
        görünümünü sağladığından yatırımcılar için önemlidir. Yatırımcılar, üç aylık veya ara dönem verilerini yıllık bazda tahmin ederek  
        şirketin uzun vadeli eğilimlerini daha iyi değerlendirebilir, potansiyel mevsimselliği belirleyebilir ve daha bilinçli yatırım kararları  
        verebilir.*   

        ---------------------------------------------------------------------
        
        """

bilanco_DESC = """

        ---------------------------------------------------------------------
        
        *Bilanço; bir şirketin finansal sağlığı, likiditesi ve uzun vadeli yaşayabilirliği hakkında kapsamlı bir görüş sağladığından yatırımcılar,  
        alacaklılar, yönetim ve analistler dahil olmak üzere paydaşlar için çok önemlidir. Finansal analiz ve karar verme için bir temel  
        görevi görür ve bir şirketin genel finansal durumuna ilişkin değerli bilgiler sunar.*   

        ---------------------------------------------------------------------
        
        """

varlik_DESC = """
        ---------------------------------------------------------------------                
        **Varlıklar:**  
        *Bir yıl içinde nakde dönüştürülmesi veya tüketilmesi beklenen varlıklardır. Yaygın dönen varlıklar nakit, alacak hesapları, envanter ve kısa vadeli yatırımları içerir.*
        
        """

dvarlik_DESC = """

        **Duran Varlıklar:**  
        *Daha uzun bir faydalı ömre sahip olan ve bir yıl içinde nakde dönüştürülmesi beklenmeyen kaynaklar. (Uzun vadeli varlıklar) Duran varlıklar maddi duran varlıkları, maddi olmayan duran varlıkları ve uzun vadeli yatırımları içermektedir.*   

        """

ozkynk_DESC = """

        **Özkaynaklar:**  
        *Bir şirketin yükümlülükleri düşüldükten sonra varlıklarında kalan pay. Özkaynaklar, bir şirketin genel finansal istikrarını ve hissedarlara getiri sağlama kabiliyetini değerlendirmeye yardımcı olduğu için yatırımcılar ve analistler için önemli bir ölçüttür.*   

        """

nborc_DESC = """

        **Net Borç:**  
        *Bir şirketin toplam borcu ile nakit ve nakit benzerleri arasındaki fark. Bir şirketin genel borçluluğu ve finansal yükümlülüklerini yerine getirme kabiliyeti hakkında fikir verir.*   

        """

fyatirim_DESC = """

        **Finansal Yatırımlar:**  
        *Sermaye kazancı, faiz, temettü veya kira geliri şeklinde bir getiri elde etme beklentisiyle edinilen varlıklar. Bu yatırımlar, her biri kendine has özelliklere ve risk-getiri profillerine sahip çeşitli şekillerde olabilir.*   

        """

nakitb_DESC = """

        **Nakit ve Nakit Benzerleri:**  
        *Hızla nakde dönüştürülebilen yüksek likiditeye sahip varlıklar. Buna eldeki nakit, banka mevduatları ve vadesi üç ay veya daha kısa olan kısa vadeli yatırımlar dahildir.*   

        ---------------------------------------------------------------------        
        """

kisavy_DESC = """

        ---------------------------------------------------------------------
        
        **Kısa Vadeli Yükümlülükler:**  
        *Vadesi bir yıl içinde dolacak olan ve ödenecek hesaplar, kısa vadeli borçlar ve tahakkuk eden giderler gibi kalemleri içeren yükümlülükler.*   

        """

uzunvy_DESC = """

        **Uzun Vadeli Yükümlülükler:**  
        *Gelecek yıl içinde vadesi gelmeyen uzun vadeli yükümlülükler. Örnekler arasında uzun vadeli borçlar, ertelenmiş vergi yükümlülükleri ve kira yükümlülükleri yer almaktadır.*   

        ---------------------------------------------------------------------
        
        """

aktifk_DESC = """

        ---------------------------------------------------------------------
        
        **Aktif Karlılık: (ROA)**  
        *Bir şirketin varlıklarından kazanç elde etmedeki verimliliğini ve karlılığını ölçer. Aktif Karlılık, bir şirketin net gelirinin belirli bir dönemdeki ortalama toplam varlıklarına bölünmesiyle hesaplanır.*   

        """

ozserk_DESC = """

        **Özsermaye Karlılığı: (ROE)**  
        *Bir şirketin karlılığını ve hissedarlarının özsermayesi için getiri üretmedeki verimliliğini ölçer. Özsermaye Karlılığı, bir şirketin kâr elde etmek için hissedar sermayesini ne kadar etkin kullandığını değerlendirmek için önemli bir ölçüttür.*   

        ---------------------------------------------------------------------
        
        """

cari_DESC = """

        ---------------------------------------------------------------------
        
        **Cari Oran:**  
        *Bir şirketin kısa vadeli yükümlülüklerini kısa vadeli varlıklarıyla karşılama kabiliyetini ölçen bir likidite oranıdır. Şirketin yakın gelecekte yükümlülüklerini yerine getirme kabiliyeti hakkında fikir verir.*   

        """

asit_DESC = """

        **Asit-test Oranı:**  
        *Bir şirketin kısa vadeli yükümlülüklerini en likit varlıkları ile karşılama kabiliyetini ölçen bir likidite oranı. Envanteri hesaplamanın dışında tutarak cari orana kıyasla bir şirketin likiditesinin daha sıkı bir şekilde değerlendirilmesini sağlar.*   

        """

kaldirac_DESC = """

        **Kaldıraç Oranı:**  
        *Bir şirketin faaliyetlerini finanse etmek için ne ölçüde borç kullandığını ölçer. 
        Kaldıraç oranları, bir şirketin sermaye yapısı, finansal riski ve borç yükümlülüklerini yerine getirme kabiliyeti hakkında bilgi sağlar. Bir miktar kaldıraç getirileri artırabilirken, aşırı kaldıraç özellikle ekonomik gerileme dönemlerinde finansal sıkıntı riskini artırabilir.*   

        ---------------------------------------------------------------------
        
        """

satis_DESC = """

        ---------------------------------------------------------------------
        
        **Satışlar:**  
        *Şirketin birincil ticari faaliyetleri yoluyla ürettiği toplam para miktarıdır. Mal veya hizmet satışlarını içerir.*   

        """

satismal_DESC = """

        **Satış Maliyetleri:**  
        *Şirket tarafından satılan mal veya hizmetlerin üretimiyle ilgili doğrudan maliyetleri temsil eder. Hammadde, işçilik ve genel üretim giderleri gibi giderleri içerir.*   

        """

netsatis_DESC = """

        **Net Satışlar:**  
        *Gelir tablosunda, iadeler, ödenekler ve indirimler düşüldükten sonra bir şirketin birincil ticari faaliyetlerinden elde ettiği toplam geliri temsil eden önemli bir tutardır.  
        Bir şirketin gerçek satış performansının daha doğru bir yansımasını sağladığı için çok önemli bir metriktir.*   

        ---------------------------------------------------------------------
        
        """

brutkar_DESC = """

        ---------------------------------------------------------------------
        
        **Brüt Kar:**  
        *Gelirden satılan malın maliyeti çıkarılarak hesaplanan brüt kâr, diğer giderler düşülmeden önce bir şirketin temel faaliyetlerinden elde edilen kârı temsil eder.*   

        ---------------------------------------------------------------------
        
        """

netkar_DESC = """

        ---------------------------------------------------------------------
        
        **Net Kar:**  
        *Kâr veya net kâr, şirketin gelirinden vergiler de dâhil olmak üzere tüm giderler düşüldükten sonra kalan nihai tutardır.  
        Net gelir, bir şirketin genel karlılığının önemli bir göstergesidir.*   

        ---------------------------------------------------------------------
        
        """

favok_DESC = """

        ---------------------------------------------------------------------
        
        **FAVÖK:**  
        *Faiz, Vergi, Amortisman ve İtfa Payı Öncesi Kazanç. Belirli faaliyet dışı giderleri hariç tutarak bir şirketin işletme performansını değerlendirmek için kullanılan finansal bir ölçüttür.  
        FAVÖK, bir şirketin finansman kararlarının, muhasebe yöntemlerinin ve vergi ortamlarının etkisinden önce faaliyet geliri elde etme kabiliyetinin bir ölçüsünü sağlar.*   

        ---------------------------------------------------------------------
        
        """

nedenusd_DESC = """

        **Neden USD?**  
        *ABD Doları genellikle istikrarlı ve yaygın olarak kabul gören bir para birimi olarak kabul edilir. Yüksek enflasyon oranlarına veya para birimi oynaklığına sahip ülkelerde faaliyet gösteren şirketler için, finansal tabloların ABD Doları cinsinden sunulması bir tür enflasyondan korunma işlevi görebilir. Daha istikrarlı ve küresel olarak tanınan bir ölçü birimi sağlar.*   

        """

fk_ratio_DESC = """

        **F/K (Fiyat/Kazanç) ?**  
        *Bir şirketin hisse senedi fiyatı ile hisse başına kazancı arasındaki ilişkiyi ölçen bir finansal metrik.*   

        """

fdfavok_DESC = """

        **FD/FAVÖK (Firma Değeri/FAVÖK) ?**  
        *Bir şirketin değerlemesini değerlendirmek için kullanılan finansal bir ölçüttür.  
        Bir şirketin toplam işletme değerini (FD) - piyasa değeri, borç ve eldeki nakit parayı içerir - faiz, vergi, amortisman ve itfa öncesi kazançlarıyla karşılaştırır.*   

        """

pddd_DESC = """

        **PD/DD (Piyasa Değeri/Defter Değeri) ?**  
        *Bir şirketin piyasa değerini defter değeriyle karşılaştıran ve yatırımcıların şirketin net varlık değerine göre ne kadar ödemek istediklerine dair fikir veren bir finansal ölçüt.*   

        """

# App title
col1, col2 = st.columns([25,75])
with col2:
    st.markdown("_Bu bir şirketlerin gelir ve bilanço tablolarını görselleştirme çalışmasıdır. Herhangi bir gelir elde edilmemektedir._")

st.subheader("")

col1,col2,col3,col4,col5 = st.columns([16,16,20,68,16])
with col1:
    ticker = st.text_input('Hisse Senedi', value='SISE',max_chars=5).upper() # Select ticker symbol
with col2:
    kur_option = st.selectbox("Kur Seçiniz",("TRY", "USD"))
with col3:
    st.markdown("")
    with st.popover("**💡 Döviz Cinsinin Önemi 📚**"):
            st.markdown(nedenusd_DESC)
with col5:
    st.write("")
    with st.popover("📬 İletişim"):
            st.markdown("✉️: tafasensei@gmail.com")

out_bil = pd.date_range('2021-03', '2026-03', freq='3M')
out_bil_df = pd.DataFrame(out_bil, columns=['DateOfBil'])

out_bil_df['year'] = out_bil_df['DateOfBil'].dt.year
out_bil_df['month'] = out_bil_df['DateOfBil'].dt.month
out_bil_df['year&month'] = out_bil_df['month'].astype(str)+"/"+out_bil_df['year'].astype(str)

@st.cache_data
def get_data(ticker,kur_option):
    link1 = 'https://www.isyatirim.com.tr/_layouts/15/IsYatirim.Website/Common/Data.aspx/MaliTablo?companyCode='+ticker+'&exchange='+kur_option+'&financialGroup=XI_29&year1=2021&period1=3&year2=2021&period2=6&year3=2021&period3=9&year4=2021&period4=12&_=1691405798292'
    link2 = 'https://www.isyatirim.com.tr/_layouts/15/IsYatirim.Website/Common/Data.aspx/MaliTablo?companyCode='+ticker+'&exchange='+kur_option+'&financialGroup=XI_29&year1=2022&period1=3&year2=2022&period2=6&year3=2022&period3=9&year4=2022&period4=12&_=1691405798292'
    link3 = 'https://www.isyatirim.com.tr/_layouts/15/IsYatirim.Website/Common/Data.aspx/MaliTablo?companyCode='+ticker+'&exchange='+kur_option+'&financialGroup=XI_29&year1=2023&period1=3&year2=2023&period2=6&year3=2023&period3=9&year4=2023&period4=12&_=1691405798292'
    link4 = 'https://www.isyatirim.com.tr/_layouts/15/IsYatirim.Website/Common/Data.aspx/MaliTablo?companyCode='+ticker+'&exchange='+kur_option+'&financialGroup=XI_29&year1=2024&period1=3&year2=2024&period2=6&year3=2024&period3=9&year4=2024&period4=12&_=1691405798292'

    bil_r = requests.get(link1)
    soup_bil = BeautifulSoup(bil_r.text, 'html.parser')
    results_dict = json.loads(soup_bil.string)["value"]
    df_2020 = pd.DataFrame.from_dict(results_dict)
    df_2020 = df_2020[['itemDescTr','value1','value2','value3','value4']].rename(columns = {'value1':out_bil_df['year&month'].loc[0],
                                                                                            'value2':out_bil_df['year&month'].loc[1],
                                                                                            'value3':out_bil_df['year&month'].loc[2],
                                                                                            'value4':out_bil_df['year&month'].loc[3]}).fillna(0)

    bil_r = requests.get(link2)
    soup_bil = BeautifulSoup(bil_r.text, 'html.parser')
    results_dict = json.loads(soup_bil.string)["value"]
    df_2021 = pd.DataFrame.from_dict(results_dict)
    df_2021 = df_2021[['value1','value2','value3','value4']].rename(columns = {'value1':out_bil_df['year&month'].loc[4],
                                                                                            'value2':out_bil_df['year&month'].loc[5],
                                                                                            'value3':out_bil_df['year&month'].loc[6],
                                                                                            'value4':out_bil_df['year&month'].loc[7]}).fillna(0)

    bil_r = requests.get(link3)
    soup_bil = BeautifulSoup(bil_r.text, 'html.parser')
    results_dict = json.loads(soup_bil.string)["value"]
    df_2022 = pd.DataFrame.from_dict(results_dict)
    df_2022 = df_2022[['value1','value2','value3','value4']].rename(columns = {'value1':out_bil_df['year&month'].loc[8],
                                                                                            'value2':out_bil_df['year&month'].loc[9],
                                                                                            'value3':out_bil_df['year&month'].loc[10],
                                                                                            'value4':out_bil_df['year&month'].loc[11]}).fillna(0)

    bil_r = requests.get(link4)
    soup_bil = BeautifulSoup(bil_r.text, 'html.parser')
    results_dict = json.loads(soup_bil.string)["value"]
    df_2023 = pd.DataFrame.from_dict(results_dict)
    df_2023 = df_2023[['value1','value2','value3','value4']].rename(columns = {'value1':out_bil_df['year&month'].loc[12],
                                                                                            'value2':out_bil_df['year&month'].loc[13],
                                                                                            'value3':out_bil_df['year&month'].loc[14],
                                                                                            'value4':out_bil_df['year&month'].loc[15]}).fillna(0)

    df_all = pd.concat([df_2020,df_2021,df_2022,df_2023], axis=1)

    return(df_all)

df=get_data(ticker,kur_option)

if (df.iloc[:,-1] == 0).all() == True :
    df = df.iloc[:, :-1]
else:
    df = df

if (df.iloc[:,-1] == 0).all() == True :
    df = df.iloc[:, :-1]
else:
    df = df

if (df.iloc[:,-1] == 0).all() == True :
    df = df.iloc[:, :-1]
else:
    df = df


df_balance = df.iloc[:70].reset_index(drop=True)
df_income = df.iloc[70:113].reset_index(drop=True)
df_dipnot = df.iloc[113:121].reset_index(drop=True)
df_cash = df.iloc[121:147].reset_index(drop=True)

ser2 = pd.Series(range(1, len(df_income.iloc[0]), 4))
ser2 = ser2.values.tolist()
#st.dataframe(ser1)

#Bilanço
df_balance_sh = df_balance['itemDescTr'].values.tolist()
df_balance_sh = pd.DataFrame(df_balance_sh, columns=['itemDescTr'])

for x in range (1,len(df_balance.iloc[0])):
    df_balance_sh[out_bil_df['year&month'].loc[x-1]]=df_balance.iloc[:, x].astype(int)

df_balance_sh = df_balance_sh.set_index(['itemDescTr'])


oz_kaynak = df_balance_sh.iloc[58]
period_bil = oz_kaynak.index.values.tolist()
oz_kaynak = oz_kaynak.values.tolist()

uzun_yuk = df_balance_sh.iloc[44]
uzun_yuk = uzun_yuk.values.tolist()

kisa_yuk = df_balance_sh.iloc[30]
kisa_yuk = kisa_yuk.values.tolist()

donen_var = df_balance_sh.iloc[0]
donen_var = donen_var.values.tolist()

duran_var = df_balance_sh.iloc[12]
duran_var = duran_var.values.tolist()

kisa_borc = df_balance_sh.iloc[31]
kisa_borc = kisa_borc.values.tolist()

uzun_borc = df_balance_sh.iloc[45]
uzun_borc = uzun_borc.values.tolist()

nakit_benzer = df_balance_sh.iloc[1]
nakit_benzer = nakit_benzer.values.tolist()

fin_yat = df_balance_sh.iloc[2]
fin_yat = fin_yat.values.tolist()

toplam_kaynak = df_balance_sh.iloc[69]
toplam_kaynak = toplam_kaynak.values.tolist()

stoklar = df_balance_sh.iloc[7]
stoklar = stoklar.values.tolist()

bil_1_data = pd.DataFrame(
        {'Period': period_bil,
        'Özkaynaklar': oz_kaynak,
        'Uzun_Vade_Yük': uzun_yuk,
        'Kısa_Vade_Yük': kisa_yuk,
        'Dönen_Var': donen_var,
        'Duran_Var': duran_var,
        'Kısa_vade_borc': kisa_borc,
        'Uzun_vade_borc': uzun_borc,
        'Nakit_benzer': nakit_benzer,
        'Finansal_yat': fin_yat,'stoklar': stoklar,
        'Toplam_Kaynak': toplam_kaynak
        })

bil_1_data['Özkaynak_per']=bil_1_data['Özkaynaklar']/(bil_1_data['Özkaynaklar']+bil_1_data['Uzun_Vade_Yük']+bil_1_data['Kısa_Vade_Yük'])
bil_1_data['Uzun_Vade_Yük_per']=bil_1_data['Uzun_Vade_Yük']/(bil_1_data['Özkaynaklar']+bil_1_data['Uzun_Vade_Yük']+bil_1_data['Kısa_Vade_Yük'])
bil_1_data['Kısa_Vade_Yük_per']=bil_1_data['Kısa_Vade_Yük']/(bil_1_data['Özkaynaklar']+bil_1_data['Uzun_Vade_Yük']+bil_1_data['Kısa_Vade_Yük'])
bil_1_data['Net_Borc']=bil_1_data['Kısa_vade_borc']+bil_1_data['Uzun_vade_borc']-bil_1_data['Nakit_benzer']-bil_1_data['Finansal_yat']
bil_1_data['Diger_Dönen_Var']=bil_1_data['Dönen_Var']-bil_1_data['Nakit_benzer']-bil_1_data['Finansal_yat']
bil_1_data['Diger_Dönen_Var_per']=bil_1_data['Diger_Dönen_Var']/bil_1_data['Dönen_Var']
bil_1_data['Nakit_benzer_per']=bil_1_data['Nakit_benzer']/bil_1_data['Dönen_Var']
bil_1_data['Finansal_yat_per']=bil_1_data['Finansal_yat']/bil_1_data['Dönen_Var']
bil_1_data['Cari_Oran']=bil_1_data['Dönen_Var']/bil_1_data['Kısa_Vade_Yük']
bil_1_data['kaldırac_Oran']=(bil_1_data['Kısa_vade_borc']+bil_1_data['Uzun_vade_borc'])/bil_1_data['Toplam_Kaynak']
bil_1_data['Asit_Test_Oran']=(bil_1_data['Dönen_Var']-bil_1_data['stoklar'])/bil_1_data['Kısa_Vade_Yük']

#nakit akışı
df_cash_sh = df_cash['itemDescTr'].values.tolist()
df_cash_sh = pd.DataFrame(df_cash_sh, columns=['itemDescTr'])

for x in range (1,len(df_cash.iloc[0])):
    df_cash_sh[out_bil_df['year&month'].loc[x-1]]=df_cash.iloc[:, x].astype(int)

#Gelir Tablosu
df_income_q = df_income['itemDescTr'].values.tolist()
df_income_q = pd.DataFrame(df_income_q, columns=['itemDescTr'])

for x in range (1,len(df_income.iloc[0])):
    if x in ser2:
        df_income_q[out_bil_df['year&month'].loc[x-1]]=df_income.iloc[:, x].astype(int)
    else:
        df_income_q[out_bil_df['year&month'].loc[x-1]]=df_income.iloc[:, x].astype(int)-df_income.iloc[:, x-1].astype(int)

df_income_qtd = df_income_q.set_index(['itemDescTr'])

#dipnot
df_dipnot_q = df_dipnot['itemDescTr'].values.tolist()
df_dipnot_q = pd.DataFrame(df_dipnot_q, columns=['itemDescTr'])

for x in range (1,len(df_dipnot.iloc[0])):
    if x in ser2:
        df_dipnot_q[out_bil_df['year&month'].loc[x-1]]=df_dipnot.iloc[:, x].astype(int)
    else:
        df_dipnot_q[out_bil_df['year&month'].loc[x-1]]=df_dipnot.iloc[:, x].astype(int)-df_dipnot.iloc[:, x-1].astype(int)

df_dipnot_qtd = df_dipnot_q.set_index(['itemDescTr'])

#Income Summary Data Quarter to Date
net_profit_qtd = df_income_qtd.iloc[38]
period_qtd = net_profit_qtd.index.values.tolist()
n_profit_qtd = net_profit_qtd.values.tolist()
#st.dataframe(net_profit_qtd)
f_profit_qtd = df_income_qtd.iloc[17]
#st.dataframe(f_profit_qtd)
b_profit_qtd = df_income_qtd.iloc[10]
b_profit_qtd = b_profit_qtd.values.tolist()
#st.dataframe(b_profit_qtd)
sale_income_qtd = df_income_qtd.iloc[1]
sale_income_qtd = sale_income_qtd.values.tolist()
sale_expense_qtd = df_income_qtd.iloc[2]
sale_expense_qtd = sale_expense_qtd.values.tolist()

sale_in_qtd = df_dipnot_qtd.iloc[3]
sale_in_qtd = sale_in_qtd.values.tolist()
sale_out_qtd = df_dipnot_qtd.iloc[4]
sale_out_qtd = sale_out_qtd.values.tolist()
#st.dataframe(sale_income_qtd)

sales_qtd = pd.DataFrame(
        {'Period': period_qtd,
        'Sale': sale_income_qtd,
        'Sale_Expense': sale_expense_qtd,
        'Sale_in': sale_in_qtd,
        'Sale_out': sale_out_qtd,
        })
sales_qtd['Sale_Discount']=sales_qtd['Sale_in']+sales_qtd['Sale_out']-sales_qtd['Sale']
sales_qtd['Gross_Sale']=sales_qtd['Sale_in']+sales_qtd['Sale_out']
sales_qtd['Sale_Expense']=sales_qtd['Sale_Expense']*(-1)
sales_qtd['Sale_in_Per']=sales_qtd['Sale_in']/sales_qtd['Gross_Sale']
sales_qtd['Sale_out_Per']=sales_qtd['Sale_out']/sales_qtd['Gross_Sale']
#st.dataframe(sales_qtd)

favok_qtd = df_income_qtd.iloc[10]+df_income_qtd.iloc[11]+df_income_qtd.iloc[12]+df_income_qtd.iloc[13]+df_dipnot_qtd.iloc[0]
favok_qtd = favok_qtd.values.tolist()
#st.dataframe(favok_qtd)

income_qtd = pd.DataFrame(
        {'Period': period_qtd,
        'B_Profit': b_profit_qtd,
        'N_Profit': n_profit_qtd,
        'Sale': sale_income_qtd,
        'Favok': favok_qtd,
        })
income_qtd['Net_Profit_Margin']=income_qtd['N_Profit']/income_qtd['Sale']
income_qtd['Gross_Profit_Margin']=income_qtd['B_Profit']/income_qtd['Sale']
income_qtd['Favok_Margin']=income_qtd['Favok']/income_qtd['Sale']

df_income_ytd = df_income_q['itemDescTr'].values.tolist()
df_income_ytd = pd.DataFrame(df_income_ytd, columns=['itemDescTr'])

for x in range (4,len(df_income_q.iloc[0])):
    df_income_ytd[out_bil_df['year&month'].loc[x-1]]=df_income_q.iloc[:, x]+df_income_q.iloc[:, x-1]+df_income_q.iloc[:, x-2]+df_income_q.iloc[:, x-3]

df_income_ytd = df_income_ytd.set_index(['itemDescTr'])

net_profit_ytd = df_income_ytd.iloc[38]
n_profit_ytd = net_profit_ytd.values.tolist()

df_dipnot_ytd = df_dipnot_q['itemDescTr'].values.tolist()
df_dipnot_ytd = pd.DataFrame(df_dipnot_ytd, columns=['itemDescTr'])

for x in range (4,len(df_dipnot_q.iloc[0])):
    df_dipnot_ytd[out_bil_df['year&month'].loc[x-1]]=df_dipnot_q.iloc[:, x]+df_dipnot_q.iloc[:, x-1]+df_dipnot_q.iloc[:, x-2]+df_dipnot_q.iloc[:, x-3]

df_dipnot_ytd = df_dipnot_ytd.set_index(['itemDescTr'])

#Income Summary Data Year to Date
net_profit_ytd = df_income_ytd.iloc[38]
period_ytd = net_profit_ytd.index.values.tolist()
#st.info(period_ytd)
n_profit_ytd = net_profit_ytd.values.tolist()
#st.info(n_profit_ytd)

f_profit_ytd = df_income_ytd.iloc[17]
f_profit_ytd = f_profit_ytd.values.tolist()
#st.info(f_profit_ytd)

b_profit_ytd = df_income_ytd.iloc[10]
b_profit_ytd = b_profit_ytd.values.tolist()
#st.info(b_profit_ytd)

sale_income_ytd = df_income_ytd.iloc[1]
sale_income_ytd = sale_income_ytd.values.tolist()
sale_expense_ytd = df_income_ytd.iloc[2]
sale_expense_ytd = sale_expense_ytd.values.tolist()
#st.info(sale_income_ytd)

sale_in_ytd = df_dipnot_ytd.iloc[3]
sale_in_ytd = sale_in_ytd.values.tolist()
sale_out_ytd = df_dipnot_ytd.iloc[4]
sale_out_ytd = sale_out_ytd.values.tolist()

sales_ytd = pd.DataFrame(
        {'Period': period_ytd,
        'Sale': sale_income_ytd,
        'Sale_Expense': sale_expense_ytd,
        'Sale_in': sale_in_ytd,
        'Sale_out': sale_out_ytd,
        })
sales_ytd['Sale_Discount']=sales_ytd['Sale_in']+sales_ytd['Sale_out']-sales_ytd['Sale']
sales_ytd['Gross_Sale']=sales_ytd['Sale_in']+sales_ytd['Sale_out']
sales_ytd['Sale_Expense']=sales_ytd['Sale_Expense']*(-1)
sales_ytd['Sale_in_Per']=sales_ytd['Sale_in']/sales_ytd['Gross_Sale']
sales_ytd['Sale_out_Per']=sales_ytd['Sale_out']/sales_ytd['Gross_Sale']
#st.dataframe(sales_ytd)

favok_ytd = df_income_ytd.iloc[10]+df_income_ytd.iloc[11]+df_income_ytd.iloc[12]+df_income_ytd.iloc[13]+df_dipnot_ytd.iloc[0]
favok_ytd = favok_ytd.values.tolist()
#st.info(favok_ytd)

income_ytd = pd.DataFrame(
        {'Period': period_ytd,
        'B_Profit': b_profit_ytd,
        'N_Profit': n_profit_ytd,
        'Sale': sale_income_ytd,
        'Favok': favok_ytd,
        })
income_ytd['Net_Profit_Margin']=income_ytd['N_Profit']/income_ytd['Sale']
income_ytd['Gross_Profit_Margin']=income_ytd['B_Profit']/income_ytd['Sale']
income_ytd['Favok_Margin']=income_ytd['Favok']/income_ytd['Sale']

#------------------------------------------------------------------------------------------------
#Hakkında

url_cari = 'https://www.isyatirim.com.tr/tr-tr/analiz/hisse/Sayfalar/sirket-karti.aspx?hisse='+ticker
r_cari_oz = requests.get(url_cari)
soup_cari= BeautifulSoup(r_cari_oz.content, 'html.parser')

#FK
fk_txt = soup_cari.find_all(class_="table vertical")[1].find_all('th')[0].text.strip()
#st.info(fk_txt)
fk_val = soup_cari.find_all(class_="table vertical")[1].find_all('td')[0].text.strip()
#st.info(fk_val)

#FD/FAVÖK
fdfvk_txt = soup_cari.find_all(class_="table vertical")[1].find_all('th')[1].text.strip()
#st.info(fdfvk_txt)
fdfvk_val = soup_cari.find_all(class_="table vertical")[1].find_all('td')[1].text.strip()
#st.info(fdfvk_val)

#PD/DD
pddd_txt = soup_cari.find_all(class_="table vertical")[1].find_all('th')[2].text.strip()
#st.info(pddd_txt)
pddd_val = soup_cari.find_all(class_="table vertical")[1].find_all('td')[2].text.strip()
#st.info(pddd_val)

#PD/DD
pddd_txt = soup_cari.find_all(class_="table vertical")[1].find_all('th')[2].text.strip()
#st.info(pddd_txt)
pddd_val = soup_cari.find_all(class_="table vertical")[1].find_all('td')[2].text.strip()
#st.info(pddd_val)

#Yabancı Oranı
ybnc_txt = soup_cari.find_all(class_="table vertical")[1].find_all('th')[4].text.strip()
#st.info(ybnc_txt)
ybnc_val = soup_cari.find_all(class_="table vertical")[1].find_all('td')[4].text.strip()
ybnc_val = float(float(ybnc_val.replace(',', '.')))
#st.info(ybnc_val)

values_ybnc = [ybnc_val, 100-ybnc_val]

# Use `hole` to create a donut-like pie chart
fig_ybnc = go.Figure(data=[
    go.Pie(
           values=values_ybnc, 
           hole=.6,
           textinfo='none',
           showlegend=False,
           marker_colors=['rgb(0,204,204)','rgb(250,250,250)']
           )
        ])

fig_ybnc.update_layout(title_text=ybnc_txt, title_x=0.3,
                       width=375, height=375,
                        annotations=[dict(text=str(ybnc_val)+"%", 
                                         x=0.5, y=0.5, 
                                         font_size=20, showarrow=False)
                              ])
#st.plotly_chart(fig_ybnc)

#Halka Açık Oranı
hlkck_txt = soup_cari.find_all(class_="table vertical")[1].find_all('th')[8].text.strip()
#st.info(hlkck_txt)
hlkck_val = soup_cari.find_all(class_="table vertical")[1].find_all('td')[8].text.strip()
hlkck_val = float(float(hlkck_val.replace(',', '.')))
#st.info(hlkck_val)

values_hlkck = [hlkck_val, 100-hlkck_val]

# Use `hole` to create a donut-like pie chart
fig_hlkck = go.Figure(data=[
    go.Pie(
           values=values_hlkck, 
           hole=.6,
           textinfo='none',
           showlegend=False,
           marker_colors=['rgb(255,0,127)','rgb(250,250,250)']
           )
        ])

fig_hlkck.update_layout(title_text=hlkck_txt, title_x=0.3,
                        width=375, height=375,
                        annotations=[dict(text=str(hlkck_val)+"%", 
                                         x=0.5, y=0.5, 
                                         font_size=20, showarrow=False)
                              ])

#st.plotly_chart(fig_hlkck)

bistinfo = 'https://www.kap.org.tr/tr/bist-sirketler'
r = requests.get(bistinfo)
soup_bist = BeautifulSoup(r.content, 'html.parser')

bist_kods = soup_bist.find_all(class_="w-clearfix w-inline-block comp-row")

master_list=[]
for bist_kod in bist_kods:
        kod = bist_kod.find(class_="comp-cell _04 vtable").a.text
        kod_link_gen = 'https://www.kap.org.tr'+bist_kod.find(class_="comp-cell _04 vtable").a['href'].replace('ozet','genel').strip()
        kod_link_oz = 'https://www.kap.org.tr'+bist_kod.find(class_="comp-cell _04 vtable").a['href'].strip()
        unvan = bist_kod.find(class_="comp-cell _14 vtable").a.text.strip()
        sehir = bist_kod.find(class_="comp-cell _12 vtable").text.strip()
        data_dict = {}
        data_dict['Kod']=kod
        data_dict['Şirket Ünvanı']=unvan
        data_dict['Şehir']=sehir
        data_dict['Kod Link Özet']=kod_link_oz
        data_dict['Kod Link Genel']=kod_link_gen
        master_list.append(data_dict)

df = pd.DataFrame(master_list)
    #st.dataframe(df)

deneme_name= df['Şirket Ünvanı'].loc[df['Kod'] == ticker ].reset_index(drop=True)
name_company = deneme_name[0]
    #st.success(name_company)

deneme_city= df['Şehir'].loc[df['Kod'] == ticker ].reset_index(drop=True)
city_company = deneme_city[0]
    #st.info(city_company)

url_genel= df['Kod Link Genel'].loc[df['Kod'] == ticker ].reset_index(drop=True)
url_company_gen = url_genel[0]
    #st.info(url_company)

r_comp_gen = requests.get(url_company_gen)
s_comp= BeautifulSoup(r_comp_gen.content, 'html.parser')

img_comp = 'https://www.kap.org.tr'+s_comp.find(class_='comp-logo').get('src')
    #st.info(img_comp)
    #st.image(f'{img_comp}',width=200)


df_oz_dummy = pd.DataFrame({
                                "Title" : ['İnternet Adresi', 'Şirketin Dahil Olduğu Endeksler','Şirketin Sektörü', 'Sermaye Piyasası Aracının İşlem Gördüğü Pazar'], 
                                "Value" : [' ', ' ', ' ',' ']})
    #st.dataframe(df_oz_dummy)

url_ozet= df['Kod Link Özet'].loc[df['Kod'] == ticker ].reset_index(drop=True)
url_company_oz = url_ozet[0]
r_comp_oz = requests.get(url_company_oz)
s_comp_oz= BeautifulSoup(r_comp_oz.content, 'html.parser')

oz_tit_len = s_comp_oz.find_all(class_="comp-cell-row-div vtable infoColumn backgroundThemeForTitle")
    #st.info(len(oz_tit_len))

oz_list=[]
for i in range (0,len(oz_tit_len)):
        oz_title = s_comp_oz.find_all(class_="comp-cell-row-div vtable infoColumn backgroundThemeForTitle")[i].text.strip()
        oz_value = s_comp_oz.find_all(class_="comp-cell-row-div vtable infoColumn backgroundThemeForValue")[i].text.strip()
        data_oz = {}
        data_oz['Title']=oz_title
        data_oz['Value']=oz_value
        oz_list.append(data_oz)

df_oz = pd.DataFrame(oz_list)
    #st.dataframe(df_oz)

new_df_oz=df_oz_dummy.merge(df_oz.rename({'Value': 'Value2'}, axis=1), on='Title', how='left')
new_df_oz=new_df_oz.drop(columns='Value').rename(columns = {'Value2':'Value'}).fillna(0)
    #st.dataframe(new_df_oz)


#------------------------------------------------------------------------------------------------
tab1, tab2, tab3 = st.tabs([" 🏯 Şirket Hakkında", " 🛟 Gelir Tablosu", " ⛽️ Bilanço Tablosu"])

with tab1 :

    cc = st.columns([0.3,0.7])
    with cc[0]:
        st.image(f'{img_comp}',width=300)
    with cc[1]:
        st.title(name_company)
    
    st.subheader("")

    with st.popover("**💡 Finansal Oranlar 📚**"):
            st.markdown(fk_ratio_DESC)
            st.markdown(fdfavok_DESC)
            st.markdown(pddd_DESC)

    col1,col2,col3,col4,col5 = st.columns(5)
    with col2:
        st.metric(fk_txt, fk_val)
    with col3:
        st.metric(fdfvk_txt, fdfvk_val)
    with col4:
        st.metric(pddd_txt, pddd_val)

    col1,col2,col3,col4 = st.columns([15,30,30,25])
    with col2:
        st.plotly_chart(fig_hlkck)
    with col3:
        st.plotly_chart(fig_ybnc)

    vv = st.columns(2)
    with vv[0]:
        st.subheader("⚙️ Sektör : ")
        if new_df_oz['Value'].loc[2] == 0:
            st.success('Bilgi Mevcut Değil')
        else:
            st.success(new_df_oz['Value'].loc[2])
    with vv[1]:
        st.subheader('🛒 Pazar : ')
        if new_df_oz['Value'].loc[3] == 0:
            st.info('Bilgi Mevcut Değil')
        else:
            st.info(new_df_oz['Value'].loc[3])

    zz = st.columns(2)
    with zz[0]:
        st.subheader('🏛 Endeks : ')
        if new_df_oz['Value'].loc[1] == 0:
            st.info('Bilgi Mevcut Değil')
        else:
            st.info(new_df_oz['Value'].loc[1])
    with zz[1]:
        st.subheader('🌐 İnternet Adresi : ')
        if new_df_oz['Value'].loc[0] == 0:
            st.success('Bilgi Mevcut Değil')
        else:
            st.success(new_df_oz['Value'].loc[0])

    descs_comp = s_comp.find_all(class_="sub-collapseblock")[1]
    desc = descs_comp.find(class_="column-type3 exportDiv").text
    st.subheader('🗃 Faaliyet Konusu :')
    st.warning(desc)

with tab2 :

    col1,col2,col3 = st.columns([13,74,13])
    with col1:
        st.subheader("")
    with col2:
        st.markdown(gelir_DESC)
    with col3:
        st.subheader("")
    
    st.markdown("")

    col1,col2,col3 = st.columns([30,35,35])
    with col1:
        st.subheader("")
    with col2:
        selected = option_menu(
                                menu_title=None,
                                options=["Çeyreklik","Yıllık"],
                                icons=["diagram-2","diagram-3"],
                                default_index=0,
                                orientation="horizontal")
    with col3:
        st.subheader("")

    if selected == "Çeyreklik":

        col1,col2,col3 = st.columns([13,74,13])
        with col1:
            st.subheader("")
        with col2:
            st.markdown(ceyrek_DESC)
        with col3:
            st.subheader("")

        with st.popover("**💡 Satışlar 📚**"):
            st.markdown(satis_DESC)
            st.markdown(satismal_DESC)
            st.markdown(netsatis_DESC)

        fig_sales_qtd = go.Figure(data=[
            go.Bar(name='Yurt İçi Satışlar', 
                x=sales_qtd['Period'], 
                y=sales_qtd['Sale_in'],
                text=sales_qtd['Sale_in_Per'],marker_color='DarkOrange',cliponaxis=False,
                textposition="inside",insidetextanchor = "start",texttemplate='%{text:.1%}',textfont={"size":11},
                #showlegend=False
                ),
            go.Bar(name='Yurt Dışı Satışlar', 
                x=sales_qtd['Period'], 
                y=sales_qtd['Sale_out'],
                text=sales_qtd['Sale_out_Per'],cliponaxis=False,
                textposition="inside",insidetextanchor = "start",texttemplate='%{text:.1%}',textfont={"size":11},
                #showlegend=False
                )
        ])

        fig_sales_qtd.add_trace(
            go.Scatter(name='Brüt Satışlar', 
                x=sales_qtd['Period'],
                y=sales_qtd['Gross_Sale'],
                text=sales_qtd['Gross_Sale'],
                mode='text',cliponaxis=False,
                textposition='top center',texttemplate= '%{text:.2s}',textfont={"size":12},
                showlegend=False
            ))

        fig_sales_qtd.add_trace(
            go.Scatter(name='Net Satışlar', 
                x=sales_qtd['Period'],
                y=sales_qtd['Sale'],
                mode='lines+markers+text',line=dict(color='red'),
                #showlegend=False
            ))

        fig_sales_qtd.add_trace(
            go.Scatter(name='Satış Maliyetleri', 
                x=sales_qtd['Period'],
                y=sales_qtd['Sale_Expense'],
                mode='lines+markers+text',line=dict(color='purple'),
                #showlegend=False
            ))

        fig_sales_qtd.update_layout(
                                    width=900, height=500,
                                    barmode='stack',
                                    xaxis_title=' ', yaxis_title=" ",
                                    yaxis={'visible': False, 'showticklabels': False, 'showgrid': False},
                                    legend=dict(orientation="h",
                                                yanchor="bottom",y=-0.25,
                                                xanchor="center",x=0.5
                                ))
        
        col1,col2,col3 = st.columns([13,74,13])
        with col1:
            st.subheader("")
        with col2:
            st.plotly_chart(fig_sales_qtd)
        with col3:
            st.subheader("")
        
        #Brüt Kar/Marjı Yıllık

        with st.popover("**💡 Brüt Kar 📚**"):
            st.markdown(brutkar_DESC)

        fig_g_profit_qtd = go.Figure()

        fig_g_profit_qtd.add_trace(
            go.Bar(
                x=income_qtd['Period'], 
                y=income_qtd['B_Profit'],
                text=income_qtd['B_Profit'],
                textposition="outside", texttemplate='%{text:.2s}',
                showlegend=False, cliponaxis=False
                )
            )
        fig_g_profit_qtd.add_trace(
            go.Scatter(
                x=income_qtd['Period'], 
                y=income_qtd['Gross_Profit_Margin'],
                text=income_qtd['Gross_Profit_Margin'],
                mode='lines+text+markers',textposition="top center", texttemplate='%{text:.1%}',
                textfont=dict(color="DarkOrange"),
                line=dict(color='red'),showlegend=False,
                yaxis="y2"
            ))
        fig_g_profit_qtd.update_layout(width=900, height=500,
                            yaxis=dict(title = " ",visible=False,showticklabels=False),
                            yaxis2=dict(title = " ",anchor = "free", overlaying="y",
                                        side="right",showticklabels=False,visible=False)
                        )

        col1,col2,col3 = st.columns([13,74,13])
        with col1:
            st.subheader("")
        with col2:
            st.plotly_chart(fig_g_profit_qtd)
        with col3:
            st.subheader("")
        

        #Favök Tutarı/Marjı Yıllık

        with st.popover("**💡 FAVÖK 📚**"):
            st.markdown(favok_DESC)
        
        fig_favok_qtd = go.Figure()

        fig_favok_qtd.add_trace(
            go.Bar(
                x=income_qtd['Period'], 
                y=income_qtd['Favok'],
                text=income_qtd['Favok'],marker_color='firebrick',
                textposition="outside", texttemplate='%{text:.2s}',
                showlegend=False, cliponaxis=False
                )
            )
        fig_favok_qtd.add_trace(
            go.Scatter(
                x=income_qtd['Period'], 
                y=income_qtd['Favok_Margin'],
                text=income_qtd['Favok_Margin'],
                mode='lines+text+markers',textposition="top center", texttemplate='%{text:.1%}',
                textfont=dict(color="DarkOrange"),
                line=dict(color='blue'),showlegend=False,
                yaxis="y2"
            ))
        fig_favok_qtd.update_layout(width=900, height=500,
                            yaxis=dict(title = " ",visible=False,showticklabels=False),
                            yaxis2=dict(title = " ",anchor = "free", overlaying="y",
                                        side="right",showticklabels=False,visible=False)
                        )
        
        col1,col2,col3 = st.columns([13,74,13])
        with col1:
            st.subheader("")
        with col2:
            st.plotly_chart(fig_favok_qtd)
        with col3:
            st.subheader("")
        
        #Net Kar/Marjı Yıllık

        with st.popover("**💡 Net Kar 📚**"):
            st.markdown(netkar_DESC)
        
        fig_profit_qtd = go.Figure()

        fig_profit_qtd.add_trace(
            go.Bar(
                x=income_qtd['Period'], 
                y=income_qtd['N_Profit'],
                text=income_qtd['N_Profit'],marker_color='teal',
                textposition="outside", texttemplate='%{text:.2s}',
                showlegend=False, cliponaxis=False
                )
            )
        fig_profit_qtd.add_trace(
            go.Scatter(
                x=income_qtd['Period'], 
                y=income_qtd['Net_Profit_Margin'],
                text=income_qtd['Net_Profit_Margin'],
                mode='lines+text+markers',textposition="top center", texttemplate='%{text:.1%}',
                textfont=dict(color="DarkOrange"),
                line=dict(color='purple'),showlegend=False,
                yaxis="y2"
            ))
        fig_profit_qtd.update_layout(width=900, height=500,
                            yaxis=dict(title = " ",visible=False,showticklabels=False),
                            yaxis2=dict(title = " ",anchor = "free", overlaying="y",
                                        side="right",showticklabels=False,visible=False)
                        )

        col1,col2,col3 = st.columns([13,74,13])
        with col1:
            st.subheader("")
        with col2:
            st.plotly_chart(fig_profit_qtd)
        with col3:
            st.subheader("")

    #-------------------------------------------------------------------------

    if selected == "Yıllık":
    
        col1,col2,col3 = st.columns([13,74,13])
        with col1:
            st.subheader("")
        with col2:
            st.markdown(yillik_DESC)
        with col3:
            st.subheader("")
        
        with st.popover("**💡 Satışlar 📚**"):
            st.markdown(satis_DESC)
            st.markdown(satismal_DESC)
            st.markdown(netsatis_DESC)

        fig_sales = go.Figure(data=[
            go.Bar(name='Yurt İçi Satışlar', 
                x=sales_ytd['Period'], 
                y=sales_ytd['Sale_in'],
                text=sales_ytd['Sale_in_Per'],marker_color='DarkOrange',cliponaxis=False,
                textposition="inside",insidetextanchor = "start",texttemplate='%{text:.1%}',textfont={"size":11},
                #showlegend=False
                ),
            go.Bar(name='Yurt Dışı Satışlar', 
                x=sales_ytd['Period'], 
                y=sales_ytd['Sale_out'],
                text=sales_ytd['Sale_out_Per'],cliponaxis=False,
                textposition="inside",insidetextanchor = "start",texttemplate='%{text:.1%}',textfont={"size":11},
                #showlegend=False
                )
        ])

        fig_sales.add_trace(
            go.Scatter(name='Brüt Satışlar', 
                x=sales_ytd['Period'],
                y=sales_ytd['Gross_Sale'],
                text=sales_ytd['Gross_Sale'],
                mode='text',cliponaxis=False,
                textposition='top center',texttemplate= '%{text:.2s}',textfont={"size":12},
                showlegend=False
            ))

        fig_sales.add_trace(
            go.Scatter(name='Net Satışlar', 
                x=sales_ytd['Period'],
                y=sales_ytd['Sale'],
                mode='lines+markers+text',line=dict(color='red'),
                #showlegend=False
            ))

        fig_sales.add_trace(
            go.Scatter(name='Satış Maliyetleri', 
                x=sales_ytd['Period'],
                y=sales_ytd['Sale_Expense'],
                mode='lines+markers+text',line=dict(color='purple'),
                #showlegend=False
            ))

        fig_sales.update_layout(
                                width=900, height=500,
                                barmode='stack',
                                xaxis_title=' ', yaxis_title=" ",
                                yaxis={'visible': False, 'showticklabels': False, 'showgrid': False},
                                legend=dict(orientation="h",
                                    yanchor="bottom",y=-0.25,
                                    xanchor="center",x=0.5
                                ))
        
        col1,col2,col3 = st.columns([13,74,13])
        with col1:
            st.subheader("")
        with col2:
            st.plotly_chart(fig_sales)
        with col3:
            st.subheader("")

        #Brüt Kar/Marjı Yıllık

        with st.popover("**💡 Brüt Kar 📚**"):
            st.markdown(brutkar_DESC)
        
        fig_g_profit = go.Figure()

        fig_g_profit.add_trace(
            go.Bar(
                x=income_ytd['Period'], 
                y=income_ytd['B_Profit'],
                text=income_ytd['B_Profit'],
                textposition="outside", texttemplate='%{text:.2s}',
                showlegend=False, cliponaxis=False
                )
            )
        fig_g_profit.add_trace(
            go.Scatter(
                x=income_ytd['Period'], 
                y=income_ytd['Gross_Profit_Margin'],
                text=income_ytd['Gross_Profit_Margin'],
                mode='lines+text+markers',textposition="top center", texttemplate='%{text:.1%}',
                textfont=dict(color="DarkOrange"),
                line=dict(color='red'),showlegend=False,
                yaxis="y2"
            ))
        fig_g_profit.update_layout(width=900, height=500,
                            yaxis=dict(title = " ",visible=False,showticklabels=False),
                            yaxis2=dict(title = " ",anchor = "free", overlaying="y",
                                        side="right",showticklabels=False,visible=False)
                        )

        col1,col2,col3 = st.columns([13,74,13])
        with col1:
            st.subheader("")
        with col2:
            st.plotly_chart(fig_g_profit)
        with col3:
            st.subheader("")
        
        #Favök Tutarı/Marjı Yıllık

        with st.popover("**💡 FAVÖK 📚**"):
            st.markdown(favok_DESC)
        
        fig_favok = go.Figure()

        fig_favok.add_trace(
            go.Bar(
                x=income_ytd['Period'], 
                y=income_ytd['Favok'],
                text=income_ytd['Favok'],marker_color='firebrick',
                textposition="outside", texttemplate='%{text:.2s}',
                showlegend=False, cliponaxis=False
                )
            )
        fig_favok.add_trace(
            go.Scatter(
                x=income_ytd['Period'], 
                y=income_ytd['Favok_Margin'],
                text=income_ytd['Favok_Margin'],
                mode='lines+text+markers',textposition="top center", texttemplate='%{text:.1%}',
                textfont=dict(color="DarkOrange"),
                line=dict(color='blue'),showlegend=False,
                yaxis="y2"
            ))
        fig_favok.update_layout(width=900, height=500,
                            yaxis=dict(title = " ",visible=False,showticklabels=False),
                            yaxis2=dict(title = " ",anchor = "free", overlaying="y",
                                        side="right",showticklabels=False,visible=False)
                        )

        col1,col2,col3 = st.columns([13,74,13])
        with col1:
            st.subheader("")
        with col2:
            st.plotly_chart(fig_favok)
        with col3:
            st.subheader("")

        #Net Kar/Marjı Yıllık

        with st.popover("**💡 Net Kar 📚**"):
            st.markdown(netkar_DESC)
        
        fig_profit = go.Figure()

        fig_profit.add_trace(
            go.Bar(
                x=income_ytd['Period'], 
                y=income_ytd['N_Profit'],
                text=income_ytd['N_Profit'],marker_color='teal',
                textposition="outside", texttemplate='%{text:.2s}',
                showlegend=False, cliponaxis=False
                )
            )
        fig_profit.add_trace(
            go.Scatter(
                x=income_ytd['Period'], 
                y=income_ytd['Net_Profit_Margin'],
                text=income_ytd['Net_Profit_Margin'],
                mode='lines+text+markers',textposition="top center", texttemplate='%{text:.1%}',
                textfont=dict(color="DarkOrange"),
                line=dict(color='purple'),showlegend=False,
                yaxis="y2"
            ))
        fig_profit.update_layout(width=900, height=500,
                            yaxis=dict(title = " ",visible=False,showticklabels=False),
                            yaxis2=dict(title = " ",anchor = "free", overlaying="y",
                                        side="right",showticklabels=False,visible=False)
                        )

        col1,col2,col3 = st.columns([13,74,13])
        with col1:
            st.subheader("")
        with col2:
            st.plotly_chart(fig_profit)
        with col3:
            st.subheader("")
        

with tab3 :
    #Bilanço Özeti

    col1,col2,col3 = st.columns([13,74,13])
    with col1:
        st.subheader("")
    with col2:
        st.markdown(bilanco_DESC)
    with col3:
        st.subheader("")
    
    with st.popover("**💡 Varlıklar 📚**"):
        st.markdown(varlik_DESC)
        st.markdown(nborc_DESC)
        st.markdown(dvarlik_DESC)
        st.markdown(ozkynk_DESC)
        st.markdown(fyatirim_DESC)
        st.markdown(nakitb_DESC)

    fig_bil_2 = go.Figure(data=[
                go.Bar(name='Stoklar,Alacaklar,Diğer', 
                    x=bil_1_data['Period'], 
                    y=bil_1_data['Diger_Dönen_Var'],
                    text=bil_1_data['Diger_Dönen_Var_per'],marker_color='cyan',cliponaxis=False,
                    textposition="inside",insidetextanchor = "middle",texttemplate='%{text:.1%}',textfont={"size":10},
                    #showlegend=False
                    ),
                go.Bar(name='Nakit ve Nakit Benzerleri', 
                    x=bil_1_data['Period'], 
                    y=bil_1_data['Nakit_benzer'],
                    text=bil_1_data['Nakit_benzer_per'],marker_color='salmon',cliponaxis=False,
                    textposition="inside",insidetextanchor = "middle",texttemplate='%{text:.1%}',textfont={"size":10},
                    #showlegend=False
                    ),
                go.Bar(name='Finansal Yatırımlar', 
                    x=bil_1_data['Period'], 
                    y=bil_1_data['Finansal_yat'],
                    text=bil_1_data['Finansal_yat_per'],marker_color='darkblue',cliponaxis=False,
                    textposition="inside",insidetextanchor = "middle",texttemplate='%{text:.1%}',textfont={"size":10},
                    #showlegend=False
                    )
            ])

    fig_bil_2.add_trace(
                go.Scatter(name='Özkaynaklar', 
                    x=bil_1_data['Period'],
                    y=bil_1_data['Özkaynaklar'],
                    text=bil_1_data['Özkaynaklar'],
                    mode='lines+markers+text',cliponaxis=False,
                    textposition='top center',texttemplate= '%{text:.2s}',textfont={"size":10},
                    line=dict(color='DarkOrange')
        ))

    fig_bil_2.add_trace(
                go.Scatter(name='Duran Varlıklar', 
                    x=bil_1_data['Period'],
                    y=bil_1_data['Duran_Var'],
                    text=bil_1_data['Duran_Var'],
                    mode='lines+markers+text',cliponaxis=False,
                    textposition='top center',texttemplate= '%{text:.2s}',textfont={"size":10},
                    line=dict(color='Teal')
        ))

    fig_bil_2.add_trace(
                go.Scatter(name='Net Borç', 
                    x=bil_1_data['Period'],
                    y=bil_1_data['Net_Borc'],
                    text=bil_1_data['Net_Borc'],
                    mode='lines+markers+text',cliponaxis=False,
                    textposition='top center',texttemplate= '%{text:.2s}',textfont={"size":10},
                    line=dict(color='Crimson')
        ))

    fig_bil_2.update_layout(barmode='stack',
                            width=900, height=500,
                            xaxis_title=' ', yaxis_title=" ",
                            yaxis={'visible': False, 'showticklabels': False, 'showgrid': False},
                            legend=dict(orientation="h",font=dict(size=12),
                                        yanchor="bottom",y=-0.25,
                                        xanchor="center",x=0.5)
                            )

    col1,col2,col3 = st.columns([13,74,13])
    with col1:
        st.subheader("")
    with col2:
        st.plotly_chart(fig_bil_2)
    with col3:
        st.subheader("")

    #Kaynak Dağılımı

    with st.popover("**💡 Kaynak Dağılımı 📚**"):
        st.markdown(kisavy_DESC)
        st.markdown(uzunvy_DESC)

    fig_bil_1 = go.Figure()
    fig_bil_1.add_trace(go.Bar(
        y=bil_1_data['Period'],
        x=bil_1_data['Özkaynaklar'],
        name='Özkaynaklar',
        orientation='h',
        text=bil_1_data['Özkaynak_per'],marker_color='DarkOrange',cliponaxis=False,
        textposition="inside",insidetextanchor = "middle",texttemplate='%{text:.1%}',textfont={"size":11}
    ))
    fig_bil_1.add_trace(go.Bar(
        y=bil_1_data['Period'],
        x=bil_1_data['Uzun_Vade_Yük'],
        name='Uzun Vadeli Yükümlülükler',
        orientation='h',
        text=bil_1_data['Uzun_Vade_Yük_per'],cliponaxis=False,marker_color='Purple',
        textposition="inside",insidetextanchor = "middle",texttemplate='%{text:.1%}',textfont={"size":11}
    ))

    fig_bil_1.add_trace(go.Bar(
        y=bil_1_data['Period'],
        x=bil_1_data['Kısa_Vade_Yük'],
        name='Kısa Vadeli Yükümlülükler',
        orientation='h',
        text=bil_1_data['Kısa_Vade_Yük_per'],cliponaxis=False,marker_color='FireBrick',
        textposition="inside",insidetextanchor = "middle",texttemplate='%{text:.1%}',textfont={"size":11}
    ))

    fig_bil_1.update_layout(
                            width=900, height=800,
                            barmode='stack',
                            xaxis_title=' ', yaxis_title=" ",
                            yaxis={'visible': True, 'showticklabels': True, 'showgrid': False},
                            legend=dict(orientation="h",
                                yanchor="top",y=1.09,xanchor="left",x=0.40,font=dict(size= 12))
                        )

    col1,col2,col3 = st.columns([13,74,13])
    with col1:
        st.subheader("")
    with col2:
        st.plotly_chart(fig_bil_1)
    with col3:
        st.subheader("")

    #Karlılık

    with st.popover("**💡 Karlılık Oranları 📚**"):
        st.markdown(aktifk_DESC)
        st.markdown(ozserk_DESC)

    bil_2_data = bil_1_data.iloc[3:].reset_index(drop=True)
    bil_2_data['Yıllık_Kar'] = n_profit_ytd
    bil_2_data['Aktif_karlılık']=bil_2_data['Yıllık_Kar']/bil_2_data['Toplam_Kaynak']
    bil_2_data['Öz_Sermaye_karlılık']=bil_2_data['Yıllık_Kar']/bil_2_data['Özkaynaklar']
    bil_2_data['Cari_Oran']=bil_2_data['Dönen_Var']/bil_2_data['Kısa_Vade_Yük']

    fig_bil_3 = go.Figure()

    fig_bil_3.add_trace(
                go.Scatter(name='Aktif Karlılık', 
                    x=bil_2_data['Period'],
                    y=bil_2_data['Aktif_karlılık'],
                    text=bil_2_data['Aktif_karlılık'],
                    mode='lines+markers+text',cliponaxis=False,
                    textposition='top center',texttemplate= '%{text:.1%}',textfont={"size":10},
                    line=dict(color='DarkOrange')
        ))

    fig_bil_3.add_trace(
                go.Scatter(name='Öz Sermaye Karlılığı', 
                    x=bil_2_data['Period'],
                    y=bil_2_data['Öz_Sermaye_karlılık'],
                    text=bil_2_data['Öz_Sermaye_karlılık'],
                    mode='lines+markers+text',cliponaxis=False,
                    textposition='top center',texttemplate= '%{text:.1%}',textfont={"size":10},
                    line=dict(color='Purple'))
                    )

    fig_bil_3.update_layout(
                            width=900, height=500,
                            xaxis_title=' ', yaxis_title=" ",
                            yaxis={'visible': False, 'showticklabels': False, 'showgrid': False},
                            legend=dict(orientation="h",
                                yanchor="bottom",y=-0.25,
                                xanchor="center",x=0.5,font=dict(size= 12))
                            )

    col1,col2,col3 = st.columns([13,74,13])
    with col1:
        st.subheader("")
    with col2:
        st.plotly_chart(fig_bil_3)
    with col3:
        st.subheader("")

    #Oranlar

    with st.popover("**💡 Oranlar 📚**"):
        st.markdown(cari_DESC)
        st.markdown(asit_DESC)
        st.markdown(kaldirac_DESC)

    fig_bil_5 = go.Figure()

    fig_bil_5.add_trace(
                go.Bar(name='Cari Oran',
                    x=bil_1_data['Period'], 
                    y=bil_1_data['Cari_Oran'],
                    text=bil_1_data['Cari_Oran'],
                    textposition="outside", texttemplate='%{text:.2}',marker_color='salmon',
                    showlegend=True, cliponaxis=False,textfont=dict(color="black", size=10),)
                )

    fig_bil_5.add_trace(
                go.Scatter(name='Asit-Test Oranı', 
                    x=bil_1_data['Period'],
                    y=bil_1_data['Asit_Test_Oran'],
                    text=bil_1_data['Asit_Test_Oran'],
                    mode='lines+markers+text',cliponaxis=False,
                    textposition='top center',texttemplate= '%{text:.2}',textfont=dict(color="black", size=10),
                    line=dict(color='Teal',width=3,dash='dot')
        ))

    fig_bil_5.add_trace(
                go.Scatter(name='Kaldıraç Oranı',
                    x=bil_1_data['Period'], 
                    y=bil_1_data['kaldırac_Oran'],
                    text=bil_1_data['kaldırac_Oran'],
                    mode='lines+text+markers',textposition="top center", texttemplate='%{text:.1%}',
                    textfont=dict(color="black", size=10),
                    line=dict(color='navy'),showlegend=True,
                    yaxis="y2"
                ))
    fig_bil_5.update_layout(width=900, height=500,
                            yaxis=dict(title = " ",visible=False,showticklabels=False),
                            yaxis2=dict(title = " ",anchor = "free", overlaying="y",side="right",showticklabels=False,visible=False),
                            legend=dict(orientation="h",
                                        yanchor="bottom",y=-0.25,
                                        xanchor="center",x=0.5,
                                        font=dict(size= 12))
                            )

    col1,col2,col3 = st.columns([13,74,13])
    with col1:
        st.subheader("")
    with col2:
        st.plotly_chart(fig_bil_5)
    with col3:
        st.subheader("")
    
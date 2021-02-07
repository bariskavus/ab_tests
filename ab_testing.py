import pandas as pd
from scipy.stats import shapiro
from scipy import stats
import matplotlib.pyplot as plt
import pylab

df_control = pd.read_excel("datasets/ab_testing_data.xlsx",
                           sheet_name="Control Group")

df_test = pd.read_excel("datasets/ab_testing_data.xlsx",
                        sheet_name="Test Group")


def describe(arg1):
    print(arg1.describe().T)


def check_df(dataframe):
    print("##################### Shape #####################")
    print(dataframe.shape)
    print("##################### Types #####################")
    print(dataframe.dtypes)
    print("##################### Head #####################")
    print(dataframe.head(3))
    print("##################### Tail #####################")
    print(dataframe.tail(3))
    print("##################### NA #####################")
    print(dataframe.isnull().sum())
    print("##################### Quantiles #####################")
    print(dataframe.quantile([0, 0.05, 0.50, 0.95, 0.99, 1]).T)


def norm_test(arg1):
    test_istatistigi, pvalue = shapiro(arg1)
    print('Test İstatistiği = %.4f, p-değeri = %.4f' % (test_istatistigi, pvalue))
    # plot
    stats.probplot(arg1, dist="norm", plot=pylab)
    pylab.title("Q-Q Plot")
    pylab.show()


def var_equal(arg1, arg2):
    levene_test, pvalue = stats.levene(arg1, arg2)
    return levene_test, pvalue
    print('Test İstatistiği = %.4f, p-değeri = %.4f' % (levene_test, pvalue))


def t_test(arg1, arg2):
    test_istatistigi, pvalue = stats.ttest_ind(arg1, arg2, equal_var=True)
    return test_istatistigi, pvalue
    print('Test İstatistiği = %.4f, p-değeri = %.4f' % (test_istatistigi, pvalue))


def mann_whitney_u(arg1, arg2):
    test_istatistigi, pvalue = stats.mannwhitneyu(arg1, arg2)
    return test_istatistigi, pvalue
    print('Test İstatistiği = %.4f, p-değeri = %.4f' % (test_istatistigi, pvalue))


check_df(df_test)
describe(df_test["Purchase"])
describe(df_control["Purchase"])

# Soru1: Bu A / B testinin hipotezini nasıl tanımlarsınız?

# H0: maximum bidding purchase ve average bidding purchase ortalamaları arasında fark yoktur.
# H1: maximum bidding purchase ve average bidding purchase ortalamaları arasında fark vardır.

# ------------------------------------------------------------------------------------------------

# Soru2: İstatistiksel olarak anlamlı sonuçlar çıkarabilir miyiz?


# Normallik varsayım kontrolleri

# H0: test grubu purchase normal dağılmaktadır.
# H1: test grubu purchase normal dağılmamaktadır.


norm_test(df_test["Purchase"])

# p_value > 0.05 olduğu için H0 REDDEDİLEMEZ. test grubu purchase normal dağılmaktadır.

# H0: test grubu purchase normal dağılmaktadır.
# H1: test grubu purchase normal dağılmamaktadır.

norm_test(df_control["Purchase"])
# p_value > 0.05 olduğu için H0 REDDEDİLEMEZ. control grubu purchase normal dağılmaktadır.


# Homojenlik varsayım kontrolleri

# H0: test_purchase ve cont_purchase varyansları homojendir.
# H1: test_purchase ve cont_purchase varyansları homojen değildir.

var_equal(df_test["Purchase"], df_control["Purchase"])
# p_value > 0.05 olduğu için H0 REDDEDİLEMEZ. control grubu purchase varyansları homojendir.

# Test istatistiği


t_test(df_test["Purchase"], df_control["Purchase"])

# p_value > 0.05 H0 REDDEDİLEMEZ.
# maximum bidding purchase ve average bidding purchase ortalamaları arasında istatistiksel olarak
# %95 güvenle anlamlı bir fark yoktur.

# --------------------------------------------------------------------------------------------------

# Soru3: Hangi testi kullandınız? Neden?

f"""

Parametrik testleri kullanabilmemiz için başta normallik varsayımının sağlanması gerekmektedir.

Normallik ve varyans homojenliği varsayımı sağlanmıştır. Bu nedenle parametrik test olan
Bağımsız İki Örneklem T Testi kullanılmıştır.
Eğer normallik varsayımı sağlanıp varyans homojenliği sağlanmasaydı yine Bağımsız iki örneklem T Testi kullanılırdı. 
Fakat test içerisindeki "equal_var=True" argümanını False olarak değiştirilirdi.

"""

# --------------------------------------------------------------------------------------------------

# Soru4: Soru 2'ye verdiğiniz cevaba göre, müşteriye tavsiyeniz nedir?

f"""
Hipotez testi sonucu iki grup ortalamaları arasında fark olmadığı gözlemlenmiştir.
Bu durumda müşterilere average bidding tavsiyesinin, şirket çıkarlarına çok bir fayda sağlayamayacağı söylenebilir.

Fakat daha sağlıklı sonuçlara ulaşmak için örneklem boyutlarının arttırılması gerekmektedir.

"""

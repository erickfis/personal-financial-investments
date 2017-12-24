library(knitr)
library(rmarkdown)
library(dplyr)
library(scales)
library(lubridate)
library(ggplot2)
library(ggthemes)
library(readxl)
library(reshape2)
library(plotly)
library(kableExtra)
library(xts)
library(broom)
library(waffle)
library(ggrepel)
library(magrittr)





dados <- read_xls("~/Documents/Google Drive/office/orçamento2017.xls", 
                  sheet = "inv")

dados <- dados[,c(1:6)]

dados$nome[dados$nome=="erick"] <- "bob"
dados$nome[dados$nome=="michelle"] <- "brown"





### compensando falta de entradas
# condicao <- with(dados, nome=="bob" & data == as.Date("2016-03-16") &
#                          fundo  == "Selic 21" & saldoI == 1140.79)
# dados$data[condicao] <- as.Date("2016-03-17")





##fixing NAs
dados[is.na.data.frame(dados)] <- 0


## removendo datas com entradas duplicadas

df.filtrado <- group_by(dados, nome, fundo, data) %>%
        summarise(
                saldoI = max(saldoI),
                investimento = sum(investimento),
                saque = sum(saque)
        )



df.filtrado$saldoF <- with(df.filtrado, saldoI + investimento - saque)

df.brown <- subset(df.filtrado, nome=="brown")
df.bob <- subset(df.filtrado, nome=="bob")



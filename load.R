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

dados <- dados[,c(1:7)]

dados$nome[dados$nome=="erick"] <- "bob"
dados$nome[dados$nome=="michelle"] <- "brown"





### compensando falta de entradas
# condicao <- with(dados, nome=="brown" & data == as.Date("2016-04-26") & 
#                          fundo  == "CDB 19 117")
# dados$saldoI[condicao] <- 0
# dados$investimento[condicao] <- 11829.93





##fixing NAs
dados[is.na.data.frame(dados)] <- 0
dados$saldoF <- with(dados, saldoI + investimento - saque)


## removendo datas com entradas duplicadas

duplicadas <- group_by(dados, nome, fundo, data) %>%
        summarise(
                counta.data = n()
        ) %>% filter(counta.data >1)



arr.duplicadas <- tapply(duplicadas$data, duplicadas$fundo, unique)

df.filtrada <- dados

for(x in 1:length(arr.duplicadas)){
        condicao <- with(df.filtrada,
                         nome = "bob",
                         fundo == names(arr.duplicadas[x]) & 
                                 data %in% arr.duplicadas[[x]] &
                                 saque==0 & investimento==0)
        df.filtrada <- df.filtrada[!condicao,]
        
}




df.brown <- subset(df.filtrada, nome=="brown")
df.bob <- subset(df.filtrada, nome=="bob")



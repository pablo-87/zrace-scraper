library("tidyverse")

data <- read_csv('data.csv')

data %>%
  select(ftp,pos,avg_power,age)


cleaned <- data %>%
  select(ftp,label,zid,pos,position_in_cat,cp,time_gun,gap,category,
         height,weight,age,np,avg_power,avg_wkg,wkg_ftp,wftp,
         wkg30,wkg1200,w30,w1200, male)

cleaned <- cleaned %>%
  mutate(height = str_remove_all(height,"\\[|\\]|\\'") %>%
           str_split_fixed(",",2) %>%
           .[,1] %>%
           as.numeric(),
         weight = str_remove_all(weight,"\\[|\\]|\\'")%>%
           str_split_fixed(",",2) %>%
           .[,1] %>%
           as.numeric(),
         np = str_remove_all(np,"\\[|\\]|\\'")%>%
           str_split_fixed(",",2) %>%
           .[,1] %>%
           as.numeric(),
         avg_power = str_remove_all(avg_power,"\\[|\\]|\\'")%>%
           str_split_fixed(",",2) %>%
           .[,1] %>%
           as.numeric(),
         avg_wkg = str_remove_all(avg_wkg,"\\[|\\]|\\'")%>%
           str_split_fixed(",",2) %>%
           .[,1] %>%
           as.numeric(),
         wkg_ftp = str_remove_all(wkg_ftp,"\\[|\\]|\\'")%>%
           str_split_fixed(",",2) %>%
           .[,1] %>%
           as.numeric(),
         wftp = str_remove_all(wftp,"\\[|\\]|\\'")%>%
           str_split_fixed(",",2) %>%
           .[,1] %>%
           as.numeric(),
         wkg30 = str_remove_all(wkg30,"\\[|\\]|\\'")%>%
           str_split_fixed(",",2) %>%
           .[,1] %>%
           as.numeric(),
         wkg1200 = str_remove_all(wkg1200,"\\[|\\]|\\'")%>%
           str_split_fixed(",",2) %>%
           .[,1] %>%
           as.numeric(),
         w30 = str_remove_all(w30,"\\[|\\]|\\'")%>%
           str_split_fixed(",",2) %>%
           .[,1] %>%
           as.numeric(),
         w1200 = str_remove_all(w1200,"\\[|\\]|\\'")%>%
           str_split_fixed(",",2) %>%
           .[,1] %>%
           as.numeric(),
         sex = if_else(male == 1,"man","women")
         )

model <- lm(data = cleaned,
            position_in_cat ~ ftp+height+weight+avg_power+avg_wkg+sex)

summary(model)

cleaned %>%
  group_by(zid) %>%
  summarise(time = min(time_gun))

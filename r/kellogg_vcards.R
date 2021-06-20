
library(tidyverse)
library(dplyr)
library(dialr)
library(xlsx)

# Import data
netids<- read_csv("input/1y_survey.csv") %>% select('netID', 'perm_email', 'kellogg_email', 'first_name', 'last_name')
df <- read_csv("input/1Y Class of 2021 Directory - 1Y Class of 2021 Directory.csv", skip=3, 
               col_types = c('Phone Number' = 'c',
                             'WhatsApp Number' = 'c'))
names(df) <- c('x1', 'first_name', 'last_name', 'student_jv', 'perm_email', 'fixed_country_code', 'fixed_phone', 'wa_country', 'fixed_wa_phone', 'industry', 'function', 'employer_clean',  'geo_country','geo_city_primary', 'geo_city_secondary' )

df <- df %>% mutate(mergeid = paste0(first_name, last_name))
netids <- netids %>% mutate(mergeid = paste0(first_name, last_name)) %>% select('netID', 'kellogg_email', 'mergeid')
# Merge netids with other dataset
df <- left_join(df, netids, by="mergeid")

# Set option for dialr format
getOption("dialr.format")
options(dialr.format = "INTERNATIONAL")

df_new <- df %>%
  
  # Format email addresses
  mutate(perm_email_corr = tolower(perm_email),
         netID = tolower(netID)) %>% 
  
  # Reformat numbers
  mutate_at("fixed_phone", ~phone(., fixed_country_code)) %>%
  mutate_at("fixed_phone",
            list(valid_phone = is_valid,
                 region = get_region,
                 type = get_type,
                 phone_final = format)) %>% 
  
  mutate_at("fixed_wa_phone", ~phone(., wa_country)) %>%
  mutate_at("fixed_wa_phone",
            list(valid_wa = is_valid,
                 region = get_region,
                 type = get_type,
                 wa_final = format))
  

write.csv(df_new, "output/1y_dir_output.csv")
backup_name = format(Sys.time(), 'output/backups/%y%m%d_%H%M%S_1y_dir_output_db.csv')
write.csv(df_new, backup_name)

#writexl::write_xlsx(df_exp, "output/1y_dir_output_db.xlsx")



# libs
import core.core

# filter for hauses in viborg randers hobro silkeborg herning kommune
# "https://www.boligsiden.dk/address/api/addressresultproperty/getdata?p=1&i=99&s=12&sd=false&searchId=1b83e5be6d0f49b184ad507ada7ea96e"
# s = 0 > price from lowest to biggest
# s = 1 > salges period old to new
# s = 12 > ligetid

# start dev mode
core.core.Parser(amount_items=40, start_from=1)
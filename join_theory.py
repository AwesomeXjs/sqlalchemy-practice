#  Join - Обьединение

# Оператор языка SQL для соединения данных таблиц в одну таблицу по заданным условиям


# SELECT fieldA, fieldB       # Выбрать колонки fieldA, fieldB
# FROM table1 JOIN table2     # ИЗ таблицы1 И таблицы2
# ON field1 = field2          # При условии (указать общий элемент, например foreignkey)


# Виды Join:
# 1. inner join - покажет только те записи у которых есть пары
# 2. left join - выведет все записи из первой таблицы а для записей без пары со второй таблицы поставит поставит в пару null
# 3. right joiin - выведет все записи из второй таблицы а для записей без пары с первой таблицы поставит поставит в пару null
# 4. full join (outer join) - выведет все записи из обеих таблиц (значениям без пары поставит в пару null)
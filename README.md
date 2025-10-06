Установка зависимостей:
pip install -r requirements.txt

Поиск шаблона формы:
python app.py get_tpl --имя_поля="значение" --другое_поле="значение"

Для шаблона "Данные пользователя":
python app.py get_tpl --login="user@mail.ru" --tel="+7 903 123 45 67"

Для шаблона "Форма заказа":
python app.py get_tpl --customer="Иван" --order_id="123" --дата_заказа="27.05.2025" --contact="+7 912 345 67 89"

Для шаблона "Проба":
python app.py get_tpl --f_name1="test@example.com" --f_name2="2024-03-15" --extra_field="любое значение"

Проверка на несовпадение с шаблоном:
python app.py get_tpl --field_1="12345" --field_2="67890"

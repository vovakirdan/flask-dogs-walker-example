# REST-API
1. [Условия](#условия)
2. [План](#план)
3. [Структура бд](#планируемая-структура-базы-данных)
4. [Реализация](#реализация)
5. [Пример запроса для создания заказа](#пример-запроса-для-создания-заказа)

## Условия 
Пётр и Антон решили открыть свой бизнес по выгулу собак в своем доме. Они решили разработать приложение через которое жильцы дома смогут направлять им заказы на выгул своих питомцев. Петру и Антону срочно нужен бэкенд разработчик, который поможет им разработать структуру БД и реализовать REST-API. И этим бэкенд разработчиком будете вы. 

Пётр и Антон сформировали ряд требований:

 1. В заказе необходимо сохранять номер квартиры, кличку и породу животного, время и дату прогулки. 

 2. Прогулка может длиться не более получаса. Прогулка может начинаться либо в начале часа, либо в половину (11:00,11:30,12:00,12:30…). 

 3. Самая ранняя прогулка может начинаться не ранее 7-ми утра, а самая поздняя не позднее 11-ти вечера. 

 4. Пётр и Антон каждый могут гулять одновременно только с одним животным. 

В API необходимо реализовать 2 метода:
 1. Вывод уже оформленных заказов на указанную дату

 2. Оформление заказа
## План
1. Создадим модель для базы данных, которая будет хранить информацию о заказах на прогулки.
2. Введем валидацию для заказов:
- Прогулка должна начинаться на целый час или полчаса.
- Время прогулки должно быть с 07:00 до 23:00.
- Продолжительность прогулки — максимум 30 минут.
- На одно время может быть только один заказ.
3. Реализуем два API-метода:
- `GET`: получить заказы на конкретную дату.
- `POST`: оформить новый заказ, проверяя доступность времени.
## Планируемая структура базы данных:
- Заказ (`Order`):
    - `id` — уникальный идентификатор.
    - `flat_number` — номер квартиры.
    - `pet_name` — кличка животного.
    - `pet_breed` — порода животного.
    - `start_time` — время начала прогулки.
    - `end_time` — время окончания прогулки.
    - `walker` — исполнитель (Петр или Антон).
### [Реализация](main.py)
## Описание:
1. **GET /orders/<date>** — Возвращает список заказов на указанную дату. Дата должна быть в формате `YYYY-MM-DD`.
2. **POST /orders** — Оформляет новый заказ. Ожидается JSON с полями: `flat_number`, `pet_name`, `pet_breed`, и `start_time` (в формате `YYYY-MM-DD HH:MM`). Время прогулки проверяется на соответствие требованиям, и выбирается свободный исполнитель.
### Пример запроса для создания заказа:
```json
{
  "flat_number": "101",
  "pet_name": "Buddy",
  "pet_breed": "Labrador",
  "start_time": "2024-09-12 11:00"
}
```
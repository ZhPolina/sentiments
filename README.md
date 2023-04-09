## Клонируйте этот репозиторий:

git clone https://github.com/ZhPolina/sentiments.git

## Запустите docker-compose:

docker-compose up --build

## Протестируйте localhost api в вашем браузере:

http://127.0.0.1:8080/

## Загрузка образов из Docker Hub:

## Маршруты:

По основному маршруту возращается HTML страница, содержащая полный глоссарий терминов ВКР.

При вводе в форму слова, которое необходимо найти в глоссарии, данные формы передаются на маршрут **/search_word**. По данному маршруту происходит поиск слова в словаре, в случае успеха на HTML страницу выводится определение для введенного термина.

По маршруту **/graph** вовзращается статическая HTML страница, содержащая изображение, на котором представлен семантический граф понятий.

Маршрут **/clear** позволяет очистить историю поиска. 

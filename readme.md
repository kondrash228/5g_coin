# Криптовалюта 5g coin

## Разработчики
- ### Александр Панфилов (backend)
- ### Егор Кондрашов (backend, analitics)
- ### Николай Снимщиков(не любит ксюшу л)

## Начало
### Склонируйте репозиторий командой
```
git clone https://github.com/kondrash228/5g_coin.git
```
### Создайте на своем компьютере виртуальное окружение, и активируйте
```python
python -m venv env
```
### Далее установите все необходимые зависимости командой
```python
pip intsall -r requirements.txt
```

## Создание локальной цепи
Повторите действия перечисленные выше два раз или более (в зависимости сколько узлов в сети вы хотите зарегестрировать), разместите каждый склонированный репозиторий в разные папки вашего проекта (каждая папка с проектом - новый узел в сети). 

Теперь вам следует указать порты на которых будет работать каждый отдельный узел, для этого вам нужно отредактировать файл block.py, а именно последнюю стоку файла.
```python
app.run(port="тут укажите порт для запуска")
```

### Пример
Создаем два узла в сети, для этого создадим две отдельные папки и назовем из node_1 и node_2 соответственною.

### Папка node_1
```python
...
if __name__ == "__main__":
    app.run(port=5000)
```

### Папка node_2
```python
...
if __name__ == "__main__":
    app.run(port=5001)
```

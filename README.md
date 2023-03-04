## Выделение ключевых слов из научных текстов

### Production-env

Установка окружения и выполнение скриптов производится с помощью setup.sh
Для его работы необходимы `setup.py` и `production_requirements.txt`

Main программа находится в файле `main.py` и зависит от файлов `keywords.json`, `text_rank_normal_form.py` и `manual_m.py`

main.py принимает в stdin текст для которого необходимо выделить ключевые слова и выдает в stdout ключевые слова в формате json:
`{"manual": ["string",...], "TextRank": ["string",...]}`

Для подключения к php необходимо выдать права "всем" на выполнение main.py

### PHP example
```php
// Определяем путь к Python скрипту
$python_script = '/path/to/main.py';
// Создаем массив с настройками для запуска процесса
$descriptorspec = array(
    0 => array('pipe', 'r'), // Стандартный поток ввода (stdin)
    1 => array('pipe', 'w'), // Стандартный поток вывода (stdout)
    2 => array('pipe', 'w'), // Стандартный поток ошибок (stderr)
);
// Создаем процесс для выполнения Python скрипта
$process = proc_open("python3 $python_script 2>&1", $descriptorspec, $pipes);
if (is_resource($process)) {
    // Записываем параметры в стандартный поток ввода процесса
    fwrite($pipes[0], "$text\n");
    fclose($pipes[0]);
    // Считываем результаты работы Python скрипта из стандартного потока вывода
    $output = stream_get_contents($pipes[1]);
    fclose($pipes[1]);
    // Закрываем процесс
    $return_value = proc_close($process);
}
// Получаем результаты работы Python скрипта
$arr = json_decode($output, true);
// Вывод ошибок
if (!($arr))
{
    echo "<p>Error:</p>";
	echo nl2br($output);
}
```